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
def event_test(message, say):
    user = message['user']
    say(f"Hello, <@{user}>! I hope you had breakfast today")


@slack_app.event("message.app_home")
def event_test(message, say):
    user = message['user']
    say(f"Hello, <@{user}>! I am still learning the ways of man. Soon, we will talk")


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
