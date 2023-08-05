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