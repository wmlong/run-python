class Version(str):
    
    #Current
    MAJOR = 0
    MINOR = 1
    MICRO = 1
    RELEASELEVEL = 'final'
    
    def __new__(self):
        items = [str(self.MAJOR), str(self.MINOR), str(self.MICRO)]
        if self.RELEASELEVEL != 'final':
            items.append(self.RELEASELEVEL)    
        return str.__new__(self, '.'.join(items))
    
    @property
    def info(self):
        return (self.MAJOR, self.MINOR, self.MICRO, self.RELEASELEVEL)         