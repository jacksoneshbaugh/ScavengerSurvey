/**
 * This file contains the JavaScript for the modal that appears when a user
 * clicks on a bingo prompt to submit a response. The modal allows the user
 * to input their response and submit it to the server.
 *
 * @file modal.js
 * @author Jackson Eshbaugh
 * @version 03/11/2024
 */

/**
 * Opens the modal and sets the prompt to the given value.
 *
 * @param prompt the prompt to display in the modal
 */
function openModal(prompt) {
    document.getElementById('modal-prompt').innerHTML = prompt;
    document.getElementById('prompt_id').value = prompt;
    document.getElementById('modal').style.display = 'block';
}

/**
 * Closes the modal and clears the response input.
 */
function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('response').value = '';
}

/**
 * Listens for the user to click anywhere outside the modal and closes the
 * modal if so.
 *
 * @param event the event that triggered the listener
 */
window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('response').value = '';
    }
}