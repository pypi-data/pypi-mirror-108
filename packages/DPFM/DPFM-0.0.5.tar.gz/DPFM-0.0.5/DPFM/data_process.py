import os
import sys
import numpy as np
import xlrd
import re
import pandas as pd
from netCDF4 import Dataset
def data_process(dirpath):
    files = os.listdir(dirpath)
    save_path = os.path.join(dirpath,'result_files')
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)
        print('making a new folder: result_files')
        print('we will put all processed files in this folder')
    func_pair={'CAHS':CAHS,'UGSZ':UGSZ,'UGWH':UGWH,'CAOT':CAOT,'DrIB':DrIB,
               'QBOU':QBOU,'WGHZ':WGHZ,'BPWH':BPWH,'FCOU':FCOU}
    for file in files:
        fun = file[0:4]
        if fun in func_pair.keys():
            print('processing the file:',file)
            file_path = os.path.join(dirpath, file)
            output = func_pair[fun](file_path)
            write2txt(output, file, save_path)


def BPWH(datapath):
    data = pd.read_csv(datapath, encoding='gbk', sep="\t")
    time = data['时间']
    time1 = time.str.split('-', expand=True)
    time2 = time1[2].str.split(':', expand=True)
    time3 = time2[0].str.split(' ', expand=True)

    year = time1[0]
    month = time1[1]
    day = time3[0]
    h = time3[1]
    m = time2[1]
    s = time2[2]
    lon = data['经度.1']
    lat = data['纬度.1']
    tem = data['电压值(V)']
    output1 = np.zeros(shape=(len(data[0:]), 11))
    output1[:, 0] = year
    output1[:, 1] = month
    output1[:, 2] = day
    output1[:, 3] = h
    output1[:, 4] = m
    output1[:, 5] = s
    output1[:, 6] = lon
    output1[:, 7] = lat
    output1[:, 8] = tem
    output1[:, 9] = np.nan
    output1[:, 10] = np.nan
    return output1


