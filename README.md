# Description
Correctly works on linux. I don't know, maybe it will correctly works on windows too.
#### Before first start, you need to have this libraries:
  `pip install mpi4py` - for mpi processes: 0 - sender, encrypts; 1 - intermediate, can corrupt data; 2 - reciever, decrypts\
  `pip install matplotlib` - graphics\
  `pip install numpy` - I use arrays from numpy in this project\
  `pip install fuzzywuzzy` - for similarity checking\
  `pip install python-Levenshtein` - additional lib for fuzzywuzzy\
  `pip install pycryptodome` - DES realization.
#### For start, in terminal:
  `mpiexec -n 3 python3 main.py`\
You need to edit `crypto_primitive.py`. You  can also edit other files if it's necessary. Most important is that you need to realize algorithm of cryptographic primitive and analyze it. `simulation.py` helps with that.
