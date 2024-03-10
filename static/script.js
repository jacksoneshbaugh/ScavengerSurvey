// Popup modal for submitting responses to bingo prompts
function openModal(prompt) {
    document.getElementById('modal-prompt').innerHTML = prompt;
    document.getElementById('prompt_id').value = prompt;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('response').value = '';
}

window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('response').value = '';
    }
}