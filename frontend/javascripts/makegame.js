class gameData{
    title = ""
    description = ""
    words = []
    public = false;
}

const form = document.querySelector('#gameData-form');

function checkWords(){
    let count = 0;
    for (let i = 1; i <= 30; i++) {
        const index = `word_${String(i).padStart(2,'0')}`;
        const el = document.getElementById(index);
        if(el.value !== "")
            count++;
    }
    return count >= 10;
}

const makeGameData = async (event) => {
    event.preventDefault(); // 기본 동작 방지

    const title = document.querySelector(".game-title-text");
    const description = document.querySelector(".game-description-text");

    if(checkWords() === false)
    {
        alert("단어를 10개 이상 작성해주세요!");
        return;
    }

    const currentGameData = new gameData();
    currentGameData.title = title.value;
    currentGameData.description = description.value;
    for (let i = 0; i < 30; i++) {
        const index = `word_${String(i + 1).padStart(2,'0')}`;
        const word = document.getElementById(index);
        if(word.value !== "")
            currentGameData.words.push(word.value);
    }

    const selectedValue = document.querySelector('input[name="contact"]:checked').value;
    currentGameData.public = selectedValue === "public";

    const res = await fetch('/create-game',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentGameData),
    })
    const data = await res.json();
    console.log(data);
}

form.addEventListener('submit', makeGameData);


