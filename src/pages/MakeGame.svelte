<script>
    import Header from "../components/Header.svelte";
    import { getDatabase, ref, push, set } from "firebase/database";

    const db = getDatabase();
    const postListRef = ref(db, 'gameDatas');

    let title = "";
    let description = "";
    let inputWords = [];
    let flag = false;

    const onHandleClick = async () => {
        const selectedValue = document.querySelector('input[name="contact"]:checked');
        flag = selectedValue.id === "contact-public";

        const words = [];
        for(let i = 0; i < inputWords.length; i++) {
            if(inputWords[i]){
                words.push(inputWords[i]);
            }
        }

        if(words.length < 10)
        {
            alert("단어를 10개 이상 입력해주세요");
            return;
        }

        try{
            const newPostRef = push(postListRef);
            const res = set(newPostRef, {
                title: title,
                description: description,
                words: words,
                public_flag: flag,
            });
            const gameLink = `${window.location.origin}/#/playGame?gameId=${newPostRef.key}`;
            alert(`게임이 생성되었습니다!\n공유 링크: ${gameLink}`);
        }catch (error) {
            console.error(error);
        }
    }

</script>

<Header/>

<div class="game-title">
    <label> Title
        <input class="game-title-text" type="text" bind:value={title} required>
    </label>
</div>
<div class="game-description">
    <label> Description
        <textarea class="game-description-text" placeholder="" bind:value={description} required></textarea>
    </label>
</div>
<div class="game-wordlist">
    <h3>Word List</h3>
    <div>Between 10 and 30 words. Puzzles are randomly generated using a selection of your words at play time
    </div>
    <div class="game-wordlist-container">
        <input id="word_01" type="text" bind:value={inputWords[0]}>
        <input id="word_02" type="text" bind:value={inputWords[1]}>
        <input id="word_03" type="text" bind:value={inputWords[2]}>
        <input id="word_04" type="text" bind:value={inputWords[3]}>
        <input id="word_05" type="text" bind:value={inputWords[4]}>
        <input id="word_06" type="text" bind:value={inputWords[5]}>
        <input id="word_07" type="text" bind:value={inputWords[6]}>
        <input id="word_08" type="text" bind:value={inputWords[7]}>
        <input id="word_09" type="text" bind:value={inputWords[8]}>
        <input id="word_10" type="text" bind:value={inputWords[9]}>
        <input id="word_11" type="text" bind:value={inputWords[10]}>
        <input id="word_12" type="text" bind:value={inputWords[11]}>
        <input id="word_13" type="text" bind:value={inputWords[12]}>
        <input id="word_14" type="text" bind:value={inputWords[13]}>
        <input id="word_15" type="text" bind:value={inputWords[14]}>
        <input id="word_16" type="text" bind:value={inputWords[15]}>
        <input id="word_17" type="text" bind:value={inputWords[16]}>
        <input id="word_18" type="text" bind:value={inputWords[17]}>
        <input id="word_19" type="text" bind:value={inputWords[18]}>
        <input id="word_20" type="text" bind:value={inputWords[19]}>
        <input id="word_21" type="text" bind:value={inputWords[20]}>
        <input id="word_22" type="text" bind:value={inputWords[21]}>
        <input id="word_23" type="text" bind:value={inputWords[22]}>
        <input id="word_24" type="text" bind:value={inputWords[23]}>
        <input id="word_25" type="text" bind:value={inputWords[24]}>
        <input id="word_26" type="text" bind:value={inputWords[25]}>
        <input id="word_27" type="text" bind:value={inputWords[26]}>
        <input id="word_28" type="text" bind:value={inputWords[27]}>
        <input id="word_29" type="text" bind:value={inputWords[28]}>
        <input id="word_30" type="text" bind:value={inputWords[29]}>
    </div>
</div>
<div class="game-subject">
    <h2>Subject</h2>
    <div>
        <input type="radio" id="contact-private" name="contact" value="private"/>
        <label for="contact-private"> Myself,family,friends etc.</label>
    </div>
    <div>
        <input type="radio" id="contact-public" name="contact" value="public"/>
        <label for="contact-public"> Non-Personal(recommended)</label>
    </div>
</div>
<button class="game-submit" on:click|preventDefault={onHandleClick}>게임 만들기</button>
<style>

    .game-title {
        text-align: start;
    }

    .game-title .game-title-text {
        width: 100%;
    }

    .game-description {
        text-align: start;
    }

    .game-description .game-description-text {
        width: 100%;
        text-align: start;
    }

    .game-wordlist .game-wordlist-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
    }

    .game-submit {
        width: 100%;
        height: 45px;
    }
</style>