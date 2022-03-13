import string
from enum import Enum


array = ['(yes,2)', '(no,4)', '(yes,2)', '(whoa,1)', '(okay,3)', '(what,1)']
array2 = []
for i in range(len(array)):
    array[i] = array[i].strip(string.punctuation)
    
    word = ''
    num = ''
    j=0
    while array[i][j] != ',':
        word += array[i][j]
        j+= 1
    print(word)

    for k in range(j+1, len(array[i])):
        num += array[i][k]
    num = int(num)
    print(num)

    test = (word, num)
    array2 += test
    print(test)
    

    
        


print(array)
print(array2)

