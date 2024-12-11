<script>
    import {onMount} from "svelte";
    import { getDatabase, ref, child, get } from "firebase/database";

    const gameDB = ref(getDatabase());

    let title;
    let description;
    let words = [];
    let collectedWords = [];

    onMount(() => {
        const currentGameStr = sessionStorage.getItem("currentGame");
        const currentGame = JSON.parse(currentGameStr);
        const gameID = currentGame.id;

        get(child(gameDB, `gameDatas/${gameID}`)).then((snapshot) => {
            if (snapshot.exists()) {
                title = snapshot.val()['title'];
                description = snapshot.val()['description'];
                words = snapshot.val()['words'];
                collectedWords = [];
                console.log(words);
            } else {
                console.log("No data available");
            }
        }).catch((error) => {
            console.error(error);
        });
    })

    function onSendWord(word)
    {
        if(words.includes(word) && !collectedWords.includes(word)) {
            collectedWords.push(word);
            console.log(collectedWords);
        }
    }
</script>
<div>
    <h5 class=game-title>{title}</h5>
</div>
<div class="word-puzzle">
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
    <div class="row">
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
        <span class="cell">E</span>
        <span class="cell">I</span>
        <span class="cell">Q</span>
    </div>
</div>



<style>
    .word-puzzle{
        width: 500px;
        display: flex;
        justify-content: start;
        flex-direction: column;
    }

    .word-puzzle .row{
        display: flex;
        justify-content: start;
        align-items: center;
        flex-direction: row;
    }

    .word-puzzle .row .cell{
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        border: 0.1px solid #d7d7d6;
        font-size: 27px;
        font-weight: 600;
        color: #333333;
        position: relative;
    }

    .line{
        position: absolute;
        background-color:  rgba(0, 149, 255, 0.5); /* 라인 색상 */;
        pointer-events: none;
        z-index: 1;
    }
</style>