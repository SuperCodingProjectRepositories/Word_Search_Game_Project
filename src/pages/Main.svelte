<script>
    // Your Svelte script here
    import Header from "../components/Header.svelte";
    import { getDatabase, ref, onValue } from "firebase/database";
    import {onMount} from "svelte";


    const db = getDatabase();
    const gameDataRef = ref(db, 'gameDatas/');

    $: gameDatas = [];

    const onClickGameListItem = (event) =>
    {
        const gameId = event.target.id;
        window.location.hash = `/playGame?gameId=${gameId}`;
        console.log(window.location.hash);
    }

    onMount(() => {
        console.log("onMount");
        onValue(gameDataRef, (res) => {
            const data = res.val();

            if (!data) {
                console.error("No game data found in Firebase.");
                return;
            }

            gameDatas = Object.entries(data).map(([key, value]) => ({
                id: key,
                ...value
            })).reverse();
        });

    })

</script>

<!-- Your HTML here -->
<Header/>

<main>
    <div class="game-list">
        {#each gameDatas as data, index}
            <button class="game-list-item" id={data.id} on:click|preventDefault={onClickGameListItem}>
                 {index + 1} : {data.title}
            </button>
        {/each}
    </div>
</main>

<style>
    .game-list-item {
        width: 100%;
        height: 50px;
        padding: 10px;
        margin: 5px 10px;
        text-align: start;
        background: none;
        border: none;
    }
</style>
