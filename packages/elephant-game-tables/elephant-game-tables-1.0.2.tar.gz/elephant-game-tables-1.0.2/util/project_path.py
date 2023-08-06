import os

from transform.resource_manager import get_relative_path
from util.path_sensor import SmartProjectPathSensor


class ProjectPathManager:
    __business_bundle_relative_path__ = "assets/bundle/FGui"

    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.project_dir = self._smart_sense_project_dir(input_dir)

    @classmethod
    def _smart_sense_project_dir(cls, input_dir):
        sensor = SmartProjectPathSensor(input_dir)
        project_dir = sensor.smart_get_project_dir()
        return project_dir

    def is_business_bundle_dir_exist(self):
        return os.path.exists(self.get_business_bundle_dir())

    def get_business_bundle_dir(self):
        return self._get_project_relative_path(self.__business_bundle_relative_path__)

    def get_business_bundle_path(self, bundle_name):
        return get_relative_path(self.get_business_bundle_dir(), bundle_name)

    def _get_project_relative_path(self, relative_path):
        return os.path.normpath(os.path.join(self.project_dir, relative_path))

    def is_project_path(self, target_path):
        relative_path = os.path.relpath(target_path, self.project_dir)
        return relative_path == '.'

    def is_business_bundle_path(self, target_path):
        business_bundle_name = os.path.relpath(target_path, self.get_business_bundle_dir())
        return self._is_pure_business_bundle_name(business_bundle_name)

    def get_business_bundle_name_of(self, business_bundle_path):
        business_bundle_name = os.path.relpath(business_bundle_path, self.get_business_bundle_dir())
        if self._is_pure_business_bundle_name(business_bundle_name):
            return business_bundle_name
        return None

    @classmethod
    def _is_pure_business_bundle_name(cls, business_bundle_name):
        return '.' not in business_bundle_name and '\\' not in business_bundle_name and '/' not in business_bundle_name
