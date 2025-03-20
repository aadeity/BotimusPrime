document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const uploadStatus = document.getElementById('upload-status');
    const queryInput = document.getElementById('query-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const modelSelect = document.getElementById('model-select');

    let currentFile = null;

    // to update my file name display when file is selected
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'No file chosen';
        }
    });

    // for hanndling file upload
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            showStatus('Please select a file first', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        showStatus('Uploading file...', 'loading');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showStatus('File uploaded successfully!', 'success');
                currentFile = data.filename;
                queryInput.disabled = false;
                sendBtn.disabled = false;

                //bot message?
                addMessage(`I've processed "${currentFile}". What would you like to know about it?`, 'bot');
            } else {
                showStatus(`Error: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            showStatus(`Error: ${error.message}`, 'error');
        });
    });

    // Handling of sending queries
    sendBtn.addEventListener('click', sendQuery);
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendQuery();
        }
    });

    function sendQuery() {
        const query = queryInput.value.trim();
        if (!query) return;

        // Adding user message
        addMessage(query, 'user');

        // Clearing input
        queryInput.value = '';

        // Adding loading message
        const loadingId = 'loading-' + Date.now();
        addMessage('Thinking...', 'bot', loadingId);

        // Getting selected model
        const selectedModel = modelSelect.value;

        // Sending query to backend
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                filename: currentFile,
                model: selectedModel
            })
        })
        .then(response => response.json())
        .then(data => {

            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.remove();
            }

            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage(`Error: ${data.error}`, 'bot');
            }
        })
        .catch(error => {

            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.remove();
            }

            addMessage(`Error: ${error.message}`, 'bot');
        });
    }

    function addMessage(text, sender, id = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        if (id) {
            messageDiv.id = id;
        }

        const messagePara = document.createElement('p');
        messagePara.textContent = text;

        messageDiv.appendChild(messagePara);
        chatMessages.appendChild(messageDiv);


        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = type;
    }
});
