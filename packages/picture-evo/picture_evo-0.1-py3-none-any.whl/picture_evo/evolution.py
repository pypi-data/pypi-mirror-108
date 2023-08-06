import random

import numpy as np

from picture_evo.species import Specie

import picture_evo.fitness as fitness


class Evolution:
    def __init__(self, size, target, genes=5):
        self.size = size
        self.target = target
        self.generation = 1
        self.genes = genes

        self.specie = Specie(size=self.size, genes=genes)

    def mutate(self, specie):
        new_specie = Specie(size=self.size, genotype=np.array(specie.genotype))

        # 랜덤
        y = random.randint(0, self.genes - 1)
        change = random.randint(0, 6)

        if change >= 6:
            change -= 1
            i, j = y, random.randint(0, self.genes - 1)
            i, j, s = (i, j, -1) if i < j else (j, i, 1)
            new_specie.genotype[i : j + 1] = np.roll(new_specie.genotype[i : j + 1], shift=s, axis=0)
            y = j

        selection = np.random.choice(5, size=change, replace=False)

        if random.random() < 0.25:
            new_specie.genotype[y, selection] = np.random.rand(len(selection))
        else:
            new_specie.genotype[y, selection] += (np.random.rand(len(selection)) - 0.5) / 3
            new_specie.genotype[y, selection] = np.clip(new_specie.genotype[y, selection], 0, 1)

        return new_specie

    def print_progress(self, fit):
        print("GEN {}, FIT {:.8f}".format(self.generation, fit))

    def evolve(self, fitness=fitness.MSEFitness, max_generation=100000):

        fitness = fitness(self.target)

        self.specie.render()
        fit = fitness.score(self.specie.phenotype)

        for i in range(max_generation):
            self.generation = i + 1

            mutated = self.mutate(self.specie)
            mutated.render()
            newfit = fitness.score(mutated.phenotype)

            if newfit > fit:
                fit = newfit
                self.specie = mutated
                self.print_progress(newfit)
