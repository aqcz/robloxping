import requests
import time
from keep_alive import keep_alive

# Your list of Roblox user IDs
user_ids = [2346725415, 5589770247, 4456108587, lol5xd19qz8sf6g2x3w7]
webhook_url = 'https://discord.com/api/webhooks/1364600481715982426/PNOfhEBw8RKwaWkhvzJtEmj_Si6wmJ4vpBXEJn9Ho6iRPSYVltFSV7HIrZ4CDjrIa2Lv'

online_users = set()

def check_users():
    global online_users
    for user_id in user_ids:
        try:
            response = requests.get(f'https://api.roblox.com/users/{user_id}')
            if response.status_code == 200:
                user_info = response.json()
                username = user_info.get("Username", f"User ID: {user_id}")
                presence = requests.post(
                    "https://presence.roblox.com/v1/presence/users",
                    json={"userIds": [user_id]},
                    headers={"Content-Type": "application/json"}
                ).json()
                is_online = presence["userPresences"][0]["userPresenceType"] != 0

                if is_online and user_id not in online_users:
                    online_users.add(user_id)
                    ping = f"{username} is now **online**!"
                    send_webhook(ping)
                elif not is_online and user_id in online_users:
                    online_users.remove(user_id)
                    ping = f"{username} is now **offline**."
                    send_webhook(ping)
        except Exception as e:
            print("Error:", e)

def send_webhook(message):
    payload = {"content": message}
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print("Failed to send webhook:", e)

keep_alive()

while True:
    check_users()
    time.sleep(300)  # check every 5 minutes
