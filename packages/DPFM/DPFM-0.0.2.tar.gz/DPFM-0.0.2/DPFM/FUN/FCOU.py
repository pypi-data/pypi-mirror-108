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