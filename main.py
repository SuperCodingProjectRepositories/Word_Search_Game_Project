from typing import Annotated

from fastapi import FastAPI, Form, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import mysql.connector
import json
import models

# MySQL 데이터베이스 연결 설정
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vudrbs90wja@",
    database="wordgame"
)

# 데이터베이스 커서 생성 (결과를 딕셔너리 형태로 반환)
cursor = connection.cursor(dictionary=True)

SECRET = "Super_Coding_Word_Search"
manager = LoginManager(SECRET,'/login')

# 전역적으로 사용할 Game 객체 초기화
current_game = models.Game(
    title="default",
    description="default",
    words=[],
    matched_words=[],
    is_completed=False
)

# FastAPI 앱 생성
app = FastAPI()

# @manager.user_loader 데코레이터로 로그인 매니저에 사용자 로드 함수 정의
@manager.user_loader()
def query_user(data):
    """
    사용자 정보를 데이터베이스에서 조회하는 함수
    - 이메일을 기준으로 사용자를 조회
    - 로그인 토큰 데이터에서 이메일(sub)를 가져와 조회
    """
    # data가 단순 문자열인 경우
    WHERE_STATEMENTS = f'email="{data}"'

    # data가 딕셔너리(로그인 토큰인 경우)인 경우
    if type(data) == dict:
        WHERE_STATEMENTS = f'''email="{data['sub']}"'''

    # SQL 쿼리를 실행하여 사용자 정보를 가져옴
    query_user = f"""
        SELECT * from userdata WHERE {WHERE_STATEMENTS};
    """
    cursor.execute(query_user)
    user = cursor.fetchone()
    return user  # 조회된 사용자 정보를 반환

# 회원가입 엔드포인트
@app.post('/signup')
def signup(email: Annotated[str, Form()],
           password: Annotated[str, Form()],
           username: Annotated[str, Form()]):
    """
    사용자 회원가입 처리
    - 클라이언트에서 이메일, 비밀번호, 사용자명을 전달받음
    - 사용자 데이터를 데이터베이스에 삽입
    """
    # INSERT 쿼리 정의 및 실행
    insert_query = """
    INSERT INTO userdata (username, email, password)
    VALUES (%s, %s, %s)
    """
    data = (username, email, password)
    cursor.execute(insert_query, data)  # 데이터베이스에 사용자 정보 삽입

    # 데이터베이스 변경 사항 저장
    connection.commit()
    print(email, password)  # 디버깅용 출력
    return {'message': 'Signup successful'}  # 회원가입 성공 메시지 반환

# 로그인 엔드포인트
@app.post('/login')
def login(email: Annotated[str, Form()],
          password: Annotated[str, Form()]):
    """
    사용자 로그인 처리
    - 클라이언트에서 이메일과 비밀번호를 전달받음
    - 데이터베이스에서 사용자를 조회하고 비밀번호를 검증
    - 검증 성공 시 액세스 토큰을 생성하여 반환
    """
    user = query_user(email)  # 이메일을 통해 사용자 조회

    # 사용자 정보가 없거나 비밀번호가 일치하지 않으면 인증 오류 발생
    if not user:
        raise InvalidCredentialsException  # 사용자 없음
    elif password != user['password']:
        raise InvalidCredentialsException  # 비밀번호 불일치

    # 인증 성공 시 액세스 토큰 생성
    access_token = manager.create_access_token(data={
        'sub': user['email'],  # 사용자 이메일을 토큰의 sub 필드에 저장
        'username': user['username']  # 사용자 이름도 토큰에 저장
    })
    return {'access_token': access_token}  # 생성된 액세스 토큰 반환


# 인증된 사용자 확인을 위한 종속성
def get_current_user(user: dict = Depends(manager)):
    if not user:
        raise HTTPException(status_code=401,detail="Unauthorized")
    return user

