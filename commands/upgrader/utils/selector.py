from commands.pre_1_13.parser.primitives import Selector
from commands.upgrader import data
from commands.pre_1_13.parser.primitives.id import ID
from commands.upgrader.utils import entity


# TODO Upgrade entity types
def upgrade(selector: Selector or str, additional_arguments: dict=None) -> str:
    if type(selector) is str:
        return selector
    
    result = '@' + selector.variable

    has_args = False

    if selector.arguments and len(selector.arguments) > 0:
        has_args = True
    
    if selector.scores and len(selector.scores) > 0:
        has_args = True
    
    if additional_arguments:
        args = additional_arguments
    else:
        args = dict()

    # Pre-process arguments: use new names and merge values like r and rm into one dict
    if selector.arguments:
        for name, value in selector.arguments.items():
            if name in ['x', 'z']:
                args[name] = int(value) + 0.5
            elif name == 'y':
                args[name] = int(value)
            elif name in ['dx', 'dy', 'dz']:
                args[name] = int(value)
            elif name == 'l':
                if 'level' not in args:
                    args['level'] = dict()
                args['level']['max'] = int(value)
            elif name == 'lm':
                if 'level' not in args:
                    args['level'] = dict()
                args['level']['min'] = int(value)
            elif name == 'r':
                if 'distance' not in args:
                    args['distance'] = dict()
                args['distance']['max'] = int(value)
            elif name == 'rm':
                if 'distance' not in args:
                    args['distance'] = dict()
                args['distance']['min'] = int(value)
            elif name in ['dx' 'dy', 'dz']:
                args[name] = int(value)
            elif name in ['tag', 'team', 'name']:
                args[name] = str(value)
            elif name == 'm':
                if value[0] == '!':
                    args['gamemode'] = '!' + data.gamemode_map[value[1:]]
                else:
                    args['gamemode'] = data.gamemode_map[value]
            elif name == 'rx':
                if 'x_rotation' not in args:
                    args['x_rotation'] = dict()
                args['x_rotation']['max'] = int(value)
            elif name == 'rxm':
                if 'x_rotation' not in args:
                    args['x_rotation'] = dict()
                args['x_rotation']['min'] = int(value)
            elif name == 'ry':
                if 'y_rotation' not in args:
                    args['y_rotation'] = dict()
                args['y_rotation']['max'] = int(value)
            elif name == 'rym':
                if 'y_rotation' not in args:
                    args['y_rotation'] = dict()
                args['y_rotation']['min'] = int(value)
            elif name == 'c':
                limit = int(value)
                if limit < 0:
                    args['sort'] = 'furthest'
                args['limit'] = abs(limit)
            elif name == 'type':
                is_negative = value.value[0] == '!'
                actual_id = ID(value.namespace, value.value[1:] if is_negative else value.value)
                upgraded_id = entity.upgrade(actual_id)
                if is_negative:
                    upgraded_id = '!' + upgraded_id
                args['type'] = upgraded_id
            else:
                raise Exception('Unknown selector argument name: {}'.format(name))
    
    if has_args:
        result += '['

    for name, value in args.items():
        if type(value) is dict:
            val = ''
            if 'min' in value and 'max' in value:
                if value['min'] == value['max']:
                    val = str(value['min'])
                else:
                    val = str(value['min']) + '..' + str(value['max'])
            elif 'min' in value:
                val = str(value['min']) + '..'
            elif 'max' in value:
                val = '..' + str(value['max'])
            
            result += name + '=' + val + ','
        else:
            result += name + '=' + str(value) + ','
    
    scores_str = ''
    if selector.scores:
        for name, value in selector.scores.items():
            val = ''
            if 'min' in value and 'max' in value:
                if value['min'] == value['max']:
                    val = str(value['min'])
                else:
                    val = str(value['min']) + '..' + str(value['max'])
            elif 'min' in value:
                val = str(value['min']) + '..'
            elif 'max' in value:
                val = '..' + str(value['max'])
            
            scores_str += name + '=' + val + ','

    if scores_str:
        if scores_str[-1] == ',':
            scores_str = scores_str[:-1]
        
        result += 'scores={' + scores_str + '},'
    
    if has_args:
        if result[-1] == ',':
            result = result[:-1]
        
        result += ']'

    return result