import numpy as np
import sys
import glob
import math
import json
import itertools

FRAME_RADIUS = 5
DIST_RADIUS = 200  # pixel

next_id = 0
dict_path = {}
dict_miss = {}


def to_float(x):
    return float("{:.2f}".format(x))


def compute_dist(x, y):
    x = x[1:]  # remove frame id
    # format x1,y1,x2,y2
    dx = (x[0]+x[2])/2 - (y[0]+y[2])/2
    dy = (x[1]+x[3])/2 - (y[1]+y[3])/2
    dist = math.sqrt(dx*dx + dy*dy)
    return dist


def match_bb(id_frame, k, x, _boxes):
    if len(_boxes) == 0:
        dict_miss[k] += 1
        return None
    distances = np.array([compute_dist(x, y) for y in _boxes])
    id_min = np.argmin(distances)
    if distances[id_min] < DIST_RADIUS:
        dict_path[k].append([id_frame]+_boxes[id_min])      # append next bb
        # reset missing counter
        dict_miss[k] = 0
        return _boxes[id_min]
    else:
        dict_miss[k] += 1
        return None
    pass


def match_bboxes(id_frame, boxes):
    matched_boxes = []
    cp_boxes = boxes.copy()
    for k in dict_path.keys():
        if dict_miss[k] < FRAME_RADIUS:
            tmp = match_bb(id_frame, k, dict_path[k][-1], cp_boxes)
            matched_boxes.append(tmp)
            if tmp != None:
                cp_boxes.remove(tmp)
            if len(cp_boxes) == 0:
                break

    global next_id
    for it in boxes:
        if it not in matched_boxes:
            dict_path[str(next_id)] = [[id_frame]+it]
            dict_miss[str(next_id)] = 0
            next_id += 1

    pass


def convert_a_Khoa_format_to_thay_An(bbox_with_categories, threshold=0.2):
    """
        Format a khoa có dạng {1:[bboxs], 2:[bboxs]}
    """
    
    bbox_with_categories_1 = np.insert(bbox_with_categories[1], -1,1,axis=1)
    bbox_with_categories_2 = np.insert(bbox_with_categories[2], -1,2,axis=1)
    
    thay_An_bboxs = np.concatenate(
        (bbox_with_categories_1, bbox_with_categories_2), axis=0)
    thay_An_bboxs = thay_An_bboxs[thay_An_bboxs[:, -1] >= threshold]
    
    thay_An_bboxs = thay_An_bboxs[:, :-1]
    for i in range(0, len(thay_An_bboxs)):
        thay_An_bboxs[i] = list(map(to_float, thay_An_bboxs[i]))
    thay_An_bboxs = thay_An_bboxs.tolist()
    thay_An_bboxs.sort()

    return list(thay_An_bboxs for thay_An_bboxs, _ in itertools.groupby(thay_An_bboxs))


if __name__ == "__main__":
    proposal_file = sys.argv[1]
    out_file = sys.argv[2]

    frames = np.load(proposal_file, allow_pickle=True)

    print('#proposals', len(frames))
    convert_a_Khoa_format_to_thay_An(frames[0])
    print(convert_a_Khoa_format_to_thay_An(frames[0]))
    # print(convert_a_Khoa_format_to_thay_An(frames[1]))
    # input()

    boxes = convert_a_Khoa_format_to_thay_An(frames[0])
    # print(boxes)
    print('#start box', len(boxes))
    for i in range(len(boxes)):
        dict_path[str(i)] = [[0]+list(boxes[i])]
        dict_miss[str(i)] = 0
    next_id = len(boxes)
    for i in range(1, len(frames), 1):
        boxes = convert_a_Khoa_format_to_thay_An(frames[i])

        match_bboxes(i, boxes)

    json.dump(dict_path, open(out_file, 'wt'), indent=4)
    # for it in dict_path.keys():
    #     print(it, len(dict_path[it]))
