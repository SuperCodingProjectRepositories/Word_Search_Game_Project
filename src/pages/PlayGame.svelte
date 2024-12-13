<script>
    import { onMount } from "svelte";
    import { getDatabase, ref, child, get, set,push ,onValue } from "firebase/database";
    import { getAuth } from "firebase/auth";
    import Header from "../components/Header.svelte";

    const gameDB = ref(getDatabase());

    const colors = [
        "#FFB6C1", "#FFE4E1", "#FFDAB9", "#FFFACD", "#E6E6FA", "#D8BFD8", "#D3D3D3", "#AFEEEE", "#ADD8E6", "#F0E68C",
        "#98FB98", "#90EE90", "#F5F5DC", "#F5F5F5", "#FFF5EE", "#FFEFD5", "#FFFAF0", "#F0FFFF", "#F5FFFA", "#FAFAD2",
        "#FFF8DC", "#FFFACD", "#FFDEAD", "#FFDAB9", "#FFE4B5", "#F0FFF0", "#E0FFFF", "#E6E6FA", "#FFE4E1", "#F8F8FF"
    ];
    let currentColorIndex = 0;

    let gameID = "";
    let title;
    let description;
    let words = [];
    let collectedWords = [];

    let isDragging = false; // 마우스 드래그 상태 플래그
    let gridSize = 12;
    let grid = [];
    let selectedCells = []; // 드래그한 셀들
    let selectedWord = "";

    let leaderboard = [];
    let timer = "00:00:00";
    let startTime = new Date();

    let gameStarted = false;

    function initGame() {
        title = "";
        description = "";
        words = [];
        grid = Array.from({length: gridSize}, () => Array(gridSize).fill(""));
        selectedCells = [];
        selectedWord = "";
        startTime = new Date();
        timer = "00:00:00";
        gameStarted = false;
    }

    const loadGame = async () => {
        const urlParams = new URLSearchParams(window.location.search);
        gameID = urlParams.get("gameId");

        if (!gameID) {
            alert("유효하지 않은 게임 링크입니다.");
            window.location.href = "/";
            return;
        }

        // 사용자 인증 상태 확인
        if (localStorage.getItem('userName') === "") {
            console.error("User is not authenticated.");
            alert("로그인이 필요합니다.");
            window.location.hash = '/login';
            return;
        }

        try {
            const gameRef = ref(getDatabase(), `gameDatas/${gameID}`);
            const snapshot = await get(gameRef);

            if (snapshot.exists()) {
                const gameData = snapshot.val();
                title = gameData.title;
                description = gameData.description;
                words = gameData.words || [];

                grid = generateGrid(gridSize, words);
                loadLeaderBoard();
            } else {
                alert("게임 데이터를 찾을 수 없습니다.");
                window.location.href = "/";
            }
        } catch (error) {
            console.error("Error loading game:", error);
        }
    };

    function loadLeaderBoard() {
        try {
            const gameDataRef = ref(getDatabase(), 'leaderboards/' + gameID);

            onValue(gameDataRef, (res) => {
                if (res.exists()) {
                    // 데이터가 배열 형태일 경우 객체로 변환
                    leaderboard = Object.values(res.val());

                    console.log(leaderboard);
                } else {
                    leaderboard = [];
                    console.log("No leaderboard data found.");
                }
            });
        } catch (error) {
            leaderboard = [];
            console.error("Error loading leaderboard:", error);
        }
    }

    function startGame(){
        startTime = new Date();
        gameStarted = true;
        updateTimer();
        setInterval(updateTimer,1000);
    }

    function updateTimer()
    {
        const now = new Date();
        const elapsed  = new Date(now - startTime);
        const hours = String(elapsed.getUTCHours()).padStart(2, "0");
        const minutes = String(elapsed.getUTCMinutes()).padStart(2, "0");
        const seconds = String(elapsed.getUTCSeconds()).padStart(2, "0");
        timer = `${hours}:${minutes}:${seconds}`;
        requestAnimationFrame(updateTimer);
    }

    onMount(() => {
        // URL에서 gameId 추출
        const hash = window.location.hash;
        const urlParams = new URLSearchParams(hash.split("?")[1]);
        gameID = urlParams.get("gameId");

        console.log(window.location.hash);
        console.log(urlParams);
        console.log(gameID);

        get(child(gameDB, `gameDatas/${gameID}`))
            .then((snapshot) => {
                if (snapshot.exists()) {
                    initGame();
                    //currentGame = JSON.parse(snapshot.val());
                    title = snapshot.val()["title"];
                    description = snapshot.val()["description"];
                    words = snapshot.val()["words"];
                    collectedWords = [];

                    grid = generateGrid(gridSize, words);
                    loadLeaderBoard(gameID);
                } else {
                    console.error("No data available");
                    grid = generateGrid(gridSize, []); // 기본값 설정
                }
            })
            .catch((error) => {
                console.error(error);
                grid = generateGrid(gridSize, []); // 기본값 설정
            });

    });

    function generateGrid(size, words) {
        let newGrid = Array.from({length: size}, () => Array(size).fill(""));

        words.forEach((word) => {
            placeWordInGrid(newGrid, word.toUpperCase());
        });

        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (newGrid[i][j] === "") {
                    newGrid[i][j] = randomLetter();
                }
            }
        }

        return newGrid;
    }

    function placeWordInGrid(grid, word) {
        const directions = [
            {x: 0, y: 1},
            {x: 1, y: 0},
            {x: 0, y: -1},
            {x: -1, y: 0},
        ];

        const size = grid.length;
        let placed = false;

        while (!placed) {
            const dir = directions[Math.floor(Math.random() * directions.length)];
            const row = Math.floor(Math.random() * size);
            const col = Math.floor(Math.random() * size);

            if (canPlaceWord(grid, word, row, col, dir)) {
                for (let i = 0; i < word.length; i++) {
                    grid[row + i * dir.y][col + i * dir.x] = word[i];
                }
                console.log(row, col,word,dir);
                placed = true;
            }
        }
    }

    function canPlaceWord(grid, word, row, col, dir) {
        const size = grid.length;

        for (let i = 0; i < word.length; i++) {
            const newRow = row + i * dir.y;
            const newCol = col + i * dir.x;

            if ( newRow < 0 || newRow >= size || newCol < 0 || newCol >= size){
                return false;
            }

            if(grid[newRow][newCol] !== "" && grid[newRow][newCol] !== word[i]) {
                return false;
            }
        }

        return true;
    }

    function randomLetter() {
        return String.fromCharCode(65 + Math.floor(Math.random() * 26)); // A-Z
    }

    function onMouseDown(row, col) {
        isDragging = true;
        resetSelection();
        addCellToSelection(row, col);
    }

    function onMouseEnter(row, col) {
        if (isDragging) {
            addCellToSelection(row, col);
        }
    }

    function onMouseUp() {
        if (isDragging) {
            finalizeSelection();
            isDragging = false;
        }
    }

    function addCellToSelection(row, col) {
        if (!selectedCells.some((cell) => cell.row === row && cell.col === col)) {
            selectedCells.push({row, col});
            selectedWord = selectedCells.map((cell) => grid[cell.row][cell.col]).join("");

            const cellElement = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
            if (cellElement && !cellElement.classList.contains("collected")) {
                cellElement.style.backgroundColor = "yellow";
                cellElement.style.transform = "scale(1.05)";
                setTimeout(() => {
                    cellElement.style.transform = "scale(1)";
                }, 150);
            }
        }
    }

    function finalizeSelection() {
        if (words.map((w) => w.toUpperCase()).includes(selectedWord) && !collectedWords.includes(selectedWord)) {
            collectedWords = [...collectedWords, selectedWord];
            selectedCells.forEach(({row, col}) => {
                const cellElement = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
                if (cellElement) {
                    cellElement.classList.add("collected");
                    cellElement.style.backgroundColor = colors[currentColorIndex];
                }
            });
            currentColorIndex++;
        } else {
            selectedCells.forEach(({row, col}) => {
                const cellElement = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
                if (cellElement && !cellElement.classList.contains("collected")) {
                    cellElement.style.backgroundColor = "red";
                    cellElement.style.transform = "scale(1.05)";
                    setTimeout(() => {
                        cellElement.style.transform = "scale(1)";
                    }, 150);
                    setTimeout(() => {
                        cellElement.style.backgroundColor = "";
                    },500);
                }
            });
            console.log("Invalid word: " + selectedWord);
        }
        finishGame();

        selectedCells = [];
        selectedWord = "";

    }

    function finishGame(){
        if(arraysAreEqual(words,collectedWords))
        {
            console.log("Finishing game...");
            try{
                const db = getDatabase();
                const userName = localStorage.getItem('userName');
                const leaderboardRef = ref(db, `leaderboards/${gameID}/${userName}`);

                set(leaderboardRef, {
                    userName: userName || "Unknown",
                    time: timer,
                });
                alert("게임을 클리어 하셨습니다.");

                setTimeout(() => {
                    initGame();
                    window.location.hash = "/"
                }, 1000);
            }catch (error){
                console.log(error);
            }
        }
    }

    // 배열 비교 함수
    function arraysAreEqual(arr1, arr2) {
        for(let i = 0; i < arr1.length; i++) {
            if(!arr2.includes(arr1[i])) {
                return false;
            }
        }
        return true;
    }

    function resetSelection() {
        selectedCells.forEach(({row, col}) => {
            const cellElement = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
            if (cellElement && !cellElement.classList.contains("collected")) {
                cellElement.style.backgroundColor = "";
            }
        });
    }

    function testCollectWord(){
        if(!gameStarted) return;
        for (let i = 0; i < words.length; i++){
            if(!collectedWords.includes(words[i]))
            {
                collectedWords.push(words[i]);
                break;
            }
        }
        finalizeSelection();
    }

