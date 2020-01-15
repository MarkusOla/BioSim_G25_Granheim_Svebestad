# -*- coding: utf-8 -*-

"""
This file will test the rossum.py-file
"""

__author__ = "Markus Ola Granheim & Rasmus Svebestad"
__email__ = "mgranhei@nmbu.no & rasmus.svebestad@nmbu.no"

from biosim.rossum import Island, Herbivores, Carnivores, Fodder
import pytest
import numpy as np


class TestIsland:
    def test_island_call(self):
        """Default constructor callable"""
        a = Island()
        assert isinstance(a, Island)

    def test_perimeter_error(self):
        """Testing if ValueError is raised when the perimeter contains something other than ocean"""
        a = "OOO\nOJJ\nOOO"
        aa = Island(a)
        with pytest.raises(ValueError):
            aa.limit_map_vals()

    def test_unvalid_terrain_error(self):
        """Tests if the map input contains unvalid terrain-types"""
        a = "OOO\nOWO\nOOO"
        aa = Island(a)
        with pytest.raises(ValueError):
            aa.limit_map_vals()

    def test_unvaild_type(self):
        """Tests if the code raises TypeError if the map input is not a string"""
        a = [['O', 'O', 'O'], ['O', 'J', 'O'], ['O', 'O', 'O']]
        with pytest.raises(TypeError):
            Island(a)

    def test_output_np_array(self):
        """Tests if the output map is right, when input has no error"""
        a = "OOO\nOJO\nOOO"
        aa = Island(a)
        el_map = [['O', 'O', 'O'], ['O', 'J', 'O'], ['O', 'O', 'O']]
        assert np.array_equal(aa.fetch_map(), el_map)

    def test_return_neturtype(self):
        a = "OOO\nOJO\nOOO"
        aa = Island(a)
        pos = (0, 0)
        assert aa.fetch_naturetype(pos) == 'O'


class TestSavannah:
    def test_savannah_call(self):
        """Default constructor callable"""
        a = Savannah()
        assert isinstance(a, Savannah)

    def test_default_values(self):
        a = Savannah()
        assert a.fsav_max == 300
        assert a.alpha == 0.3

    def test_values(self):
        a = Savannah(fsav_max=200, alpha=0.4)
        assert a.fsav_max == 200
        assert a.alpha == 0.4

    def test_set_food(self):
        a = Savannah(fsav_max=300)
        a.set_food((1, 3))
        assert a.food == {(1, 3): 300}

    def test_set_more_food(self):
        a = Savannah(fsav_max=300)
        for i in range(3):
            for j in range(3):
                a.set_food((i, j))
        assert a.food[(0, 2)] == 300
        assert a.food[(1, 1)] == 300

    def test_grow_food(self):
        a = Savannah(fsav_max=300, alpha=0.3)
        a.set_food((1, 1))
        a.grow_food((1, 1))
        assert a.food[1, 1] == (300 + 0.3 * (300 - 300))

    def test_multiple_grow_food(self):
        a = Savannah()
        for i in range(3):
            for j in range(3):
                a.set_food((i, j))
        for i in range(3):
            for j in range(3):
                a.grow_food((i, j))
        assert a.food[0, 0] == (300 + 0.3 * (300 - 300))
        assert a.food[1, 1] == (300 + 0.3 * (300 - 300))
        assert a.food[2, 2] == (300 + 0.3 * (300 - 300))
        assert a.food[1, 2] == (300 + 0.3 * (300 - 300))

    def test_food_gets_eaten_with_less_food(self):
        a = Savannah(fsav_max=0)
        b = Savannah(fsav_max=5)
        c = Savannah()
        a.set_food((1, 1))
        b.set_food((1, 2))
        c.set_food((2, 2))
        aa = a.food_gets_eaten((1, 1))
        bb = b.food_gets_eaten((1, 2))
        cc = c.food_gets_eaten((2, 2))
        assert aa == 0
        assert a.food[(1, 1)] == 0
        assert bb == 5
        assert b.food[(1, 2)] == 0
        assert cc == 10
        assert c.food[(2, 2)] == 290


