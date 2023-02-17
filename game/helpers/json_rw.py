from json import dump, load

from game.config import Config

Block = dict[str, str | int | list[str]]

def read_json(json_path: str) -> Block:
    
    with open(json_path) as json_file:
        return load(json_file)

def write_json(json_path: str, json_data: Block):
    
    with open(json_path, "w") as json_file:
        dump(json_data, json_file, indent=2)

get_block = lambda player_name, block_number: f"{Config.block_path}/{player_name}/block{block_number}.json"
read_block = lambda block_number: read_json(get_block('', block_number))
write_block = lambda player_name, block_number, block_data: write_json(get_block(player_name, block_number), block_data)