# transcribe_streaming_mic.py

import re # 정규표현식 모듈
import sys

from google.cloud import speech
import pyaudio  # 파이썬에서 오디오 입력 사용
import queue
from PIL import Image, ImageDraw, ImageFont
import board
import digitalio
import adafruit_ssd1306
import requests
import json

WIDTH = 128
HEIGHT = 64

spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D8)
oled_dc = digitalio.DigitalInOut(board.D25)
oled_reset = digitalio.DigitalInOut(board.D24)

oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

oled.fill(0)
oled.show()

imageBack = Image.new('1', (128, 64), 0)
image = Image.new('1', (64, 128), 0)
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("malgun.ttf", 10)


def display_messages(line1, line2):
    draw.rectangle((0, 0, 64, 128), outline=0, fill=0)
    draw.text(
        (10, 10),
        line1,
        font=font,
        fill=1,
    )
    draw.text(
        (10, 30),
        line2,
        font=font,
        fill=1,
    )
    rotimage = image.transpose(Image.ROTATE_90)
    flipedim = rotimage.transpose(Image.FLIP_TOP_BOTTOM)
    imageBack.paste(flipedim, (0, 0, 128, 64))
    oled.image(imageBack)
    oled.show()
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  

GOOGLE_APPLICATION_CREDENTIALS="/home/pi/rc-project-405706-39625327fe12.json"

class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()  # pyaudio가 전달해주는 데이터를 담을 큐 
        self.closed = True

    # 파이썬 context manager사용. 여기에서는 실행중 문제가 발생해도 오디오장치를 제대로 닫도록 할 수 있기 위함.
    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()   # 시작할 때 pyaudio 데이터 스트림 열림
        self._audio_stream = self._audio_interface.open( # pyaudio.open()은 pyaudio.Stream object를 리턴.
            format=pyaudio.paInt16, # 16bit 다이나믹 레인지
            channels=1,
            rate=self._rate,
            input=True,     
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,  # pyaudio에서 한 블록의 데이터가 들어올 때 호출되는 콜백
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()   # 끝날 때 반드시 pyaudio 스트림 닫도록 한다.

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):  # pyaudio.Stream에서 호출되는 콜백은 4개 매개변수 갖고, 2개값 리턴한다. pyaudio문서 참고.
        self._buff.put(in_data) # 큐에 데이터 추가
        return None, pyaudio.paContinue

    # 한 라운드의 루프마다 현재 버퍼의 내용을 모아서 byte-stream을 yield함.
    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)  # 가장 오래된 데이터부터 순차적으로 data[]에 추가함.
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty: # 큐에 더이상 데이터가 없을 때까지
                    break

            yield b''.join(data) # byte-stream

# response  화면에 출력
def listen_print_loop(responses):
    global image,draw
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        # 최종적인 결과값은 언제나 results[0]에 반영되므로 result[0]만 고려.
        result = response.results[0]
        
        if not result.alternatives:
            continue

        # 확실성 가장 높은 alternative의 해석
        transcript = result.alternatives[0].transcript

        
        order=transcript.split()[-1]
        image = Image.new('1', (64, 128), 0)
        draw = ImageDraw.Draw(image)

        stwid, sthgt = 26, 11
        gap = 20
        gap_mmdd = 5
        draw.text(
            (stwid, sthgt),
            order,
            font=font,
            fill=1,
        )

        rotimage = image.transpose(Image.ROTATE_90)
        flipedim = rotimage.transpose(Image.FLIP_TOP_BOTTOM)
        imageBack.paste(flipedim, (0, 0, 128, 64))
        oled.image(imageBack)
        oled.show()
        if '종료' in order:
            print("Mic Mode Exit")
            break
        if '전진' in order:
            print('전진')
        if '후진' in order:
            print('후진')
        if '좌회전' in order:
            print('좌회전')
        if '우회전' in order:
            print('우회전')
        

def main():
    # 한국말 사용
    language_code = 'ko-KR'  # a BCP-47 language tag

    display_messages("명령을","말하세요")
    print("Mic Mode")
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding='LINEAR16', # enums.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate_hertz=RATE,
        max_alternatives=1, # 가장 가능성 높은 1개 alternative만 받음.
        language_code=language_code)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True) # 해석완료되지 않은(is_final=false) 중도값도 사용.

    with MicrophoneStream(RATE, CHUNK) as stream:   # 사운드 스트림 오브젝트 생성. 
                                                    # pyaudio가 terminate()되는 것을 보장하기 위해 python
                                                    # context manager  사용.
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator) # generator expression. 요청 생성

        responses = client.streaming_recognize(streaming_config, requests)  # 요청 전달 & 응답 가져옴
        listen_print_loop(responses)    # 결과 출력. requests, responses 모두 iterable object

