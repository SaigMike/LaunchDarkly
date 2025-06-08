document.getElementById('target-form').onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const region = document.getElementById('region').value;
    const subscription = document.getElementById('subscription').value;
    const filename = document.getElementById('filename').value;

    const response = await fetch(
        `/scenario2/download-file?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}&filename=${encodeURIComponent(filename)}`
    );

    if(response.status === 200){
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        document.getElementById('download-status').innerText = 'File download initiated ✅';
    } else {
        const result = await response.json();
        document.getElementById('download-status').innerText = `Error: ${result.message}`;
    }
};
