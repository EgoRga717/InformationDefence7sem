import matplotlib.pyplot as plt
import numpy as np

crypto_primitives = ['aes_default', 'kuznechik', 'belt']


byte_size = np.load('none_none_byte_size_aes_l.npy')


plt.title("Зависимость времени шифрования от длины сообщения\n" +
        "key_corr=none, text_corr=none")
plt.xlabel("Длина сообщения")
plt.ylabel("Время")
plt.grid()
for cp in crypto_primitives:
    encryption_time = np.load('none_none_encrypion_time_{}.npy'.format(cp))
    plt.plot(byte_size, encryption_time, label="{}".format(cp))
plt.legend()
plt.show()


plt.title("Зависимость времени расшифровки от длины сообщения\n" +
        "key_corr=none, text_corr=none")
plt.xlabel("Длина сообщения")
plt.ylabel("Время")
plt.grid()
for cp in crypto_primitives:
    decryption_time = np.load('none_none_decrypion_time_{}.npy'.format(cp))
    plt.plot(byte_size, decryption_time, label="{}".format(cp))
plt.legend()
plt.show()

corrupted_bytes = np.load('none_chg_corrupted_bytes_text_aes_l.npy')
cor_type = "chg"

plt.title("Зависимость похожести от размера ошибки\n" +
        "key_corr=none, text_corr={}".format(cor_type))
plt.xlabel("Размер ошибки")
plt.ylabel("Похожесть")
plt.grid()
for cp in crypto_primitives:
    if cp == "dig_sign":
        ct = "ds text: " + cor_type
    else:
        ct = cor_type
    similarity = np.load('none_{}_similarity_text{}.npy'.format(ct, cp))
    plt.plot(corrupted_bytes, similarity, label="{}".format(cp))
plt.legend()
plt.show()