</script>

<Header />

<main>
    <div>
        <h1 class="game-title">{title}</h1>
        <h3>{description}</h3>
        <h4>{timer}</h4>
    </div>

    <div class="game-board">
        <div class="wordList">
            <h3>찾아야 할 단어들</h3>
            <ul>
                {#each words as word}
                    <li class={collectedWords.includes(word) ? 'collectWord' : ''}>
                        {word}
                    </li>
                {/each}
            </ul>
        </div>

        <div class="game-panel">
            {#if !gameStarted}
                <div class="start-panel">
                    <button on:click={startGame} class="gameStart">게임 시작</button>
                </div>
            {/if}

            <div class="word-puzzle">
                {#each grid as row, rowIndex}
                    <div class="row">
                        {#each row as letter, colIndex}
                            <div
                                    class="cell"
                                    data-row={rowIndex}
                                    data-col={colIndex}
                                    on:mousedown={() => onMouseDown(rowIndex, colIndex)}
                                    on:mouseover={() => onMouseEnter(rowIndex, colIndex)}
                                    on:focus={() => onMouseEnter(rowIndex, colIndex)}
                                    on:mouseup={onMouseUp}
                                    role="gridcell"
                                    tabindex="0">
                                {letter}
                            </div>
                        {/each}
                    </div>
                {/each}
            </div>
        </div>

        <div class="leaderboard">
            <h3>현황판</h3>
            <div>
                {#each leaderboard as {userName, time}, index}
                    <div class="leaderboard-item" style={index < 3 ? 'font-weight: bold;' : ''}>
                        {index + 1}. {userName} - {time}
                    </div>
                {/each}
            </div>
        </div>
    </div>
</main>

<style>
    .game-board {
        display: flex;
        justify-content: start;
        align-items: start;
        position: relative;
    }

    .game-panel {
        position: relative;
        width: 480px;
        height: 100%;
    }

    .start-panel {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10;
    }

    .gameStart {
        padding: 10px 20px;
        font-size: 18px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .gameStart:hover {
        background-color: #45a049;
    }

    .word-puzzle {
        width: 100%;
        height: 100%;
        display: inline-block;
        user-select: none;
    }

    .row {
        display: flex;
    }

    .cell {
        width: 40px;
        height: 40px;
        border: 1px solid #ddd;
        text-align: center;
        vertical-align: middle;
        line-height: 40px;
        cursor: pointer;
        transition: transform 0.15s;
    }

    .cell[data-row][data-col]:hover {
        background-color: rgba(200, 200, 200, 0.3);
    }

    .collectWord {
        text-decoration: line-through 2px;
        color: green;
    }

    .wordList {
        width: 200px;
        padding: 10px;
    }

    .leaderboard {
        width: 200px;
        padding: 10px;
    }

    .leaderboard-item {
        font-weight: 700;
    }
</style>
