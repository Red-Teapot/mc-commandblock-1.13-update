import logging

from ..data import block, blockstate
from commands.pre_1_13.parser.primitives import ID, BlockState
from commands.pre_1_13.nbtstr import Parser
from commands.pre_1_13.nbtstr.types import NBTCompound


nbtstr_parser = Parser()
logger = logging.getLogger(__name__)

# a - b
# Only one level deep
def subtract_dict(a: dict, b: dict) -> dict:
    if not a:
        return None
    
    if not b:
        return a
    
    result = dict()
    for k, v in a.items():
        if k not in b:
            result[k] = v
    return result

def check_dict_in(what: dict, where: dict) -> bool:
    if not what:
        return True
    elif not where:
        return False
    
    for k, v in what.items():
        if k not in where:
            return False
        
        if type(where[k]) is dict:
            if not check_dict_in(v, where[k]):
                return False
        else:
            if v != where[k]:
                return False
    
    return True

class BlockUpgrader(object):
    
    def __init__(self, id: ID, state: BlockState, data: int, nbt: NBTCompound):
        self.id = id
        self.state = state
        self.data = data
        self.nbt = nbt

        if self.id.namespace:
            self.id.namespace = self.id.namespace.lower()
        if self.id.value:
            self.id.value = self.id.value.lower()

        self.res_id = ID(self.id.namespace, self.id.value)
        self.res_state = BlockState(self.state.data.copy() if self.state and self.state.data else dict())
        self.res_nbt = None
    
    def __set(self, id_value: str, state: BlockState):
        if not self.res_id:
            self.res_id = ID(self.id.namespace, self.id.value)
        
        if not self.res_state:
            self.res_state = BlockState(dict())
        
        if id_value:
            self.res_id.value = id_value
        
        if state:
            self.res_state = state
    
    def __merge(self, id_value: str, state: BlockState):
        if not self.res_id:
            self.res_id = ID(self.id.namespace, self.id.value)
        
        if not self.res_state:
            self.res_state = BlockState(dict())
        
        if id_value:
            self.res_id.value = id_value
        
        if state:
            self.res_state.data.update(state.data)
    
    def upgrade(self):
        # Apply block data (if defined)
        if self.data:
            if self.state:
                raise Exception('Both data and state can not be defined at one time')
            
            if self.id.value in block.data_state_map:
                value = block.data_state_map[self.id.value][self.data]

                logger.debug('Added block state from block data %s: %s', self.data, BlockState(value))

                self.state = BlockState(value)
                self.res_state = BlockState(value.copy())
                self.data = None
        
        nbt_keys_to_drop = list()
        
        if self.id.value in blockstate.default_no_nbt_map:
            value = blockstate.default_no_nbt_map[self.id.value]
            self.__set(value[0], BlockState(value[1]) if value[1] else None)
            logger.debug('Set default non-NBT values: %s %s', value[0], value[1])
        
        if self.nbt and self.id.value in blockstate.default_nbt_map:
            replacement_data = blockstate.default_nbt_map[self.id.value]

            for key, value in replacement_data.items():
                key_nbt = nbtstr_parser.parse(key)[0]
                
                if check_dict_in(key_nbt.values, self.nbt.values):
                    logger.debug('Set default NBT values [%s]: %s %s', key, value[0], value[1])
                    self.__set(value[0], BlockState(value[1]) if value[1] else None)
                    nbt_keys_to_drop = list(key_nbt.values.keys())
                    break
        
        if self.state and self.id.value in blockstate.actual_no_nbt_map:
            replacement_data = blockstate.actual_no_nbt_map[self.id.value]

            for key, value in replacement_data.items():
                key_bstate = BlockState.parse(key)

                if check_dict_in(key_bstate.data, self.state.data):
                    logger.debug('Set actual non-NBT values [%s]: %s %s', key, value[0], value[1])
                    self.__set(value[0], BlockState(value[1]) if value[1] else None)
        
        if self.nbt and self.id.value in blockstate.actual_nbt_map:
            replacement_data = blockstate.actual_nbt_map[self.id.value]

            for key, value in replacement_data.items():
                key_bstate_str, key_nbt_str = key.split('|')

                key_bstate = BlockState.parse(key_bstate_str)
                key_nbt = nbtstr_parser.parse(key_nbt_str)[0]

                if check_dict_in(key_bstate.data, self.state.data) and check_dict_in(key_nbt.values, self.nbt.values):
                    logger.debug('Set actual NBT values [%s]: %s %s', key, value[0], value[1])
                    self.__set(value[0], BlockState(value[1]) if value[1] else None)
                    nbt_keys_to_drop += list(key_nbt.values.keys())
        
        if self.nbt and self.id.value in blockstate.additional_nbt_map:
            additional_data = blockstate.additional_nbt_map[self.id.value]

            for key, value in additional_data.items():
                key_nbt = nbtstr_parser.parse(key)[0]

                if check_dict_in(key_nbt.values, self.nbt.values):
                    logger.debug('Add additional blockstate data [%s]: %s', key, value)
                    self.__merge(value[0], BlockState(value[1]) if value[1] else None)
                    nbt_keys_to_drop += list(key_nbt.values.keys())
        
        if self.nbt:
            for key, value in self.nbt.values.items():
                if key not in nbt_keys_to_drop:
                    if not self.res_nbt:
                        self.res_nbt = NBTCompound(dict())
                    
                    self.res_nbt.values[key] = value
        
        if self.res_state and len(self.res_state.data) == 0:
            self.res_state = None
        
        return (self.res_id, self.res_state, self.res_nbt)

def upgrade(id: ID, bstate: BlockState, bdata: int, bnbt: NBTCompound):
    upgrader = BlockUpgrader(id, bstate, bdata, bnbt)

    return upgrader.upgrade()