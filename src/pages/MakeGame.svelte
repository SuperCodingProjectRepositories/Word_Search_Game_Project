<script>
    import Header from "../components/Header.svelte";
</script>

<Header/>

<form id="gameData-form">
    <div class="game-title">
        <label> Title
            <input class="game-title-text" type="text" required>
        </label>
    </div>
    <div class="game-description">
        <label> Description
            <textarea class="game-description-text" placeholder="" required></textarea>
        </label>
    </div>
    <div class="game-wordlist">
        <label>Word List</label>
        <div>Between 10 and 30 words. Puzzles are randomly generated using a selection of your words at play time
        </div>
        <div class="game-wordlist-container">
            <input id="word_01" type="text">
            <input id="word_02" type="text">
            <input id="word_03" type="text">
            <input id="word_04" type="text">
            <input id="word_05" type="text">
            <input id="word_06" type="text">
            <input id="word_07" type="text">
            <input id="word_08" type="text">
            <input id="word_09" type="text">
            <input id="word_10" type="text">
            <input id="word_11" type="text">
            <input id="word_12" type="text">
            <input id="word_13" type="text">
            <input id="word_14" type="text">
            <input id="word_15" type="text">
            <input id="word_16" type="text">
            <input id="word_17" type="text">
            <input id="word_18" type="text">
            <input id="word_19" type="text">
            <input id="word_20" type="text">
            <input id="word_21" type="text">
            <input id="word_22" type="text">
            <input id="word_23" type="text">
            <input id="word_24" type="text">
            <input id="word_25" type="text">
            <input id="word_26" type="text">
            <input id="word_27" type="text">
            <input id="word_28" type="text">
            <input id="word_29" type="text">
            <input id="word_30" type="text">
        </div>
    </div>
    <div class="game-subject">
        <label>Subject</label>
        <div>
            <input type="radio" id="contact-private" name="contact" value="private"/>
            <label for="contact-private">Myself,family,friends etc.</label>
        </div>
        <div>
            <input type="radio" id="contact-public" name="contact" value="public"/>
            <label for="contact-public"> Non-Personal(recommended)</label>
        </div>
    </div>
    <input class="game-submit" type="submit">
</form>

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