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

# 创建输出视频的Writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 可以根据需要选择不同的编码器

count = 0
# 创建进度条对象
progress_bar = tqdm(total=int(video.get(cv2.CAP_PROP_FRAME_COUNT)))

# 循环遍历视频帧并保存图像
for i in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
    success, image = video.read()
    if success:
        cv2.imwrite(f'video/frame/frame_{i}.jpg', image)
        progress_bar.update(1)
        progress_bar.set_description(f"Processed video {i + 1}/{int(video.get(cv2.CAP_PROP_FRAME_COUNT))} frames")
    else:
        break
    count += 1

progress_bar.close()

# 释放资源
video.release()

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# output_video_file = 'video/output/output.mp4'
# out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))
#
# image_folder = 'video/frame/'
# image_file_names = os.listdir(image_folder)
#
# images = []
# # 使用tqdm显示进度条
# with tqdm(range(image_file_names.__len__())) as t:
#     t.set_description("Processing read frame picture")
#     for c in t:
#         # 加载当前图像
#         images.append(cv2.imread(image_folder + 'frame_' + str(c) + '.jpg'))
#         c += 1
#
# t.close()
#
# with tqdm(range(images.__len__())) as t:
#     t.set_description("Processing picture to video")
#     for c in t:
#         # 加载当前图像
#         out.write(images[c])
#         c += 1
#
# # 释放输出视频对象
# out.release()
