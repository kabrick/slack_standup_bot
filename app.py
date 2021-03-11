from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
import os

slack_app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SLACK_EVENTS_TOKEN")
)

channel = "team-stan-ups"


@slack_app.event("app_mention")
def hello(event, say):
    say(f"Hello, <@{event['user']}>! I hope you had breakfast today")


@slack_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


app = Flask(__name__)
handler = SlackRequestHandler(slack_app)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@app.route('/')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
