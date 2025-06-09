// Handle form submission for experiment evaluation and event tracking
document.getElementById('experiment-form').onsubmit = async (e) => {
    e.preventDefault();

    // Retrieve user inputs
    const email = document.getElementById('email').value;
    const region = document.getElementById('region').value;
    const subscription = document.getElementById('subscription').value;

    try {
        // Request evaluation of the user's experiment variation
        const variationResponse = await fetch('/scenario3/evaluate-experiment', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, region, subscription})
        });

        const variationData = await variationResponse.json();

        // Display assigned experiment variation to user
        document.getElementById('experiment-result').innerText =
            `You are assigned to: ${variationData.variation}`;

        // Track banner click event for analytics
        const clickResponse = await fetch('/scenario3/banner-clicked', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, region, subscription})
        });

        const clickData = await clickResponse.json();

        // Update UI with event tracking confirmation
        document.getElementById('experiment-result').innerText +=
            `\nBanner click event tracked: ${clickData.status}`;
    } catch (error) {
        console.error('Error processing experiment:', error);
        document.getElementById('experiment-result').innerText = 'Error processing experiment ⚠️';
    }
};