from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import crypto_primitive as cp #here you chose name of your file with crypto primitive
#import dig_sign as cp
from fuzzywuzzy import fuzz
import time
import random
import os


def corruption(input_data, corruption_type, corruption_number = 0):
    output_data = None
    if corruption_type == "none":
        return input_data
    else:
        length = len(input_data)
        l = list(range(0, length))
        random.shuffle(l)
        sorted_l = sorted(l[:corruption_number])

        tmp_data = list(input_data)
        if corruption_type == "add": #Adds random bytes in random places
            for idx, i in enumerate(sorted_l):
                tmp_data = tmp_data[:i+idx] + [int.from_bytes(os.urandom(1), "big")] + tmp_data[i+idx:]
        elif corruption_type == "del":
            for idx, i in enumerate(sorted_l): #Deletes bytes in random places
                tmp_data = tmp_data[:i-idx] + tmp_data[i-idx+1:]
        elif corruption_type == "chg": #Changes random bytes in random places
            for i in sorted_l:
                tmp_data[i] = int.from_bytes(os.urandom(1), "big")
        elif corruption_type == ">>": #Cyclic shift to the right
            tmp_data = tmp_data[-corruption_number:] + tmp_data[:-corruption_number]
        elif corruption_type == "<<": #Cyclic shift to the left
            tmp_data = tmp_data[corruption_number:] + tmp_data[:corruption_number]
        elif corruption_type[:9] == "ds sign: ":
            tmp_data = list(corruption(bytes(tmp_data[:128]), corruption_type[9:], corruption_number)) + tmp_data[128:]
        elif corruption_type[:9] == "ds text: ":
            tmp_data = tmp_data[:128] + list(corruption(bytes(tmp_data[128:]), corruption_type[9:], corruption_number))
        else:
            corruption_type = "none"
            return input_data
        output_data = bytes(tmp_data)
    return output_data


