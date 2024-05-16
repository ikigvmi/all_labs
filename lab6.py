# база 1
def Write_file():
    with open('Numbers', 'a') as File:
        numbers = list(map(str, input('Введите все числа через пробел: ').split()))
        for i in numbers:
            File.writelines(i + '\n')
def Read_file():
    try:
        with open('Numbers', 'r') as File:
            for line in File:
                try:
                    num = float(line)
                    maximum = num
                    minimum = num
                    summa = 0
                    if num > maximum:
                        maximum = num
                    if num < minimum:
                        minimum = num
                    summa += num
                except:
                    pass
    except:
        return print('Ошибка чтения файла')
    return str(maximum), str(minimum), str(summa)

def Operatinon(a):
    with open('Numbers', 'a') as File:
        File.write(a[0] + '\n')
        File.writelines(a[1] + '\n')
        File.writelines(a[2] + '\n')
for i in range(10):
    Write_file()
    Operatinon(Read_file())

# база 2
def Write_file():
    with open('Numbers', 'a') as File:
        numbers = list(map(str, input('Введите все числа через пробел: ').split()))
        for i in numbers:
            File.writelines(i + '\n')
def Read_file():
    max_num = float('-inf')
    min_num = float('inf')
    sum_num = 0
    with open('Numbers', 'r') as File:
        for line in File:
            try:
                x = float(line)
                if x > max_num:
                    max_num = x
                if x < min_num:
                    min_num = x
                sum_num += float(line)
            except:
                pass
    return max_num, min_num, sum_num

def Operatinon(a):
    with open('Numbers', 'a') as File:
        File.write(str(a[0]) + '\n')
        File.writelines(str(a[1]) + '\n')
        File.writelines(str(a[2]) + '\n')

Write_file()
Operatinon(Read_file())


# база 3
def Total():
    with open('Kino', 'r') as f:
        x = f.readlines()
        temp = []
        total = []
        for Lines in range(len(x)):
            for Element in x[Lines]:
                if Element in '01':
                    temp.append(Element)
            total.append(temp)
            temp = []
    return total

def Counter():
    total_places = Total()

    Places_all = 0
    Places = 0

    for i in range(len(total_places)):
        Places_all += total_places[i].count('0') + total_places[i].count('Base')
        Places += total_places[i].count('0')
        print(f'На ряду номер {i}: {total_places[i].count('0')} свободных мест')
    num1, num2 = map(int, input('\nВведите номер ряда и места через пробел (отсчёт начинать с 0): ').split())
    if total_places[num1][num2] == '0':
        print('Данное место свободно')
    elif total_places[num1][num2] == 'Base':
        print('Данное место занято')

Counter()


# база 4
n1, n2, m1, m2 = int(input('Ввеедите количество столбцов первой матрицы: ')), int(input('Ввеедите количество столбцов второй матрицы: ')), int(input('Ввеедите количество строк первой матрицы: ')), int(input('Ввеедите количество строк второй матрицы: '))  # при изменении файлов matrix1.txt и matrix2.txt настоятельно требуется изменить вручную эти данные.

new_elem_flag = True
curr_summands_count = 0
new_row_flag = False
curr_elems_in_a_row = 0
curr_seek = 0

with open('matrix_res.txt', 'w') as f:
    pass

for i in range(m1 * n2 * n1):
    with open('matrix1.txt', 'r') as matrix1:
        curr_el_1 = int([i.strip().split() for i in matrix1.readlines()][i // (n2 * n1)][i % n1])
        with open('matrix2.txt', 'r') as matrix2:
            curr_el_2 = int([i.strip().split() for i in matrix2.readlines()][i % m2][(i // m2) % n2])
            with open('matrix_res.txt', 'r+') as matrix_result:
                if new_row_flag:
                    matrix_result.seek(curr_seek)
                    matrix_result.write('\n')
                    curr_seek += 1
                    new_row_flag = False

                if new_elem_flag:
                    matrix_result.seek(curr_seek)
                    matrix_result.write(' ')
                    curr_seek += 1
                    matrix_result.write(str(curr_el_1 * curr_el_2))
                    curr_summands_count += 1
                    new_elem_flag = False
                else:
                    curr_res_el = [i.strip().split() for i in matrix_result.readlines()][-1][-1]
                    matrix_result.seek(curr_seek, 0)
                    matrix_result.write(str(int(curr_res_el) + curr_el_2 * curr_el_1))
                    curr_summands_count += 1

                if curr_summands_count == n1:
                    new_elem_flag = True
                    curr_summands_count = 0
                    curr_elems_in_a_row += 1
                    curr_seek += len(str(int(curr_res_el) + curr_el_2 * curr_el_1))

                if curr_elems_in_a_row == m1:
                    new_row_flag = True
                    curr_elems_in_a_row = 0

if n1 == n2 == m1 == m2 == 3:
    with open('matrix1.txt', 'r') as mat1:
        with open('matrix2.txt', 'r') as mat2:
            with open('matrix_res.txt', 'r') as mat_res:
                mat1_read = mat1.readlines()
                mat2_read = mat2.readlines()
                matres_read = mat_res.readlines()
                for i in range(max(m1, m2, n1, n2)):
                    if i < m1 and i < m2:
                        if i == m1 // 2:
                            print(
                                f'{mat1_read[i].strip():5s}   X   {mat2_read[i].strip():5s}   =   {matres_read[i].strip()}')
                            continue
                        print(
                            f'{mat1_read[i].strip():5s}       {mat2_read[i].strip():5s}       {matres_read[i].strip()}')
                    elif i < m1:
                        print(f'{mat1_read[i].strip():10f} {matres_read[i].strip()}')

# база 5
import os
print(os.path.abspath("Laba 6.ipynb"))

# доп 1
def is_exe(filename):
    try:
        with open(filename, 'rb') as file:
            signature = file.read(2)
            return int(signature == b'MZ')
    except:
        return 'Файл не был найден'


filename = 'Setup.exe'
print(is_exe(filename))

# доп 2
import shutil

def copy_file(filename_from, filename_to):
    shutil.copyfile(filename_from, filename_to)


with open('ИмяФайла', 'w') as f1:
    f1.write("Hello =)")

with open('Copy ИмяФайла', 'w'):
    pass

filename_from = 'ИмяФайла'
filename_to = 'Copy ИмяФайла'
copy_file(filename_from, filename_to)
