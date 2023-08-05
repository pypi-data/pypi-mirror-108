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