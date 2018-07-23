from .target_selector import TargetSelector


class Command(object):
    def __init__(self, name=None, args=None):
        self.name = name if name else None
        self.args = args if args else list()
    
    def __str__(self):
        return '<Command \'{} {}\''.format(self.name, ' '.join([str(x) for x in self.args]))