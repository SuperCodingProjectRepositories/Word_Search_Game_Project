<script>
    // Your Svelte script here
    import Header from "../components/Header.svelte";
    import { getDatabase, ref, onValue } from "firebase/database";
    import {onMount} from "svelte";
    const db = getDatabase();
    const gameDataRef = ref(db, 'gameDatas');

    $: gameDatas = [];

    const onClickGameListItem = (event) =>
    {
        const currentGame = gameDatas.find((x) => x.id === event.target.id);
        sessionStorage.setItem("currentGame",JSON.stringify(currentGame));
        window.location.hash = '/playGame'
    }


    onMount(() => {
        onValue(gameDataRef, (res) => {
            const data = res.val();
            gameDatas = Object.entries(data).map(([key,value]) => ({
                id: key,
                ...value
            })).reverse();
            console.log(gameDatas);
        });
    })

</script>

<!-- Your HTML here -->
<Header/>

<main>
    <ul class="game-list">
        {#each gameDatas as data}
            <li class="game-list-item" id={data.id}
                on:click|preventDefault={onClickGameListItem}>
                {data.title}
            </li>
        {/each}
    </ul>
</main>

<style>
    /* Your Svelte styles here */
</style>
