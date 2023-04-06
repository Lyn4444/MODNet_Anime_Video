import os
import shutil
import random

import cv2
from tqdm import tqdm


def videoRandom():
    video_num = str(random.randint(100000, 999999))
    # print("generate video num: " + video_num + " done!")
    return video_num


def videoCopy(video_path, input_path, video_num, video_name):
    new_path = input_path + "/" + video_num
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if not os.path.isfile(video_path):
        print(video_path + " not exist!")
    else:
        shutil.copy(video_path, new_path + "/" + video_name)
    print("video copy done!")


def videoOperate(input_path, video_name, frame_path, video_num):
    video_path = input_path + "/" + video_num
    if not os.path.exists(video_path):
        os.makedirs(video_path)
    video_name_path = video_path + "/" + video_name
    video = cv2.VideoCapture(video_name_path)

    fps = video.get(cv2.CAP_PROP_FPS)
    print("video fps: " + str(fps))

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # progress_bar = tqdm(total=int(video.get(cv2.CAP_PROP_FRAME_COUNT)), leave=False)

    new_frame_path = frame_path + "/" + video_num

    if not os.path.exists(new_frame_path):
        os.makedirs(new_frame_path)

    count = 0
    for i in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
        success, image = video.read()
        if success:
            cv2.imwrite(new_frame_path + '/frame_' + str(i) + '.jpg', image)
            # progress_bar.update(1)
            # progress_bar.set_description(f"Processed video {i + 1}/{int(video.get(cv2.CAP_PROP_FRAME_COUNT))} frames")
        else:
            break
        count += 1
    # progress_bar.close()

    # 释放资源
    video.release()
    print("video operate done!")

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# output_video_file = 'video/output/output.mp4'
# out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))
# image_folder = 'video/frame/'
# image_file_names = os.listdir(image_folder)
# images = []
# # 使用tqdm显示进度条
# with tqdm(range(image_file_names.__len__())) as t:
#     t.set_description("Processing read frame picture")
#     for c in t:
#         # 加载当前图像
#         images.append(cv2.imread(image_folder + 'frame_' + str(c) + '.jpg'))
#         c += 1
# t.close()
# with tqdm(range(images.__len__())) as t:
#     t.set_description("Processing picture to video")
#     for c in t:
#         # 加载当前图像
#         out.write(images[c])
#         c += 1
# # 释放输出视频对象
# out.release()
