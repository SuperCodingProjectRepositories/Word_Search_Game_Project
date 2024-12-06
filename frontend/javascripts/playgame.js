const gameID = window.sessionStorage.getItem('currentGameID');
let ws = new WebSocket(`ws://127.0.0.1:8000/ws/game/${gameID}`);

ws.onopen = () =>{
    console.log("Game WebSocket connected");
}

ws.onmessage = (event) => {
    console.log("Raw event data:", event.data); // 원본 데이터 로그
    const data = JSON.parse(event.data);
    if(data["is_completed"])
        window.location.pathname = "/";
};

ws.onerror = (error) => console.error("WebSocket error:", error);

async function initData(){
    const res = await fetch(`/games/id=${gameID}`);
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }
    const gameData = await res.json(); // 응답 데이터를 JSON으로 파싱
    console.log(gameData); // 콘솔에 출력
}

function sendWord(word) {
    ws.send(word);
}