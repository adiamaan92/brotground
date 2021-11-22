import matplotlib.pyplot as plt

from brotground.BrotBase import BrotBase


class MatplotJupyterRenderer:
    def __init__(self):
        pass

    def plot(self, brot: BrotBase, figsize=(10, 10), cmap="plasma"):
        plt.figure(figsize=(figsize))
        plt.imshow(brot.fetch_array(), cmap=cmap)
        plt.axis("off")
