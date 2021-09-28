'''based on sudo code given, code the select sort algo out'''

def selectionsort(A):
    '''given a list of element, sort the list, A is the list of element'''
    for i in range(0,len(A)):  #0,1,2,3
        # For position i
        # find the ith smallest elemt and swap wi with A[i]
        min = i
        # for selection of the elem/ counter shift
        # i+1 bc it doesn't need to loop thur the beginning of the range as it has been sorted already!
        for j in range(i+1,len(A)):  # 1, 2,3,4
            # comparison
            if A[min] > A[j]:
                min = j
                # Swapping
        A[i], A[min] = A[min], A[i]
    return A

    # # Traverse through all array elements
    # for i in range(len(A)):
        
    #     # Find the minimum element in remaining 
    #     # unsorted array
    #     min_idx = i
    #     for j in range(i+1, len(A)):
    #         if A[min_idx] > A[j]:
    #             min_idx = j
                
    #     # Swap the found minimum element with 
    #     # the first element        
    #     A[i], A[min_idx] = A[min_idx], A[i]
    # return A

print(selectionsort([6,3,2,5]))
# res should be [2,3,5,6]

