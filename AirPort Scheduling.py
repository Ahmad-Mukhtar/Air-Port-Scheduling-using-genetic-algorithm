import random

# 18L-0950
# 18L-1028
# 18L-1035
# 18L-1079

POPULATION_SIZE = 1000

GENES = '01'

Pheno_Type = {'Monday': {'12-3': ['100', '101', '110'], '3-6': ['001', '010', '111'], '6-9': ['000', '101', '110']},
              'Tuesday': {'12-3': ['011', '100', '001'], '3-6': ['010', '101', '111'], '6-9': ['000', '011', '110']},
              'Wednesday': {'12-3': ['100', '001', '111'], '3-6': ['010', '101', '000'], '6-9': ['100', '011', '110']},
              'Thursday': {'12-3': ['000', '010', '001'], '3-6': ['100', '101', '110'], '6-9': ['010', '111', '001']},
              'Friday': {'12-3': ['000', '101', '010'], '3-6': ['100', '110', '011'], '6-9': ['000', '001', '010']}}


class AirPort_Scheduling(object):

    def __init__(self, chromosome):
        self.Chromosome = chromosome
        self.fitness = self.cal_fitness()

    def create_gene(self):
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_chromosome(self):
        Chromosome = {'Monday': {'12-3': [], '3-6': [], '6-9': []},
                      'Tuesday': {'12-3': [], '3-6': [], '6-9': []},
                      'Wednesday': {'12-3': [], '3-6': [], '6-9': []},
                      'Thursday': {'12-3': [], '3-6': [], '6-9': []},
                      'Friday': {'12-3': [], '3-6': [], '6-9': []}}
        Days = list(Chromosome.keys())
        Time = list(list(Chromosome.values())[0].keys())
        Total_Runways = 3
        for day in Days:
            for t in Time:
                for _ in range(Total_Runways):
                    val = self.create_gene(self) + self.create_gene(self) + self.create_gene(self)
                    Chromosome.get(day).get(t).append(val)

        return Chromosome

    def produce_offspring(self, Second_Chromosome):

        Days = list(self.Chromosome.keys())
        child_chromosome = {}

        for Day in Days:
            prob = random.random()

            if prob < 0.45:
                child_chromosome[Day] = self.Chromosome.get(Day)


            elif prob < 0.90:

                child_chromosome[Day] = Second_Chromosome.Chromosome.get(Day)

            else:
                muatated_chromosome = self.create_chromosome()
                child_chromosome[Day] = muatated_chromosome.get(Day)

        # create new Individual(offspring) using
        # generated chromosome for offspring
        return AirPort_Scheduling(child_chromosome)

    def cal_fitness(self):

        global Pheno_Type
        fitness = 0
        Days = list(self.Chromosome.keys())
        Time = list(list(self.Chromosome.values())[0].keys())
        for day in Days:
            for t in Time:
                temp_list = self.Chromosome.get(day).get(t)
                target_list = Pheno_Type.get(day).get(t)

                for val, target in zip(temp_list, target_list):
                    for i in range(len(val)):
                        if val[i] != target[i]:
                            fitness += 1

        return fitness


def create_schduling():
    global POPULATION_SIZE

    # current generation
    generation = 1

    found = False
    population = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        gnome = AirPort_Scheduling.create_chromosome()
        population.append(AirPort_Scheduling(gnome))

    while not found:

        population = sorted(population, key=lambda x: x.fitness)

        if population[0].fitness <= 0:
            found = True
            break

        new_generation = []
        new_generation.extend(population[:100])
        s = 900
        for _ in range(s):
            parent1 = random.choice(population[:500])
            parent2 = random.choice(population[:500])
            child = parent1.produce_offspring(parent2)
            new_generation.append(child)

        population = new_generation

        print("Generation: {}\tTimeTable: {}\tFitness: {}".format(generation, population[0].Chromosome,
                                                                  population[0].fitness))

        generation += 1

    print(
        "Generation: {}\TimeTable: {}\tFitness: {}".format(generation, population[0].Chromosome, population[0].fitness))


create_schduling()
