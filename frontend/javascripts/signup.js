const form = document.querySelector('#signup-form');

const checkPassword = () => {
    const formData = new FormData(form);
    const password = formData.get('password');
    const password2 = formData.get('password2');

    return password2 === password;
}

const handleSubmit = async (event) => {
    event.preventDefault();
    const formdata = new FormData(form);

    const div = document.querySelector("#info");
    if(!checkPassword()){
        div.innerText = "비밀번호가 같지 않습니다."
        div.style.color = 'red';
    }
    else
    {
        const sha256Password = sha256(formdata.get('password'));
        formdata.set('password', sha256Password);

        try{
            const res = await fetch('/signup', {
                method: 'POST',
                body: formdata,
            });
            // 회원가입 성공
            if(res.status === 200){
                alert("회원 가입에 성공했습니다.")
                window.location.pathname = '/login.html'
            }
        }
        catch(err){
            console.log(err)
        }
    }
}

form.addEventListener('submit', handleSubmit);