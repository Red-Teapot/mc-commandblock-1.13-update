from .target_selector import TargetSelector


class Command(object):
    name = None
    args = list()

    def __init__(self, name=None, args=list()):
        self.name = name
        self.args = args
    
    def __str__(self):
        return '<Command \'{} {}\''.format(self.name, ' '.join(self.args))