class TestAnimals:
    def test_add_animals_simple(self):
        added_list = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}]
        a = BaseAnimals()
        a.add_animal(added_dict)
        assert a.herbs == {(3, 1): [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}

    def test_add_animals_both(self):
        added_list = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]},
                      {'loc': (3, 1), 'pop': [{'species': 'Carnivore', 'age': 0.1, 'Weight': 1.3}]}]
        a = BaseAnimals()
        a.add_animal(added_dict)
        assert a.herbs == {(3, 1): [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}
        assert a.carns == {(3, 1): [{'species': 'Carnivore', 'age': 0.1, 'Weight': 1.3}]}

    def test_add_complex_list(self):
        added_list = [{'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 20, 'weight': 17.3},
                                          {'species': 'Herbivore', 'age': 30, 'weight': 19.3},
                                          {'species': 'Herbivore', 'age': 10, 'weight': 107.3}]},
                      {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 3, 'weight': 10},
                      {'species': 'Herbivore', 'age': 4, 'weight': 9},
                      {'species': 'Herbivore', 'age': 5, 'weight': 10}]},
                      {'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 1000, 'weight': 1000000.3},
                                              {'species': 'Carnivore', 'age': 1, 'weight': 20.3},
                                              {'species': 'Carnivore', 'age': 1, 'weight': 0.3}]}]
        a = BaseAnimals()
        a.add_animal(added_list)
        assert len(a.herbs[(3, 3)]) == 4
        assert len(a.carns[(3, 3)]) == 2

    def test_aging(self):
        added_list = [{'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 20, 'weight': 17.3},
                                              {'species': 'Herbivore', 'age': 30, 'weight': 19.3},
                                              {'species': 'Herbivore', 'age': 10, 'weight': 107.3},
                                              {'species': 'Carnivore', 'age': 1, 'weight': 20.3}]}]
        a = BaseAnimals()
        a.add_animal(added_list)
        a.aging((3,3))
        assert a.herbs[(3,3)][0]['age'] == 21
        assert a.herbs[(3, 3)][1]['age'] == 31
        assert a.herbs[(3, 3)][2]['age'] == 11
        assert a.carns[(3, 3)][0]['age'] == 2


