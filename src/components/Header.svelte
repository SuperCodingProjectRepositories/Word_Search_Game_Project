<script>
    const onMoveToMakeGame = () => {
        window.location.hash = '/makeGame';
    };
    const onMoveToMain = () => {
        window.location.hash = '/';
    }
</script>

<header>
    <div class="title">
        <button class="title-container-left" on:click={onMoveToMain}>
            <div class="title-text">The Word Search</div>
        </button>
        <div class="title-container-right">
            <button class="title-btn" on:click={onMoveToMakeGame}>
                <div class="title-btn-icon">
                    <img alt="panicle" src="asset/svg/pancle.svg">
                </div>
                <div class="title-btn-text">Word Search Make</div>
            </button>
            <div class="title-btn">
                <div class="title-btn-icon">
                    <img src="asset/svg/pancle.svg" alt="panicle">
                </div>
                <div class="title-btn-text">Word Search Make</div>
            </div>
            <div class="title-btn">
                <div class="title-btn-icon">
                    <img src="asset/svg/pancle.svg" alt="panicle">
                </div>
                <div class="title-btn-text">Word Search Make</div>
            </div>
        </div>
    </div>
</header>

<style>
    button{
        border: none;
        background: none;
    }

    header {
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid red;
    }

    .title {
        width: 100%;
        height: 65px;
        margin: 0 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .title-container-left {
        display: flex;
        justify-content: start;
        align-items: center;
    }

    .title-container-right {
        display: flex;
        justify-content: end;
        align-items: center;
    }

    .title-btn {
        display: flex;
        justify-content: start;
        align-items: center;
    }

    .title-btn-icon {
        width: 25px;
        height: 25px;
    }

</style>