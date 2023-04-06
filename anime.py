import cv2
import os

from tqdm import tqdm

from source.cartoonize import Cartoonizer


def animeOperate(anime_path, frame_path, tmp_path, video_num, data_root):
    input_path = tmp_path + "/" + video_num
    out_path = anime_path + "/" + video_num
    images_path = frame_path + "/" + video_num

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    images = os.listdir(images_path)
    algo = Cartoonizer(dataroot=data_root)
    # with tqdm(range(images.__len__()), leave=False) as t:
    #     for c in t:
    # t.set_description("Processing frame to anime")
    for c in range(images.__len__()):
        img_path = input_path + "/" + "frame_" + str(c) + "_fg.png"
        res_path = out_path + "/" + "frame_" + str(c) + "_fg.png"
        img = cv2.imread(img_path)[..., ::-1]
        result = algo.cartoonize(img)
        cv2.imwrite(res_path, result)
        # c += 1

    # t.close()
    print("anime operate done!")
