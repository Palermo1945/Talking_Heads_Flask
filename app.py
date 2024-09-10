from flask import Flask, render_template, jsonify, request
import requests
import time

app = Flask(__name__)

# Define the route for the UI
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for making the API call to D-ID
@app.route('/generate-video', methods=['POST'])
def generate_video():
    # Extract data from the frontend
    user_input = request.json.get('input_text')

    # D-ID API request to generate the video
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "input": user_input,
            "provider": {
                "type": "microsoft",
                "voice_id": "ja-JP-KeitaNeural"
            }
        },
        "source_url": "https://i.imgur.com/Z9NVvnb.png",
        "config": {
            "stitch": True
            
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Basic YnJlYWRjcm9pc3NhbnRzOEBnbWFpbC5jb20:xNZSg09H2xNP7DcEbJfoF"
    }

    # Make the POST request to D-ID API
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    # Extract the ID from the response
    talk_id = response_data.get("id")

    # Print the talk_id to the console
    print(f"Talk ID: {talk_id}")

    if not talk_id:
        return jsonify({"error": "Failed to get ID from D-ID API"}), 400

    # Polling to check the status of the generated video
    status_url = f"https://api.d-id.com/talks/{talk_id}"

    while True:
        status_response = requests.get(status_url, headers=headers)
        status_data = status_response.json()

        # If the status is 'done' and result_url is available, break the loop
        if status_data.get("status") == "done" and status_data.get("result_url"):
            break

        # Wait for 10 seconds before checking again
        time.sleep(10)

    # Structure the response according to your expected format
    formatted_response = {
        "user": {
            "features": status_data.get("user", {}).get("features", []),
            "stripe_plan_group": status_data.get("user", {}).get("stripe_plan_group", ""),
            "authorizer": status_data.get("user", {}).get("authorizer", ""),
            "owner_id": status_data.get("user", {}).get("owner_id", ""),
            "id": status_data.get("user", {}).get("id", ""),
            "plan": status_data.get("user", {}).get("plan", ""),
            "email": status_data.get("user", {}).get("email", "")
        },
        "script": {
            "length": status_data.get("script", {}).get("length", 0),
            "subtitles": status_data.get("script", {}).get("subtitles", False),
            "type": status_data.get("script", {}).get("type", ""),
            "provider": status_data.get("script", {}).get("provider", {})
        },
        "metadata": {
        },
        "result_url": status_data.get("result_url", "")
    }

    # Return the formatted response to the frontend
    return jsonify(formatted_response)

if __name__ == '__main__':
    app.run(debug=True)
