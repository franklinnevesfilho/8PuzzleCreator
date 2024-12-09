from screen import Screen
import numpy as np 
from PIL import Image
import random 
import heapq




image_paths = create_puzzle_pieces


#Creating the Shuffler
def shuffled_puzzle_pieces(image_paths):
    # Load the images into a list
    images = [Image.open(img_path) for img_path in image_paths]

    # Convert the list into a 2D list (3x3 matrix)
    matrix = np.array(images).reshape(3, 3)

    # Flatten the matrix to a 1D list for shuffling
    flattened_images = matrix.flatten()

    # Shuffle the 1D list
    random.shuffle(flattened_images)

    # Reshape the shuffled images back to a 3x3 matrix
    shuffled_matrix = np.array(flattened_images).reshape(3, 3)
    print(shuffled_matrix)

# A* Algorithm
goal_state = [[create_puzzle_pieces]]

MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = puzzle[i][j]
            if tile != 0:
                
                goal_x, goal_y = divmod(tile - 1, 3)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def find_blank(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return i, j

def get_neighbors(puzzle):
    i, j = find_blank(puzzle)
    neighbors = []
    for direction, (dx, dy) in MOVES.items():
        new_i, new_j = i + dx, j + dy
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            
            new_puzzle = [row[:] for row in puzzle]
           
            new_puzzle[i][j], new_puzzle[new_i][new_j] = new_puzzle[new_i][new_j], new_puzzle[i][j]
            neighbors.append((new_puzzle, direction))
    return neighbors

def a_star(shuffled_puzzle_pieces):
    
    open_list = []
    
    heapq.heappush(open_list, (manhattan_distance(solve_puzzle), 0, solve_puzzle, []))
    

    visited = set()
    visited.add(tuple(tuple(row) for row in solve_puzzle))
    
    while open_list:
       
        f, g, current_puzzle, path = heapq.heappop(open_list)
        
      
        if current_puzzle == goal_state:
            return path
        
    
        for neighbor, direction in get_neighbors(current_puzzle):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                new_g = g + 1
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [direction]))

    return '-1'  



