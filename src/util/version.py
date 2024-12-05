class version:
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0, build: int = 0):
        self._major = major
        self._minor = minor
        self._patch = patch
        self._build = build
    
    @property
    def major(self) -> int:
        return self._major
    
    @major.setter
    def major(self, value: int):
        self._major = value
    
    @property
    def minor(self) -> int:
        return self._minor
    
    @minor.setter
    def minor(self, value: int):
        self._minor = value
    
    @property
    def patch(self) -> int:
        return self._patch
    
    @patch.setter
    def patch(self, value):
        self._patch = value
    
    @property
    def build(self) -> int:
        return self._build
    
    @build.setter
    def build(self, value):
        self._build = value
    
    def __str__(self) -> str:
        return f"{self._major}.{self._minor}.{self._patch}.{self._build}"
    
    def __repr__(self) -> str:
        return f"version{{major={self._major}, minor={self._minor}, patch={self._patch}, build={self._build}}}"
    
    def __eq__(self, other: 'version') -> bool:
        return self._major == other._major and \
               self._minor == other._minor and \
               self._patch == other._patch and \
               self._build == other._build
    
    def __lt__(self, other: 'version') -> bool:
        if self._major != other._major:
            return self._major < other._major
        if self._minor != other._minor:
            return self._minor < other._minor
        if self._patch != other._patch:
            return self._patch < other._patch
        return self._build < other._build
    
    def __le__(self, other: 'version') -> bool:
        return self == other or self < other
    
    def __gt__(self, other: 'version') -> bool:
        return not self <= other
    
    def __ge__(self, other: 'version') -> bool:
        return not self < other
