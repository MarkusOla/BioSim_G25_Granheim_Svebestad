# -*- coding: utf-8 -*-

"""
"""

__author__ = "Markus Ola Granheim & Rasmus Svebestad"
__email__ = "mgranhei@nmbu.no & rasmus.svebestad@nmbu.no"


from biosim.rossum import Island
from biosim.rossum_to import Animal, Herbivores, Carnivores
import numpy as np


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.ini_pop = ini_pop
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.island_map = island_map
        self.island = Island(island_map)
        self.island.limit_map_vals()
        self.herbivores = Herbivores()
        self.carnivores = Carnivores()
        self.animal = Animal()
        np.random.seed(seed)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            self.herbivores.set_new_params(params)
        else:
            self.carnivores.set_new_params(params)

    def set_landscape_parameters(self, params):
        """
        Set parameters for landscape type.

        :param params: Dict with valid parameter specification for landscape
        """
        self.island.set_new_params(params)

    def setup_simulation(self):
        for i in range(self.island.rader):
            for j in range(self.island.col):
                self.island.set_food((i, j))
        self.island.add_animals(self.ini_pop)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        for year in range(num_years):
            for i in range(self.island.rader):
                for j in range(self.island.col):
                    pos = (i, j)
                    self.island.grow_food(pos)
                    self.herbivores.calculate_fitness(pos, self.island.herbs)
                    self.herbivores.calculate_fitness(pos, self.island.herbs)
                    self.herbivores.sort_by_fitness(pos, self.island.herbs)
                    self.herbivores.animals_eat(pos, self.island, self.island.herbs)
                    self.herbivores.sort_before_getting_hunted(pos, self.island.herbs)
                    self.carnivores.calculate_fitness(pos, self.island.carns)
                    self.carnivores.sort_by_fitness(pos, self.island.carns)
                    self.carnivores.carnivores_eat(pos, self.island, self.island.carns)
                    self.herbivores.breeding(pos, self.island, self.island.herbs)
                    self.carnivores.breeding(pos, self.island, self.island.carns)
                    self.herbivores.calculate_fitness(pos, self.island.herbs)
                    self.carnivores.calculate_fitness(pos, self.island.carns)
            self.herbivores.migration_calculations(self.island.rader, self.island.col,
                                                   self.island, self.island.herbs)
            self.carnivores.migration_calculations(self.island.rader, self.island.col,
                                                   self.island, self.herbivores, self.island.carns)
            self.herbivores.migration_execution(self.island, self.island.herbs)
            self.carnivores.migration_execution(self.island, self.island.carns)
            for i in range(self.island.rader):
                for j in range(self.island.col):
                    pos = (i, j)
                    self.herbivores.aging(pos, self.island.herbs)
                    self.carnivores.aging(pos, self.island.carns)
                    self.herbivores.loss_of_weight(pos, self.island.herbs)
                    self.carnivores.loss_of_weight(pos, self.island.carns)
                    self.herbivores.calculate_fitness(pos, self.island.herbs)
                    self.carnivores.calculate_fitness(pos, self.island.carns)
                    self.herbivores.death(pos, self.island.herbs)
                    self.carnivores.death(pos, self.island.carns)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.add_animals(population)

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == "__main__":
    herbivores = [{'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 20, 'weight': 17.3},
                                          {'species': 'Herbivore', 'age': 30, 'weight': 19.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 20, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 30, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 10.3}
                                          ]},
                  {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 3, 'weight': 10},
                  {'species': 'Herbivore', 'age': 4, 'weight': 9},
                  {'species': 'Herbivore', 'age': 5, 'weight': 10}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 1000, 'weight': 1000000.3}]}]
    carnivores = [{'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 20.3}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 20.3}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 20.3}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 20.3}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 20.3}]},
                  {'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 1, 'weight': 25.3}]}]
    seed = 2
    a = BioSim("OOOOO\nOJJJO\nOJJOO\nOJJJO\nOJJJO\nOOOOO", ini_pop=herbivores, seed=seed)
    a.setup_simulation()
    a.simulate(40)
    a.add_population(carnivores)
    a.simulate(60)
    print(a.island.herbs)
    print(len(a.island.herbs[(3, 3)]))
    print(len(a.island.carns[(3, 3)]))
    print(a.island.carns)
