#!/bin/bash
#run_app.sh
#This script runs the API so you can host it on any server.
export ESTETIK_SERVER_BASE_URL="estetik-api.albins.website" #Change me to the server's base URL
echo "Running app on $ESTETIK_SERVER_BASE_URL..."
cd /srv/estetik/api
node app #Runs the app