# WebSocket 엔드포인트 (테스트용)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        # 클라이언트 연결 수락
        await websocket.accept()
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            # 클라이언트로 메시지 전송 (Echo)
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")

# 특정 게임에 대한 WebSocket 연결을 처리하는 엔드포인트
@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    try:
        # 데이터베이스에서 해당 게임 ID의 데이터를 가져옴
        game_query = "SELECT * FROM gamedata WHERE id = %s"
        cursor.execute(game_query, (game_id,))
        result = cursor.fetchone()

        # 데이터가 없으면 연결 종료
        if not result:
            return JSONResponse({"error": "Invalid game ID"}, status_code=404)

        # Game 객체 생성
        word_list = json.loads(result["words"])
        current_game = models.Game(
            title=result["title"],
            description=result["description"],
            words=word_list,
            matched_words=[],
            is_completed=False
        )

        print(f"WebSocket connection initiated for: {current_game.title}")
        # WebSocket 연결 수락
        await websocket.accept()

        # 초기 게임 데이터 클라이언트로 전송
        await websocket.send_json(jsonable_encoder(current_game))

        # 게임 진행 루프
        while not current_game.is_game_complete():
            # 클라이언트로부터 단어 수신
            data = await websocket.receive_text()
            print(f"Received Word: {data}")
            # 단어 확인 및 업데이트
            current_game.check_word(data)

            # 업데이트된 게임 데이터를 클라이언트로 전송
            await websocket.send_json(jsonable_encoder(current_game))

        # 게임 완료 시 최종 데이터 전송
        await websocket.send_json(jsonable_encoder(current_game))
    except Exception as e:
        print(f"WebSocket error: {e}")

    return '200'

# 특정 게임 데이터를 반환하는 엔드포인트
@app.get('/games/id={game_id}')
def start_games(game_id: int, user: dict = Depends(get_current_user)):
    print(f"Received request for game_id: {game_id}")
    # 데이터베이스에서 해당 게임 ID의 데이터를 가져옴
    game_query = "SELECT * FROM gamedata WHERE id = %s"
    cursor.execute(game_query, (game_id,))
    result = cursor.fetchone()

    # 데이터가 없으면 에러 응답
    if not result:
        return JSONResponse({"error": "Invalid game ID"}, status_code=404)

    # Game 객체 생성
    word_list = json.loads(result["words"])
    current_game = models.Game(
        title=result["title"],
        description=result["description"],
        words=word_list,
        matched_words=[],
        is_completed=False
    )

    # JSON 형식으로 게임 데이터 반환
    return JSONResponse(jsonable_encoder(current_game))

# 새로운 게임 데이터를 생성하는 엔드포인트
@app.post('/create-game')
def create_game(game_data: models.GameData, user: dict = Depends(get_current_user)):
    # words 필드를 JSON 문자열로 변환
    words_json = json.dumps(game_data.words)

    # INSERT 쿼리 정의 및 실행
    insert_query = """
    INSERT INTO gamedata (title, description, words, public)
    VALUES (%s, %s, %s, %s)
    """
    data = (game_data.title, game_data.description, words_json, game_data.public)
    cursor.execute(insert_query, data)

    # 데이터베이스 커밋
    connection.commit()

    # 성공 응답 반환
    return '200'

# 모든 게임 데이터를 반환하는 엔드포인트
@app.get('/games')
def get_games(user: dict = Depends(get_current_user)):
    # 데이터베이스에서 모든 게임 데이터 조회
    query = """
    SELECT * FROM gamedata;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # 조회된 데이터를 처리
    result = []
    for row in rows:
        # words 필드 JSON 변환
        row['words'] = json.loads(row['words'])
        result.append(row)

    # JSON 형식으로 데이터 반환
    return JSONResponse(jsonable_encoder(dict(ret) for ret in result))

@app.get('/')
def get_root():
    return "Hello World!"

# 정적 파일 (frontend) 서빙
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
