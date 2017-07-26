import sys

def writeFootFile(inName, outName, prefix='footcomp2_', suffix='.vtk', firstLine='feet/sulcus/'):
  timesteps = []
  suffix += '\n'
  with open(inName) as f:
    with open(outName, 'w') as w:
      w.write(firstLine + '\n')
      nextLine = False
      for line in f:
        if nextLine:
          nextLine = False
          timesteps.append(line[:-1])
          w.write(prefix + line[:-1] + suffix)
        if 'TIMESTEP' in line:
          nextLine = True
  return timesteps

if __name__ == '__main__':
  n = len(sys.argv)
  a = sys.argv
  inFile = 'dataset.lammps'
  outFile = 'dataset.feet'
  prefix = 'footcomp2_'
  suffix = '.vtk'
  firstLine = 'feet/dataset/'
  if n > 1:
    inFile = a[1]
  if n > 2:
    prefix = a[2]
  if n > 3:
    suffix = a[3]
  if n > 4:
    firstLine = a[4]
  if n > 5:
    outFile = a[5]
  writeFootFile(inFile, outFile, prefix, suffix, firstLine)
