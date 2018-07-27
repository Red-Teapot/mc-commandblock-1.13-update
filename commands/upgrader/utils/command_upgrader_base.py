from commands.pre_1_13.cmdex import CMDEx

def upgrade(CMDEXs: list, command: str, callback: callable) -> str:
    order = None
    props = None

    for cmdex in CMDEXs:
        try:
            order, props = cmdex.match(command)
        except:
            pass
    
    if not order or not props:
        raise Exception('Unknown syntax for command \'{}\''.format(command))
    
    return callback(order, props)