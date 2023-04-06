class Config:
    def __init__(self):
        self.anime_path = "./video/anime"
        self.audio_path = "./video/audio"
        self.frame_path = "./video/frame"
        self.input_path = "./video/input"
        self.output_path = "./video/output"
        self.tmp_path = "./video/tmp"

        self.video_path = ""
        self.video_name = ""
        self.video_num = ""
        self.video_have_audio = True
        self.complete_delete = False

        self.MODNet_ckpt_path = "pretrained/modnet_photographic_portrait_matting.ckpt"
        self.DCTNet_data_root = "DCT-Net/damo/cv_unet_person-image-cartoon_compound-models"
