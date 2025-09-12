def bubble_sort(array):
    n = len(array)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                swapped = True
        if (swapped == False):
            break
    print(array)
      
arr = [5, 4, 9, 1, 3, 6, 7]        
bubble_sort(arr)