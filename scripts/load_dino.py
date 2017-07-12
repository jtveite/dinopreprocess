# A skeleton file which imports the dinosaur file specified and provides some useful functions I'll want everywhere
import sys
import numpy as np
import math

fileName = 'slices-68-trimmed.out'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

dinodata = np.loadtxt(fileName)
indices = dinodata[:,0]
paths = dinodata[:,1:]


#Converts a path from list of points (at timesteps) to list of points (evenly distributed along the path)
def rebase_path(path, number_of_steps = 100):
    total_length = get_path_length(path)
    timesteps = int(math.floor(np.shape(paths)[1] / 3))
    newpath = np.empty(number_of_steps * 3)
    current_timestep = 0
    current_distance = 0
    next_timestep_distance = 0
    last_timestep_distance = 0
    for i in range(number_of_steps):
        target_distance = i * total_length / timesteps
        next_timestep = current_timestep + 1
        while next_timestep_distance < target_distance:
            j = next_timestep
            next_timestep +=1
            last_timestep_distance = next_timestep_distance
            dx = path[3*j+3] - path[3*j]
            dy = path[3*j+4] - path[3*j+1]
            dz = path[3*j+5] - path[3*j+2]
            next_timestep_distance += math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        current_timestep = next_timestep - 1
        

#reshapes a path down to the origin
def reshape_to_origin(paths):
    timesteps = int(math.floor(np.shape(paths)[1] / 3))
    for i in range(np.shape(paths)[0]):
        ox = paths[i,0]
        oy = paths[i,1]
        oz = paths[i,2]
        for j in range(timesteps):
            paths[i,3*j] -= ox
            paths[i,3*j+1] -= oy
            paths[i,3*j+2] -= oz
    return paths

def reshape_to_distances(paths):
    timesteps = int(math.floor(np.shape(paths)[1] / 3))
    for i in range(np.shape(paths)[0]):
        ox = paths[i,0]
        oy = paths[i,1]
        oz = paths[i,2]
        for j in range(timesteps - 1):
            paths[i,3*j+3] -= paths[i, 3*j]
            paths[i,3*j+4] -= paths[i, 3*j+1]
            paths[i,3*j+5] -= paths[i, 3*j+2]
    return paths

#filters a matrix of index + paths down
def filter_paths(paths, threshold = 0.01):
    wanted_paths = []
    for i in range(np.shape(paths)[0]):
        if get_path_length(paths[i,1:]) > threshold:
            wanted_paths.append(i)
    return paths[wanted_paths, :]
    
#path is a 1x3n vector
def get_path_length(path):
    l = 0
    lx = path[0]
    ly = path[1]
    lz = path[2]
    for i in range(int(math.floor(len(path) / 3)) - 1): #length/3 because 3 dimensions, -1 because we're looking ahead 1
        dx = path[3*i+3] - path[3*i]
        dy = path[3*i+4] - path[3*i+1]
        dz = path[3*i+5] - path[3*i+2]
        l += math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    return l
    