default: all

#dataset.lammps should be an ovito export using the lammps format, all timesteps in one file, exporting id x y z
dataset.out: dataset.lammps
	python3 scripts/many_to_one.py dataset.lammps dataset.out

#The first argument is the data file, the rest are numbers of clusters to generate
pca-dataset-50.clusters: dataset.out
	python scripts/process_paths_pca.py dataset.out 50 100 200

#The second argument is the number of layers
#The rest of the arguments are the gap sizes to use for creating triangles
dataset-0.01.tris: dataset.out
	python scripts/Surfaces.py dataset.out 4 0.1 0.05 0.03 0.01 0.005 0.003 0.001

all: dataset.out  dataset-0.01.tris pca-dataset-50.clusters
