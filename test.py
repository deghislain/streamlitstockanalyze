from numpy.core.defchararray import swapcase

file = open('temp.txt', 'w')

file.write("This is the first line. \n")
file.close()

file_read = open('temp.txt', 'r')
line = file_read.readline()
print(line[-1])
select = "IBM"
test = "stock_symbol==\'{0}\'".format(select)
print(test)