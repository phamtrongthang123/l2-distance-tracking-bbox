# L2 distance tracking

## Giới thiệu

Repo này chứa các file cần thiết để phục vụ việc tracking, tức là từ 1 bộ các bbox, ta gộp nó lại thành những dãy bbox ở từng frame khác nhau cho 1 đối tượng

Giả sử ta có video tên cam_1.mp4 và bộ bbox format:

```{json}
[
    {1:list bbox with score, 2:list bbox with score},
    {...}
]
```

- 1,2 ở phía trên chính là category id, ví dụ 1:car, 2:truck.
- list bbox with score sẽ là dãy `[...,[x1,y1,x2,y2,score],...]`

Mục đích của code repo này là sinh file json, format được biểu diễn dưới dạng 1 dictionary gồm nhiều đối tượng (là con số xanh trong video) được track, mỗi đối tượng sẽ chứa 1 chuỗi các item gồm bbox đi kèm số frame xuất hiện của nó. Cụ thể, xét đối tượng thứ `10` xuất hiện ở frame `1`, frame `2` với bbox tương ứng lần lượt là `(x1,y1,x2,y2)` và `(a1,b1,a2,b2)` thì bên trong json sẽ có dạng:

```
{
    ...,
    '10': [[1,x1,y1,x2,y2],[2,a1,b1,a2,b2]]
    ...,
}
```

## Quick usage

Với video cam_1.mp4 trên, vào file vid2frame.py để chỉnh path ở chỗ này

```{python}
def vid2frames(video_path, ratio, frames_path):
    count = 0
    for video_name in os.listdir(video_path):
        if(video_name == "cam_1.mp4"):  
            count += 1
            print("Processing video ", count)
```

Sau khi chỉnh video_name về đúng tên (như trên chỉ muốn chạy cam_1) thì gọi lần lượt:

```{sh}
mkdir sampled_frames # nếu chưa có thư mục
python vid2frame.py
```

Toàn bộ frame sẽ được sinh ra bên trong thư mục trên, dưới format
`cam_1.mp4_fr<frame id>.jpg` với frame id bắt từ đầu 1.

Sau đó gọi search_path.py để chuyển bbox raw từ pkl sang json, có threshold bên trong.

```{sh}
python search_path.py path/to/pkl/raw.pkl path/to/output.json
```

Ví dụ như cam_1.mp4 với pkl file là cam_1.mp4.pkl nằm ngay thư mục chứa code thì mình sẽ gọi:

```
python search_path.py cam_1.mp4.pkl cam_1.json
```

muốn chỉnh threshold buộc phải vào source code chỉnh, nó nằm ngay hàm `def convert_a_Khoa_format_to_thay_An(bbox_with_categories, threshold=0.2):`

Sau đó vào lần lượt file `draw.py` _(dùng để vẽ bbox từ json và ảnh frame gốc)_, `rename_for_fmpeg.py` _(để rename về đúng format ffmpeg để sinh video vizualize)_ và `copy_missing.py` _(do vẽ từ json nên sẽ có frame thiếu, do đó phải copy frame không có bbox từ frame gốc để xíu ffmpeg ra video đầy đủ)_ để chỉnh path:

```{python}
# draw.py
lstDir = ['1']
for lsd in lstDir:
    bboxes = []
    with open('cam_{}.json'.format(lsd), 'r') as f:
        file_content = json.load(f)
    # ...
    # Chỗ này có thể không cần chỉnh
    os.system('mkdir ./rendered_cam_{}'.format(lsd))

    for imgtmp, lsbbox in dic_result_demo.items():
        # phía dưới phải chỉnh về ./sampled_frames/cam_{}.mp4_fr{}.jpg nếu chạy mặc định code vid2frame.py
        img = './cam_{}/cam_{}.mp4_fr{}.jpg'.format(
            lsd, lsd, imgtmp+1)


# rename_for_fmpeg.py
# chỗ này nếu được có thể refactor code gọn, nhưng ý tưởng là ghi path mà đã lưu bộ ảnh
fon01 = ['rendered_cam_1']
for fo in fon01:
    path = '{}'.format(fo)

# copy_missing.py
# Nếu dùng mặc định vid2frame thì uncomment cái source đầu, xóa source sau đi
lstDir = ['1']
# source = './sampled_frames'
source = 'cam_1'
for lsd in lstDir:
    rendered = "rendered_cam_{}".format(lsd)
```

Chỉnh xong hết thì chạy `sh run.sh` là treo máy được rồi, vẽ sẽ rất lâu.
Nếu muốn sinh video thì mình dùng ffmpeg, gọi lệnh bên dưới:

```
ffmpeg -framerate 10 -f image2 -start_number 1  -i "./rendered_cam_1/cam_1.mp4_fr%05d.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p ./rendered_cam_1.mp4
```

Các tham số thì google để hiểu rõ, đại loại là kết quả sẽ là video fps = 10, và id chạy của ảnh là 1.

## Chạy sinh nhiều json để treo máy

Có thể dùng script bên dưới (giả sử tất cả nằm ở thư mục bboxes)

```{sh}
mkdir alljson # nên gom kết quả về 1 thư mục
for pklfile in "./bboxes"/*
do
  filename=$(basename -- "$pklfile")
  echo "converting $pklfile to alljson/${filename%.mp4.*}.json"
  python search_path.py "$pklfile" "alljson/${filename%.mp4.*}.json"
done
```
