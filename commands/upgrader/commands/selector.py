from commands.pre_1_13.parser.primitives import Selector


GAMEMODES = {
    '0': 'survival',
    's': 'survival',

    '1': 'creative',
    'c': 'creative',

    '2': 'adventure',
    'a': 'adventure',

    '3': 'spectator',
    'sp': 'spectator'
}

def upgrade(selector: Selector, additional_arguments: dict=None) -> str:
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
    for name, value in selector.arguments.items():
        if name in ['x', 'z']:
            args[name] = int(value) + 0.5
        elif name == 'y':
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
        elif name in ['tag', 'team', 'name', 'type']:
            args[name] = str(value)
        elif name == 'm':
            args['gamemode'] = GAMEMODES[value]
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