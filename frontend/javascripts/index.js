
const onClickGameListItem = (event) => {
    event.preventDefault(); // 필요 시 기본 동작 방지
    window.location.pathname = '/playgame.html'; // 올바른 절대 경로 사용
}

async function renderGames (data){
    const gameList = document.querySelector(".game-list");
    for(let i = 0; i < 10; i++)
    {
        const li = document.createElement('li');
        li.textContent = '게임 타이틀입니다.';
        li.className = 'game-list-item';
        li.addEventListener('click', onClickGameListItem);
        gameList.appendChild(li);
    }
}

async function updateGameList(){
    const accessToken = window.localStorage.getItem('token');
    const res = await fetch('/games',{
        headers:{
            'Authorization': `Bearer ${accessToken}`
        }
    });
    if(res.status === 200){
        const gameData = await res.json();
        renderGames(gameData)
    }
    else {
        alert("로그인이 필요합니다.")
        window.location.pathname = '/login.html';
    }
}

updateGameList();






