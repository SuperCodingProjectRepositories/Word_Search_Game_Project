<script>
    import Main from "./pages/Main.svelte";
    import MakeGame from "./pages/MakeGame.svelte";
    import PlayGame from "./pages/PlayGame.svelte";
    import NotFound from "./pages/NotFound.svelte";
    import Router from 'svelte-spa-router';

    // 경로와 컴포넌트를 매핑
    const routes = {
        '/': Main,           // 기본 경로에 Main 컴포넌트 연결
        '/makeGame': MakeGame,
        '/playGame': PlayGame,
        '*': NotFound,       // 모든 경로가 일치하지 않을 경우 NotFound 컴포넌트 표시
    }
</script>

<!--&lt;!&ndash; 라우터 컴포넌트에 router 객체 전달 &ndash;&gt;-->
<Router {routes}></Router>
