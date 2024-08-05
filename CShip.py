class CShip:
    def __init__(self, size):
        self._size: int = size

    @property
    def size(self) -> int:
        return self._size


class CThreeDeckShip(CShip):
    def __init__(self):
        super().__init__(3)


class CTwoDeckShip(CShip):
    def __init__(self):
        super().__init__(2)


class CSingleDeckShip(CShip):
    def __init__(self):
        super().__init__(1)
