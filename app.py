from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import os

app = Flask(__name__)
channel = "team-stan-ups"
token = os.environ.get("SLACK_TOKEN")
events_token = os.environ.get("SLACK_EVENTS_TOKEN")

# Create a slack client
slack_web_client = WebClient(token)

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(events_token, "/slack/events", app)


@app.route('/')
def hello_world():
    messages = {
        "channel": channel,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hallo bruder, welkome"
                }
            },
        ],
    }

    slack_web_client.chat_postMessage(**messages)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    # Since the activation phrase was met, get the channel ID that the event
    # was executed on
    # channel_id = event.get("channel")
    hello_world()


if __name__ == '__main__':
    app.run()
