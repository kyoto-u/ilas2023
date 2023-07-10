import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

SLACK_USER_TOKEN = "xoxb-5402560680054-5479643041253-YGjfZ2Wphy94r69U7mdtGYWN"

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token= SLACK_USER_TOKEN)
    
@app.command("/create_channels")
def create_channels(body, ack, respond, command):
    # command リクエストを確認
    ack()
    channel_names = command['text'].split(",")
    for channel_name in channel_names:
        try:
            response = app.client.conversations_create(name=channel_name)
            channel_id = response["channel"]["id"]
            app.client.conversations_invite(
                channel=channel_id,
                users=body['user_id'],
            )
            respond(f"Created channel '{channel_name}' and invited you.")
        except SlackApiError as e:
            respond(f"Failed to create channel '{channel_name}': {e.response['error']}")


@app.command("/invite_channels")
def invite_channels(body, ack, respond, command):
    # command リクエストを確認
    ack()
    channel_names = command['text'].split(",")
    for channel_name in channel_names:
        try:
            response = app.client.conversations_list(types="public_channel,private_channel")
            channels = response["channels"]
            matching_channels = [
                channel for channel in channels if channel_name.lower() in channel["name"].lower()
            ]
            if len(matching_channels) > 0:
                for matching_channel in matching_channels:
                    channel_id = matching_channel["id"]
                    app.client.conversations_invite(
                        channel=channel_id,
                        users=body['user_id'],
                    )
                respond(f"Invited you to matching channels for '{channel_name}'.")
            else:
                respond(f"No matching channels found for '{channel_name}'.")
        except SlackApiError as e:
            respond(f"Failed to invite to channels for '{channel_name}': {e.response['error']}")

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, "xapp-1-A05DZSFRG0N-5496825775649-2d41d78283c2d932776d1a49674dba44a665d1ecf099c324c54ab50e2b03f4b2").start()