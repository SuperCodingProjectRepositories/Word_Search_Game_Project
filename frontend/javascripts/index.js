
const onClickGameListItem = (event) => {
    event.preventDefault(); // 필요 시 기본 동작 방지
    // 이동하기 전에 게임 데이터 아이디를 저장
    console.log(event);
    const element = event.target;
    const gameID = element.id.match(/\d+/);
    console.log(gameID[0]);
    window.sessionStorage.setItem('currentGameID',gameID[0]);
    window.location.pathname = '/playgame.html'; // 올바른 절대 경로 사용
}

async function renderGames (data){
    console.log(data);
    const gameList = document.querySelector(".game-list");
    for (const gd of data){
        console.log(gd);
        const li = document.createElement('li');
        li.textContent = gd['title'];
        li.className = 'game-list-item';
        li.id = `game_${gd['id']}`;
        li.addEventListener('click', onClickGameListItem);
        gameList.appendChild(li);
    }
}

const updateGameList = async () =>{
    const accessToken = window.localStorage.getItem('token');
    const res = await fetch('/games',{
        headers:{
            'Authorization': `Bearer ${accessToken}`
        }
    });
    if(res.status === 200){
        const gameData = await res.json();
        await renderGames(gameData)
    }
    else {
        alert("로그인이 필요합니다.")
        window.location.pathname = '/login.html';
    }
}

const makeGameBtn = document.querySelector("#make-game-btn");
makeGameBtn.addEventListener("click", () =>{
    window.location.pathname = '/makegame.html';
});


updateGameList();






