from tkinter.constants import N
from xml.dom.minidom import parse
import os
import cv2
import re

index = {'HeavyVehicle':0,'MidsizeVehicle':1,'CompactVehicle':2,'Car':3,'NoneVehicle':4,'Pedestrian':5,'LargeBus':6,'LightBus':7}

class bbox():
    type = ''
    mid_x = 0
    mid_y = 0
    dis_x = 0
    dis_y = 0

def get(dir):
    DOMTree=parse(dir)
    collection=DOMTree.documentElement
    
    result = []
    w = int(collection.getElementsByTagName('width')[0].childNodes[0].data)
    h = int(collection.getElementsByTagName('height')[0].childNodes[0].data)

    items = collection.getElementsByTagName('item')
    for i in items:
        b = bbox()
        b.type = i.getElementsByTagName('name')[0].childNodes[0].data

        lu_1 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('xmin')[0].childNodes[0].data)
        lu_2 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('ymin')[0].childNodes[0].data)
        rb_1 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('xmax')[0].childNodes[0].data)
        rb_2 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('ymax')[0].childNodes[0].data)

        # 0 中心点（归一化宽） 中心点（归一化长） 框宽度（归一化） 框长度（归一化）
        b.mid_x = (rb_1 + lu_1) / 2 / w
        b.mid_y = (rb_2 + lu_2) / 2 / h
        b.dis_x = (rb_1 - lu_1) / w
        b.dis_y = (rb_2 - lu_2) / h

        result.append(b)
    return result
    
dir = '../0517zyq/PV2001_ImageAnnotation/'
dir_0 = dir + 'outputs/'
result_dir = dir + 'outputs_yolo/'
jpg_dir = dir + 'jpg/'

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

if not os.path.exists(jpg_dir):
    os.makedirs(jpg_dir)

filelists = os.listdir(dir)
for file in filelists[:-3]:
    img = cv2.imread(dir + file,-1)
    cv2.imwrite(jpg_dir + file.split('.bmp')[0] + '.jpg',img)
    print('已转换'+file+'为jpg')  

for n_0 in filelists:
    n_0 = n_0.split('.bmp')[0] + '.xml'
    if os.path.exists(dir_0 + n_0):
        res = ''
        r = get(dir_0 + n_0)
        tar_num = len(get(dir_0 + n_0))
        print(n_0 + ', 目标数量：' + str(tar_num))

       
        for k in range(tar_num):
            t = re.sub('[\W_]+', '', r[k].type)
            res += str(index[t]) + ' ' + str(r[k].mid_x) + ' ' + str(r[k].mid_y) + ' ' + str(r[k].dis_x) + ' ' + str(r[k].dis_y) + '\n'

        f = open(result_dir + n_0.split('.xml')[0] + '.txt', 'a')
        f.write(res)
        f.close()