import numpy as np

from skimage.metrics import structural_similarity as ss


class Fitness:
    def __init__(self, target):

        self.target = target

    def score(self, phenotype):
        raise NotImplementedError


class MSEFitness(Fitness):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_error = (np.square((1 - (self.target >= 127)) * 255 - self.target)).mean(axis=None)

    def score(self, phenotype):
        fit = (np.square(phenotype - self.target)).mean(axis=None)
        fit = (self._max_error - fit) / self._max_error
        return fit


class SSFitness(Fitness):
    def score(self, phenotype):
        fit = ss(phenotype, self.target)
        return fit
