import math

def cosineSimilarity(A, B):

    #referenced wikipedia

    #A and B are movie vectors
    
    return (dotproduct(A,B) / (norm(A)*norm(B)))

def dotproduct(A, B):

    #referenced wikipedia

    addition = 0

    for i in range(0,len(A)):

        addition = addition + (int(A[i]) + int(B[i]))

    return addition

def norm (A):

    #referenced wikipedia

    addition = 0

    for i in range(0,len(A)):

        addition = addition + (int(A[i]))**2

    return math.sqrt(addition)

def RMSE(originalMatrix, newMatrix):

    #rating in 3rd column, 0,1,2
    #size of new matrix is size of first half of utility matrix
    #ratings are integers so yiu can use int() to convert from str to int

    addition = 0

    N = len(newMatrix)

    for i in range(0,N):

        addition = addition + (abs(int(newMatrix[i][2]) - int(originalMatrix[i][2])))**2

    return math.sqrt(addition / N)


def dev(item1, item2, ratedHash,cluster_set):

    summ = 0   #calculate for set of users that rated both item1 and item2
    cardinality = 0

    i=0

    #focus on rated items, ratedHash. Go through rated items to find user(s) that rated the two items being compared.
    #so, go through user keys. Also, only go through users most similar to the user in question based on previously
    #determined clusters. cluster_set is a list of userIDs.
    
    for user in cluster_set: #go through user IDs, keys in the ratedHash dictionary. check other users that rated
                             #both item1 and item2 and are similar to the user in question.

        #Store movieIDs on their own in the movieIDs list to make search easier

        movieIDs = [x[0] for x in ratedHash[user]] #stores first element of tuple for each tuple

        #reference: http://stackoverflow.com/questions/2917372/how-to-search-a-list-of-tuples-in-python

        if (item1 in movieIDs) and (item2 in movieIDs):

            #get index of element that is = item1, do same for item2
            #index corresponds to tuple from ratedHash

            item1_index = movieIDs.index(item1)
            item2_index = movieIDs.index(item2) 

            summ = summ + (int(ratedHash[user][item1_index][1]) - int(ratedHash[user][item2_index][1]))   #substract ratings
            cardinality = cardinality + 1 #number of users that rated i and j

    return (summ / cardinality)

                    

###OTHER longer implementation of the dev()
###check list corresponding to ratedHash[user] to find item1 and item2
##
##        for movie1 in range(0,len(ratedHash[user])): #look for item 1. NOTE:smaller list than for implementation with matrices.
##
##            if ((item1 == ratedHash[user][movie1][0]) or (item2 == ratedHash[user][movie1][0])): #compare movie IDs
##
##                for movie2 in range(movie1,len(ratedHash[user])): #look for item 2. NOTE:smaller list than for implementation with matrices.
##
##                    if ((item2 == ratedHash[user][movie2][0]) or (item1 == ratedHash[user][movie1][0])):
##
##                        summ = summ + (int(ratedHash[user][movie1][1]) - int(ratedHash[user][movie2][1]))   #substract ratings
##                        cardinality = cardinality + 1 #number of users that rated i and j

