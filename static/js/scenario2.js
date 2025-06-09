// Fetch feature status based on user inputs and update UI
async function fetchFeatureStatus() {
  // Retrieve input values or use defaults
  const email = document.getElementById('email').value.trim() || 'guest@example.com';
  const region = document.getElementById('region').value.trim() || 'us-east';
  const subscription = document.getElementById('subscription').value.trim() || 'free';

  try {
    // Fetch feature status from server
    const response = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}`
    );

    const data = await response.json();

    // Update UI to reflect feature status
    document.getElementById('feature-status').innerText =
      `Feature is currently: ${data.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴'}`;

    // Toggle visibility of the download section
    document.getElementById('download-section').style.display = data.feature_flag ? 'block' : 'none';
  } catch (error) {
    console.error('Error fetching feature status:', error);
    document.getElementById('feature-status').innerText = 'Error fetching feature status ⚠️';
  }
}

// Toggle feature flag status based on current state
async function toggleFeature() {
  const email = document.getElementById('email').value.trim() || 'guest@example.com';
  const region = document.getElementById('region').value.trim() || 'us-east';
  const subscription = document.getElementById('subscription').value.trim() || 'free';

  try {
    // Retrieve current feature state
    const currentResponse = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}`
    );

    const currentData = await currentResponse.json();

    // Send request to toggle the feature state
    await fetch('/scenario2/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: !currentData.feature_flag })
    });

    // Refresh feature status after toggling
    fetchFeatureStatus();
  } catch (error) {
    console.error('Error toggling feature:', error);
    alert('Error toggling feature ⚠️');
  }
}

// Attach event listeners to elements
// Feature toggle button
document.getElementById('toggle-btn').addEventListener('click', toggleFeature);

// User input fields for real-time feature status updates
['email', 'region', 'subscription'].forEach(id => {
  document.getElementById(id).addEventListener('input', fetchFeatureStatus);
});

// Initial feature status fetch
fetchFeatureStatus();

// Periodically update feature status every second
setInterval(fetchFeatureStatus, 1000);

// Handle form submission for file download
document.getElementById('target-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  // Retrieve input values
  const email = document.getElementById('email').value;
  const region = document.getElementById('region').value;
  const subscription = document.getElementById('subscription').value;
  const filename = document.getElementById('filename').value;

  try {
    // Request file download from server
    const response = await fetch(
      `/scenario2/download-file?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}&filename=${encodeURIComponent(filename)}`
    );

    if (response.status === 200) {
      // Initiate file download on successful response
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
      // Display error message from server response
      const result = await response.json();
      document.getElementById('download-status').innerText = `Error: ${result.message}`;
    }
  } catch (error) {
    console.error('Error initiating file download:', error);
    document.getElementById('download-status').innerText = 'Error initiating download ⚠️';
  }
});