import os


class ProductFileManager:
    def __init__(self):
        self.product_dir = ""
        pass

    def clear_all(self):
        self.remove_all_files(os.path.join(self.product_dir, "Script/ThirdParty/game/Table"), ".ts", ["TableBase.ts"])
        self.remove_all_files(os.path.join(self.product_dir, "resources/Table"), ".json")
        self.remove_all_files(os.path.join(self.product_dir, "resources/Table"), ".bin")

    @staticmethod
    def remove_all_files(target_dir, ext_name, white_list=None):
        if white_list is None:
            white_list = []

        for root, dirs, files in os.walk(target_dir):
            for name in files:
                if not name.endswith(ext_name):
                    continue

                is_in_white_list = False
                for item in white_list:
                    if name.endswith(item):
                        is_in_white_list = True
                        continue

                if is_in_white_list:
                    continue

                os.remove(os.path.join(root, name))
