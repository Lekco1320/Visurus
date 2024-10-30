class wrapper:
    def __init__(self, data: object = None) -> None:
        if isinstance(data, wrapper):
            self._data = data.data
        else:
            self._data = data
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value
