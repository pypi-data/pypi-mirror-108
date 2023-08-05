import os
import sys
sys.path.append('./FUN/')
import numpy as np
import xlrd
import re
import pandas as pd
from netCDF4 import Dataset
from FUN import CAHS,UGSZ,UGWH,CAOT,DrIB,QBOU,WGHZ,BPWH,FCOU

def data_process(dirpath):
    files = os.listdir(dirpath)
    save_path = os.path.join(dirpath,'all_result')
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)
        print('new folder: all_result')
    func_pair={'CAHS':CAHS,'UGSZ':UGSZ,'UGWH':UGWH,'CAOT':CAOT,'DrIB':DrIB,
               QBOU:'QBOU','WGHZ':WGHZ,'BPWH':BPWH,'FCOU':FCOU}
    for file in files:
        fun = file[0:4]
        if fun in func_pair.keys():
            file_path = os.path.join(dirpath, file)
            output = func_pair[fun](file_path)
            write2txt(output, file, save_path)




def write2txt(output,filename,savepath):
    file_newname = filename + '_result.txt'
    if filename[-2:]=='nc':
        file_newname = filename[:-3] + '_result.txt'
    if filename[-3:]=='txt':
        file_newname = filename[:-4] + '_result.txt'
    if filename[-4:]=='xlsx':
        file_newname = filename[:-5] + '_result.txt'
    file_newpath=os.path.join(savepath,file_newname)
    file_txt = open(file_newpath, mode='w')
    file_txt.write("{:<15} {:<14} {:<14} {:<13} {:<13} {:<14} {:<14} {:<15} {:<18} {:<15} {:<15}\n".format('年','月','日','时','分','秒','经度','纬度','温度','盐度','深度'))
    length = len(output)
    for i in range(length):
        file_txt.write("{:<15}".format(int(output[i, 0])))
        file_txt.write("{:<15}".format(int(output[i, 1])))
        file_txt.write("{:<15}".format(int(output[i, 2])))
        file_txt.write("{:<15}".format(int(output[i, 3])))
        file_txt.write("{:<15}".format(int(output[i, 4])))
        file_txt.write("{:<15}".format(int(output[i, 5])))
        file_txt.write("{:<16.6f}".format(output[i, 6]))
        file_txt.write("{:<16.6f}".format(output[i, 7]))
        file_txt.write("{:<15.4f}".format(output[i, 8]))
        file_txt.write("{:<15.4f}".format(output[i, 9]))
        file_txt.write("{:<15.3f}".format(output[i, 10]))
        file_txt.write("\n")
    file_txt.close()
    return file_txt


