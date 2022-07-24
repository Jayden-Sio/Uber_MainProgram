from datetime import datetime

from PySide6.QtCore import QThread, Slot, Signal
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
import sys, time
import pyaudio, wave
from tqdm import tqdm
import of2 as of
import logging




class MainWindow():
    def __init__(self):
        self.th = None
        self.ui = QUiLoader().load("untitled.ui")
        self.ui.StartBtn.clicked.connect(self.handelStart)
        self.ui.StopBtn.clicked.connect(self.handelStop)

        logging.debug("MainWindow initialized")

    @Slot()
    def handelStart(self):
        logging.debug("Start recording")
        print("Start button clicked")
        self.th = Th()
        self.th.start()
    @Slot()
    def handelStop(self):
        logging.debug("End recording")
        self.th.terminate()


class Th(QThread):
    def __init__(self) -> None:
        super().__init__()


    @Slot()
    def run(self):
        classes = ["air_conditioner", "car_horn", "children_playing", "dog_bark", "drilling", "engine_idling",
                   "gun_shot",
                   "jackhammer", "siren", "street_music"]
        while Flag:
            self.read_audio()
            o = of.output()
            print(o)
            msg = classes[o]
            self.output_msg(msg, o)
            logging.info("Output: %s" % msg)

    def read_audio(self):
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 1

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

    def output_msg(self, msg, o):  # output_msg
        x = 0
        y = 0
        label = MainWindow.ui.Result
        if str(o) in ("13568"):
            label.setStyleSheet('''background: rgba(255, 0, 0, 1); 
                       font-family: YouYuan;
                       font-size: 24pt;
                       color: white;
                       ''')
            label.setText(f"{msg}\n-{datetime.now()}")
        else:
            label.setStyleSheet('''background: rgba(255, 255, 255, 0.2); 
                       font-family: YouYuan;
                       font-size: 24pt;
                       color: white;
                       ''')
            label.setText("")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG  # 设置日志输出格式
                        , filename="app.log"  # log日志输出的文件位置和文件名
                        , filemode="w"  # 文件的写入格式，w为重新写入文件，默认是追加
                        ,
                        format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
                        # 日志输出的格式
                        # -8表示占位符，让输出左对齐，输出长度都为8位
                        , datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
                        )


    Flag = True
    app = QApplication([])
    MainWindow = MainWindow()
    MainWindow.ui.show()
    sys.exit(app.exec())
