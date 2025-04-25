import requests
import time
import discord
from flask import Flask

app = Flask(__name__)

# Your Roblox user ID(s)
TARGET_USER_IDS = [2346725415, 5589770247, 4456108587, 3023198676]  # Replace with actual player IDs

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1364600481715982426/PNOfhEBw8RKwaWkhvzJtEmj_Si6wmJ4vpBXEJn9Ho6iRPSYVltFSV7HIrZ4CDjrIa2Lv"

# Roblox API to get players in the game
ROBLOX_API_URL = "https://api.roblox.com/users/{user_id}/onlinestatus"

# Discord webhook function
def send_discord_notification(player_name):
    data = {
        "content": f"**{player_name}** has joined the game!"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response

# Function to check if a player is in the game
def check_player_online(user_id):
    response = requests.get(ROBLOX_API_URL.format(user_id=user_id))
    data = response.json()

    # Check if the user is currently online
    if data.get('IsOnline') == True:
        return data.get('PlayerName')  # Return the player name if online
    return None

@app.route('/')
def index():
    online_players = []

    for user_id in TARGET_USER_IDS:
        player_name = check_player_online(user_id)
        if player_name:
            online_players.append(player_name)
            send_discord_notification(player_name)

    if online_players:
        return f"Notified about the following players: {', '.join(online_players)}"
    else:
        return "No players online right now."

# Keep the Flask app running
if __name__ == '__main__':
    app.run(debug=True)
