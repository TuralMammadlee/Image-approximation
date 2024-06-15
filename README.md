## Genetic Algorithm for Image Optimization

This Python project implements a genetic algorithm designed to optimize a image by minimizing the difference between a target image and generated solutions. The algorithm evolves a population of chromosome solutions, each represented as a binary matrix, towards the target image through genetic operations such as selection, crossover, and mutation.

### Features

- **Dynamic Image Input**: Users can input any grayscale image which is then resized to 20x20 pixels for the optimization process.
- **Genetic Operations**: Implements basic genetic operations including selection, crossover, and mutation to evolve the population.
- **Real-time Visualization**: Displays real-time updates of the genetic algorithm's progress, showing both the original target image and the current best solution.
- **Fitness Tracking**: Plots the evolution of the best fitness value across generations, providing insight into the algorithm's performance.

### Usage

1. **Running the Script**:
   - Launch the script via command line or an IDE:
   - When prompted, enter the path to the target grayscale image.

2. **Understanding the Output**:
   - Two images will be displayed side by side in real-time: the original and the current best solution.
   - Every 10 generations, and at the end of the process, the best fitness score will be printed.
   - If a solution with perfect fitness (0 difference from the target) is found, the algorithm will pause for 3 seconds and then terminate.
   - At the end, a plot showing the best fitness per generation will be displayed.
