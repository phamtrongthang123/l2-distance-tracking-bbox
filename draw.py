import json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

count = 0
lstDir = ['1']
for lsd in lstDir:
    bboxes = []
    with open('cam_{}.json'.format(lsd), 'r') as f:
        file_content = json.load(f)

        for k, bbox in file_content.items():
            for ebbox in bbox:
                ebbox.append(int(k))
                bboxes.append(ebbox)
    bboxes = list(sorted(bboxes))
    dic_result_demo = {}
    for bbox in bboxes:
        if bbox[0] not in dic_result_demo:
            dic_result_demo[bbox[0]] = []
        dic_result_demo[bbox[0]].append(bbox[1:])

    # print(bboxes[:10])
    # use new format to draw
    os.system('mkdir ./rendered_cam_{}'.format(lsd))

    for imgtmp, lsbbox in dic_result_demo.items():
        img = './cam_{}/cam_{}.mp4_fr{}.jpg'.format(
            lsd, lsd, imgtmp+1)
        print('drawing {}'.format(img))
        source_img = Image.open(img).convert("RGB")
        draw = ImageDraw.Draw(source_img)
        for bbxs in lsbbox:

            draw.rectangle(
                ((bbxs[0], bbxs[1]), (bbxs[2], bbxs[3])), outline='red', width=5)

            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', 30)
            draw.text((bbxs[0], bbxs[1]-30), str(
                bbxs[-1]), (0, 255, 0), font=font)
        source_img.save(
            './rendered_cam_{}/{}'.format(lsd, img.split('/')[-1]))
        print('saved ./rendered_cam_{}/{}'.format(lsd, img.split('/')[-1]))


# print(count)
# dic_result_demo
