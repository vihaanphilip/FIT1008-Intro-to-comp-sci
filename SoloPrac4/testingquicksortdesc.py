""" A simple implementation of the QuickSort algorithm.
    Picks pivot elements randomly.
"""
from list_adt import ArrayList

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'


import random
from typing import List, Optional


def qsort(array: ArrayList[tuple]) -> None:
    """ QuickSort public interface. """

    #random.seed()
    _qsort_aux(array, 0, len(array) - 1)


def partition(array: ArrayList[tuple], low: int, high: int, pivot : Optional[int] = None) -> int:
    """ Randomly selects a pivot element and
            1. moves smaller elements to the left
            2. moves greater elements to the right
        Returns the position of the pivot element.
    """
    pivot = (low+high)//2

    # TODO
    array[low], array[pivot] = array[pivot], array[low]
    boundary = low

    for k in range(low+1, high+1):
        if array[k][1] > array[low][1]:
            boundary += 1
            array[k], array[boundary] = array[boundary], array[k]

    array[low], array[boundary] = array[boundary], array[low]
    return boundary



def _qsort_aux(array: ArrayList[int], low: int, high: int) -> None:
    """ Actual implementation of QuickSort.
        Sorts a list of elements in-place.
    """

    # TODO
    if low < high:
        boundary = partition(array, low, high)
        _qsort_aux(array, low, boundary-1)
        _qsort_aux(array, boundary+1, high)

if __name__ == '__main__':
    #array = [int(v) for v in input('Enter integer array: ').split()]
    #pivot = int(input('Enter pivot index: '))
    #pivot_loc = partition(array, 0, len(array) - 1, pivot)
    #print(pivot_loc, array)
    #qsort(array)
    #print(array)

    array = [('yes',2), ('no', 4), ('heh',2), ('no', 1), ('okay',3), ('what', 1)]
    pivot = 2
    pivot_loc = partition(array, 0, len(array) - 1, pivot)
    #print(pivot_loc, array)


    qsort(array)
    print(array)

    """
    [1,3,5,2,4]
    [5,1,3,2,4]
    [4,1,3,2,5]
    """
