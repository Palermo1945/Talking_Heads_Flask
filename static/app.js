document.getElementById('generateButton').addEventListener('click', function() {
    const inputText = document.getElementById('inputText').value;

    fetch('/generate-video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        const resultMessage = document.getElementById('resultMessage');
        const downloadButton = document.getElementById('downloadButton');

        if (data.result_url) {
            resultMessage.textContent = 'Video generated successfully!';
            downloadButton.style.display = 'inline-block';
            downloadButton.textContent = 'Download Video';

            // Use JavaScript to set up the download
            downloadButton.addEventListener('click', function() {
                window.location.href = data.result_url;
            });
        } else {
            resultMessage.textContent = 'Failed to generate video. Please try again.';
            downloadButton.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
