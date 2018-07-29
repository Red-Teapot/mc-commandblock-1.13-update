from .. import data


def upgrade(id: str) -> str:
    id = str(id)
    
    if id in data.effect_id_map:
        return effect_id_map[id]
    
    return id