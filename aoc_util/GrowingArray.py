import numpy as np


class GrowingArray:
    def __init__(self, row_strs, on_char, dimensions):
        self.dimensions = dimensions
        # Define grid of 1s / 0s based on whether or not it matches the specified "on" character
        if self.dimensions == 3:
            self.grid = np.array([[[int(cell == on_char) for cell in row] for row in row_strs]], dtype=np.int8)
        elif self.dimensions == 4:
            self.grid = np.array([[[[int(cell == on_char) for cell in row] for row in row_strs]]], dtype=np.int8)

    def grow(self, activate_counts, remain_active_counts):
        if self.dimensions == 3:
            self.grow_3d(activate_counts, remain_active_counts)
        elif self.dimensions == 4:
            self.grow_4d(activate_counts, remain_active_counts)

    def grow_3d(self, activate_counts, remain_active_counts):
        # Pad the array to allow for growing dimensions
        self.grid = np.pad(self.grid, 1, mode='constant')

        # Duplicate the array to avoid issues modifying while iterating
        new_grid = self.grid.copy()

        # Iterate over the new grid and handle switching on / off
        for k in range(new_grid.shape[0]):
            for j in range(new_grid.shape[1]):
                for i in range(new_grid.shape[2]):
                    neighbors = self.grid[
                                max(k - 1, 0): min(k + 2, new_grid.shape[0]),
                                max(j - 1, 0): min(j + 2, new_grid.shape[1]),
                                max(i - 1, 0): min(i + 2, new_grid.shape[2])
                                ]
                    neighbor_count = np.count_nonzero(neighbors)
                    if self.grid[k][j][i] and neighbor_count - 1 not in remain_active_counts:
                        new_grid[k][j][i] = 0
                    elif not self.grid[k][j][i] and neighbor_count in activate_counts:
                        new_grid[k][j][i] = 1

        # Store new grid
        self.grid = new_grid

    def grow_4d(self, activate_counts, remain_active_counts):
        # Pad the array to allow for growing dimensions
        self.grid = np.pad(self.grid, 1, mode='constant')

        # Duplicate the array to avoid issues modifying while iterating
        new_grid = self.grid.copy()

        # Iterate over the new grid and handle switching on / off
        for l in range(new_grid.shape[0]):
            for k in range(new_grid.shape[1]):
                for j in range(new_grid.shape[2]):
                    for i in range(new_grid.shape[3]):
                        neighbors = self.grid[
                                    max(l - 1, 0): min(l + 2, new_grid.shape[0]),
                                    max(k - 1, 0): min(k + 2, new_grid.shape[1]),
                                    max(j - 1, 0): min(j + 2, new_grid.shape[2]),
                                    max(i - 1, 0): min(i + 2, new_grid.shape[3])
                                    ]
                        neighbor_count = np.count_nonzero(neighbors)
                        if self.grid[l][k][j][i] and neighbor_count - 1 not in remain_active_counts:
                            new_grid[l][k][j][i] = 0
                        elif not self.grid[l][k][j][i] and neighbor_count in activate_counts:
                            new_grid[l][k][j][i] = 1

        # Store new grid
        self.grid = new_grid

    def count_on(self):
        return np.count_nonzero(self.grid)
