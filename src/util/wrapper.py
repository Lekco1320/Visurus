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
        if isinstance(value, wrapper):
            self._data = value.data
        else:
            self._data = value
    
    def __repr__(self):
        return f'wrapper{{{repr(self._data)}}}'

    def __str__(self):
        return str(self._data)
    
    def __eq__(self, other):
        if isinstance(other, wrapper):
            return self._data == other._data
        return self._data == other
    
    def __getattr__(self, name: str):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
