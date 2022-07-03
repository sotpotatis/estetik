#!/bin/bash
#Estetik Discord bot runner
#Runs the Estetik Discord bot
#NOTE: Set the following keys below to match your setup
export ESTETIK_BOT_TOKEN=""
export ESTETIK_TOKEN=""
export ESTETIK_API_DOMAIN=""
export ESTETIK_SSL="True"
cd /srv/estetik/automation/discord_bot
python3 main.py --api_client_path="/srv/estetik/automation/python_api_client"