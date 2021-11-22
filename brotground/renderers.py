import matplotlib.pyplot as plt


class MatplotJupyterRenderer:
    def __init__(self):
        pass

    def plot(self, brot, figsize=(10, 10), cmap="plasma"):
        plt.figure(figsize=(figsize))
        plt.imshow(brot.fetch_array(), cmap=cmap)
        plt.axis("off")