#!/bin/bash
gcloud run jobs deploy lemmy-sightengine --project bots-424808 --region europe-west1 --source . --set-env-vars=LEMMY_USER="eric",LEMMY_INSTANCE="feddit.uk",API_USER="144260338",MODULES="no_ai_images|check_comments" --set-secrets="LEMMY_PW=eric:latest","API_SECRET=sightengine:latest"