class TestHerbivores:
    def test_herbivores_call(self):
        """Default constructor callable"""
        a = Herbivores()
        assert isinstance(a, Herbivores)

    def test_default_values(self):
        a = Herbivores()
        assert a.w_birth == 8.0
        assert a.sigma_birth == 1.5
        assert a.beta == 0.9
        assert a.eta == 0.05
        assert a.a_half == 40.0
        assert a.phi_age == 0.2
        assert a.w_half == 10.0
        assert a.phi_weight == 0.1
        assert a.mu == 0.25
        assert a.lambda1 == 1.0
        assert a.gamma == 0.2
        assert a.zeta == 3.5
        assert a.xi == 1.2
        assert a.omega == 0.4

    def test_set_values(self):
        a = Herbivores(w_birth=34, sigma_birth=12)
        assert a.w_birth == 34
        assert a.sigma_birth == 12

    def test_add_animals_simple(self):
        added_dict = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}]
        a = Herbivores()
        a.add_animal(added_dict)
        assert a.herbs == {(3, 1): [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}

    def test_add_animals_twice(self):
        added_dict = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}]
        a = Herbivores()
        a.add_animal(added_dict)
        a.add_animal(added_dict)
        assert a.herbs == {(3, 1): [{'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3},
                                    {'species': 'Herbivore', 'age': 0.1, 'Weight': 1.3}]}

    def test_add_multiple_animals(self):
        added_dict = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 16, 'Weight': 1356.3},
                                              {'species': 'Herbivore', 'age': 113, 'Weight': 1323}]}]
        added_list = [{'loc': (3, 3), 'pop': [{'species': 'Herbivore', 'age': 12, 'Weight': 21.3},
                                              {'species': 'Herbivore', 'age': 123, 'Weight': 321.3}]},
                      {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 166, 'Weight': 135.3},
                                              {'species': 'Herbivore', 'age': 11, 'Weight': 323}]}]
        a = Herbivores()
        a.add_animal(added_dict)
        a.add_animal(added_list)
        assert a.herbs[(3, 1)] == [{'species': 'Herbivore', 'age': 16, 'Weight': 1356.3},
                                   {'species': 'Herbivore', 'age': 113, 'Weight': 1323},
                                   {'species': 'Herbivore', 'age': 166, 'Weight': 135.3},
                                   {'species': 'Herbivore', 'age': 11, 'Weight': 323}]
        assert a.herbs[(3, 3)] == [{'species': 'Herbivore', 'age': 12, 'Weight': 21.3},
                                   {'species': 'Herbivore', 'age': 123, 'Weight': 321.3}]

    def test_calculate_fitness(self):
        added_list = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 1.3},
                                              {'species': 'Carnivore', 'age': 1, 'weight': 1.3}]}]
        b = Herbivores()
        b.add_animal(added_list)
        b.calculate_fitness((3, 1))
        assert abs(b.herbs[(3, 1)][0]['fitness'] - 0.2951333) < 0.001

    def test_sort_by_fitness(self):
        added_list1 = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.3}]},
                       {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 16}]}]
        added_list2 = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 16}]},
                       {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.3}]}]
        a = Herbivores()
        b = Herbivores()
        a.add_animal(added_list1)
        a.calculate_fitness((3, 1))
        a.sort_by_fitness((3, 1))
        b.add_animal(added_list2)
        b.calculate_fitness((3, 1))
        b.sort_by_fitness((3, 1))
        assert a.herbs[(3, 1)][0]['fitness'] >= a.herbs[(3, 1)][1]['fitness']
        assert b.herbs[(3, 1)][0]['fitness'] >= b.herbs[(3, 1)][1]['fitness']

    def test_animals_eat(self):
        added_list1 = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.3}]}]
        a = Herbivores()
        b = Fodder()
        c = Island("OOOOO\nOSSSO\nOJJJO\nOSSJO\nOSSSO\nOOOOO")
        b.set_food(pos=(3, 1), isle_class=c)
        a.add_animal(added_list1)
        abc = a.herbs[(3, 1)][0]['weight']
        a.animals_eat((3, 1), b)
        assert abc < a.herbs[(3, 1)][0]['weight']

    def test_breeding(self):
        population = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 3, 'weight': 29.3},
                                              {'species': 'Herbivore', 'age': 12, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 3, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 5, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 6, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 7, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 8, 'weight': 27.3},
                                              {'species': 'Herbivore', 'age': 9, 'weight': 27.3}
                                              ]}]
        a = Herbivores(seed=3)
        b = Fodder()
        c = Island("OOOOO\nOSSSO\nOJJJO\nOSSJO\nOSSSO\nOOOOO")
        b.set_food((3, 1), c)
        a.add_animal(population)
        a.animals_eat((3, 1), b)
        len_list1 = len(a.herbs[(3, 1)])
        a.calculate_fitness((3, 1))
        a.breeding((3, 1))
        len_list2 = len(a.herbs[(3, 1)])
        assert len_list2 > len_list1

    def test_aging(self):
        population = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.3}]},
                      {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 16}]}]
        a = Herbivores()
        a.add_animal(population)
        a.aging((3, 1))
        assert a.herbs[(3, 1)][0]['age'] == 2
        assert a.herbs[(2, 2)][0]['age'] == 6
        a.aging((2, 2))
        assert a.herbs[(2, 2)][0]['age'] == 7

    def test_loss_of_weight(self):
        population = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 10.3}]},
                      {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 16}]}]
        a = Herbivores()
        a.add_animal(population)
        a0 = a.herbs[(3, 1)][0]['weight']
        a1 = a.herbs[(3, 1)][1]['weight']
        a.loss_of_weight((3, 1))
        assert a0 > a.herbs[(3, 1)][0]['weight']
        assert a1 > a.herbs[(3, 1)][1]['weight']

    def test_death(self):
        population = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 10000, 'weight': 10.3}]},
                      {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 60000, 'weight': 0}]}]
        a = Herbivores()
        a.add_animal(population)
        a.calculate_fitness((3, 1))
        initial_len = len(a.herbs[(3, 1)])
        a.death((3, 1))
        assert len(a.herbs[(3, 1)]) < initial_len

    def test_migration_calculation(self):
        population = [{'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 13.3}]},
                      {'loc': (3, 1), 'pop': [{'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10},
                                              {'species': 'Herbivore', 'age': 4, 'weight': 10}]}]
        a = Island("OOOOO\nOOOOO\nOJOOO\nOJOOO\nOOOOO\nOOOOO")
        b = Herbivores(seed=1)
        c = Fodder()
        b.add_animal(population)
        c.set_food((3, 1), a)
        c.set_food((2, 1), a)
        c.set_food((3, 2), a)
        c.set_food((3, 0), a)
        c.set_food((4, 1), a)
        b.calculate_fitness((3, 1))
        b.migration_calculations(a.rader, a.col, a, c)
        assert len(b.herbs[(3, 1)]) == 9
        assert len(b.idx_for_animals_to_remove) > 0
        print(b.idx_for_animals_to_remove)
        print((sorted(b.idx_for_animals_to_remove, reverse=True)))
        print(b.animals_with_new_pos)
        b.migration_execution()
        assert len(b.herbs[(3,1)]) == 7
        assert len(b.herbs[(2,1)]) == 2