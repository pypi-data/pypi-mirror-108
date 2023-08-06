import random

import numpy as np
import torch


class Randomizer:
    @staticmethod
    def set_seed(seed: int = 9) -> None:
        torch.backends.cudnn.deterministic = True
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)


if __name__ == '__main__':
    Randomizer.set_seed()

