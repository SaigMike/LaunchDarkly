document.getElementById('experiment-form').onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const region = document.getElementById('region').value;
    const subscription = document.getElementById('subscription').value;

    const response = await fetch('/scenario3/banner-clicked', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, region, subscription})
    });

    const data = await response.json();

    document.getElementById('experiment-result').innerText = 
        'Banner click event: ' + data.status;
};
