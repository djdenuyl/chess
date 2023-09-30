class ReversibleDict(dict):
    @property
    def reverse(self):
        return {v: k for k, v in self.items()}
