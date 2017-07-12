

def readFile(inFile):
  particles = {} # map from particle id to array[location]
  counter = 0
  with open(inFile) as f:
    for line in f:
      if counter % 500000 == 0:
        print(counter)
      counter += 1
      if line == "ITEM: TIMESTEP\n":
        try:
          for i in range(8):
            x = next(f)
        except StopIteration:
          break
      else:
        s = line.split()
        if len(s) < 4:
          continue
        p = s[0]
        x = s[1]
        y = s[2]
        z = s[3]
        particles[p] = particles.get(p,[]) + [x,y,z]
  return particles
        
def writeFile(outFile, particles):
  with open(outFile, 'w') as f:
    for p in particles:
      s = p + ' ' + ' '.join(particles[p]) + '\n'
      f.write(s)


def processFile(inFile, outFile):
  particles = readFile(inFile)
  print('particles read')
  writeFile(outFile, particles)
  print('particles written')

def validateParticles(particles):
  newparts = {}
  for particle in particles:
    row = particles[particle]
    if len(row) != 144:
      continue
    if float(row[2]) > 0.077:
      continue
    newparts[particle] = row
  return newparts

def lowMemoryMode(inFile, outFile):
  particles = set()
  with open(inFile) as f:
   counter = 0
   for line in f:
    if counter % 1000000 == 0:
      print(counter)
    counter += 1
    if line == "ITEM: TIMESTEP\n":
      try:
        for i in range(8):
          x = next(f)
      except StopIteration:
        break
    else:
      s = line.split()
      p = s[0]
      particles.add(p)
  return particles
    
def get_line_sizes(inFile):
  vals = {}
  with open(inFile) as f:
    counter = 0
    for line in f:
      if counter % 10000 == 0:
        print(counter)
      counter += 1
      s = line.split()
      q = len(s)
      vals[q] = vals.get(q, 0) + 1
  return vals

def filter_lines_size(inFile, outFile, expected):
   outf = open(outFile, 'w')
   with open(inFile) as f:
    counter = 0
    for line in f:
      if counter % 10000 == 0:
        print(counter)
      counter += 1
      s = line.split()
      q = len(s)
      if q == expected:
        outf.write(line)
    close(outf)

def get_line_sizes_mem(particles):
  vals = {}
  for p in particles:
    q = len(particles[p])
    vals[q] = vals.get(q,0) + 1
  return vals

def get_expected_line_size(vals):
  best = 0
  bestval = 0
  for val in vals:
    if vals[val] > bestval:
      bestval = vals[val]
      best = val
  return best

def filter_line_sizes_mem(particles):
  best_size = get_expected_line_size(get_line_sizes_mem(particles))
  return {id : pos for id,pos in particles.items() if len(pos) == best_size}

if __name__ == "__main__":
  import sys
  inFile = sys.argv[1]
  outFile = sys.argv[2]
  particles = readFile(inFile)
  writeFile(outFile, filter_line_sizes_mem(particles))
