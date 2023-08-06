import os

from task.export.bundle import BundleTableExportTask
from task.export.loader.abstract import AbstractScopeLoader
from task.export.scope import TaskScope
from transform.resource_manager import BundleResourceManager


class FrameworksScopeLoader(AbstractScopeLoader):
    __scope__ = TaskScope.Frameworks

    def __init__(self):
        super(FrameworksScopeLoader, self).__init__()
        self.business_white_list = None

    def set_white_list(self, business_white_list):
        self.business_white_list = business_white_list

    def load_tasks(self):
        if not self.project_paths.is_business_bundle_dir_exist():
            return []
        yield from self._load_business_bundle()

    def _load_business_bundle(self):
        business_bundle_dir = self.project_paths.get_business_bundle_dir()
        for business_bundle_name in os.listdir(business_bundle_dir):
            bundle_path_manager = BundleResourceManager(self.project_paths.get_business_bundle_path(business_bundle_name))
            if bundle_path_manager.is_table_dir_exist() and self._filter_bundle(business_bundle_name):
                yield BundleTableExportTask(self, bundle_path_manager, business_bundle_name)

    def _filter_bundle(self, business_bundle_name):
        if self.business_white_list is None:
            return True
        for white_list_item in self.business_white_list:
            if business_bundle_name.lower() == white_list_item.lower():
                return True
        return False
