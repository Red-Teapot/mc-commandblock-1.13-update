from commands.pre_1_13.parser.primitives import ID
from commands.upgrader import data

def upgrade(id: ID) -> str:
    if id.value in data.entity_id_map:
        id.value = data.entity_id_map[id.value]
    
    return str(id)