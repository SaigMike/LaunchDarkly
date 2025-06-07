import os
from flask import Flask, jsonify, request
import ldclient
from ldclient.config import Config
from ldclient import Context
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file in project root
load_dotenv()

# Retrieve SDK key securely from environment variable
LD_SDK_KEY = os.getenv("LD_SDK_KEY")
if not LD_SDK_KEY:
    raise Exception(
        "Missing LaunchDarkly SDK Key! Set LD_SDK_KEY environment variable."
    )

# Initialize LaunchDarkly client
ldclient.set_config(Config(LD_SDK_KEY))
ld_client = ldclient.get()

# Release/Remediate Scenario
@app.route("/feature-one")
def feature_one():
    user_context = Context.create("example-user")

    # Replace the 'new-feature' variable with your actual feature flag key from LaunchDarkly
    flag_value = ld_client.variation("new-feature", user_context, False)

    return jsonify({"feature_flag": flag_value})


# Target Scenario
@app.route("/landing-page")
def landing_page():
    email = request.args.get("email", "guest@example.com")
    region = request.args.get("region", "us-east")
    subscription = request.args.get("subscription", "free")

    # Context attributes for rule-based targeting
    user_context = (
        Context.builder(email)
        .set("region", region)
        .set("subscription", subscription)
        .build()
    )

    # Replace 'landing-page-banner' with your LaunchDarkly feature flag key
    flag_value = ld_client.variation("landing-page-banner", user_context, False)

    content = (
        "New Banner Component Activated!" if flag_value else "Default Landing Page."
    )

    return jsonify(
        {
            "feature_flag": flag_value,
            "content": content,
            "user": {"email": email, "region": region, "subscription": subscription},
        }
    )


# Experimentation Scenario
@app.route("/banner-clicked", methods=["POST"])
def banner_clicked():
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

    # Track metric event defined in LaunchDarkly
    ld_client.track("banner-click", user_context)

    return jsonify({"status": "event tracked"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
