import string
from enum import Enum

class Test(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

#%%
array = [('yes',2), ('no', 4), ('yes',2), ('no', 1), ('okay',3), ('no', 1)]
print(array[1][1])
# %%
array = ['(yes,2)', '(no, 4)', '(yes,2)', '(whoa, 1)', '(okay,3)', '(what, 1)']
for elem in array:
    elem.strip(string.punctuation)

print(array)