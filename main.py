from simulation import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#pre_main() #Just check if your cryptographic primitive works correctly

#pre_main(fixed_data_size = 1024 * 16, block_bytes_size = 128, iterations_number = 128)
#pre_main(fixed_data_size = 1024 * 16, text_corruption = "del", text_corrupted_number = 32, corrupted_block = 4)

#pre_main(key_corruption = "chg", key_corrupted_number = 4, fixed_data_size = 1337)
#pre_main(text_corruption = "del", text_corrupted_number = 20, fixed_data_size = 1337)
#pre_main(text_corruption = "add", text_corrupted_number = 20, fixed_data_size = 1337)
#pre_main(text_corruption = ">>", text_corrupted_number = 24, fixed_data_size = 1337)
#pre_main(text_corruption = "<<", text_corrupted_number = 24, fixed_data_size = 1337)

#Only for digital signature
pre_main(fixed_data_size = 1024 * 16, text_corruption = "ds text: del", text_corrupted_number = 32, corrupted_block = 4)
#pre_main(text_corruption = "ds sign: >>", text_corrupted_number = 4, fixed_data_size = 1337)
#pre_main(text_corruption = "ds text: chg", text_corrupted_number = 4, fixed_data_size = 1337)

