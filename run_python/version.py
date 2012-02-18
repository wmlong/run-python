class Version(str):
    
    #Current
    MAJOR = 0
    MINOR = 1
    MICRO = 2
    LEVEL = 'final'
    
    #Metadata
    ORDER = [
        'MAJOR', 
        'MINOR', 
        'MICRO', 
        'LEVEL'
    ]
    
    def __new__(cls):
        elements = []
        for name in cls.ORDER:
            value = str(getattr(cls, name))
            if value != 'final':
                elements.append(value)
        return str.__new__(cls, '.'.join(elements))
    
    @property
    def info(self):
        return tuple(getattr(self, name) 
                     for name in self.ORDER)
    
    @property
    def path(self):
        return __file__.replace('.pyc', '.py')
    
    @property
    def code(self):
        lines = []
        with open(self.path) as f:
            for line in f:
                for name in self.ORDER:
                    if line.strip().startswith(name):
                        line = line.replace(
                            str(getattr(Version, name)),
                            str(getattr(self, name))
                        )
                        break
                lines.append(line)
        return ''.join(lines)

    def next(self, step='minor', level='final'):
        base = self.__class__
        name = base.__name__                 
        if step == 'major':
            Version = type(name, (base,), {
                'MAJOR': base.MAJOR+1,
                'MINOR': 0,
                'MICRO': 0,
                'LEVEL': level,
            })
        elif step == 'minor':
            Version = type(name, (base,), {
                'MINOR': base.MINOR+1,
                'MICRO': 0,
                'LEVEL': level,
            })
        elif step == 'micro':
            Version = type(name, (base,), {
                'MICRO': base.MICRO+1,
                'LEVEL': level,
            })
        else:
            Version = type(name, (base,), {
                'LEVEL': level,
            })            
        return Version()