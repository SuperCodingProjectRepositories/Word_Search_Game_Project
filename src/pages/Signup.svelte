<script>
    import {getAuth, createUserWithEmailAndPassword, validatePassword} from "firebase/auth";

    const auth = getAuth();

    let email = "";       // 초기값 설정
    let password = "";    // 초기값 설정
    let password2 = "";   // 초기값 설정
    let state = "";       // 상태 메시지

    function isValidPassword() {
        const minLength = 6;
        const maxLength = 30;

        // 정규 표현식
        const hasLowercase = /[a-z]/;              // 소문자
        const hasUppercase = /[A-Z]/;              // 대문자
        const hasNumber = /[0-9]/;                 // 숫자
        const hasSpecialChar = /[^\w\s]/;          // 영숫자가 아닌 문자 (제공된 특수문자 포함)

        // 길이 체크
        if (password.length < minLength && password.length > maxLength) {
            state = `비밀번호는 ${minLength}~${maxLength}자 사이여야 합니다.`;
            return false;
        }

        // 소문자 체크
        if (!hasLowercase.test(password)) {
            state = "비밀번호에 최소 1개의 소문자가 필요합니다.";
            return false;
        }

        // 대문자 체크
        if (!hasUppercase.test(password)) {
            state = "비밀번호에 최소 1개의 대문자가 필요합니다.";
            return false;
        }

        // 숫자 체크
        if (!hasNumber.test(password)) {
            state = "비밀번호에 최소 1개의 숫자가 필요합니다.";
            return false;
        }

        // 영숫자가 아닌 문자 체크
        if (!hasSpecialChar.test(password)) {
            state = `비밀번호에 최소 1개의 특수문자가 필요합니다. (${'^ $ * . [ ] { } ( ) ? " ! @ # % & / \\ , > < \' : ; | _ ~'})`;
            return false;
        }

        return true;
    }

    const handleSubmit = async () => {
        if (password !== password2) {
            state = "비밀번호가 같지 않습니다."
            return false;
        }
        if(!isValidPassword()){
            return false;
        }
        state = "";
        try {
            const res = await createUserWithEmailAndPassword(auth, email, password);
            state = "회원가입에 성공하셨습니다.";
            // 1초 뒤에 로그인 화면으로 이동
            setTimeout(() => window.location.hash = '/login', 1000);
        } catch (error) {
            state = "회원가입에 실패하셨습니다.";
            console.log(error)
        }
    }

</script>

<div>
    <label for="email">이메일</label>
    <input type="email" id="email" name="email" bind:value={email} required/>
</div>
<div>
    <label for="password">비밀번호</label>
    <input type="password" id="password" name="password" bind:value={password} required>
</div>
<div>
    <label for="password2">비밀번호 확인</label>
    <input type="password" id="password2" name="password2" bind:value={password2} required>
</div>
<div>
    <button on:click|preventDefault={handleSubmit}>회원 가입하기</button>
</div>
<div id="info">{state}</div>