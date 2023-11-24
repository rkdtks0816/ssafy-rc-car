from PIL import Image, ImageDraw, ImageFont
import board
import digitalio
import adafruit_ssd1306
from datetime import datetime

WIDTH = 128
HEIGHT = 64

spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D8)
oled_dc = digitalio.DigitalInOut(board.D25)
oled_reset = digitalio.DigitalInOut(board.D24)

oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc,
oled_reset, oled_cs)

oled.fill(0)
oled.show()

imageBack = Image.new('1',(128,64),0)
image = Image.new('1', (64, 128), 0)
draw = ImageDraw.Draw(image)
sizefNorm = 10
sizefYear = 17
sizefMandD = 22
font = ImageFont.truetype("malgun.ttf",10)
fontNorm = ImageFont.truetype("malgun.ttf",sizefNorm)
fontYear = ImageFont.truetype("malgun.ttf",sizefYear)
fontMandD = ImageFont.truetype("malgun.ttf",sizefMandD)

def one():
    global image, draw, fontNorm, fontYear, fontMandD, sizefNorm, sizefYear, sizefMandD
    draw.rectangle((0, 0, 64, 128), outline=0, fill=0)
    print("Date Mode")
    now = datetime.now()
    strYear = f"{now.year}"
    strMonth = f"{now.month}"
    strMM = "월"
    strDay = f"{now.day}"
    strDD = "일"
    stwid, sthgt = 26, 11
    gap = 20
    gap_mmdd = 5
    draw.text(
        (stwid,sthgt),
        strYear,
        font = fontYear,
        fill=1,
    )
    draw.text(
        (20, sthgt+gap),
        strMonth,
        font = fontMandD,
        fill = 1,
    )
    draw.text(
        (20+font.getsize(strMonth)[1], sthgt+gap+sizefMandD+gap_mmdd),
        strMM,
        font = fontNorm,
        fill = 1,
    )
    draw.text(
        (20,sthgt+gap+sizefMandD+gap_mmdd+sizefNorm+3),
        strDay,
        font = fontMandD,
        fill = 1
    )
    draw.text(
        (20 + font.getsize(strMonth)[1], sthgt+gap+sizefMandD+gap_mmdd+sizefNorm+3+sizefMandD+gap_mmdd),
        strDD,
        font=fontNorm,
        fill=1,
    )
    rotimage = image.transpose(Image.ROTATE_90)
    flipedim = rotimage.transpose(Image.FLIP_TOP_BOTTOM)
    imageBack.paste(flipedim,(0,0,128,64))
    oled.image(imageBack)
    oled.show()
