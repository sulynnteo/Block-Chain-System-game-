from os import environ as env

from dotenv import load_dotenv


class Config:

    load_dotenv()

    initial_turn = 0
    grid_names = ['A','B','C','D','E','F','G','H','I']
    player_that_starts_first = 'Alice'
    block_path = 'blocks'
    message_path = 'messages'
    sha_limit = 2 ** 244
    pubnub_subscribe_key = env.get("PUBNUB_SUBSCRIBE_KEY")
    pubnub_publish_key = env.get("PUBNUB_PUBLISH_KEY")
    pubnub_channel = env.get("PUBNUB_CHANNEL")
