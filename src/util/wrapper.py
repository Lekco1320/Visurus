class Wrapper:
    def __init__(self, data: object = None) -> None:
        if isinstance(data, Wrapper):
            self._data = data.data
        else:
            self._data = data
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if isinstance(value, Wrapper):
            self._data = value.data
        else:
            self._data = value
    
    def set(self, value):
        self.data = value
    
    def get(self):
        return self.data
    
    def __repr__(self):
        return f'wrapper{{{repr(self._data)}}}'

    def __str__(self):
        return str(self._data)
    
    def __eq__(self, other):
        if isinstance(other, Wrapper):
            return self._data == other._data
        return self._data == other
    
    def __getattr__(self, name: str):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

__all__ = ["Wrapper"]
