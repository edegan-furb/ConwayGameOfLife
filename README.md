# Conway's Game of Life Simulation

This project is a simulation of Conway's Game of Life using Python with the Pygame library. It visualizes the cellular automaton on a grid and allows for interactive manipulation of cells. The game rules and simulation can be controlled through keyboard and mouse inputs.

## Requirements

- Python 3.x
- Pygame
- NumPy

You can install the required packages using pip:

```bash
pip install pygame numpy
```

## How It Works

### Game of Life Rules

Conway's Game of Life is a zero-player game where the evolution of cells is determined by the following rules:

1. Any live cell with fewer than two live neighbors dies as if caused by under-population.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by over-population.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

### Simulation Controls

- Spacebar: Toggle the simulation between running and paused states.
- C key: Clear the grid, setting all cells to dead.
- Left Mouse Button: Toggle the state of a cell (alive or dead) by clicking on the grid.

### Running the Simulation
To run the simulation, execute the script:

  ```bash
python main.py
```

The Pygame window will open, displaying the grid and the current state of the cells.

## Code Overview

- **update(screen, cells, size, with_progress=False)** : Updates the grid based on Conway's Game of Life rules and draws the cells on the screen.

- **main()** : Initializes Pygame, sets up the display window, and handles the main event loop for user interactions and simulation updates.