def pre_main(key_corruption = "none", text_corruption = "none", key_corrupted_number = 0,
text_corrupted_number = 0, show_graph = True, show_text = True, fixed_data_size = 0, 
iterations_number = 20, block_bytes_size = 16):
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    key = None

    if rank == 0:
        encryption_time = np.zeros(iterations_number + 1, dtype = float)
        decryption_time = np.zeros(iterations_number + 1, dtype = float)
        similarity_arr = np.zeros(iterations_number + 1, dtype = int)
        similarity_arr[0] = 100
        byte_size = np.linspace(0, block_bytes_size * iterations_number, iterations_number + 1)
        input_text = ""
        with open('input.txt') as f:
            input_text = f.read()
        if cp.key.type_ == "go":
            key = cp.key.generate()
            comm.send(key, dest=1)
        for i in range(iterations_number):
            start_idx = random.randint(0, len(input_text) - block_bytes_size * iterations_number) #random start
            start_time = time.time()
            if cp.key.type_ == "gps":
                key = cp.key.generate() #Here we generate encoded key
                comm.send(key, dest=1)
            input_text = input_text.encode("utf-8")
            comm.send(cp.encryption(input_text[start_idx: start_idx + block_bytes_size * (i + 1)], key), dest=1)
            encryption_time[i + 1] = time.time() - start_time
            decryption_time[i + 1] = comm.recv(source=2)
            result_text = comm.recv(source=2)
            similarity_arr[i + 1] = fuzz.ratio(input_text[start_idx: start_idx + block_bytes_size * (i + 1)]
                                    .decode("utf-8", errors = "ignore"),result_text)
            input_text = input_text.decode("utf-8", errors = "ignore")

        if show_graph == True:
            plt.title("Зависимость времени шифрования/дешифрования от длины сообщения\n" +
                    "key_corr={}({}), text_corr={}({})".format(key_corruption, key_corrupted_number,
                                                            text_corruption, text_corrupted_number))
            plt.xlabel("Длина сообщения")
            plt.ylabel("Время")
            plt.grid()
            plt.plot(byte_size, encryption_time, color='red', label="Шифрование")
            plt.plot(byte_size, decryption_time, color='blue', label="Дешифровка")
            plt.legend()
            plt.show()

            plt.title("Зависимость похожести от длины сообщения\n" +
                    "key_corr={}({}), text_corr={}({})".format(key_corruption, key_corrupted_number,
                                                            text_corruption, text_corrupted_number))
            plt.xlabel("Длина сообщения")
            plt.ylabel("Похожесть, %")
            plt.grid()
            plt.plot(byte_size, similarity_arr)
            plt.show()

        
        if fixed_data_size != 0: #There we build graph of similarity vs corruption size
            #comm.send(input_text, dest=1)
            key = cp.key.generate()
            comm.send(key, dest=1)
            input_text = input_text.encode("utf-8")
            comm.send(cp.encryption(input_text[0 : fixed_data_size], key), dest=1)
            compare_text = input_text[0 : fixed_data_size].decode("utf-8", errors = "ignore") #Just for not decoding same several times

            similarity_key = np.zeros(key_corrupted_number + 1, dtype = int)
            corrupted_bytes_key = np.linspace(0, key_corrupted_number + 1, key_corrupted_number + 1)
            for i in range(key_corrupted_number + 1):
                result_text = comm.recv(source=2)
                similarity_key[i] = fuzz.ratio(compare_text, result_text)
                if i == 0 and show_text == True: #Without any corruption
                    print("\n---Before---\n{}\n\n---After(key_corr=none, text_corr=none)---\n{}".format
                                                                             (compare_text, result_text))
                if i == key_corrupted_number and show_text == True and key_corrupted_number > 0: #With key corruption
                    print("\n---Before---\n{}\n\n---After(key_corr={}({}), text_corr=none)---\n{}".format
                                         (compare_text, key_corruption, key_corrupted_number, result_text))
            if show_graph == True and key_corrupted_number > 0 and key_corruption != "none":
                plt.title("Зависимость похожести от размера ошибки\n" 
                        "key_corr={}, text_corr=none".format(key_corruption))
                plt.xlabel("Размер ошибки")
                plt.ylabel("Похожесть")
                plt.grid()
                plt.plot(corrupted_bytes_key, similarity_key)
                plt.show()
     
            
            similarity_text = np.zeros(text_corrupted_number + 1, dtype = int)
            corrupted_bytes_text = np.linspace(0, text_corrupted_number + 1, text_corrupted_number + 1)
            for i in range(text_corrupted_number + 1):
                result_text = comm.recv(source=2)
                similarity_text[i] = fuzz.ratio(compare_text, result_text)
                if i == text_corrupted_number and show_text == True: #With text corruption
                    print("\n---Before---\n{}\n\n---After(key_corr=none, text_corr={}({}))---\n{}".format
                         (compare_text, text_corruption, text_corrupted_number, result_text))
            if show_graph == True and text_corrupted_number > 0 and text_corruption != "none":
                plt.title("Зависимость похожести от размера ошибки\n"
                        "key_corr=none, text_corr={}".format(text_corruption))
                plt.xlabel("Размер ошибки")
                plt.ylabel("Похожесть")
                plt.grid()
                plt.plot(corrupted_bytes_text, similarity_text)
                plt.show()


    elif rank == 1:
        if cp.key.type_ == "go":
            key = comm.recv(source=0)
            corrupted_key = corruption(key, key_corruption, key_corrupted_number)
            comm.send(corrupted_key, dest=2)
        for i in range(iterations_number):
            if cp.key.type_ == "gps":
                key = comm.recv(source=0)
                corrupted_key = corruption(key, key_corruption, key_corrupted_number)
                comm.send(corrupted_key, dest=2)
            recv_text = comm.recv(source=0)
            corrupted_text = corruption(recv_text, text_corruption, text_corrupted_number)
            comm.send(corrupted_text, dest=2)
        
        if fixed_data_size != 0:
            key = comm.recv(source=0)
            recv_text = comm.recv(source=0)
            for i in range(key_corrupted_number + 1):
                corrupted_key = corruption(key, key_corruption, i)
                comm.send(corrupted_key, dest=2)
                comm.send(recv_text, dest=2)
            for i in range(text_corrupted_number + 1): #once without corruption
                corrupted_text = corruption(recv_text, text_corruption, i)
                comm.send(key, dest=2)
                comm.send(corrupted_text, dest=2)


    elif rank == 2:
        if cp.key.type_ == "go":
            key = comm.recv(source=1)
        for i in range(iterations_number):
            if cp.key.type_ == "gps":
                key = comm.recv(source=1)
            start_time = time.time()
            output_text = cp.decryption(comm.recv(source=1), key)
            output_text = output_text.decode("utf-8", errors = "ignore")
            comm.send(time.time() - start_time, dest=0)
            comm.send(output_text, dest=0)
        if fixed_data_size != 0:
            for i in range(key_corrupted_number + 1 + text_corrupted_number + 1):
                key = comm.recv(source=1)
                output_text = cp.decryption(comm.recv(source=1), key)
                output_text = output_text.decode("utf-8", errors = "ignore")
                comm.send(output_text, dest=0)
