<script>
    // Your Svelte script here
    import Header from "../../Components/Header.svelte";

    const onClickGameListItem = () => {window.location.hash = '/playGame'}

</script>

<!-- Your HTML here -->
<Header/>

<main>
    <ul class="game-list">
        <li class="game-list-item"
            on:click|preventDefault={onClickGameListItem}>
            게임 타이틀입니다.
        </li>
    </ul>
</main>

<style>
    /* Your Svelte styles here */
</style>
