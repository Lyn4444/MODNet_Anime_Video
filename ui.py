"""
本代码由[Tkinter布局助手]生成
当前版本:3.1.2
官网:https://www.pytk.net/tkinter-helper
QQ交流群:788392508
"""
import os
import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import cv2
from PIL import ImageTk, Image

from operate import Operate

"""
全局通用函数
"""


# 自动隐藏滚动条
def scrollbar_autohide(bar, widget):
    def show():
        bar.lift(widget)

    def hide():
        bar.lower(widget)

    hide()
    widget.bind("<Enter>", lambda e: show())
    bar.bind("<Enter>", lambda e: show())
    widget.bind("<Leave>", lambda e: hide())
    bar.bind("<Leave>", lambda e: hide())


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_video_local = self.__tk_label_video_local()
        self.tk_label_video_anime = self.__tk_label_video_anime()
        self.tk_label_framelabel = self.__tk_label_framelabel()
        self.tk_button_selectlocalvideo = self.__tk_button_selectlocalvideo()
        self.tk_select_box_framecombobox = self.__tk_select_box_framecombobox()
        self.tk_label_animelabel = self.__tk_label_animelabel()
        self.tk_select_box_animecombobox = self.__tk_select_box_animecombobox()
        self.tk_button_generatevideo = self.__tk_button_generatevideo()
        self.tk_button_playlocalvideo = self.__tk_button_playlocalvideo()
        self.tk_button_playgeneratevideo = self.__tk_button_playgeneratevideo()
        self.tk_text_textout = self.__tk_text_textout()
        self.tk_label_settinglabel = self.__tk_label_settinglabel()
        self.tk_select_box_settingcombobox = self.__tk_select_box_settingcombobox()

    def __win(self):
        self.title("video character animation")
        self.iconbitmap("./logo.ico")
        # 设置窗口大小、居中
        width = 1280
        height = 800
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def __tk_label_video_local(self):
        label = Label(self, text="本地视频", anchor="center", borderwidth=2, relief="ridge")
        label.place(x=20, y=20, width=600, height=450)
        return label

    def __tk_label_video_anime(self):
        label = Label(self, text="生成视频", anchor="center", borderwidth=2, relief="ridge")
        label.place(x=660, y=20, width=600, height=450)
        return label

    def __tk_label_framelabel(self):
        label = Label(self, text="人物切割模型", anchor="center")
        label.place(x=260, y=520, width=80, height=30)
        return label

    def __tk_button_selectlocalvideo(self):
        btn = Button(self, text="选择视频")
        btn.place(x=20, y=520, width=100, height=30)
        return btn

    def __tk_select_box_framecombobox(self):
        cb = Combobox(self, state="readonly")
        cb['values'] = ("MODNet", "BSHM")
        cb.current(0)
        cb.place(x=360, y=520, width=130, height=30)
        return cb

    def __tk_label_animelabel(self):
        label = Label(self, text="人物动画化模型", anchor="center")
        label.place(x=520, y=520, width=90, height=30)
        return label

    def __tk_select_box_animecombobox(self):
        cb = Combobox(self, state="readonly")
        cb['values'] = ("DCTNet")
        cb.current(0)
        cb.place(x=630, y=520, width=130, height=30)
        return cb

    def __tk_button_generatevideo(self):
        btn = Button(self, text="生成视频")
        btn.place(x=1050, y=520, width=90, height=30)
        return btn

    def __tk_button_playlocalvideo(self):
        btn = Button(self, text="播放视频")
        btn.place(x=140, y=520, width=100, height=30)
        return btn

    def __tk_button_playgeneratevideo(self):
        btn = Button(self, text="播放视频")
        btn.place(x=1160, y=520, width=100, height=30)
        return btn

    def __tk_text_textout(self):
        text = Text(self)
        text.place(x=20, y=580, width=1240, height=200)

        vbar = Scrollbar(self)
        text.configure(yscrollcommand=vbar.set)
        vbar.config(command=text.yview)
        vbar.place(x=1245, y=580, width=15, height=200)
        scrollbar_autohide(vbar, text)
        return text

    def __tk_label_settinglabel(self):
        label = Label(self, text="视频处理配置", anchor="center")
        label.place(x=780, y=520, width=90, height=30)
        return label

    def __tk_select_box_settingcombobox(self):
        cb = Combobox(self, state="readonly")
        cb['values'] = ("仅视频，删除缓存", "仅视频，不删除缓存", "有声音，删除缓存", "有声音，不删除缓存")
        cb.current(2)
        cb.place(x=880, y=520, width=150, height=30)
        return cb


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.video_path = ""
        self.anime_video_path = ""
        self.cap_local = ""
        self.cap_anime = ""
        self.is_play_local_video = False
        self.is_play_anime_video = False
        self.video_have_audio = True
        self.complete_delete = True
        self.frame_combobox_value = self.tk_select_box_framecombobox.get()
        self.anime_combobox_value = self.tk_select_box_animecombobox.get()
        self.setting_combobox_value = self.tk_select_box_settingcombobox.get()

        self.isDone = False

        # 控制台输出重定向
        self.stdoutCall = sys.stdout
        self.stderrCall = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        self.tk_text_textout.insert('end', info)
        self.tk_text_textout.update()
        self.tk_text_textout.see(tkinter.END)

    def restoreStd(self):
        sys.stdout = self.stdoutCall
        sys.stderr = self.stderrCall

    def read_local_video(self, _local_path):
        self.cap_local = cv2.VideoCapture(_local_path)

    def read_anime_video(self, _anime_video):
        self.cap_anime = cv2.VideoCapture(_anime_video)

    def play_local_video_label(self):
        ret, frame = self.cap_local.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        height = cv2image.shape[0]
        width = cv2image.shape[1]
        if height >= width:
            _width = int(width * 450 / height)
            cv2image = cv2.resize(cv2image, (_width, 450), interpolation=cv2.INTER_AREA)
        else:
            _height = int(height * 600 / width)
            cv2image = cv2.resize(cv2image, (600, _height), interpolation=cv2.INTER_AREA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.tk_label_video_local.imgtk = imgtk
        self.tk_label_video_local.configure(image=imgtk)
        self.tk_label_video_local.after(10, self.play_local_video_label)

    def play_anime_video_label(self):
        ret, frame = self.cap_anime.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        height = cv2image.shape[0]
        width = cv2image.shape[1]
        if height >= width:
            _width = int(width * 450 / height)
            cv2image = cv2.resize(cv2image, (_width, 450), interpolation=cv2.INTER_AREA)
        else:
            _height = int(height * 600 / width)
            cv2image = cv2.resize(cv2image, (600, _height), interpolation=cv2.INTER_AREA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.tk_label_video_anime.imgtk = imgtk
        self.tk_label_video_anime.configure(image=imgtk)
        self.tk_label_video_anime.after(10, self.play_anime_video_label)

    def select_local_video(self, evt):
        _path = filedialog.askopenfilename()
        _path = _path.replace("/", "\\\\")
        self.video_path = _path
        print("选择的本地视频路径：" + self.video_path)

    def do_frame_model(self, evt):
        self.frame_combobox_value = self.tk_select_box_framecombobox.get()
        print("选择的人物切割模型：" + self.frame_combobox_value)

    def do_anime_model(self, evt):
        self.anime_combobox_value = self.tk_select_box_animecombobox.get()
        print("选择的人物动画化模型：" + self.anime_combobox_value)

    def generate_anime_video(self, evt):
        print("\n***********************************************************************************")
        print("生成视频总配置：")
        print("本地视频路径：" + self.video_path)
        print("人物切割模型：" + self.frame_combobox_value)
        print("人物动画化模型：" + self.anime_combobox_value)
        print("视频处理配置：" + self.setting_combobox_value)

        operate = Operate()
        video_num = operate.getRandom()
        if self.video_have_audio:
            video_name = "anime_" + video_num + "_audio." + self.video_path.split(".")[-1]
        else:
            video_name = "anime_" + video_num + "." + self.video_path.split(".")[-1]
        print("生成人物动画化视频地址：" + (os.getcwd() + "/video/output/" + str(video_num) + "/" + str(video_name))
              .replace("/", "\\\\"))
        print("***********************************************************************************\n")
        video_dict = {"video_path": self.video_path, "video_name": video_name, "video_num": video_num,
                      "video_have_audio": self.video_have_audio, "complete_delete": self.complete_delete}
        operate.setConfig(video_dict)
        operate.doVideo()
        operate.doFrame()
        operate.doAnime()
        operate.generateVideo()
        self.anime_video_path = (os.getcwd() + "/video/output/" + str(video_num) + "/" + str(video_name))\
            .replace("/", "\\\\")
        self.isDone = True

    def play_local_video(self, evt):
        self.read_local_video(self.video_path)
        self.play_local_video_label()

    def play_anime_video(self, evt):
        if self.isDone:
            self.read_anime_video(self.anime_video_path)
            self.play_anime_video_label()

    def do_config_video(self, evt):
        self.setting_combobox_value = self.tk_select_box_settingcombobox.get()
        index = str(self.tk_select_box_settingcombobox['values'].index(self.setting_combobox_value))
        if index == "0":
            self.video_have_audio = False
            self.complete_delete = True
        elif index == "1":
            self.video_have_audio = False
            self.complete_delete = False
        elif index == "2":
            self.video_have_audio = True
            self.complete_delete = True
        else:
            self.video_have_audio = True
            self.complete_delete = False
        print("选择的视频处理配置：" + self.setting_combobox_value)

    def __event_bind(self):
        self.tk_button_selectlocalvideo.bind('<Button>', self.select_local_video)
        self.tk_button_generatevideo.bind('<Button>', self.generate_anime_video)
        self.tk_button_playlocalvideo.bind('<Button>', self.play_local_video)
        self.tk_button_playgeneratevideo.bind('<Button>', self.play_anime_video)
        self.tk_select_box_framecombobox.bind('<<ComboboxSelected>>', self.do_frame_model)
        self.tk_select_box_animecombobox.bind('<<ComboboxSelected>>', self.do_anime_model)
        self.tk_select_box_settingcombobox.bind('<<ComboboxSelected>>', self.do_config_video)


if __name__ == "__main__":
    win = Win()
    win.mainloop()
