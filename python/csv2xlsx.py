import pandas as pd
import os


def csv_2_xlsx(csv_dir):
    for root, dirs, files in os.walk(csv_dir):
        for name in files:
            file_full_name = f'{root}/{name}'
            file_name, file_type = file_full_name.split('.')
            if file_type == 'csv':
                df = pd.read_csv(file_full_name, encoding='gb18030')
                xlsx_filename = f'{file_name}.xlsx'
                df.to_excel(xlsx_filename)
                # os.remove(file_full_name)  # 删除csv文件


if __name__ == '__main__':
    csv_2_xlsx(csv_dir='~/Desktop/csv')
