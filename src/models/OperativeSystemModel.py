class OperativeSystem():

    def __init__(self, id, name, version) -> None:
        self.id = id
        self.name = name
        self.version = version
        self.enabled = True

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'enabled': self.enabled
        }