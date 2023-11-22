import serial
import mysql.connector

HOST = '192.168.110.165'  # 서버의 IP 주소
PORT = 65432           # 사용 중인 서버의 포트

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

db = mysql.connector.connect(host='192.168.110.164', port = '3306', user='root', password='1234', database='RC')
cur = db.cursor()


def insertCommand(cmd_string, arg_string):
    is_finish = 0

    query = "insert into command(time, cmd_string, arg_string, is_finish) values (NOW(), %s, %s, %s)"
    value = (cmd_string, arg_string, is_finish)

    cur.execute(query, value)
    db.commit()

def Y(dataY):
    if dataY > 3500:
        insertCommand("back", "0")
    elif dataY > 1500:
        insertCommand("stop", "0")
    else:
        insertCommand("go", "0")
def X(dataX):
    if dataX > 3500:
        insertCommand("left", "0")
    elif dataX > 1500:
        insertCommand("mid", "0")
    else:
        insertCommand("right", "0")

while True:
    if ser.in_waiting >= 4:  # 전체 패킷을 모두 수신할 때까지 기다림
        data = ser.read(4)  # 4바이트 데이터를 읽음

        # 두 개의 2바이트 데이터로 분리 (빅 엔디안에서 리틀 엔디안으로 변환)
        data_x = (data[0] << 8) | data[1]
        data_y = (data[2] << 8) | data[3]
        X(data_x)
        Y(data_y)