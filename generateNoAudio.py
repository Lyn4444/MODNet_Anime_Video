import os

import cv2
from tqdm import tqdm

# 打开视频文件
video = cv2.VideoCapture('video/input/test2.mp4')

# 获取视频帧率
fps = video.get(cv2.CAP_PROP_FPS)
print("fps: " + str(fps))

# 获取视频尺寸
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video_file = 'video/output/output_anime_delect.mp4'
out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

image_folder = 'video/anime/'
image_file_names = os.listdir(image_folder)

images = []
# 使用tqdm显示进度条
with tqdm(range(image_file_names.__len__())) as t:
    t.set_description("Processing read frame picture")
    for c in t:
        # 加载当前图像
        images.append(cv2.imread(image_folder + 'frame_' + str(c) + '_fg.png'))
        c += 1

t.close()

with tqdm(range(images.__len__())) as t:
    t.set_description("Processing picture to video")
    for c in t:
        # 加载当前图像
        out.write(images[c])
        c += 1

# 释放输出视频对象
out.release()
