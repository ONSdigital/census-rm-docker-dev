#!/bin/sh

source .env

curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$RECEIPT_TOPIC_PROJECT_ID/topics/$RECEIPT_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$RECEIPT_TOPIC_PROJECT_ID/subscriptions/$SUBSCRIPTION_NAME -H 'Content-Type: application/json' -d '{"topic": "projects/'$RECEIPT_TOPIC_PROJECT_ID'/topics/'$RECEIPT_TOPIC_NAME'"}'
