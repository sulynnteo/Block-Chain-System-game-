# Assignment personal

## Requirements

This personal assignment requires Python 3.10 or higher.

```bash
 pip3 install -r requirements.txt
```

## Setup

create environment in folder if unable to run:

```
python3 -m venv venv
source venv/bin/activate
```
Add your PubNub keys and channel name to the `.env` file.

```bash
vi .env
-------------------------------------------
PUBNUB_SUBSCRIBE_KEY="<your_subscribe_key>"
PUBNUB_PUBLISH_KEY="<your_publish_key>"
PUBNUB_CHANNEL="<your_channel>"
```

## Usage

```bash
sh launch.sh
```
