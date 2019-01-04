import logging

from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import selector, command_upgrader_base
from commands.pre_1_13.parser.primitives.selector import Selector

CMDEXS = [
    CMDEx('scoreboard objectives list'),

    CMDEx('scoreboard objectives add {str:name} {str:criteria}'),
    CMDEx('scoreboard objectives add {str:name} {str:cirteria} {json:display_name}'),

    CMDEx('scoreboard objectives remove {str:name}'),

    CMDEx('scoreboard objectives setdisplay {str:slot}'),
    CMDEx('scoreboard objectives setdisplay {str:slot} {str:objective}'),

    CMDEx('scoreboard objectives modify {str:objective} displayname {json:displayname}'),

    CMDEx('scoreboard players list'),
    CMDEx('scoreboard players list *'),
    CMDEx('scoreboard players list {selector:entity}'),

    CMDEx('scoreboard players set * {str:objective} {int:score}'),
    CMDEx('scoreboard players set * {str:objective} {int:score} {nbtstr:nbt}'),
    CMDEx('scoreboard players set {selector:entity} {str:objective} {int:score}'),
    CMDEx('scoreboard players set {selector:entity} {str:objective} {int:score} {nbtstr:nbt}'),

    CMDEx('scoreboard players add * {str:objective} {int:score}'),
    CMDEx('scoreboard players add * {str:objective} {int:score} {nbtstr:nbt}'),
    CMDEx('scoreboard players add {selector:entity} {str:objective} {int:score}'),
    CMDEx('scoreboard players add {selector:entity} {str:objective} {int:score} {nbtstr:nbt}'),

    CMDEx('scoreboard players remove * {str:objective} {int:score}'),
    CMDEx('scoreboard players remove * {str:objective} {int:score} {nbtstr:nbt}'),
    CMDEx('scoreboard players remove {selector:entity} {str:objective} {int:score}'),
    CMDEx('scoreboard players remove {selector:entity} {str:objective} {int:score} {nbtstr:nbt}'),

    CMDEx('scoreboard players reset *'),
    CMDEx('scoreboard players reset * {str:objective}'),
    CMDEx('scoreboard players reset {selector:entity}'),
    CMDEx('scoreboard players reset {selector:entity} {str:objective}'),

    CMDEx('scoreboard players enable * {str:trigger}'),
    CMDEx('scoreboard players enable {selector:entity} {str:trigger}'),

    CMDEx('scoreboard players operation * {str:target_objective} {op:operation} {selector:other} {str:objective}'),
    CMDEx('scoreboard players operation {selector:entity} {str:target_objective} {op:operation} * {str:objective}'),
    CMDEx('scoreboard players operation {selector:entity} {str:target_objective} {op:operation} {selector:other} {str:objective}'),

    CMDEx('scoreboard players tag * add {tag:tag_name}'),
    CMDEx('scoreboard players tag * add {tag:tag_name} {nbtstr:nbt}'),
    CMDEx('scoreboard players tag {selector:entity} add {tag:tag_name}'),
    CMDEx('scoreboard players tag {selector:entity} add {tag:tag_name} {nbtstr:nbt}'),

    CMDEx('scoreboard players tag * remove {tag:tag_name}'),
    CMDEx('scoreboard players tag * remove {tag:tag_name} {nbtstr:nbt}'),
    CMDEx('scoreboard players tag {selector:entity} remove {tag:tag_name}'),
    CMDEx('scoreboard players tag {selector:entity} remove {tag:tag_name} {nbtstr:nbt}'),

    CMDEx('scoreboard players tag * list'),
    CMDEx('scoreboard players tag {selector:entity} list'),

    CMDEx('scoreboard players test * {str:objective} *'),
    CMDEx('scoreboard players test * {str:objective} * *'),
    CMDEx('scoreboard players test * {str:objective} * {int:max}'),
    CMDEx('scoreboard players test * {str:objective} {int:min}'),
    CMDEx('scoreboard players test * {str:objective} {int:min} *'),
    CMDEx('scoreboard players test * {str:objective} {int:min} {int:max}'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} *'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} * *'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} * {int:max}'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} {int:min}'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} {int:min} *'),
    CMDEx('scoreboard players test {selector:entity} {str:objective} {int:min} {int:max}'),

    CMDEx('scoreboard teams list'),
    CMDEx('scoreboard teams list {str:team_name}'),

    CMDEx('scoreboard teams add {str:name}'),
    CMDEx('scoreboard teams add {str:name} {str:displayname}'),

    CMDEx('scoreboard teams remove {str:name}'),

    CMDEx('scoreboard teams empty {str:name}'),

    CMDEx('scoreboard teams join {str:team}'),
    CMDEx('scoreboard teams join {str:team} *'),
    CMDEx('scoreboard teams join {str:team} {selector:entity}'),
    CMDEx('scoreboard teams join {str:team} {*:entities}'),

    CMDEx('scoreboard teams leave'),
    CMDEx('scoreboard teams leave *'),
    CMDEx('scoreboard teams leave {selector:entity}'),
    CMDEx('scoreboard teams leave {*:entities}'),

    CMDEx('scoreboard teams option {str:team} color {str:value}'),
    CMDEx('scoreboard teams option {str:team} friendlyfire {str:value}'),
    CMDEx('scoreboard teams option {str:team} seeFriendlyInvisibles {str:value}'),
    CMDEx('scoreboard teams option {str:team} nametagVisibility {str:value}'),
    CMDEx('scoreboard teams option {str:team} deathMessageVisibility {str:value}'),
    CMDEx('scoreboard teams option {str:team} collisionRule {str:value}'),
]

