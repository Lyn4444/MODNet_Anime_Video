import cv2
import os

from tqdm import tqdm

from source.cartoonize import Cartoonizer


def process(input_path, out_path, frame_path):
    images = os.listdir(frame_path)
    algo = Cartoonizer(dataroot="DCT-Net/damo/cv_unet_person-image-cartoon_compound-models")
    with tqdm(range(images.__len__())) as t:
        for c in t:
            t.set_description("Processing frame to anime")
            img_path = input_path + "/" + "frame_" + str(c) + "_fg.png"
            res_path = out_path + "/" + "frame_" + str(c) + "_fg.png"
            img = cv2.imread(img_path)[..., ::-1]
            result = algo.cartoonize(img)
            cv2.imwrite(res_path, result)
            c += 1

    t.close()


if __name__ == '__main__':
    input_path = "video/tmp"
    out_path = "video/anime"
    frame_path = "video/frame"

    process(input_path, out_path, frame_path)
