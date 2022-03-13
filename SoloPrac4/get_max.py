


def getMax(arr, n=None):
    print(n)

    if len(arr) == 1:
        return n

    new_arr = []
    for i in range(1, len(arr)):
        new_arr.append(arr[i])
    
    
    getMax(new_arr, n)


print(getMax([0,4,1,2,3]))
    
    