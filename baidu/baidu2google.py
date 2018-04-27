#encoding:utf-8

import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')
pi = 3.14159265358979324 * 3000.0 / 180.0
a = 6378245.0
ee = 0.00669342162296594323
'''
百度坐标转高德、谷歌坐标
bd09->gcj02
'''
def bd09IItogcj02(lng, lat):
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * pi)
    gg_lon = z * math.cos(theta)
    gg_lat = z * math.sin(theta)

    return float('%.6f' % gg_lon), float('%.6f' % gg_lat)
#
#print bd09IItogcj02(113.955791,22.509315)

'''
1.百度原始坐标转经纬度
2.经纬度坐标转gcj02
'''


def gcj02towgc84(lng,lat):
    '''
    gcj02->wgc84
    '''
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng

    return [float('%.6f' % (lng * 2 - mglng)), float('%.6f' % (lat * 2 - mglat))]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

#print gcj02towgc84(113.955791,22.509315)




class GPS:
    PI = 3.14159265358979324
    x_pi = 3.14159265358979324 * 3000.0 / 180.0

    def delta(self,lat, lon):
        a = 6378245.0
        ee = 0.00669342162296594323
        dLat = self.transformLat(lon - 105.0, lat - 35.0)
        dLon = self.transformLon(lon - 105.0, lat - 35.0)
        radLat = lat / 180.0 * self.PI
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * self.PI)
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * self.PI)
        return {'lat': dLat, 'lon': dLon}

    def gps84_to_gcj02(self, wgsLon, wgsLat):
        if self.outOfChina(wgsLat, wgsLon):
            return {'lat': wgsLat, 'lon': wgsLon}

        d = self.delta(wgsLat, wgsLon)
        return float('%.06f' % (wgsLon + d['lon'])), float('%.06f' % (wgsLat + d['lat']))

    def outOfChina(self,lat, lon):
        if lon < 72.004 or lon > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False

    def transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * float(x) * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * self.PI) + 40.0 * math.sin(y / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * self.PI) + 320 * math.sin(y * self.PI / 30.0)) * 2.0 / 3.0
        return ret

    def transformLon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * self.PI) + 40.0 * math.sin(x / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * self.PI) + 300.0 * math.sin(x / 30.0 * self.PI)) * 2.0 / 3.0
        return ret


#gps = GPS()
#print gps.gps84_to_gcj02(113.949235,22.503618)
#
data_file = open('bd_station7.txt')
line = data_file.readline().decode("utf-8")
while line:
    datas = line.strip('\n').split('\t')

    if len(datas) > 5:
        tmp = []
        for i in datas:
            try:
                if i.find(':') != -1:
                    zb = i.split(':')
                    x = float(zb[1].split(',')[0])
                    y = float(zb[1].split(',')[1])
                    tx,ty = bd09IItogcj02(x, y)
                    stri = str(zb[0])+":" + str(tx) + "," + str(ty)
                    tmp.append(stri)
                else:
                    tmp.append(i)
            except Exception as e:
                print "---------------",i,e
                
        print '\t'.join(tmp)
    line = data_file.readline().decode("utf-8")
data_file.close()