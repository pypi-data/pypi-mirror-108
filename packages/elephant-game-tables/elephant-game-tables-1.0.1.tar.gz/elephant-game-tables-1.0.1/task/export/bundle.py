from sheet.table_sheet_files import TableSheetFiles
from sheet.table_sheet_manager import TableSheetManager
from task.abstract import AbstractTask
from transform.table_transform import TableTransformManager


class BundleTableExportTask(AbstractTask):
    __task_name__ = "bundle_table_export_task"

    def __init__(self, parent_task, path_manager, prefix):
        super().__init__()
        self.parent_task = parent_task
        self.path_manager = path_manager
        self.prefix = prefix

        self.append_task_steps({
            "load_file": self._load_files,
            "load_sheets": self._load_sheets,
            "transform_and_save": self._transform_and_save,
        })

        self.all_files = []
        self.all_table_sheets = []

    def _load_files(self):
        table_dir = self.path_manager.get_table_dir()
        production_files = TableSheetFiles()
        production_files.read_product_files(table_dir, self.parent_task.dimensions)
        if production_files.has_file():
            self.all_files = production_files.get_all_files()
            return True
        return False

    def _load_sheets(self):
        sheet_manager = TableSheetManager()
        sheet_manager.load_all_sheets(self.all_files)
        if sheet_manager.has_sheets():
            sheet_manager.merge_tables()
            self.all_table_sheets = sheet_manager.get_all_sheets()
            return True
        return False

    def _transform_and_save(self):
        transform_manager = TableTransformManager(self.prefix)
        transform_manager.translate(self.all_table_sheets)
        transform_manager.save_to(self.path_manager)
        return True
