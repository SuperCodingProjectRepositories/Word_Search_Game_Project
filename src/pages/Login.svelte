<script>
    import {user$} from "../Store.js";
    import {getAuth, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider} from "firebase/auth";

    const provider = new GoogleAuthProvider();
    const auth = getAuth();

    let email = "";
    let password = "";

    const onClickEmailLogin = async () => {
        if(email.length <= 0 || password.length <= 0) {
            return false;
        }
        try {
            const res = await signInWithEmailAndPassword(auth, email, password);
            const userJson = res.user.toJSON();
            const accessToken = userJson['stsTokenManager'].accessToken;
            user$.set(res.user);
            localStorage.setItem('token', accessToken);
            localStorage.setItem('loginType', "Email");
            localStorage.setItem('userName', res.user.displayName);

            console.log("Successfully logged in!");
            window.location.hash = "/";
        } catch (error) {
            console.log(error);
        }
    }

    const onClickGoogleLogin = async () => {
        try {
            const result = await signInWithPopup(auth,provider);
            // This gives you a Google Access Token. You can use it to access the Google API.
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            // The signed-in user info.
            const user = result.user;
            console.log(user);
            console.log(credential);
            user$.set(user);
            localStorage.setItem('token', token);
//            localStorage.setItem('loginType', "Google");
            localStorage.setItem('userName', user.displayName);
            console.log("Successfully logged in!");
            window.location.hash = "/";
        }
        catch (error) {
            console.log(error);
        }
    }

    const onClickSignup = () => {
        window.location.hash = '/signup'
    }
</script>

<!--
<div>
    <label for="email">이메일</label>
    <input type="email" id="email" name="email" bind:value={email} required>
</div>
<div>
    <label for="password">비밀번호</label>
    <input type="password" id="password" name="password" bind:value={password} required>
</div>
<div>
    <button on:click={onClickEmailLogin}>로그인</button>
</div>
-->
<div class="display">
    <button class="login-button" on:click={onClickGoogleLogin}>
        <img
                class="google-logo"
                src="https://lh3.googleusercontent.com/qnaJEbFIpvsWJm2KrRI_GIvz1yZdXntgEsCZxy-1pVZi244bCk1RFwdk0ZBRmmvdHiUl6sIa_tsmskL5WLKiigp2AMsIIxinOJNf39qCmacViRGXIOY"
                alt="google-logo"
        />
        <div>Google로 시작하기</div>
    </button>
</div>
<!--
<div>
    <button id="signup-btn" type="submit" on:click={onClickSignup}>회원가입</button>
</div>
-->

<style>
    .display {
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .login-button {
        width: 200px;
        height: 50px;
        border: 1px solid gray;
        border-radius: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .google-logo {
        width: 30px;
    }
</style>
