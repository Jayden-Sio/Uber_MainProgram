import os
import time

import pygame
import sys

import pyaudio, wave
from tqdm import tqdm

import of2 as of
from playsound import playsound


class Screen:
    @staticmethod
    def center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def __init__(self, caption, width, height, flags=0):
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((400, 600), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.fps = 60

    def idle(self):
        self.delta = self.clock.tick(self.fps)


class Pen:
    def __init__(self, font, color):
        self.font = font
        self.color = color

    def draw(self, surface, text, position=(0, 0), anchor="topleft"):
        image = self.font.render(text, 1, self.color)
        rect = image.get_rect(**{anchor: position})
        surface.blit(image, rect)


class OvalButton:
    def __init__(self, color, size, text, pen, position, anchor):
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        pygame.draw.ellipse(self.image, color, self.rect)
        pen.draw(self.image, text, self.rect.center, "center")
        setattr(self.rect, anchor, position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class HoverAlphaEvent:
    def __init__(self, normal, hover, callback, user_data=None):
        self.normal = normal
        self.hover = hover
        self.image = normal
        self.callback = callback
        self.user_data = user_data

    def draw(self, surface):
        self.image.draw(surface)

    def on_mousemotion(self, event):
        if self.normal.rect.collidepoint(event.pos):
            pos = event.pos[0] - self.normal.rect.x, event.pos[1] - self.normal.rect.y
            if self.normal.image.get_at(pos).a:
                self.image = self.hover
            else:
                self.image = self.normal
        else:
            self.image = self.normal

    def on_mousebuttondown(self, event):
        if self.hover.rect.collidepoint(event.pos):
            pos = event.pos[0] - self.hover.rect.x, event.pos[1] - self.hover.rect.y
            if self.hover.image.get_at(pos).a:
                self.callback(self.user_data)


def buzz():  # buzzing
    playsound("beep.wav")


def output_msg(msg, o):  # output_msg
    x = 0
    y = 0
    if str(o) in ("13568"):
        buzz()
    # font=pygame.font.Font()
    msg1 = pygame.font.render(msg)
    screen.blit(msg1, (x, y))

def read_audio():
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2

    # 实例化一个PyAudio对象
    pa = pyaudio.PyAudio()
    # 打开声卡，设置 采样深度为16位、声道数为2、采样率为16、输入、采样点缓存数量为2048
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    # 新建一个列表，用来存储采样到的数据
    record_buf = []
    count = 0
    for i in tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
        audio_data = stream.read(2048)  # 读出声卡缓冲区的音频数据
        record_buf.append(audio_data)  # 将读出的音频数据追加到record_buf列表
        count += 1
        print('*')
    wf = wave.open('quake_sounds/test/audio-0-0.wav', 'wb')  # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(1)  # 设置声道数为1
    wf.setsampwidth(2)  # 设置采样深度为2
    wf.setframerate(RATE)
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(record_buf))
    # 写完后将文件关闭
    wf.close()
    # 停止声卡
    stream.stop_stream()
    # 关闭声卡
    stream.close()


def button_push(user_data):  # changing the output_file into output functionx
    classes = ["air_conditioner", "car_horn", "children_playing", "dog_bark", "drilling", "engine_idling", "gun_shot",
               "jackhammer", "siren", "street_music"]
    read_audio()
    o = of.output()
    print(o)
    msg = classes[o]
    output_msg(msg, o)


def main():
    pygame.init()
    Screen.center()
    screen = Screen("Mouse Double Click", 800, 600)
    background = pygame.Color("black")

    pen = Pen(pygame.font.Font(None, 32), pygame.Color("white"))
    buttons = [
        HoverAlphaEvent(
            OvalButton(pygame.Color("firebrick"), (350, 350), "Button", pen, (20, 20), "topleft"),
            OvalButton(pygame.Color("lawngreen"), (350, 350), "Button", pen, (20, 20), "topleft"),
            button_push, "Button"), ]

    running = True
    while running:
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.on_mousemotion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        button.on_mousebuttondown(event)

        screen.surface.fill(background)
        for button in buttons:
            button.draw(screen.surface)

        pygame.display.update()
        screen.idle()


if __name__ == "__main__":
    main()
