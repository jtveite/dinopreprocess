
# coding: utf-8

# In[142]:

import scipy as sp
import numpy as np
from sklearn import decomposition
from sklearn import cluster
import sys


# In[178]:


# In[143]:

    
def load_dinosaur_data(fileName):
    dinodata = np.loadtxt(fileName)
    indices = dinodata[:,0]
    paths = dinodata[:,1:]
    return (dinodata, indices, paths)



# In[ ]:




# In[14]:

def getDist(a, b):
    c = a[1:4]
    d = b[1:4]
    return np.linalg.norm(c-d)

#data is samples x 1 + 3 * timesteps matrix
#gap is a double
#returns indices (right now at least)
def poissonDiscSample(data, gap = 0.001):
    outvals = []
    indices = range(np.size(data,0))
    tested = 0
    for i in indices:
        tested += 1
        good = True
        for j in outvals:
            if getDist(data[i, :], data[j,:]) < gap:
                good = False
                break
        if good:
            outvals.append(i)
            if len(outvals) % 100 == 0:
                print("Found {} points so far out of {} tested, {} total.".format(len(outvals), tested, np.size(data,0)))
    return outvals

            


# In[208]:

#out = poissonDiscSample(dinodata, 0.001)
#len(out)


# In[216]:


# In[228]:

#a = dinodata[indices]
#np.shape(a)
#a = dinodata


# In[229]:

#b = a[:,3]
#c = b.reshape((-1,1))
#np.shape(c)


# In[241]:


def clusterLayers(dinodata, n_layers = 1):
    b = dinodata[:,3]
    c = b.reshape((-1,1))
    #Take only the z coordinate and cluster based on it
    sc = cluster.KMeans(n_clusters=n_layers)
    labels = sc.fit_predict(c)
    return labels


# In[26]:

#get_ipython().magic('matplotlib notebook')
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


# In[240]:
def get_layer_levels(data, labels, n_layers):
    vals = []
    for i in range(n_layers):
        vals.append((i, data[labels==i,3][0]))
    return sorted(vals, key=lambda x : x[1])


# In[187]:

#fig = plt.figure()
#plt.scatter(a[:,1], a[:,3], c=(labels == 5))


# In[242]:

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(a[:,1], a[:,2], a[:,3], s=10, c=(labels))


# In[243]:
def triangulate(data, labels, n_layers):
    dlist = []
    outstr = []
    for i in range(n_layers):
        d = data[labels == i,1:3];
        delaunay = sp.spatial.Delaunay(d)
        dlist.append(delaunay)
        s = dlist[i].simplices
        outints = data[labels == i,0][s]
        outstr.append('\n'.join([' '.join([str(int(v)) for v in arr]) for arr in outints]))
    out = '\n'.join(outstr)
    return out


# In[245]:

#f = plt.figure()
#t = 0
#plt.triplot(a[labels==t, 1], a[labels==t, 2], dlist[t].simplices.copy())


# In[237]:

#len(outstr[0])


# In[246]:

#out = '\n'.join([outstr[i] for i in [0]])


# In[247]:
def write_tris(filename, tris):
     with open(filename, 'w') as f:
        f.write(tris)


# In[ ]:

if __name__ == '__main__':
    infile = 'dataset.out'
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    n_layers = 4
    if len(sys.argv) > 2:
        n_layers = int(sys.argv[2])
    gaps = [0.001, 0.01]
    if len(sys.argv) > 3:
        gaps = map(float, sys.argv[3:])
    print("Reading file ", infile)
    data, indices, paths = load_dinosaur_data(infile)
    for gap in gaps:
        try:
            print("Computing gap ", gap)
            subindices = poissonDiscSample(data, gap)
            subdata = data[subindices,:]
            clusters = clusterLayers(subdata, 4)
            tris = triangulate(subdata, clusters, 4)
            write_tris('dataset-{}.tris'.format(gap), tris)
        except:
            print("Error computing last gap")