def CAHS(filename) :
    file = open(filename)
    p = []
    t = []
    s = []
    d = []
    lines = file.readlines()
    for line in lines:
        # 读取时间
        str3 = line[0:25]
        if str3 == "START TRANSMISSION YY-MM-":
            date1 = line[-13:]
            year1 = date1[0:4]
            month1 = date1[5:7]
            day1 = date1[8:10]
        if str3 == "START TRANSMISSION HH:MM:":  # 读取开始时间
            time1 = line[-11:]
            hour1 = time1[0:2]
            minute1 = time1[3:5]
            second1 = time1[6:8]
        if str3 == "FINISH TRANSMISSION HH:MM":  # 读取结束时间
            time2 = line[-11:]
            hour2 = time2[0:2]
            minute2 = time2[3:5]
            second2 = time2[6:8]
        if str3 == "START TRANSMISSION LONGIT":
            long1 = line[-9:]
        if str3 == "START TRANSMISSION LATITU":
            lati1 = line[-8:]
        # 读取横向的P、T、S
        str4 = line[0:14]
        if str4 == "DRIFT  PRESSUR":
            p.append(float(line[-8:]))
            d.append((float(float(line[-8:])) * 10000 / (1025 * 9.8)))
        if str4 == "DRIFT TEMPERAT":
            t.append(float(line[-7:]))
        if str4 == "DRIFT SALINITY":
            s.append(float(line[-8:]))
        # 读取纵向的P、T、S
        str5 = line[0:3]
        if len(str5) == 3 and len(str.lstrip(str5)) == 0:
            p.append(float(line.split()[0]))
            t.append(float(line.split()[1]))
            s.append(float(line.split()[2]))
            d.append((float(float(line.split()[0])) * 10000 / (1025 * 9.8)))
        #  横向数据个数
        str6 = line[0:28]
        if str6 == "FINISH TRANSMISSION HH:MM:SS":
            count = len(d)

    file.close()
    d = [("%.3f" % i) for i in d]
    t = [("%.3f" % i) for i in t]
    s = [("%.3f" % i) for i in s]

    #  输出时间插值
    start_time = int(hour1) * 3600 + int(minute1) * 60 + int(second1)
    total_time = (int(hour2) - int(hour1)) * 3600 + (int(minute2) - int(minute1)) * 60 + (
            int(second2) - int(second1))  # 观测总时间
    length = len(d) - count  # 剖面实际观测数量
    each_time = total_time // length  # 每个间隔的时间
    #  注意 这里的时间间隔计算时取整了，所以最后一个点的结束时间并不是读到的结束时间

    output = np.zeros((len(t), 11))
    for i in range(len(d)):
        output[i, 0] = int(year1)
        output[i, 1] = int(month1)
        output[i, 2] = int(day1)
        output[i, 3] = int(hour1)
        output[i, 4] = int(minute1)
        output[i, 5] = int(second1)
        output[i, 6] = float(long1)
        output[i, 7] = float(lati1)
        output[i, 8] = t[i]
        output[i, 9] = s[i]
        output[i, 10] = d[i]
        if i > count:
            output[i, 3] = int((start_time + each_time * (i - count)) // 3600)
            output[i, 4] = int(((start_time + each_time * (i - count)) - output[i, 3] * 3600) // 60)
            output[i, 5] = int(((start_time + each_time * (i - count)) - output[i, 3] * 3600 - output[i, 4] * 60))
    return output




def CAOT(filename) :
    file = open(filename)
    p = []
    t = []
    s = []
    d = []
    count = []
    lines = file.readlines()
    for line in lines:
        str2 = line[0:3]
        str3 = line[0:5]
        if str3 == "(FMT)":  # 开始时间
            date1 = line[-20:]
            year1 = date1[0:4]
            month1 = date1[5:7]
            day1 = date1[8:10]
            hour1 = date1[11:13]
            minute1 = date1[14:16]
            second1 = date1[17:19]
        if str3 == "(LMT)":  # 结束时间
            date2 = line[-20:]
            hour2 = date2[11:13]
            minute2 = date2[14:16]
            second2 = date2[17:19]
        if str3 == "LONGI":
            long1 = line[-9:]
        if str3 == "LATIT":
            lati1 = line[-8:]
        if not str2.isdecimal(): continue
        count.append((float(line.split()[0])))  # 提取序号
        p.append(float(line.split()[1]))
        t.append(float(line.split()[2]))
        s.append(float(line.split()[3]))
        d.append((float(float(line.split()[1])) * 10000 / (1025 * 9.8)))
    file.close()
    # 保留精度位数
    d = [("%.3f" % i) for i in d]
    t = [("%.3f" % i) for i in t]
    s = [("%.3f" % i) for i in s]
    #  输出时间插值
    start_time = int(hour1) * 3600 + int(minute1) * 60 + int(second1)
    total_time = (int(hour2) - int(hour1)) * 3600 + (int(minute2) - int(minute1)) * 60 + (
                int(second2) - int(second1))
    length = len(count)
    each_time = total_time // length
    #  注意 这里的时间间隔计算时取整了，所以最后一个点的结束时间并不是读到的结束时间
    for i in range(length - 1):
        for j in range(length - i - 1):
            if count[j] > count[j + 1]:
                count[j], count[j + 1] = count[j + 1], count[j]
                d[j], d[j + 1] = d[j + 1], d[j]
                t[j], t[j + 1] = t[j + 1], t[j]
                s[j], s[j + 1] = s[j + 1], s[j]

    output = np.zeros((len(d), 11))
    for i in range(len(d)):
        output[i, 0] = int(year1)
        output[i, 1] = int(month1)
        output[i, 2] = int(day1)
        output[i, 3] = int((start_time + each_time * i) // 3600)
        output[i, 4] = int(((start_time + each_time * i) - output[i, 3] * 3600) // 60)
        output[i, 5] = int(((start_time + each_time * i) - output[i, 3] * 3600 - output[i, 4] * 60))
        output[i, 6] = float(long1)
        output[i, 7] = float(lati1)
        output[i, 8] = t[i]
        output[i, 9] = s[i]
        output[i, 10] = d[i]
    return output


def DrIB(datapath):
    data = []
    with open(datapath, encoding='utf-8') as f:  # 打开文件
        line = f.readline()
        while line:
            a = line.split()
            data.append(a)
            line = f.readline()
    list = data[2:]
    var = np.zeros(shape=(len(data[2:]), len(data[2])))
    for i in range(len(list)):
        for j in range(len(list[0])):
            var[i, j] = float(list[i][j])
    output = np.zeros((len(var), 7))
    for i in range(len(var)):
        output[i, :2] = var[i, 1:3]
        output[i, 2] = var[i, 6]
        output[i, 3] = var[i, 5]
        output[i, 4:6] = var[i, 16:18]
        output[i, 6:] = 0
    """extract time"""
    day = output[:, 0] % 100
    month = (output[:, 0] % 10000) // 100
    year = (output[:, 0]) // 10000
    second = output[:, 1] % 100
    m = (output[:, 1] % 10000) // 100
    h = (output[:, 1]) // 10000

    output1 = np.zeros((len(var), 11))
    output1[:, 0] = int(year[0] + 2000)
    output1[:, 1] = month
    output1[:, 2] = day
    output1[:, 3] = h
    output1[:, 4] = m
    output1[:, 5] = second
    output1[:, 6:] = output[:, 2:]
    return output1


def FCOU(file_Path):
    with open(file_Path, 'r') as f:
        for num, line in enumerate(f):
            if num == 1:
                break
    DataTime = re.split(r"[\s:-]", line)
    Year = DataTime[2]
    Month = DataTime[3]
    Day = DataTime[4]
    Hour = DataTime[5]
    Minute = DataTime[6]
    Second = DataTime[7]

    def extractData(file_Path):
        file = open(file_Path, mode='r')
        pattern = re.compile(r'[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        line1 = file.readline()
        data = []
        while line1:
            strList = line1.split()
            isNum = pattern.match(strList[0])
            if isNum:
                data.append(strList)
            line1 = file.readline()
        file.close()
        return data

    data = extractData(file_Path)
    data1 = np.array(data)
    Temperature = data1[:, 0]
    floatT = Temperature
    floatT = list(map(float, floatT))
    arrayT = np.array(floatT)
    Pressure = data1[:, 1]
    floatP = Pressure
    floatP = list(map(float, floatP))
    arrayP = np.array(floatP)
    Depth = (arrayP * 10000) / (1025 * 9.8)
    Conductivity = data1[:, 2]
    floatC = Conductivity
    floatC = list(map(float, floatC))
    arrayC = np.array(floatC)
    Salinity = arrayC * 1388.8 - 24.87 * arrayC * arrayT - 6171.9
    Temperature1 = arrayT
    Temperature1 = Temperature1.reshape(-1, 1)
    Depth1 = Depth
    Depth1 = Depth1.reshape(-1, 1)
    Salinity1 = Salinity
    Salinity1 = Salinity1.reshape(-1, 1)

    output = np.zeros((len(Temperature1), 11))
    for i in range(len(Temperature1)):
        output[i, 0] = int(Year)
        output[i, 1] = int(Month)
        output[i, 2] = int(Day)
        output[i, 3] = int(Hour)
        output[i, 4] = int(Minute)
        output[i, 5] = int(Second)
        output[i, 6] = np.nan
        output[i, 7] = np.nan
        output[i, 8] = Temperature1[i][0]
        output[i, 9] = Salinity1[i][0]
        output[i, 10] = Depth1[i][0]
    return output

def QBOU(datapath):
    inp0 = Dataset(datapath, 'r')

    Time_Julian = inp0.variables['Time_Julian']
    Location = inp0.variables['Location']
    CTD_Conductivity = inp0.variables['CTD_Conductivity']
    CTD_Temperature = inp0.variables['CTD_Temperature']
    CTD_Pressure = inp0.variables['CTD_Pressure']
    Time = inp0.variables['Time']

    output = np.zeros((len(Time_Julian[0]), 11))
    Time = np.array(Time)
    Location = np.array(Location)
    Temperature = np.array(CTD_Temperature)
    Salinity = np.array(CTD_Conductivity)
    Depth = (np.array(CTD_Pressure)*10000)/(1025*9.8)

    for i in range(len(output)):
        for j in range(4):
            output[i][j] = int(Time.T[i][j])
        for k in range(2):
            output[i][6 + k] = Location.T[i][k]
        output[i, 8] = Temperature.T[i][0]
        output[i, 9] = Salinity.T[i][0]
        output[i, 10] = Depth.T[i][0]
    return output


def UGSZ(filename):
    inp1 = Dataset(filename, 'r')
    time = inp1.dimensions['samp'].size
    num = inp1.dimensions['n'].size
    lat = inp1.variables['start_lat']
    lon = inp1.variables['start_lon']
    depth = inp1.variables['depth']
    temperature = inp1.variables['temperature']
    salinity = inp1.variables['conductivity']

    output = np.zeros((time * num, 11))
    for i in range(time * num):
        output[i, :6] = 0
        output[i, 6] = lon[0]
        output[i, 7] = lat[0]
        output[i, 8] = temperature[i / time][i % time]
        output[i, 9] = salinity[i / time][i % time]
        output[i, 10] = depth[i / time][i % time]
    return output


def UGWH(filename):
    inp1 = Dataset(filename, 'r')
    time = inp1.dimensions['samp'].size
    num = inp1.dimensions['n'].size
    lat = inp1.variables['start_lat']
    lon = inp1.variables['start_lon']
    depth = inp1.variables['depth']
    temperature = inp1.variables['temperature']
    salinity = inp1.variables['salinity']

    output = np.zeros((time * num, 11))
    for i in range(time * num):
        output[i, :6] = 0
        output[i, 6] = lon[0]
        output[i, 7] = lat[0]
        output[i, 8] = temperature[i / time][i % time]
        output[i, 9] = salinity[i / time][i % time]
        output[i, 10] = depth[i / time][i % time]
    return output

def WGHZ(file_Path):
    data = xlrd.open_workbook(file_Path)
    booksheet = data.sheet_by_name('Sheet1')
    p = list()
    for row in range(booksheet.nrows):
        row_data = []
        for col in range(booksheet.ncols):
            cel = booksheet.cell(row, col)
            val = cel.value
            try:
                val = cel.value
            except:
                pass

            if type(val) == float:
                val = int(val)
            else:
                val = str(val)
            row_data.append(val)
        p.append(row_data)
    data1 = p[1]
    datatime = data1[2]
    Year = datatime[0:4]
    Month = datatime[5:7]
    Day = datatime[8:10]

    datatime1 = data1[3]
    Hour = datatime1[0:2]
    Minute = datatime1[3:5]
    Second = datatime1[6:8]

    lon = data1[4]
    lat = data1[5]

    temperature = data1[18]
    Salinity = 'NAN'
    Depth = 'NAN'
    arrayT = []
    arrayT.append(temperature)
    output = np.zeros((len(arrayT), 11))
    for i in range(len(arrayT)):
        output[i, 0] = int(Year)
        output[i, 1] = int(Month)
        output[i, 2] = int(Day)
        output[i, 3] = int(Hour)
        output[i, 4] = int(Minute)
        output[i, 5] = int(Second)
        output[i, 6] = float(lon)
        output[i, 7] = float(lat)
        output[i, 8] = float(temperature[i][0])
        output[i, 9] = np.nan
        output[i, 10] = np.nan
    return output

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


