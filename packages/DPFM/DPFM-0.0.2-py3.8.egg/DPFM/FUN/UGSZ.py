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