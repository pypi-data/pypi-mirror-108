import xlrd
import xlwt
import math
import os
from xlutils.copy import copy
import argparse


def main():
    parser = argparse.ArgumentParser(description='Process excel file of matrix price')
    parser.add_argument('-f', help='enter file name and location')
    # parser.add_argument('number', metavar='-c', type=int, help='enter number of columns')
    args = vars(parser.parse_args()) #parser.parse_args()
    print(args['f'])
    book = xlrd.open_workbook(args['f'], formatting_info=True)
    sheet = book.sheet_by_index(0)
    wb = copy(book)
    z = 2
    # print((sheet.nrows >= z and sheet.cell_value(z, 0) != ''))
    while sheet.nrows-1 >= z and sheet.cell_value(z, 0) != '':
        z = z + 1
    x = 2 
    # print((sheet.ncols >= x and sheet.cell_value(0, x) != ''))
    while sheet.ncols-1 >= x and sheet.cell_value(0, x) != '':
        # print(sheet.ncols)
        # print(x)
        x = x + 1
        
    # print(z)
    # print(x)
    data = [[sheet.cell_value(r, c) for c in range(0,x,1)] for r in range(0,z,1)]
    res = wb.add_sheet('res',cell_overwrite_ok=True)
    book.release_resources()
    del book
    # print(data)
    t = 0
    for i in range(1,z,1):
        for j in range(1,x,1):
            if(j != 0 and i != 0 and data[j][i] != ''):
                # print(math.ceil(float(data[i][j])))
                res.write(t, 0, data[0][i])
                res.write(t, 1, data[j][0])
                res.write(t, 2, math.ceil(float(data[j][i])))
                t = t + 1
    filename, file_extension = os.path.splitext(args['f'])
    wb.save(filename + '1' + file_extension)
    # planeTextLog += '\r\n' + str(pos)
    # plainTextEdit.setPlainText(planeTextLog)
    # lisOfOrder = [str(data[r][pos[0][0][1]]).replace('.0','') for r in range(pos[0][0][0]+1,len(data),1)]
    # planeTextLog += '\r\n' + str(lisOfOrder)
    # lcd2.display(len(lisOfOrder))
    # plainTextEdit.setPlainText(planeTextLog)
