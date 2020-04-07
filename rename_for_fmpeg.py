import os
from os import listdir
from os.path import isfile, join
# fon01 = [f for f in listdir('/content/average_drawn_best_dla_01')]
# fon01 = list(sorted(fon01))
fon01 = ['rendered_cam_1']
for fo in fon01:
    path = '{}'.format(fo)
    for filename in os.listdir(path):
        prefix, num = filename[:-4].split('fr')
        num = num.zfill(5)
        new_filename = prefix + "fr" + num + ".jpg"
        os.rename(os.path.join(path, filename),
                  os.path.join(path, new_filename))
