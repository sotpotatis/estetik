#!/bin/bash
#run_app.sh
#This script runs the API so you can host it on any server.
export ESTETIK_SERVER_BASE_URL="http://estetik-api.albins.website" #Change me to the server's base URL
export ESTETIK_SERVER_PORT=4000 #Change me to whichever port you want to run on
#SSL settings:
export ESTETIK_SERVER_SSL=false #Change me to "true" to run SSL
export ESTETIK_SERVER_SSL_KEY_PATH=/srv/estetik.albins.website.key #Set the key path here if using SSL
export ESTETIK_SERVER_SSL_CERT_PATH=/srv/estetik.albins.website.pem #Set the cert path here if using SSL
export ESTETIK_SERVER_SSL_PORT=2053 #Set the port for SSL here if using SSL
echo "Running app on $ESTETIK_SERVER_BASE_URL..."
echo "Running app on $ESTETIK_SERVER_BASE_URL..."
cd /srv/estetik/api
node app #Runs the app