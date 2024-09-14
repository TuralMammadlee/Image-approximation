import random
import copy
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time 

def prompt_for_image_name():
    return input('Enter the image name: ')

class GeneticSettings:
    def __init__(self):
        self.GENE_COUNT = 400
        self.MUT_PROB = 0.002
        self.POP_SIZE = 600
        self.ELITE_COUNT = 20
        self.CROSS_PROB = 0.95
        self.FITNESS_TYPE = "min" 
        self.image_name = prompt_for_image_name()
        self.target_image = self.load_image()

    def load_image(self):
        image = cv2.imread(self.image_name, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError("The specified image could not be loaded.")
        image = cv2.resize(image, (20, 20))
        image = np.where(image > 128, 1, 0)
        return image.flatten()

class Chromosome:
    def __init__(self, gene_count):
        self.genes = [random.randint(0, 1) for _ in range(gene_count)]
        self.fitness = float('inf') 

    def mutate(self, mutation_prob):
        for i in range(len(self.genes)):
            if random.random() <= mutation_prob:
                self.genes[i] = 1 - self.genes[i]  

class Population:
    def __init__(self, size, gene_count):
        self.chromosomes = [Chromosome(gene_count) for _ in range(size)]
        self.best_fitness_history = []  

    def evolve(self, generations, config, fitness_function, step_execution=None):
        plt.ion() 
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for generation in range(generations):
            for chromosome in self.chromosomes:
                chromosome.fitness = fitness_function(chromosome.genes, config.target_image)

            self.selection(config.ELITE_COUNT)
            self.crossover(config.POP_SIZE, config.CROSS_PROB, config.GENE_COUNT)
            self.mutation(config.MUT_PROB)

            if step_execution:
                step_execution(self.chromosomes[0], config.target_image, fig, axes)

            best_fitness = min(chromo.fitness for chromo in self.chromosomes)
            self.best_fitness_history.append(best_fitness) 

            if generation % 10 == 0 or generation == generations - 1:
                print(f"Generation {generation}: Best Fitness = {best_fitness}")

            if best_fitness == 0:
                print("Best fitness is 0. Ending evolution.")
                plt.ioff()  
                plt.show()
                time.sleep(3) 
                break 

        plt.ioff() 
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(self.best_fitness_history, label='Best Fitness per Generation')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Evolution of Best Fitness')
        plt.legend()
        plt.grid(True)
        plt.show()

    def selection(self, elite_count):
        self.chromosomes.sort(key=lambda x: x.fitness)
        self.chromosomes = self.chromosomes[:elite_count]

    def crossover(self, pop_size, cross_prob, gene_count):
        next_generation = []
        while len(next_generation) < pop_size:
            parent1, parent2 = random.sample(self.chromosomes, 2)
            if random.random() <= cross_prob:
                crossover_point = random.randint(1, gene_count - 1)
                child1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
                child2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
                next_generation.extend([Chromosome(gene_count) for _ in range(2)])
                next_generation[-2].genes, next_generation[-1].genes = child1_genes, child2_genes
            else:
                next_generation.extend(copy.deepcopy([parent1, parent2]))
        self.chromosomes = next_generation[:pop_size]

    def mutation(self, mut_prob):
        for chromosome in self.chromosomes:
            chromosome.mutate(mut_prob)

def display_chromosome(chromo, target_image, fig, axes):
    image = np.array(chromo.genes).reshape(20, 20) * 255
    original = target_image.reshape(20, 20) * 255

    axes[0].clear()
    axes[1].clear()

    axes[0].imshow(original, cmap='gray')
    axes[0].title.set_text('Original Image')
    axes[0].axis('off')

    axes[1].imshow(image, cmap='gray')
    axes[1].title.set_text('Evolved Image')
    axes[1].axis('off')

    plt.draw()
    plt.pause(0.1)  
def fitness_function(genes, target_image):
   
    return sum((gene - pixel) ** 2 for gene, pixel in zip(genes, target_image))


# Initialize and run the genetic algorithm
config = GeneticSettings()
population = Population(config.POP_SIZE, config.GENE_COUNT)
population.evolve(300, config, fitness_function, display_chromosome)

