<script>
    import Main from "./pages/Main.svelte";
    import MakeGame from "./pages/MakeGame.svelte";
    import PlayGame from "./pages/PlayGame.svelte";
    import NotFound from "./pages/NotFound.svelte";
    import Router from 'svelte-spa-router';
    import Login from "./pages/Login.svelte";
    import Signup from "./pages/Signup.svelte";
    import {onMount} from "svelte";
    import { user$ } from './Store';
    import Loading from "./pages/Loading.svelte";
    import {getAuth, GoogleAuthProvider,signInWithCredential ,signInWithEmailAndPassword} from "firebase/auth";

    const auth = getAuth();
    let isLoading = true;
    let loginType = "";

    const checkLogin = async () => {
        const token = localStorage.getItem("token");
        if(!token)
        {
            window.location.hash = '/login';
            isLoading = false;
            return;
        }
        try{
            const credential = GoogleAuthProvider.credential(null, token);
            const result = await signInWithCredential(auth, credential);
            const user = result.user;
            user$.set(user);
            isLoading = false;
        }catch (error) {
            localStorage.removeItem("token");
            user$.set(null);
            isLoading = false;
            console.log(error);
        }
    }

    // 경로와 컴포넌트를 매핑
    const routes = {
        '/': Main,           // 기본 경로에 Main 컴포넌트 연결
        '/makeGame': MakeGame,
        '/playGame': PlayGame,
        '/login': Login,
        '/signup': Signup,
        '*': NotFound,       // 모든 경로가 일치하지 않을 경우 NotFound 컴포넌트 표시
    }

    onMount(() => checkLogin());
</script>

{#if isLoading}
    <Loading />
{:else if !user$}
    <Login />
{:else}
    <Router {routes}></Router>
{/if}
