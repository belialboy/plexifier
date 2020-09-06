# plexifier

This project creates a connector between Plex webhooks and Pushbullet using AWS API Gateway and an AWS Lambda Function, so that you are alerted when changes are made to your media server

## Pre-reqs

You will need:

* An AWS Account
* AWS CLI and suitable AWS Credentials configured in your shell
* AWS SAM installed
* Python 3.6 installed onto the PATH
* A Pushbullet API key (Get this from your Pushbullet account page)

## Build and Deploy

```
sam build
sam deploy -g
```

Follow the prompts, and then grab the PlexifierFunctionAPI URL, and add this to the webhooks section of your Plex Media Server.
