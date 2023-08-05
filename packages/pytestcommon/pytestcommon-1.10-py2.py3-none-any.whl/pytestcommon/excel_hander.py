from os import path

import openpyxl


class ExcelHandler:
    def __init__(self, file_path):
        """初始化传入文件的路径"""
        self.file_path = file_path
        self.workbook = None

    def open_excel(self):
        """定义打开Excel的方法"""
        workbook = openpyxl.load_workbook(self.file_path)
        self.workbook = workbook
        return workbook

    def get_sheet(self, sheet_name):
        """获取表格"""
        workbook = self.open_excel()
        return workbook[sheet_name]

    def read_sheet_data(self, sheet_name):
        """读取 sheet 表格数据"""
        sheet = self.get_sheet(sheet_name)
        rows = list(sheet.rows)

        data = []
        # 获取标题
        headers = []
        for title in rows[0]:
            headers.append(title.value)
        # 添加数据
        for row in rows[1:]:
            row_data = {}
            for idx, cell in enumerate(row):
                row_data[headers[idx]] = cell.value
            data.append(row_data)
        return data

    def write(self, sheet_name, row, column, data):
        """写入单元格数据"""
        sheet = self.get_sheet(sheet_name)
        sheet.cell(row, column).value = data
        self.save()
        self.close_file()

    def save(self):
        """保存文件"""
        self.workbook.save(self.file_path)

    def close_file(self):
        """关闭文件"""
        self.workbook.close()


if __name__ == '__main__':
    excel = ExcelHandler(path.join(path.join(path.dirname(path.abspath(__file__)), "data"), "test_login.xlsx"))
    print(excel.get_sheet("login"))
    print(excel.read_sheet_data("login"))
