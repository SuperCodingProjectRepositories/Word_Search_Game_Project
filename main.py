from fastapi import FastAPI,Form, WebSocket,WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
import json
import models

#MySQL 연결
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vudrbs90wja@",
    database="wordgame"
)

cursor = connection.cursor(dictionary=True)

current_game = models.Game(
    title="default",
    description="default",
    words=[],
    matched_words=[],
    is_completed= False
)

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    try:
        # 데이터베이스에서 입력받은 게임 id 데이터로 쿼리를 한다.
        game_query = "SELECT * FROM gamedata WHERE id = %s"
        cursor.execute(game_query, (game_id,))
        result = cursor.fetchone()

        if not result:
            return JSONResponse({"error": "Invalid game ID"}, status_code=404)

        # 게임 생성
        word_list = json.loads(result["words"])
        current_game = models.Game(
            title=result["title"],
            description=result["description"],
            words=word_list,
            matched_words=[],
            is_completed= False
        )

        print(f"WebSocket connection initiated for : {current_game.title}")
        await websocket.accept()
        await websocket.send_json(jsonable_encoder(current_game))
        while not current_game.is_game_complete():
            data = await websocket.receive_text()
            print(f"Received Word : {data}")
            current_game.check_word(data)

            await websocket.send_json(jsonable_encoder(current_game))

        await websocket.send_json(jsonable_encoder(current_game))
    except Exception as e:
        print(f"WebSocket error: {e}")

    return '200'



# 게임을 시작을 요청하는 URL
@app.get('/games/id={game_id}')
def start_games(game_id: int):
    print(f"Received request for game_id: {game_id}")
    # 데이터베이스에서 입력받은 게임 id 데이터로 쿼리를 한다.
    game_query = "SELECT * FROM gamedata WHERE id = %s"
    cursor.execute(game_query, (game_id,))
    result = cursor.fetchone()

    if not result:
        return JSONResponse({"error": "Invalid game ID"}, status_code=404)

    # 게임 생성
    word_list = json.loads(result["words"])
    current_game = models.Game(
        title=result["title"],
        description=result["description"],
        words=word_list,
        matched_words=[],
        is_completed= False
    )

    return JSONResponse(jsonable_encoder(current_game))



@app.post('/create-game')
def create_game(game_data: models.GameData):
    # 입력받은 words 필드를 JSON 문자열로 변환
    words_json = json.dumps(game_data.words)

    # INSERT 쿼리 정의
    insert_query = """
    INSERT INTO gamedata (title, description, words, public)
    VALUES (%s, %s, %s, %s)
    """
    # 쿼리에 전달할 데이터 튜플 생성
    data = (game_data.title, game_data.description, words_json, game_data.public)

    # 쿼리 실행
    cursor.execute(insert_query, data)

    # 데이터베이스에 변경 사항 커밋
    connection.commit()

    # 성공 응답 반환
    return '200'


@app.get('/games')
def get_games():
    # 데이터베이스에서 모든 게임 데이터를 조회하는 쿼리
    query = """
    SELECT * FROM gamedata;
    """
    # 쿼리를 실행하여 데이터 가져오기
    cursor.execute(query)
    rows = cursor.fetchall()

    # 결과 데이터를 처리할 리스트 초기화
    result = []
    for row in rows:
        # words 필드의 JSON 문자열을 파이썬 객체로 변환
        row['words'] = json.loads(row['words'])
        # 변환된 데이터를 결과 리스트에 추가
        result.append(row)

    # 데이터를 JSON 형식으로 반환
    # jsonable_encoder를 사용하여 데이터 직렬화 후 JSONResponse로 감쌈
    return JSONResponse(jsonable_encoder(dict(ret) for ret in result))


app.mount("/",StaticFiles(directory="frontend",html=True),name="frontend")