logger = logging.getLogger(__name__)

def __upgrade_entity(order: list, props: list) -> str:
    additional_args = dict()
    if 'nbt' in props:
        additional_args['nbt'] = props['nbt']
    
    if 'entity' in props:
        return selector.upgrade(props['entity'], additional_args)
    elif len(order) > 4 and order[3] == '*':
        return str(Selector('a', additional_args, {}))
    else:
        raise Exception('Can not upgrade entity')

def __upgrade(order, props):
    logger.debug('%s %s', order, props)

    result = ''

    if order[1] == 'players':
        new_entity = __upgrade_entity(order, props)

        if order[2] == 'tag':
            result += 'tag ' + new_entity + ' '
            for tok in order[4:]:
                if tok == '#nbt':
                    continue
                if tok[0] == '#':
                    result += str(props[tok[1:]]) + ' '
                else:
                    result += tok + ' '
        elif order[2] == 'test':
            if 'min' not in props and 'max' not in props:
                result += 'execute if entity ' + new_entity + ' '
            else:
                result += 'execute if score ' + new_entity + ' '
                result += props['objective'] + ' matches '
                if 'min' in props and 'max' in props and props['min'] == props['max']:
                    result += str(props['min']) + ' '
                else:
                    if 'min' in props:
                        result += str(props['min'])
                    result += '..'
                    if 'max' in props:
                        result += str(props['max'])
                    result += ' '
        else:
            result += 'scoreboard players ' + order[2] + ' ' + new_entity + ' '
            for tok in order[4:]:
                if tok == '#nbt':
                    continue
                if tok == '#other':
                    result += selector.upgrade(props['other']) + ' '
                elif tok[0] == '#':
                    result += str(props[tok[1:]]) + ' '
                else:
                    result += tok + ' '
    elif order[1] == 'teams':
        result += 'team '
        for tok in order[2:]:
            if tok == '#entity':
                result += selector.upgrade(props['entity']) + ' '
            elif tok[0] == '#':
                result += str(props[tok[1:]]) + ' '
            else:
                result += tok + ' '
    else:
        for tok in order:
            if tok == '#entity':
                result += selector.upgrade(props['entity']) + ' '
            elif tok[0] == '#':
                result += str(props[tok[1:]]) + ' '
            else:
                result += tok + ' '
    
    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)