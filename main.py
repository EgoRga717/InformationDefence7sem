from simulation import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

pre_main() #Just check if your cryptographic primitive works correctly
#pre_main(fixed_data_size = 1337)
#pre_main(key_corruption = "chg", key_corrupted_number = 4, fixed_data_size = 1337)
#pre_main(text_corruption = "chg", text_corrupted_number = 20, fixed_data_size = 1337)
#pre_main(text_corruption = "del", text_corrupted_number = 20, fixed_data_size = 1337)
#pre_main(text_corruption = "add", text_corrupted_number = 20, fixed_data_size = 1337)
#pre_main(text_corruption = ">>", text_corrupted_number = 24, fixed_data_size = 1337)
#pre_main(text_corruption = "<<", text_corrupted_number = 24, fixed_data_size = 1337)

