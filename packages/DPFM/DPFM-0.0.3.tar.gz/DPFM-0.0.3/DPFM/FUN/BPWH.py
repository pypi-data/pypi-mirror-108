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
