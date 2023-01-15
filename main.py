import collections
import csv
import math
import random
from collections import Counter
import Crypto.Util.number
import scipy.special as sc


# Перевод из двоичного массива в число
def from_bitarray_to_number(bitarr):
    template_str = ''
    for i in bitarr:
        template_str += str(i)
    num = int(template_str, 2)
    return num


# Алгоритм Криптографического ГПСЧ, основанного на RSA
def generate_bits_rsa(bits_count):
    # Генерация 2 256-битных чисел
    p = Crypto.Util.number.getPrime(256, randfunc=Crypto.Random.get_random_bytes)
    q = Crypto.Util.number.getPrime(256, randfunc=Crypto.Random.get_random_bytes)
    # Расчет модуля
    n = p * q
    # Расчет функции Эйлера
    fi = (p - 1) * (q - 1)
    # Генерируем начальное значение
    x0 = random.randint(2, n - 1)
    x = x0
    # Подбираем ключ e
    e = random.randint(2, fi - 1)
    while math.gcd(e, fi) != 1:
        e = random.randint(2, fi - 1)
    list_of_bits = []
    # Генерируем биты
    for i in range(0, bits_count):
        x = pow(x, e, n)
        list_of_bits.append(x & 1)
    return list_of_bits


# Функция генерации целого числа в заданном промежутке
def random_int(min_value, max_value):

    # Количество генерируемых бит
    COUNT_OF_BITS = 32

    # Верхняя граница 32 битного числа
    MAX_UINT32 = 4294967295

    if min_value > max_value:
        raise 'Неверно заданы границы'
    if min_value == max_value:
        return min_value

    # Разница между нижней и верхней границей промежутка
    diff = max_value - min_value

    while True:
        # Генерирование бит
        rand_bits = generate_bits_rsa(COUNT_OF_BITS)
        # Перевод из массива битов в целое число
        rand = from_bitarray_to_number(rand_bits)
        max_val = 1 + MAX_UINT32
        remainder = max_val % diff
        if rand < max_val - remainder:
            return min_value + (rand % diff)


# Функция генерации последовательности случайных чисел
def random_sequence():
    # Цикл, в котором получаем 10000 случайных значений на промежутке
    list_of_nums = []
    for j in range(0, 10000):
        list_of_nums.append(random_int(0, 100))

    # Подсчет частоты сгенерированных чисел
    counter_nums = Counter(list_of_nums)
    counter_nums = collections.OrderedDict(sorted(counter_nums.items()))

    # Запись в файл
    with open('output_random_sequence.csv', 'w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        for key, value in counter_nums.items():
            writer.writerow([key, value])


# Блочный тест на частоту
def block_frequency():
    # Размер блока
    size_of_block = 30

    # Количество генерируемых битов
    size_of_bits = 300

    # альфа значение
    alpha = 0.01

    # Генерация бит
    list_of_bits = generate_bits_rsa(size_of_bits)
    print('Последовательность бит: ', list_of_bits, sep='')
    list_of_blocks = []

    # Количество блоков
    count_of_blocks = len(list_of_bits) // size_of_block

    # Разделение на блоки
    print('Блоки: ')
    for i in range(0, count_of_blocks):
        list_of_blocks.append(list_of_bits[30 * i:30 * (i + 1)])
        print(i + 1, ') блок: ', list_of_blocks[i], sep='')
    list_of_propotrion_ones = []

    # Подсчет единиц в каждом блоке
    for i in list_of_blocks:
        count_of_ones = i.count(1)
        list_of_propotrion_ones.append(count_of_ones / size_of_block)
    print('Количество единиц в каждом блоке от общего количества: ',
          [round(item, 3) for item in list_of_propotrion_ones], sep='')

    # Статистика Хи-квадрат
    chi2 = 0
    for i in list_of_propotrion_ones:
        chi2 += pow((i - 0.5), 2)
    chi2 *= 4 * size_of_block
    print('Статистика Хи-квадрат: ', chi2, sep='')

    print('alpha значение: ', alpha, sep='')

    # Вычисление P_value
    p_value = sc.gammaincc(count_of_blocks / 2, chi2 / 2)
    print('P значение: ', p_value, sep='')

    # Проверка
    print('Частотный блочный тест пройден!' if p_value > alpha else 'Частотный блочный тест провален!')


# Проверка функций
random_sequence()
block_frequency()
