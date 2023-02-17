from os import _exit as force_exit
from os import makedirs, walk
from os.path import exists
from random import choice

from game.config import Config
from game.helpers import Block, encrypt_sha256, read_block, write_block
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class Player:

    def __init__(self, player_name: str, remaining_grids: list[str], pubnub: PubNub):

        self.player_name = player_name
        self.remaining_grids = remaining_grids
        self.pubnub = pubnub

        player_block_path = f'{Config.block_path}/{player_name}'

        if not exists(player_block_path):
            makedirs(player_block_path)

    def remove_grid(self, move: str):

        self.remaining_grids = [grid for grid in self.remaining_grids if grid != move]
        print(f'Remaining grids left: {self.remaining_grids} Count: {len(self.remaining_grids)}')

        if len(self.remaining_grids) <= 0:
            print('There are no remaining grids.')
            force_exit(0)

    def generate_next_turn(self, current_block: Block):

        current_transaction = current_block['Transaction']
        current_move = 'NO MOVE' if not current_transaction else current_transaction[1]
        self.remove_grid(current_move)

        block_names = [file.split('.')[0] for sublist in (files for _, _, files in walk(Config.block_path)) for file in sublist]
        current_turn = max(int(block_name[5:]) for block_name in block_names)
        next_turn = current_turn + 1
        next_move = choice(self.remaining_grids)

        hash_value = encrypt_sha256(current_block)
        nonce = 0

        while hash(hash_value) > Config.sha_limit:
            nonce += 1
            current_block['Nonce'] = nonce
            hash_value = encrypt_sha256(current_block)

        next_transaction = (self.player_name, next_move)

        next_block = {
            'TxID': next_turn,
            'Hash': hash_value,
            'Nonce': nonce,
            'Transaction': next_transaction
        }

        write_block(self.player_name, next_turn, next_block)
        self.pubnub.publish().channel(Config.pubnub_channel).message(next_block).sync()
        print(f'Player {self.player_name} played the move {next_move}.')

        self.remove_grid(next_move)

class SubscribeHandler(SubscribeCallback):

    def __init__(self, player: Player):

        self.player = player

    def message(self, _, message):
        
        transaction = message.message.get('Transaction')

        if not transaction or transaction[0] == self.player.player_name:
            return

        print(f'Player {transaction[0]} played the move {transaction[1]}.')

        self.player.generate_next_turn(message.message)

def main(player_name):

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = Config.pubnub_subscribe_key
    pnconfig.publish_key = Config.pubnub_publish_key
    pnconfig.user_id = player_name
    pubnub = PubNub(pnconfig)
    remaining_grids = Config.grid_names
    player = Player(player_name, remaining_grids, pubnub)

    if player_name == Config.player_that_starts_first:
        print(f'Player {player_name} starts the game.')
        player.generate_next_turn(read_block(Config.initial_turn))

    else:
        print(f'Player {player_name} waits for the game to start.')

    pubnub.add_listener(SubscribeHandler(player))
    pubnub.subscribe().channels(Config.pubnub_channel).execute()
