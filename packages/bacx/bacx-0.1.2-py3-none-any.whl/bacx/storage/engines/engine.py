class StorageEngine:
    """ """

    def __init__(self, link: str = None, cache_path: str = None, other: dict = None, remote: dict = None):
        self._link = link
        self._cache_path = cache_path
        self._other = other
        self._remote = remote
