import matplotlib.pyplot as plt


class StaticRenderer:
    def __init__(self, figsize=(10, 10)):
        self.figsize = figsize

    def plot(self, brot, figsize=(10, 10), cmap="plasma"):
        plt.figure(figsize=(figsize))
        plt.imshow(brot.fetch_array(), cmap=cmap)
        plt.axis("off")
