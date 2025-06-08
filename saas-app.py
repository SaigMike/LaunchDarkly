from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
import requests
from dotenv import load_dotenv
import ldclient
from ldclient.config import Config
from ldclient import Context

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder for file uploads
app.config["UPLOAD_FOLDER"] = "upload"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Retrieve LaunchDarkly configuration from environment
LD_SDK_KEY = os.getenv("PRODUCTION_LD_SDK_KEY")
LD_PROJECT_KEY = os.getenv("PRODUCTION_LD_PROJECT_KEY")
LD_FLAG_KEY = os.getenv("PRODUCTION_LD_FLAG_KEY")
LD_API_TOKEN = os.getenv("LD_API_TOKEN")

# Initialize LaunchDarkly client
ldclient.set_config(Config(LD_SDK_KEY))
ld_client = ldclient.get()


# Route for landing page
@app.route("/")
def index():
    return render_template("index.html")


# Route for Scenario 1: Release and Remediate page
@app.route("/scenario1")
def scenario1():
    return render_template("scenario1.html")


# Endpoint to check feature flag state for Scenario 1
@app.route("/scenario1/feature")
def scenario1_feature():
    user_context = Context.create("example-user")
    flag_value = ld_client.variation(LD_FLAG_KEY, user_context, False)
    return jsonify({"feature_flag": flag_value})


# Endpoint to toggle feature flag state for Scenario 1 via LaunchDarkly API
@app.route("/scenario1/toggle", methods=["POST"])
def scenario1_toggle():
    url = f"https://app.launchdarkly.com/api/v2/flags/{LD_PROJECT_KEY}/{LD_FLAG_KEY}"
    new_state = request.json.get("on", False)
    headers = {
        "Authorization": LD_API_TOKEN,
        "Content-Type": "application/json; domain-model=json-patch",
    }
    payload = [
        {"op": "replace", "path": "/environments/production/on", "value": new_state}
    ]
    response = requests.patch(url, headers=headers, json=payload)
    return jsonify({"success": response.status_code == 200, "details": response.json()})


# Endpoint to handle file upload for Scenario 1
@app.route("/scenario1/upload", methods=["POST"])
def scenario1_upload():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return jsonify({"success": True, "filename": filename})

# Route for Scenario 2: Targeting page
@app.route("/scenario2")
def scenario2():
    return render_template("scenario2.html")


# Endpoint to check feature flag state for Scenario 2
@app.route("/scenario2/feature")
def scenario2_feature():
    email = request.args.get("email", "guest@example.com")
    region = request.args.get("region", "us-east")
    subscription = request.args.get("subscription", "free")

    user_context = (
        Context.builder(email)
        .set("region", region)
        .set("subscription", subscription)
        .build()
    )

    flag_value = ld_client.variation("landing-page-banner", user_context, False)

    return jsonify({"feature_flag": flag_value})


@app.route("/scenario2/toggle", methods=["POST"])
def scenario2_toggle():
    new_state = request.json.get("on", False)

    url = f"https://app.launchdarkly.com/api/v2/flags/{LD_PROJECT_KEY}/landing-page-banner"
    headers = {
        "Authorization": LD_API_TOKEN,
        "Content-Type": "application/json; domain-model=json-patch",
    }
    payload = [
        {"op": "replace", "path": "/environments/production/on", "value": new_state}
    ]
    response = requests.patch(url, headers=headers, json=payload)

    return jsonify({"success": response.status_code == 200, "details": response.json()})


# Endpoint to control file downloads based on LaunchDarkly targeting rules
@app.route("/scenario2/download-file", methods=["GET"])
def scenario2_download_file():
    email = request.args.get("email", "guest@example.com")
    region = request.args.get("region", "us-east")
    subscription = request.args.get("subscription", "free")
    filename = request.args.get("filename")

    if not filename:
        return jsonify({"success": False, "message": "No filename provided"}), 400

    user_context = (
        Context.builder(email)
        .set("region", region)
        .set("subscription", subscription)
        .build()
    )

    flag_value = ld_client.variation("landing-page-banner", user_context, False)

    if not flag_value:
        return (
            jsonify({"success": False, "message": "Feature not enabled for this user"}),
            403,
        )

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "File not found"}), 404

    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )

# Route for Scenario 3: Experimentation page
@app.route("/scenario3")
def scenario3():
    return render_template("scenario3.html")


# Endpoint to track user interactions for experimentation purposes
@app.route("/scenario3/banner-clicked", methods=["POST"])
def scenario3_banner_clicked():
    data = request.json
    email = data.get("email", "guest@example.com")
    region = data.get("region", "us-east")
    subscription = data.get("subscription", "free")

    user_context = (
        Context.builder(email)
        .set("region", region)
        .set("subscription", subscription)
        .build()
    )

    ld_client.track("banner-click", user_context)

    return jsonify({"status": "event tracked"})


# Main entry point to run the Flask application
if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5001)
