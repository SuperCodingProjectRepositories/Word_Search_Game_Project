<script>
    // Your Svelte script here
    import Header from "../../Components/Header.svelte";

    const onClickGameListItem = (event) => {
        event.preventDefault(); // 필요 시 기본 동작 방지
        window.location.pathname = '/playgame.html'; // 올바른 절대 경로 사용
    }

</script>

<!-- Your HTML here -->
<Header/>

<body>
<div> Hello World</div>
<main>
    <ul class="game-list">
        <li class="game-list-item" on:click={onClickGameListItem}>
            게임 타이틀입니다.
        </li>
    </ul>
</main>
<footer></footer>
<script src="javascripts/index.js"></script>
</body>

<style>
    /* Your Svelte styles here */
</style>
