async function submit(e) {
    const numCol = document.getElementById('numCol').value;
    const codeLength = document.getElementById('codeLength').value;
    const sel = document.getElementById('duplicateSel');
    const duplicate = sel.options[sel.selectedIndex].value;

    await fetch()
}

function init() {
    const form = document.getElementById('setup_form');
    form.addEventListener('submit', submit);

}

//init();