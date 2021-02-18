function addTextInputEventListeners() {
    const newText= document.getElementsByClassName('new-textarea');
    const remainingText = document.getElementsByClassName('text-remaining-chars');
    const MAX_CHARS = 100;

    function test() {
        const remaining = MAX_CHARS - newText.value.length;
        const color = remaining < MAX_CHARS * 0.1 ? 'red' : null;

        remainingText.innerHTML = `${remaining}/100`;
        remainingText.style.color = color;

        if(remaining <= 0) {
            alert('글자수는 100자로 제한됩니다.');
            newText.value = newText[0].value.substring(0, 100);
            newText.focus()
        }
    }

    test();
}