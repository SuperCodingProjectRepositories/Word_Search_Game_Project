<script>
    import {user$} from "../Store.js";
    import {getAuth, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider} from "firebase/auth";

    const auth = getAuth();
    const provider = new GoogleAuthProvider();

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
            user$.set(user);
            localStorage.setItem('token', token);
            localStorage.setItem('loginType', "Google");
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
<div>
    <button on:click={onClickGoogleLogin}>구글 로그인</button>
</div>

<div>
    <button id="signup-btn" type="submit" on:click={onClickSignup}>회원가입</button>
</div>

<style></style>
