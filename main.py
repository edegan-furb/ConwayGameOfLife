import time
import pygame
import numpy as np

# Define color constants for background, grid, and cells
COLOR_BG = (10, 10, 10)           # Background color (dark gray)
COLOR_GRID = (40, 40, 40)         # Grid color (slightly lighter gray)
COLOR_DIE_NEXT = (170, 170, 170)  # Color for cells that are dying in the next step (light gray)
COLOR_ALIVE_NEXT = (255, 255, 255) # Color for cells that will remain alive in the next step (white)

# Function to count the number of alive cells
def count_alive_cells(cells):
    return np.sum(cells)

# Function to update the grid based on the rules of Conway's Game of Life
def update(screen, cells, size, with_progress=False):
    # Create a new grid to store the updated cell states
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Loop through each cell in the grid
    for row, col in np.ndindex(cells.shape):
        # Count the number of alive neighbors, considering wrap-around edges
        alive = (
            cells[row, (col-1) % cells.shape[1]] +  # Left neighbor
            cells[row, (col+1) % cells.shape[1]] +  # Right neighbor
            cells[(row-1) % cells.shape[0], col] +  # Top neighbor
            cells[(row+1) % cells.shape[0], col] +  # Bottom neighbor
            cells[(row-1) % cells.shape[0], (col-1) % cells.shape[1]] +  # Top-left neighbor
            cells[(row-1) % cells.shape[0], (col+1) % cells.shape[1]] +  # Top-right neighbor
            cells[(row+1) % cells.shape[0], (col-1) % cells.shape[1]] +  # Bottom-left neighbor
            cells[(row+1) % cells.shape[0], (col+1) % cells.shape[1]]    # Bottom-right neighbor
        )
        
        # Determine the color of the current cell based on its state
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT
        
        # Apply Conway's Game of Life rules to determine the cell's future state
        if cells[row, col] == 1:  # Current cell is alive
            if alive < 2 or alive > 3:  # Underpopulation or overpopulation
                if with_progress:
                    color = COLOR_DIE_NEXT  # Change color to indicate dying
            elif 2 <= alive <= 3:  # Stable population
                updated_cells[row, col] = 1  # Keep the cell alive
                if with_progress:
                    color = COLOR_ALIVE_NEXT  # Color indicating the cell remains alive
        else:  # Current cell is dead
            if alive == 3:  # Reproduction
                updated_cells[row, col] = 1  # The cell becomes alive
                if with_progress:
                    color = COLOR_ALIVE_NEXT  # Color indicating the cell becomes alive
        
        # Draw the cell on the screen
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    
    # Return the updated grid
    return updated_cells

# Main function to run the simulation
def main():
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((1400, 700))  # Create a display window of size 1400x700
    
    # Set the initial density of live cells (25% live, 75% dead)
    density = 0.25
    cells = np.random.choice([0, 1], size=(70, 140), p=[1-density, density])
    
    screen.fill(COLOR_GRID)  # Fill the screen with the grid color
    update(screen, cells, 10)  # Draw the initial grid with cells
    
    pygame.display.flip()  # Update the full display surface to the screen
    pygame.display.update()  # Update the display (typically used to update parts of the screen)
    
    running = False  # Variable to control the simulation's run/pause state
    start_time = None  # Variable to store the start time
    elapsed_time = 0  # Variable to store elapsed time
    
    # Main event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                pygame.quit()  # Exit Pygame
                return
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_SPACE:  # Spacebar toggles the running state
                    running = not running
                    if running:
                        start_time = time.time() - elapsed_time  # Resume timing
                    else:
                        elapsed_time = time.time() - start_time  # Pause timing
                    update(screen, cells, 10)  # Update the grid for the new state
                    pygame.display.update()  # Refresh the screen
                elif event.key == pygame.K_c:  # 'C' key clears the grid and resets the time
                    running = False  # Pause the simulation
                    cells = np.zeros((70, 140))  # Reset all cells to dead
                    screen.fill(COLOR_GRID)  # Clear the screen
                    update(screen, cells, 10)  # Update the display with the cleared grid
                    pygame.display.update()  # Refresh the screen
                    elapsed_time = 0  # Reset elapsed time
                    start_time = None  # Reset start time
                elif event.key == pygame.K_r:  # 'R' key repopulates the grid with random values
                    running = False  # Pause the simulation
                    cells = np.random.choice([0, 1], size=(70, 140), p=[1-density, density])
                    screen.fill(COLOR_GRID)  # Clear the screen
                    update(screen, cells, 10)  # Update the display with the new random grid
                    pygame.display.update()  # Refresh the screen
                    elapsed_time = 0  # Reset elapsed time
                    start_time = None  # Reset start time
            if pygame.mouse.get_pressed()[0]:  # If the left mouse button is pressed
                pos = pygame.mouse.get_pos()  # Get the mouse position
                row, col = pos[1] // 10, pos[0] // 10  # Convert mouse position to grid coordinates
                cells[row, col] = 1 - cells[row, col]  # Toggle the cell's state (alive <-> dead)
                update(screen, cells, 10)  # Update the grid with the new cell state
                pygame.display.update()  # Refresh the screen
        
        screen.fill(COLOR_GRID)  # Clear the screen before the next update
        
        if running:  # If the simulation is running
            cells = update(screen, cells, 10, with_progress=True)  # Update the grid for the next step
            pygame.display.update()  # Refresh the screen
            elapsed_time = time.time() - start_time  # Update elapsed time
        
        # Update the window title with the number of alive cells and elapsed time
        alive_count = int(count_alive_cells(cells))
        elapsed_time_display = int(elapsed_time)  # Convert elapsed time to integer seconds
        pygame.display.set_caption(f"Conway's Game of Life - Alive Cells: {alive_count} - Time: {elapsed_time_display} s ")
        
        time.sleep(0.05)  # Delay to control the speed of the simulation

# Entry point of the program
if __name__ == '__main__':
    main()  # Call the main function to start the simulation
