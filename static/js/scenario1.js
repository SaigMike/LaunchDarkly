// Function to fetch feature status and update UI accordingly
async function fetchFeatureStatus() {
  const response = await fetch('/scenario1/feature');
  const data = await response.json();
  document.getElementById('feature-status').innerText =
    'Feature is currently: ' + (data.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴');

  document.getElementById('upload-section').style.display = data.feature_flag ? 'block' : 'none';
}

// Function to toggle the feature flag
async function toggleFeature() {
  const currentResponse = await fetch('/scenario1/feature');
  const currentData = await currentResponse.json();
  await fetch('/scenario1/toggle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ on: !currentData.feature_flag })
  });
}

// Function to handle file upload
async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  const response = await fetch('/scenario1/upload', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  document.getElementById('upload-status').innerText = result.success
    ? `File uploaded: ${result.filename} ✅`
    : `Upload failed: ${result.message || 'Unknown error'} ❌`;
}

// Event listeners and periodic updates
document.getElementById('toggle-btn').addEventListener('click', toggleFeature);
fetchFeatureStatus();
setInterval(fetchFeatureStatus, 1000);
