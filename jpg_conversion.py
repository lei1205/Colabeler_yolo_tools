import os
import cv2

# convert bmp to jpg (Not used)
def bmptojpg(dir):
    if not os.path.exists(dir + 'jpg/'):
        os.makedirs(dir + 'jpg/')

    filelists = os.listdir(dir)
    for file in filelists:
        img = cv2.imread(dir + file,-1)
        cv2.imwrite(dir + 'jpg/' + file.split('.bmp')[0] + '.jpg',img)
        print('已转换'+file+'为jpg') 