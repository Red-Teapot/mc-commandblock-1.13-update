from .. import data

def upgrade(id: str or int) -> str:
    id = str(id)

    if id in data.enchant_id_map:
        return data.enchant_id_map[id]
    else:
        return id