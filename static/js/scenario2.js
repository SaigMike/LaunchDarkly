async function fetchFeatureStatus() {
  const email = document.getElementById('email').value.trim() || 'guest@example.com';
  const region = document.getElementById('region').value.trim() || 'us-east';
  const subscription = document.getElementById('subscription').value.trim() || 'free';

  try {
    const response = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}`
    );

    const data = await response.json();
    document.getElementById('feature-status').innerText =
      'Feature is currently: ' + (data.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴');

    document.getElementById('download-section').style.display = data.feature_flag ? 'block' : 'none';
  } catch (error) {
    console.error('Error fetching feature status:', error);
    document.getElementById('feature-status').innerText = 'Error fetching feature status ⚠️';
  }
}

async function toggleFeature() {
  const email = document.getElementById('email').value.trim() || 'guest@example.com';
  const region = document.getElementById('region').value.trim() || 'us-east';
  const subscription = document.getElementById('subscription').value.trim() || 'free';

  try {
    const currentResponse = await fetch(
      `/scenario2/feature?email=${encodeURIComponent(email)}&region=${encodeURIComponent(region)}&subscription=${encodeURIComponent(subscription)}`
    );

    const currentData = await currentResponse.json();

    await fetch('/scenario2/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: !currentData.feature_flag })
    });

    fetchFeatureStatus();
  } catch (error) {
    console.error('Error toggling feature:', error);
    alert('Error toggling feature ⚠️');
  }
}

document.getElementById('toggle-btn').addEventListener('click', toggleFeature);
['email', 'region', 'subscription'].forEach(id => {
  document.getElementById(id).addEventListener('input', fetchFeatureStatus);
});

fetchFeatureStatus();
setInterval(fetchFeatureStatus, 1000);

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