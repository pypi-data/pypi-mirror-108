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