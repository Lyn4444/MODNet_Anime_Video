import anime
import generateAudio
import video
from config import Config
import frame

import shutil


class Operate:
    def __init__(self):
        self.config = Config()

    def setConfig(self, _config):
        self.config.video_path = _config['video_path']
        self.config.video_name = _config['video_name']
        self.config.video_num = _config['video_num']
        self.config.video_have_audio = _config['video_have_audio']
        self.config.complete_delete = _config['complete_delete']
        print("generate video config done!")

    def getRandom(self):
        return video.videoRandom()

    def doVideo(self):
        video.videoCopy(self.config.video_path, self.config.input_path, self.config.video_num, self.config.video_name)
        video.videoOperate(self.config.input_path, self.config.video_name, self.config.frame_path,
                           self.config.video_num)

    def doFrame(self):
        frame.frameOperate(self.config.frame_path, self.config.video_num, self.config.tmp_path,
                           self.config.MODNet_ckpt_path)

    def doAnime(self):
        anime.animeOperate(self.config.anime_path, self.config.frame_path, self.config.tmp_path, self.config.video_num,
                           self.config.DCTNet_data_root)

    def generateVideo(self):
        generateAudio.generate_anime_picture(self.config.frame_path, self.config.anime_path, self.config.tmp_path,
                                             self.config.video_num)
        generateAudio.generate_video(self.config.input_path, self.config.video_name, self.config.video_num,
                                     self.config.frame_path, self.config.output_path, self.config.tmp_path)
        if self.config.video_have_audio:
            generateAudio.generate_video_audio(self.config.input_path, self.config.video_name, self.config.output_path,
                                               self.config.audio_path, self.config.video_num)
        if self.config.complete_delete:
            _input_path = self.config.input_path + "/" + self.config.video_num
            _anime_path = self.config.anime_path + "/" + self.config.video_num
            _audio_path = self.config.audio_path + "/" + self.config.video_num
            _frame_path = self.config.frame_path + "/" + self.config.video_num
            _tmp_path = self.config.tmp_path + "/" + self.config.video_num
            shutil.rmtree(_input_path)
            shutil.rmtree(_anime_path)
            shutil.rmtree(_audio_path)
            shutil.rmtree(_frame_path)
            shutil.rmtree(_tmp_path)
            print("delete temp files done!")


if __name__ == "__main__":
    operate = Operate()
    video_num = operate.getRandom()
    video_path = "F:\\others_projects\\MODNet\\video\\input\\test3.mp4"
    video_have_audio = True
    complete_delete = True
    video_name = video_num + "." + video_path.split(".")[-1]
    video_dict = {"video_path": video_path, "video_name": video_name, "video_num": video_num,
                  "video_have_audio": video_have_audio, "complete_delete": complete_delete}

    operate.setConfig(video_dict)
    operate.doVideo()
    operate.doFrame()
    operate.doAnime()
    operate.generateVideo()
