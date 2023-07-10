import os
import csv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import datetime

SLACK_USER_TOKEN = "xoxb-5402560680054-5479643041253-YGjfZ2Wphy94r69U7mdtGYWN"

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=SLACK_USER_TOKEN)

def record_message(channel_name, username, message, timestamp, reaction_count, file_urls):
    # メッセージをCSVファイルに記録する処理を行います
    file_path = f"{channel_name}.csv"
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, channel_name, username, message, reaction_count, file_urls])

@app.event("message")
def handle_message_events(body, logger):
    # 新着メッセージイベントを処理します
    event = body["event"]
    channel_id = event["channel"]
    user_id = event["user"]
    message = event.get("text", "")
    timestamp = datetime.datetime.fromtimestamp(float(event["event_ts"])).strftime("%Y-%m-%d %H:%M:%S")

    # ユーザー名を取得します
    try:
        result = app.client.users_info(user=user_id)
        username = result["user"]["name"]
    except SlackApiError as e:
        logger.error(f"Failed to fetch user information: {e.response['error']}")

    # チャンネル名を取得します
    try:
        result = app.client.conversations_info(channel=channel_id)
        channel_name = result["channel"]["name"]
    except SlackApiError as e:
        logger.error(f"Failed to fetch channel information: {e.response['error']}")

    # リアクション数を取得します
    reaction_count = len(event.get("reactions", []))

    # ファイルのURLを取得します
    file_urls = []
    if "files" in event:
        for file in event["files"]:
            file_urls.append(file["url_private"])

    # メッセージを記録します
    record_message(channel_name, username, message, timestamp, reaction_count, file_urls)

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, "xapp-1-A05DZSFRG0N-5496825775649-2d41d78283c2d932776d1a49674dba44a665d1ecf099c324c54ab50e2b03f4b2").start()

