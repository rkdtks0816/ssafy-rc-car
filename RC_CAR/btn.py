import timeMode
import mic
import conMode

from gpiozero import Button
from signal import pause
import board

spi=board.SPI()
btnG=Button(3)

mode=0

# 버튼 눌림 이벤트에 대한 처리
def handle_button_press():
    global mode  # 전역 변수로 선언하여 함수 내에서 외부 변수 수정

    # 현재 모드에 따라 동작 결정
    if mode == 0:
        timeMode.one()
        mode = 1
    elif mode == 1:
        mic.main()
        mode = 2
    else:
        conMode.three()
        mode = 0

# 버튼에 이벤트 핸들러 등록
btnG.when_pressed = handle_button_press
pause()
