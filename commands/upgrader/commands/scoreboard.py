import logging

from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import selector, command_upgrader_base

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

    CMDEx('scoreboard players operation * {str:target_objective} {op:operation} {selector:entity} {str:objective}'),
    CMDEx('scoreboard players operation {selector:target_name} {str:target_objective} {op:operation} * {str:objective}'),
    CMDEx('scoreboard players operation {selector:target_name} {str:target_objective} {op:operation} {selector:entity} {str:objective}'),

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

def __upgrade(order, props):
    logger.debug('%s %s', order, props)

    result = ''

    for tok in order:
        if tok[0] == '#':
            tok = tok[1:]

            if tok not in props:
                raise Exception('Unknown token name: {}'.format(tok))
            
            if tok in ['entity', 'target_name']:
                result += selector.upgrade(props[tok]) + ' '
            else:
                result += str(props[tok]) + ' '
        else:
            result += tok + ' '
    
    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)