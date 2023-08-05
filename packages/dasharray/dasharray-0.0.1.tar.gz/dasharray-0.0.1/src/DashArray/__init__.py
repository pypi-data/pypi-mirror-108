class _(list):
    def get(self, index, default="Index Out of Range"):
        try:
            return self[index]
        except IndexError:
            return default
