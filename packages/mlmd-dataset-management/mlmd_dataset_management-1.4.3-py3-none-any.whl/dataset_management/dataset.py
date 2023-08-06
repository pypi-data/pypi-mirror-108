import os
import logging
import json

from ml_metadata.proto import Artifact
from mlmd.dataset_manager_scheme import ArtifactType, ExecutionType, ContextType
from mlmd.dataset_manager_dao import *
from dataset_management.utils import generate_version_id
from dataset_management.blob import _upload_blob, get_bucket_name, list_blob, _download_blob
import datetime
from multiprocessing import Array, cpu_count, Pool

from mlmd.metadata_dao import get_tenant_id, insert_image_log_bulk, insert_image_metadata_bulk, get_image_executions_by_version
from .triggers import ApiTrigger

class Dataset():
    def __init__(self, datasetname, version="latest", username="Anomymous") -> None:        
        dataset = get_artifact_by_type_and_name(ArtifactType.DATASET, datasetname)
        if dataset is None:
            raise Exception("Dataset {} not found".format(datasetname))
        self.metadata = dataset.properties
        self.datasetname = dataset.name
        self.created_at = datetime.datetime.fromtimestamp(dataset.create_time_since_epoch//1000.0)
        self.id = dataset.id
        self.username = username
        self.version = version
        if self.version == "latest":
            self.version = self.metadata["latest_version"].string_value
        self.uncommitted_version = self.metadata["uncommitted_version"].string_value
        self.filelist = self.get_filelist()
        self.trigger = ApiTrigger.from_json_string(self.metadata["trigger"].string_value)

    def __str__(self) -> str:
        return str({
            "name": self.datasetname,
            "version": self.version,
            "trigger": self.metadata["trigger"].string_value,
            "tags": self.metadata["tags"].string_value,
            "created_by": self.metadata["created_by"].string_value,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def list_staged_executions(self):
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return [{
            "execution": get_type_name_from_id(exe.type_id),
            "executed_by": exe.properties["executed_by"].string_value
        } for exe in get_executions_by_context(tobe_committed_ctx.id)]


    def list_versions(self, short=False):
        if short:
            return [ctx.name for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]            
        return [
            {"version": ctx.name,
             "committed_by": ctx.properties["committed_by"].string_value,
             "prev_version": ctx.properties["prev_ref"].string_value,
             "created_at": datetime.datetime.fromtimestamp(ctx.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S")
            } for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]

    def add_files_from_dir(self, _dir, override=False, annotation=None, tenant="unknown"):
        if _dir is None or os.path.isdir(_dir) == False:
            raise Exception("Data dir {} not valid".format(_dir))

        tenant_id = get_tenant_id(tenant)
        if tenant_id is None:
            raise Exception("Tenant {} is invalid".format(tenant))

        blobnamelist = {blob.name for blob in list_blob(get_bucket_name(self.datasetname))}

        filelist = [_file for _file in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, _file)) 
            and (override == True or _file not in blobnamelist)]

        arglist = [(_file, self.datasetname, _dir) for _file in filelist]
        if len(arglist) > 0:
            proc_count = cpu_count()
            if len(arglist) < cpu_count():
                proc_count = len(arglist)
            print("{} {} is being uploaded by {} processes...".format(filelist, len(filelist), proc_count))
            p = Pool(proc_count)
            r = p.map(_upload_blob, arglist)
            p.close()
            p.join()
            success_list = []
            for i,_ in enumerate(r):
                if r[i] == False:
                    logging.warning("Failed to update {} in changelist".format(self.changelist[i][0]))
                else:
                    success_list.append(r[i])
            print("Successfully uploaded {} files".format(len(success_list)))
        else:
            print("No file to upload. Override option is being set to {}".format(override))

        exe_id = create_execution(ExecutionType.ADD_FILES_TO_DATASET, {"executed_by": self.username,"file_location": _dir})
        #insert image metadata
        image_metadata = [(image_name, tenant_id, self.id, annotation) for image_name in filelist]
        if len(image_metadata) > 0:
            image_metadata_ids = insert_image_metadata_bulk(image_metadata, return_ids=True)
            # execution and image artifacts link
            log_metadata = [(image_id, exe_id, self.uncommitted_version, self.id) for image_id in image_metadata_ids]
            if len(log_metadata) > 0:
                insert_image_log_bulk(log_metadata)

        # version and execution link
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return create_association_attribution(ctx.id, exe_id, None)

    def remove_files(self, filelist):
        if filelist is None or len(filelist) <= 0:
            return None
        exe_id = create_execution(ExecutionType.REMOVE_FILES_FROM_DATASET, {"executed_by": self.username})
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return create_association_attribution(ctx.id, exe_id, None)

    def commit_version(self, trigger=None, ref_version=None):
        # update uncommited version to become official version
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)

        if len(get_executions_by_context(tobe_committed_ctx.id)) <= 0:
            print("Nothing to commit")
            return False

        tobe_committed_ctx.properties["committed_by"].string_value = self.username
        tobe_committed_ctx.properties["prev_ref"].string_value = self.version if ref_version is None else ref_version
        update_context(tobe_committed_ctx)
        committed_version_id = tobe_committed_ctx.name
        # new uncommited version ref to committed version and its link
        new_uncommitted_version_id = generate_version_id()
        context_id = create_context(ContextType.COMMIT_DATASET_VERSION, new_uncommitted_version_id, None, self.version)
        create_association_attribution(context_id, None, self.id)

        update_artifact(ArtifactType.DATASET, self.datasetname, None, committed_version_id, new_uncommitted_version_id)
        self.uncommitted_version = new_uncommitted_version_id
        self.version = committed_version_id
        self.filelist = self.get_filelist()

        # execute trigger if have
        if trigger is not None:
            trigger.execute()
        elif self.trigger is not None:
            self.trigger.execute()
        return committed_version_id

    def get_trigger(self):
        return ApiTrigger.from_json_string(self.metadata.get("trigger"))

    def set_trigger(self, trigger: ApiTrigger):
        self.metadata["trigger"].string_value = str(trigger)
        self.trigger = trigger
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, self.metadata["trigger"].string_value)

    def get_tags(self):
        return self.metadata["tags"].string_value

    def add_tag(self, tag):
        tag_str = self.metadata["tags"].string_value
        if tag_str is None or tag_str == '':
            tag_arr = [tag]
        else:
            tag_arr = tag_str.split(",")
            if tag not in tag_arr:
                tag_arr.append(tag)
            else:
                print("Tag existed")
                return False
        tag_str = ",".join(tag_arr)
        self.metadata["tags"].string_value = tag_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tag_str)

    def set_tags(self, tags: Array):
        tags_str = ",".join(tags)
        self.metadata["tags"].string_value = tags_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tags_str)

    def __collect_changelist(self, version, global_changelist):
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, version)
        if ctx is None:
            raise Exception("Version {} not exists in this dataset".format(self.version))
        executions = get_executions_by_context(ctx.id)

        image_log_arr = get_image_executions_by_version(version)
        for item in image_log_arr:
            if global_changelist.get(item.get("image_name")) is None:
                global_changelist[item.get("image_name")] = [item.get("execution_id")]
            else:
                global_changelist[item.get("image_name")].append(item.get("execution_id"))


        # for execution in executions: 
        #     # filelist = json.loads(execution.properties["filelist"].string_value)
        #     execution_contexts = get_contexts_by_execution(execution.id, [ContextType.EXECUTE_ADDING_FILES, ContextType.EXECUTE_REMOVING_FILES])
        #     if len(execution_contexts) == 1:
        #         image_artifacts = get_artifacts_by_context(execution_contexts[0].id)
        #         filelist = [artifact.name for artifact in image_artifacts]
        #         for _file in filelist:
        #             if global_changelist.get(_file) is None:
        #                 global_changelist[_file] = [execution.type_id]
        #             else:
        #                 global_changelist[_file].append(execution.type_id)
                
        prev_version = ctx.properties["prev_ref"].string_value
        if prev_version is not None and prev_version != '':
            return self.__collect_changelist(prev_version, global_changelist)
        return global_changelist

    def get_filelist(self):
        if self.version is None or self.version == "":
            return None
        addtype = get_execution_type_by_name(ExecutionType.ADD_FILES_TO_DATASET)
        filelist = []
        global_changelist = self.__collect_changelist(self.version, {})
        for key,value in global_changelist.items():
            if value[0] == addtype.id:
                filelist.append(key)
        return filelist

    def get_current_version(self):
        return self.version

    def checkout(self, version, image_annotations=None):
        if version == "latest":
            version = self.metadata["latest_version"].string_value
        if version not in self.list_versions(short=True):
            raise Exception("Version is not valid")
        self.version = version
        self.filelist = self.get_filelist()

    def download_to_dir(self, _dir):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if self.filelist is None:
            self.filelist = self.get_filelist()
        if self.filelist is None or len(self.filelist) == 0:
            print("Nothing to download")
            return False

        print("Downloading {}...".format(self.filelist))
        arglist = [(_f, self.datasetname, _dir) for _f in self.filelist]
        proc_count = max(cpu_count(), len(arglist))
        p = Pool(proc_count)
        r = p.map(_download_blob, arglist)
        p.close()
        p.join()
        success_list = []
        for i,_ in enumerate(r):
            if r[i] == False:
                logging.warning("Failed to update {} in changelist".format(self.changelist[i][0]))
            else:
                success_list.append(r[i])
        print("Successfully downloaded {}".format(success_list))

    def load_filelist(splitter=None):
        """
        Load the images specified in self.filelist. A logic of how to split can be defined by input splitter
        """
        pass

    def update_filelist_metadata():
        """
        Update metadata of images specified in self.filelist
        """
        pass

    def get_annotations(version=None):
        """
        Return all annotations of the images of the current version

        """
        pass
