# Description
#### Before first start, you need to have this libraries:
  `pip install mpi4py` - for mpi processes: 0 - sender, encrypts; 1 - intermediate, can corrupt data; 2 - reciever, decrypts\
  `pip install matplotlib` - graphics\
  `pip install numpy` - I use arrays from numpy in this project\
  `pip install fuzzywuzzy` - for similarity checking\
  `pip install python-Levenshtein` - additional lib for fuzzywuzzy
#### For start:
  `mpiexec -n 3 python3 simulation.py`\
You need to edit `crypto_primitive.py`. You  can also edit `simulation.py` if it's necessary. Most important is that you need to realize algorithm of kryptographic primitive and analyze it. `simulation.py` helps with that.
