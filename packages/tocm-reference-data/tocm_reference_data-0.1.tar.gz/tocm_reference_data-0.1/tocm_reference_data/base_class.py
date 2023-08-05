class Reference():
    
    metadata = {}

    def __init__(self, metadata: dict, figures: list):
        self.metadata.update(metadata)

        for fig in figures:
            setattr(self, fig.name, fig)


class Figure():
    """
    This is the base class for figure data.
    """
    def __init__(self, name: str, lines: list):
        self.name = name
        self.lines = lines


class Line():
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label