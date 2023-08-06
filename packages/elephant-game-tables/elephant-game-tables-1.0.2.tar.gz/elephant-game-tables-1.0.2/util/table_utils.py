import os


def get_sheet_dimension(sheet_name):
    sheet_name_list = sheet_name.split("@")
    if len(sheet_name_list) > 1:
        return sheet_name_list[1]
    return ""


def get_sheet_name(sheet_name):
    sheet_name_list = sheet_name.split("@")
    return sheet_name_list[0]


def is_file_filtered(file_path):
    # 过滤扩展名不对的表
    ext_name = os.path.splitext(file_path)[1].lower()
    if ext_name not in ['.xls', '.xlsx']:
        return True

    # 过滤掉打开的临时表
    file_name = os.path.basename(file_path)
    if '~$' in file_name:
        return True
    return False
