from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

import os.path
import Functions

import chromedriver_autoinstaller

'''Check if the current version of chromedriver exists
and if it doesn't exist, download it automatically,
then add chromedriver to path'''
chromedriver_autoinstaller.install()

'# Excel headers'
headers = ["Kuupäev",
           "Kinnisvara puhas väärtus",
           "Füüsilise isiku aktsiad",
           "Juriidilise isiku aktsiad",
           "Aktsiad kokku",
           "Terve portfell kokku",
           "Mörr-i portfell",
           "Pere portfell kokku",
           "Vilde after Tax",
           "Vaba Raha",
           "Funderbeam Väärtus",
           "Kelly portfell kokku"]


def freeze_excel_row(excel_name):

    '# add file type'
    file_name = excel_name + ".xlsx"

    workbook_name = file_name
    wb = load_workbook(workbook_name)
    sheet1 = wb.active

    'freeze 1st row'
    sheet1.freeze_panes = 'A2'

    wb.save(filename=workbook_name)


def create_excel(excel_name, sheet_name):

    wb = Workbook()
    sheet1 = wb.active
    sheet1.title = sheet_name

    '#add file type'
    file_name = excel_name + ".xlsx"
    '#salvestab exceli'
    wb.save(filename=file_name)

    wb.close()
    print("========================")
    print("Loodud uus fail", file_name)


'#tuleb sisse anda ka faili nimi, kontrollib kahjuks ainult kodu arvutit'


def check_if_excel_exists(excel_name):

    '#kodu path ja töö path viidud muutujasse'
    if os.path.isfile(Functions.what_path_for_file() + 'Portfolio_calculator/' + excel_name + ".xlsx"):
        return True
    else:
        return False


'# append new rows/info to excel'
'# how_to_add: 1 = append, 2 = overwrite, 3 = compare if change is needed'


def write_to_excel(excel_name, list_of_data, how_to_add):
    '# add file type'
    file_name = excel_name + ".xlsx"

    workbook_name = file_name
    wb = load_workbook(workbook_name)
    sheet1 = wb.active
    # New data to write:
    new_data = [list_of_data]

    if how_to_add == 1:
        for info in new_data:
            sheet1.append(info)

    '''elif how_to_add == 2:
        print('overwrite')
        max_row = sheet1.max_row
        for col_cells in sheet1.iter_rows(min_row=max_row, max_row=max_row):
            for index, cell in enumerate(col_cells):
                #print(index+1, max_row, cell, cell.value)
                for info in list_of_data:
                    print(info)
                    cell.value(row=max_row, column=int(index+1))
                #cell.value(row=max_row, )=2
                #print(max_row, cell, cell.value)





    elif how_to_add == 3:
        print('compare')'''

    wb.save(filename=workbook_name)

    print("Tänane seis lisatud.")


'# makes columns length wider'


def column_width(excel_name, excel_headers):
    '# add file type'
    file_name = excel_name + ".xlsx"

    workbook_name = file_name
    wb = load_workbook(workbook_name)
    sheet1 = wb.active

    '# 1 so enumerate, would start form 1, not 0'
    for i, col_value in enumerate(excel_headers, 1):
        '# if column length is very small (less then 5), then give static length of 10, else length of column'
        if len(col_value) < 5:
            column_extender = 10
        else:
            column_extender = len(col_value)
        '# wants column letter for input, as i. Width input is in the end of it'
        sheet1.column_dimensions[get_column_letter(i)].width = column_extender

    wb.save(filename=workbook_name)


'# check if excel file is there, if not create it'


def need_new_excel_file(excel_name, sheet_name, excel_headers):
    if check_if_excel_exists(excel_name):
        print("========================")
        print("Fail juba kaustas olemas.")
    else:
        create_excel(excel_name, sheet_name)
        freeze_excel_row(excel_name)
        write_to_excel(excel_name, headers)
        column_width(excel_name, excel_headers)


'# returns all values of given column in list'


def get_excel_column_values(excel_name, column_letter):
    '# add file type'
    file_name = excel_name + ".xlsx"

    workbook_name = file_name
    wb = load_workbook(workbook_name)
    sheet1 = wb.active

    column_list = []
    '# using enumerate to get index and then to skip header row'
    for index, col in enumerate(sheet1[column_letter]):
        if index == 0:
            continue
        column_list.append(col.value)

    return column_list


'# returns last row of given columns number'


def get_last_row(excel_name, column_number):
    '# add file type'
    file_name = excel_name + ".xlsx"

    workbook_name = file_name
    wb = load_workbook(workbook_name)
    sheet1 = wb.active

    max_rows = sheet1.max_row
    cell = sheet1.cell(column=column_number, row=max_rows).value
    return cell
'''
values_list = []
values_list.extend(('1-1-2023', 3,3,3,3,3))
write_to_excel('excel_name', values_list, 2)'''