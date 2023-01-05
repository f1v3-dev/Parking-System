
number_data = []
date_data = []

def file_search(arr_number,arr_date):
    f = open("/home/jeongwoo/sambashare/number.txt",'r')
    line = f.readline()


    number_d = line[0:7]
    date_d = line[8:-1]

    arr_number.append(number_d)
    arr_date.append(date_d)
    print(line)
    print(number_d)
    print(date_d)
    f.close()
file_search(number_data,date_data)

print("number_data and date_data")
print(number_data)
print(date_data)
