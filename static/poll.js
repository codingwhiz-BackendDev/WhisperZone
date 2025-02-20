const addOptionBtn = document.getElementById('add-option-btn');
const optionsContainer = document.getElementById('options-container');

addOptionBtn.addEventListener('click', () => {
    const inputCount = optionsContainer.querySelectorAll('input').length + 1;
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'options[]';
    newInput.placeholder = `Option ${inputCount}`;
    newInput.required = true;
    optionsContainer.appendChild(newInput);
});

// Copy Poll
function copyPollUrl() {
    const pollUrl = window.location.href
    navigator.clipboard.writeText(pollUrl)
        .then(() => alert("URL copied to clipboard!"))
        .catch(err => console.error("Failed to copy: ", err));
}