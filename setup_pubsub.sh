#!/bin/sh

source .env

# Wait for pubsub-emulator to come up
bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' '$PUBSUB_SETUP_HOST')" != "200" ]]; do sleep 1; done'

curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$RECEIPT_TOPIC_PROJECT_ID/topics/$RECEIPT_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$PPO_UNDELIVERED_SUBSCRIPTION_PROJECT_ID/topics/$PPO_UNDELIVERED_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$QM_UNDELIVERED_SUBSCRIPTION_PROJECT_ID/topics/$QM_UNDELIVERED_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$RECEIPT_TOPIC_PROJECT_ID/subscriptions/$SUBSCRIPTION_NAME -H 'Content-Type: application/json' -d '{"topic": "projects/'$RECEIPT_TOPIC_PROJECT_ID'/topics/'$RECEIPT_TOPIC_NAME'"}'
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$OFFLINE_RECEIPT_TOPIC_PROJECT_ID/topics/$OFFLINE_RECEIPT_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$OFFLINE_RECEIPT_TOPIC_PROJECT_ID/subscriptions/$OFFLINE_SUBSCRIPTION_NAME -H 'Content-Type: application/json' -d '{"topic": "projects/'$OFFLINE_RECEIPT_TOPIC_PROJECT_ID'/topics/'$OFFLINE_RECEIPT_TOPIC_NAME'"}'
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$QM_UNDELIVERED_SUBSCRIPTION_PROJECT_ID/subscriptions/$QM_UNDELIVERED_SUBSCRIPTION_NAME -H 'Content-Type: application/json' -d '{"topic": "projects/'$QM_UNDELIVERED_SUBSCRIPTION_PROJECT_ID'/topics/'$QM_UNDELIVERED_TOPIC_NAME'"}'
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$PPO_UNDELIVERED_SUBSCRIPTION_PROJECT_ID/subscriptions/$PPO_UNDELIVERED_SUBSCRIPTION_NAME -H 'Content-Type: application/json' -d '{"topic": "projects/'$PPO_UNDELIVERED_SUBSCRIPTION_PROJECT_ID'/topics/'$PPO_UNDELIVERED_TOPIC_NAME'"}'
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$FULFILMENT_CONFIRMED_PROJECT/topics/$FULFILMENT_CONFIRMED_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$FULFILMENT_CONFIRMED_PROJECT/subscriptions/$FULFILMENT_CONFIRMED_SUBSCRIPTION -H 'Content-Type: application/json' -d '{"topic": "projects/'$FULFILMENT_CONFIRMED_PROJECT'/topics/'$FULFILMENT_CONFIRMED_TOPIC_NAME'"}'
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$EQ_FULFILMENT_PROJECT/topics/$EQ_FULFILMENT_TOPIC_NAME
curl -X PUT http://$PUBSUB_SETUP_HOST/v1/projects/$EQ_FULFILMENT_PROJECT/subscriptions/$EQ_FULFILMENT_SUBSCRIPTION -H 'Content-Type: application/json' -d '{"topic": "projects/'$EQ_FULFILMENT_PROJECT'/topics/'$EQ_FULFILMENT_TOPIC_NAME'"}'
