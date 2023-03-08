#!/usr/bin/env python
import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', 0)
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN', 0)
OPENAI_API_KEY  = os.environ.get('OPENAI_API_KEY', 0)

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN) 
client = WebClient(SLACK_BOT_TOKEN)

# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Let the user know that we are busy with the request 
    # response = client.chat_postMessage(channel=body["event"]["channel"], 
    #                                    thread_ts=body["event"]["event_ts"],
    #                                    text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")
    
    # Check ChatGPT
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text
    
    
    # Reply to thread 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"{response}")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
