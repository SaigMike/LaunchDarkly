// Fetch default feature status using explicitly stable context
async function fetchDefaultFeatureStatus() {
  const email = 'user@example.com';
  const region = 'us-east';
  const subscription = 'premium';

  try {
    const response = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}`
    );
    const data = await response.json();

    document.getElementById('feature-status').innerText =
      `Feature is currently: ${data.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴'}`;

    document.getElementById('download-section').style.display = data.feature_flag ? 'block' : 'none';
  } catch (error) {
    console.error('Error fetching feature status:', error);
    document.getElementById('feature-status').innerText = 'Error fetching feature status ⚠️';
  }
}

// Explicit toggle based on a stable default context (not form input)
async function toggleFeature() {
  // Stable default context ensures consistent toggling
  const defaultEmail = 'user@example.com';
  const defaultRegion = 'us-east';
  const defaultSubscription = 'premium';

  try {
    // Fetch the current feature state based on the default stable context
    const currentResponse = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(defaultEmail)}&region=${encodeURIComponent(defaultRegion)}&subscription=${encodeURIComponent(defaultSubscription)}`
    );
    const currentData = await currentResponse.json();

    // Send request to toggle the feature state (on → off, off → on)
    await fetch('/scenario2/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: !currentData.feature_flag })
    });

    // Fetch updated feature state immediately after toggling
    const updatedResponse = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(defaultEmail)}&region=${encodeURIComponent(defaultRegion)}&subscription=${encodeURIComponent(defaultSubscription)}`
    );
    const updatedData = await updatedResponse.json();

    // Update UI based on the updated global feature state
    document.getElementById('feature-status').innerText =
      `Feature is currently: ${updatedData.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴'}`;

    document.getElementById('download-section').style.display = updatedData.feature_flag ? 'block' : 'none';

  } catch (error) {
    console.error('Error toggling feature:', error);
    alert('Error toggling feature ⚠️');
  }
}


// Initial load and periodic check using stable default context
document.addEventListener('DOMContentLoaded', fetchDefaultFeatureStatus);
setInterval(fetchDefaultFeatureStatus, 1000);

// Attach explicit toggle to button click
document.getElementById('toggle-btn').addEventListener('click', toggleFeature);

// Handle form submission for file download explicitly
document.getElementById('target-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const region = document.getElementById('region').value;
  const subscription = document.getElementById('subscription').value;
  const filename = document.getElementById('filename').value;

  try {
    const response = await fetch(
      `/scenario2/download-file?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}&filename=${encodeURIComponent(filename)}`
    );

    if (response.status === 200) {
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
  } catch (error) {
    console.error('Error initiating file download:', error);
    document.getElementById('download-status').innerText = 'Error initiating download ⚠️';
  }
});
