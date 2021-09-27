#!/bin/bash

cd chargify-listener
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 831731636870.dkr.ecr.us-east-1.amazonaws.com
docker build -t outbound-chargify-listener .
docker tag outbound-chargify-listener:latest 831731636870.dkr.ecr.us-east-1.amazonaws.com/outbound-chargify-listener:latest
docker push 831731636870.dkr.ecr.us-east-1.amazonaws.com/outbound-chargify-listener:latest

cd ../whatsapp-listener
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 831731636870.dkr.ecr.us-east-1.amazonaws.com
docker build -t outbound-whatsapp-listener .
docker tag outbound-whatsapp-listener:latest 831731636870.dkr.ecr.us-east-1.amazonaws.com/outbound-whatsapp-listener:latest
docker push 831731636870.dkr.ecr.us-east-1.amazonaws.com/outbound-whatsapp-listener:latest