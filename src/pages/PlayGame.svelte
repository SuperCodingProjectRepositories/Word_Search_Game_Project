<script>
    import { onMount } from "svelte";
    import { getDatabase, ref, child, get, set,push ,onValue } from "firebase/database";
    import { getAuth } from "firebase/auth";

    const auth = getAuth();
    const user = auth.currentUser;

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

    function startGame(){
        startTime = new Date();
        gameStarted = true;
        updateTimer();
        setInterval(updateTimer,1000);
    }

    function loadLeaderBoard(){
        try{
            const gameDataRef = ref(getDatabase(), 'leaderboards/' + {gameID});
            onValue(gameDataRef,(res) => {
                if(res.exists()){
                    leaderboard = Object.values( res.val());
                    leaderboard.sort((a,b) => a.time.localeCompare(b.time)); // 타임 기준 정렬
                    console.log(leaderboard);
                }
                else {
                    leaderboard = [];
                }
            });
        }catch (error){
            leaderboard = [];
            console.log(error);
        }

    }

    function uploadLeaderBoard(){
        try{
            const db = getDatabase();
            const leaderboardRef = ref(db, `leaderboards/${gameID}`);
            const newPostRef = push(leaderboardRef);

            set(newPostRef, {
                userName: user.displayName || "Unknown",
                time: timer,
            });
        }catch (error){
            console.log(error);
        }
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
        const currentGameStr = sessionStorage.getItem("currentGame");
        if (!currentGameStr) {
            console.error("No current game data in sessionStorage");
            return;
        }

        const currentGame = JSON.parse(currentGameStr);
        gameID = currentGame.id;

        get(child(gameDB, `gameDatas/${gameID}`))
            .then((snapshot) => {
                if (snapshot.exists()) {
                    initGame();

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
                console.log(row,col,dir);
                placed = true;
            }
        }
    }

    function canPlaceWord(grid, word, row, col, dir) {
        const size = grid.length;

        for (let i = 0; i < word.length; i++) {
            const newRow = row + i * dir.y;
            const newCol = col + i * dir.x;

            if (
                newRow < 0 ||
                newRow >= size ||
                newCol < 0 ||
                newCol >= size ||
                (grid[newRow][newCol] !== "" && grid[newRow][newCol] !== word[i])
            ) {
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
        selectedCells = [];
        selectedWord = "";

    }

    function resetSelection() {
        selectedCells.forEach(({row, col}) => {
            const cellElement = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
            if (cellElement && !cellElement.classList.contains("collected")) {
                cellElement.style.backgroundColor = "";
            }
        });

    }
</script>

<main>
    <div>
        <h5 class="game-title">{title}</h5>
        <p>{description}</p>
        <p>{timer}</p>
    </div>

    <div class="game-board">
        <div class="wordList">
            <h3>찾아야 할 단어들</h3>
            <ul>
                {#each words as word}
                    <li class= {collectedWords.includes(word) ? 'collectWord' : ''}>
                        {word}
                    </li>
                {/each}
            </ul>
        </div>

        <div class="word-puzzle">
            <button on:click={startGame} disabled={gameStarted} class="gameStart">
                {gameStarted ? "게임 진행 중" : "게임 시작"}
            </button>
            {#each grid as row, rowIndex}
                <div class="row">
                    {#each row as letter, colIndex}
                    <span
                            class="cell"
                            data-row={rowIndex}
                            data-col={colIndex}
                            on:mousedown={() => onMouseDown(rowIndex, colIndex)}
                            on:mouseover={() => onMouseEnter(rowIndex, colIndex)}
                            on:mouseup={onMouseUp}>
                        {letter}
                    </span>
                    {/each}
                </div>
            {/each}
        </div>
        <div class="leaderboard">
            <h3>현황판</h3>
            <ul>
                {#each leaderboard as {userName, time},index}
                    <li class=leaderboard-item style={index < 3 ? 'font-weight: bold; color: gold;' : ''} >
                        {index + 1}. {userName} - {time}
                    </li>
                {/each}
            </ul>
        </div>
    </div>
</main>


<style>
    .game-board {
        display: flex;
        justify-content: start;
        align-items: start;
    }

    .wordList {
        width: 200px;

    }

    .gameStart {
        width: 100%;
        height: 100%;
    }

    .word-puzzle {
        width: 480px;
        height: 480px;
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

    .leaderboard {
        width: 200px;
    }

    .leaderboard-item {
        color: gold;
    }
</style>
