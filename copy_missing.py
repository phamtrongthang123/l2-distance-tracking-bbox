from os import listdir
from os.path import isfile, join
import os 
lstDir = ['1']
# source = './sampled_frames'
source = 'cam_1'
for lsd in lstDir:
    rendered = "rendered_cam_{}".format(lsd)
    rendered_files = [f.split('.jp')[0] for f in listdir(rendered) if isfile(join(rendered, f))]
    source_files = [f.split('.jp')[0] for f in listdir(source) if (isfile(join(source, f)) and f.split('.mp4')[0].split('_')[1] == '{}'.format(lsd))]
    old_source_files = source_files.copy()
    for i,sf in enumerate(source_files):
        prefix, num = sf.split('fr')
        num = num.zfill(5)
        source_files[i] = prefix + "fr" + num
    # print(len(source_files))
    # print(len(rendered_files))
    for i,sf in enumerate(source_files):
        if sf not in rendered_files:
            print('cp {}/{}.jpg {}/{}.jpg'.format(source,old_source_files[i],rendered,sf))
            os.system('cp {}/{}.jpg {}/{}.jpg'.format(source,old_source_files[i],rendered,sf))