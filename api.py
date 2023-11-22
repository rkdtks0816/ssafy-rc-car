from fastapi import FastAPI, Response               # Json Response
from fastapi.middleware.cors import CORSMiddleware  # CORS
import pymysql

app = FastAPI()

# CORS
origins = [
    "http://192.168.110.164"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 연동
def GetConnection():
    connection = pymysql.connect(host='192.168.110.164', port=3306, user='root', password='1234',
                                    db='RC', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection

async def InsertCmd(Cmd: str):
    try:
        connection = GetConnection()
        
        with connection.cursor() as cursor:
            query = f"""
                `INSERT INTO command(time, cmd_string, arg_string, is_finish) VALUES (CURRENT_TIMESTAMP(), '${Cmd}', 0, 0)`;
            """

            cursor.execute(query)

            connection.commit()

            print(f"succeed to do 'InsertCmd('{Cmd}')'")

    except Exception as ex:
        print(f"error to do 'GetCreatID('{Cmd}')'")

# WAS

@app.get("/InsertCmd")
async def InsertCmd(Cmd: str):
    result = await InsertCmd(Cmd)
    return Response(content=result, media_type="application/json")