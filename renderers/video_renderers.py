import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from brots import BrotBase


class VideoInterface(ABC):
    @abstractmethod
    def make_video(self, *args, **kwargs):
        pass


class MatplotVideoJupyterRenderer(VideoInterface):
    def __init__(self):
        pass

    def make_video(self, BrotBase, figsize=(10, 10), cmap="plasma"):
        plt.figure(figsize=(figsize))
        plt.imshow(BrotBase.fetch_array(), cmap=cmap)
        plt.axis("off")
