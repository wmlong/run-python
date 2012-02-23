class Patcher(object):
    """
    Patch scope by data. 
    """
    
    PATTERN = ('self.patched.setdefault(key, {key})\n'
               '{key} = value')
    
    def __init__(self, scope):
        """
        Instantiates class object by scope to patch.
        """
        self.scope = scope
        self.patched = {}

    def patch(self, data):
        """
        Patchs instance scope by data.
        """
        for key, value in data.items():
            if self.scope.has_key(key):
                self.patched.setdefault(key, self.scope[key])
                self.scope[key] = value
            else:
                exec (self.PATTERN.format(key=key)) in self.scope, locals()
        
    def restore(self):
        """
        Restores instance scope.
        """
        self.patch(self.patched)
        self.patched = {}