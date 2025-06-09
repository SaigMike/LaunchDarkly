// Fetch the current feature status from the server and update UI accordingly
async function fetchFeatureStatus() {
  const response = await fetch('/scenario1/feature');
  const data = await response.json();

  // Update feature status text based on fetched flag state
  document.getElementById('feature-status').innerText =
    `Feature is currently: ${data.feature_flag ? 'Enabled 🟢' : 'Disabled 🔴'}`;

  // Toggle visibility of the upload section based on feature state
  document.getElementById('upload-section').style.display = data.feature_flag ? 'block' : 'none';
}

// Toggle the feature flag state (enabled/disabled)
async function toggleFeature() {
  // Retrieve the current state of the feature flag
  const currentResponse = await fetch('/scenario1/feature');
  const currentData = await currentResponse.json();

  // Send request to server to toggle feature state
  await fetch('/scenario1/toggle', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ on: !currentData.feature_flag })
  });
}

// Handle file upload action by user
async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const formData = new FormData();

  // Append selected file to FormData object
  formData.append('file', fileInput.files[0]);

  // Send file upload request to the server
  const response = await fetch('/scenario1/upload', {
    method: 'POST',
    body: formData
  });

  // Process and display upload result
  const result = await response.json();
  document.getElementById('upload-status').innerText = result.success
    ? `File uploaded: ${result.filename} ✅`
    : `Upload failed: ${result.message || 'Unknown error'} ❌`;
}

// Attach event listeners and initialize periodic feature status updates
// Toggle button event listener
document.getElementById('toggle-btn').addEventListener('click', toggleFeature);

// Initial feature status check
fetchFeatureStatus();

// Periodically refresh feature status every second (1000 milliseconds)
setInterval(fetchFeatureStatus, 1000);