from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request, render_template
import ldclient
from ldclient.config import Config
from ldclient import Context

app = Flask(__name__)

# Explicitly load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

LD_SDK_KEY = os.getenv("LD_SDK_KEY")
if not LD_SDK_KEY:
    raise Exception("Missing LaunchDarkly SDK Key! Set LD_SDK_KEY environment variable.")

ldclient.set_config(Config(LD_SDK_KEY))
ld_client = ldclient.get()

# Scenario 1: Release and Remediate
@app.route("/scenario1")
def scenario1():
    return render_template('scenario1.html')

@app.route("/scenario1/feature")
def scenario1_feature():
    user_context = Context.create("example-user")
    flag_value = ld_client.variation("new-feature", user_context, False)
    return jsonify({"feature_flag": flag_value})

# Scenario 2: Target
@app.route("/scenario2")
def scenario2():
    return render_template('scenario2.html')

@app.route("/scenario2/landing-page")
def scenario2_landing_page():
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

    content = ("New Banner Component Activated!" if flag_value else "Default Landing Page.")

    return jsonify({
        "feature_flag": flag_value,
        "content": content,
        "user": {"email": email, "region": region, "subscription": subscription}
    })

# Scenario 3: Experimentation
@app.route("/scenario3")
def scenario3():
    return render_template('scenario3.html')

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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
