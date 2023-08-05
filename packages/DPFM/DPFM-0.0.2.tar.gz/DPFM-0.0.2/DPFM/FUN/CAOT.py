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