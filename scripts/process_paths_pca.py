
# coding: utf-8

# In[1]:

import scipy as sp
import numpy as np
from sklearn import decomposition
from sklearn import cluster
import math
import sys
    
    
def load_dinosaur_data(fileName):
    dinodata = np.loadtxt(fileName)
    indices = dinodata[:,0]
    paths = dinodata[:,1:]
    return (dinodata, indices, paths)



#filters a matrix of index + paths down
def filter_paths(paths, threshold = 0.01):
    wanted_paths = []
    for i in range(np.shape(paths)[0]):
        if get_path_length(paths[i,1:]) > threshold:
            wanted_paths.append(i)
    print("Started with {}, ended with {} after threshold of {}.".format(np.shape(paths)[0], len(wanted_paths), threshold))
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

# In[3]:
# dinodata contains full data
# threshold is motion threshold
# rezero positions all paths at the origin
# rebase - represent paths by arclength
# rebase_resolution - number of increments to divide the path into

# outs
# 0 - indices
# 1 - paths

def filter_and_reshape_paths(dinodata, threshold=.02, rezero=False, rebase=False, rebase_resolution=100):
    filtered_data = filter_paths(dinodata, threshold)
    indices = filtered_data[:,0]
    paths = filtered_data[:,1:]
    if rezero:
        reshape_to_distances(paths)
        np.shape(paths)
    if rebase:
        rebase_paths(paths, rebase_resolution)
    return (indices, paths)


# In[6]:
def run_pca(paths, num_elements = 5):
    pca = decomposition.PCA(num_elements)
    return pca.fit_transform(paths)


# In[ ]:

#sum([  0.77505258,  0.11530088,  0.09391347,  0.00602776,  0.0037433])


# In[7]:

#sum(pca.explained_variance_ratio_)


# In[4]:

def rebase_paths(paths, number_of_steps = 100):
    newpaths = np.empty((np.shape(paths)[0], 3 * number_of_steps))
    for i in range(np.shape(paths)[0]):
        if i % 1000 == 0:
            print(i)
        newpaths[i,:] = rebase_path(paths[i,:], number_of_steps)
    return newpaths

#Converts a path from list of points (at timesteps) to list of points (evenly distributed along the path)
def rebase_path(path, number_of_steps = 100):
    total_length = get_path_length(path)
    timesteps = int(math.floor(np.shape(paths)[1] / 3))
    newpath = np.zeros(number_of_steps * 3)
    current_timestep = 0
    current_distance = 0
    next_timestep_distance = 0
    last_timestep_distance = 0
    for i in range(number_of_steps):
        target_distance = i * 1.0 / number_of_steps * total_length
        next_timestep = current_timestep + 1
        #First we check to see which 2 points it's in between (current_timestep and next_timestep)
        while next_timestep_distance < target_distance:
            j = next_timestep
            if (j >= timesteps - 1):
                break
            next_timestep +=1
            last_timestep_distance = next_timestep_distance
            dx = path[3*j+3] - path[3*j]
            dy = path[3*j+4] - path[3*j+1]
            dz = path[3*j+5] - path[3*j+2]
            next_timestep_distance += math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        current_timestep = next_timestep - 1
        #Now figure out how far between them it is
        j = current_timestep
        ax = path[3 * j]
        ay = path[3 * j + 1]
        az = path[3 * j + 2]
        bx = path[3 * j + 3]
        by = path[3 * j + 4]
        bz = path[3 * j + 5]
        try:
            lerp_ratio = (target_distance - last_timestep_distance) / (next_timestep_distance - last_timestep_distance)
        except:
            lerp_ratio = 0
        lerp_ratio = np.clip(lerp_ratio, 0, 1)
        newpath[3 * i] = (1 - lerp_ratio) * ax + lerp_ratio * bx
        newpath[3 * i + 1] = (1 - lerp_ratio) * ay + lerp_ratio * by
        newpath[3 * i + 2] = (1 - lerp_ratio) * az + lerp_ratio * bz
        #print(i,current_timestep,target_distance, lerp_ratio)
    return newpath


# In[5]:

#repaths = rebase_paths(paths,300)


# In[8]:
def get_mask(target=5000, number = 10000):
    p = target / number
    p = np.clip(p, 0, 1)
    mask = np.random.choice([False, True], number, p=[1-p, p])
    return mask
    #ss_paths = paths[mask]
    #ss_indices = indices[mask]
    #ss_m = m[mask]
    #np.shape(ss_m)


# In[9]:
def do_agglom_cluster(data, clusters = 50):
    agglom = cluster.AgglomerativeClustering(n_clusters=clusters)
    return agglom.fit_predict(data)




# In[ ]:

#get_ipython().magic('matplotlib notebook')
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


# In[ ]:

#plt.scatter(ss_m[:,0], ss_m[:,1], c=labels)


# In[ ]:

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(ss_m[:,0], ss_m[:,1], ss_m[:,2], s=10, c=labels)


# In[11]:
def generate_labelmap(labels, indices):
    labelmap = {}
    for i, label in enumerate(labels):
        if labelmap.get(label, []) == []:
            labelmap[label] = []
        labelmap[label].append(indices[i])
    return labelmap

# In[ ]:

#labelmap[0][0]


# In[ ]:

#Method for selecting 1 point from each cluster
def labels_pathlines(labelmap):
    outlabels = [values[0] for label, values in labelmap.items()]
    outstr = '\n'.join([str(int(v)) for v in outlabels])
    return outstr
#print(outstr)


# In[ ]:

#method for printing out clusterings (cluster id per line)
def labels_oldclusters(labelmap):
    outlabels = [(v, l) for l, vs in labelmap.items() for v in vs ]#for clusterings
    outstr = '\n'.join([str(int(v)) + ' ' + str(int(l+1)) for v, l in outlabels])
    return outstr


# In[12]:

#alternate method for printing clusterings (all members of a cluster on one line)
def labels_clusters(labelmap):
    outlabels = [' '.join([str(int(i)) for i in items]) for _,items in labelmap.items()]
    outstr = '\n'.join(outlabels)
    return outstr


# In[13]:

def write_file(filename='pca-OLD_TEMP_FILENAME.clusters', outstr=''):
    with open(filename, 'w') as f:
        f.write(outstr)


#inFile is the data file to be read
#n_clusters is a list of the number of clusters to be determined.
def run(inFile= 'scripts/slices-1k.out', n_clusters = [50, 100], printMethods = [(labels_clusters, 'clusters'), (labels_pathlines, 'pathlines')]):
    print("Reading file {}".format(inFile))
    dinodata, indices, paths = load_dinosaur_data(inFile)
    print("File Read.")
    indices, paths = filter_and_reshape_paths(dinodata)
    m = run_pca(paths)
    mask = get_mask(100000, m.shape[0])
    print(m.shape[0])
    print("a")
    print(n_clusters)
    for clusters in n_clusters:
        print("b")
        print(clusters)
        labels = do_agglom_cluster(m, clusters)
        for fun, label in printMethods:
            print('pca-dataset-{}.{}'.format(clusters, label))
            labelmap = generate_labelmap(labels, indices)
            write_file('pca-dataset-{}.{}'.format(clusters, label), fun(labelmap))
    
    
if __name__ == '__main__':
    #print("test")
    #print(sys.argv)
    datafile = 'dataset.out'
    if len(sys.argv) > 1:
        datafile = sys.argv[1]
    clusters = [50,100]
    if len(sys.argv) > 2:
        clusters = map(int, sys.argv[2:])
    run(inFile = datafile, n_clusters = list(clusters))
