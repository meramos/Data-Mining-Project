import RecomHash #self-made library
import math
import time
import Pycluster #http://stackoverflow.com/questions/9847026/plotting-output-of-kmeanspycluster-impl
import numpy
from operator import add

#To run program in Windows' cmd: C:\Python33\python.exe program.py
#other python libraries as reference: http://www.lfd.uci.edu/~gohlke/pythonlibs/

#Have to run program in terminal/cmd. Running it in IDLE will make it slow
#and it will stop responding.
#http://stackoverflow.com/questions/17219490/idle-not-responding-when-building-a-dictionary

#Next approach to try: don't store data in matrices, get data continuously
#from the files

#Input is u.data and u.item files. 100,000 entries o_o

#Read u.data and u.item files for utility matrix and movie matrix

#Store information from u.data

filename = "u.data.txt"
delimeter = '\t'
unratedMatrix = []
ratedHash = {}

#Will have a matrix (list with list elements) to store first half of matrix, 50,000
#entries, which will be the entries we will predict ratings for.
#We will store the second half in a hash table where the key is the user ID and the element
#is a list of 2-tuples. We will use the information in the hash table to calculate rating
#predictions for the entries in the previously created matrix.

#While we read u.data and store the unrated and rated information into a matrix and hash,
#store rating and movie data into matrix for clustering, where the position will correspond
#to the position in the u.data file. Will inly store second half of file into the cluster
#matrix, so i = 0 will correspond to i = 0 + 50,000.

f1 = open(filename, 'r')

#store whole file into a string

lestring = f1.read()

whole = lestring.split('\n')

#Store the first half into matrix unratedMatrix
for i in range(0,int(len(whole)/2)): #first 50,000 entries
    
    the_line = whole[i].split(delimeter)

    #remove \n from elements
    for cow in range(0,len(the_line)):

        the_line[cow] = the_line[cow].strip("\n")

    unratedMatrix.append([the_line[0],the_line[1],the_line[2]]) #ignore timestamp

#Store the second half into dictionary ratedHash
for i in range(0,abs(1 - int(len(whole)/2))): #second 50,000 entries

    #file has 4 columns: userID, movieID, rating and timestamp.
    #we will only store the first 3 columns, we don't care for the timestamp.

    #store read userID, movieID, rating and timestamp into a list
    the_line = whole[i].split(delimeter)

    #remove \n from elements
    for cow in range(0,len(the_line)):

        the_line[cow] = the_line[cow].strip("\n")
        
    #Only use userID, movieID and rating (1st 3 columns).

    #store user ID
    user = the_line[0]

    #store movieID and rating into a tuple.
    tupl = (the_line[1],the_line[2])

    #Create dictionary entry using above stored information, userID is key and tuple is element

    #if userID already an entry in the dictionary
    if user in ratedHash:
        
        ratedHash[user].append(tupl)
        
    else:   #if userID not in dictionary, then created entry
        
        matri = [tupl] #put into array because dictionary elements are arrays in this case
        ratedHash[user] = matri    
    

f1.close()


#Store movie information from u.item file. Will be stored in a hash table.

filename = "u.item.txt"
delimeter = '|'
movieHash = {}

f2 = open(filename, 'r')

#store whole file into a string

lestring = f2.read()

whole = lestring.split('\n')

#Store data into dictionary movieHash
for i in range(0,len(whole)): #second 50,000 entries

    #file has 24 columns. We only care about the first column (movieID) and the last 19 columns which correspond to the genres.

    #store read data into a list
    the_line = whole[i].split(delimeter)

    #remove \n from elements
    for cow in range(0,len(the_line)): 

        the_line[cow] = the_line[cow].strip("\n")
        
    #Store wanted information

    #store movie ID
    movie = the_line[0]

    #store genre information into a list (vector)
    vector = []
                  
    for i in range(5,len(the_line)): #from 5 to 23. elements are 0 to 23.

        vector.append(the_line[i])

    #Create dictionary entry using above stored information, movieID is key and vector is the element

    movieHash[movie] = vector   

#write output into file to make sure it is right
#f = open('output.txt', 'w')
#f.write(str(movieHash))
#f.close()

f2.close()


#Now to create cluster matrix!
#Each element of the cluster will be the addition of the genre elements of the movies rated by a user.
#We only add the genre info of movies that were given a rating of 3 or higher by a user.
#In the future I may use the average value of ratings per user to decide what rating is a high enough
#or good enough rating.

clusterMatrix = []

users = list(ratedHash) #let's store this to keep track of the index of a user in the cluster matrix

for user in users:

    #Create addition vector that will store the addition of 19 genre binary elements
    #from the movieHash for each user. Initialize to 19 elements of value 0.

    genres = len(movieHash[ratedHash[user][0][0]]) #assuming all movies have the same number of genre elements,
                                                   #just use the # of elements for the first movie of the user in question

    addition = []

    for i in range(0,genres):
        
        addition.append(0)

    for i in range(0,len(ratedHash[user])): 

        movieID = ratedHash[user][i][0]
        rating = int(ratedHash[user][i][1])

        if rating >= 3:

            #Add movie genres information of the same user. Cumulative.

            for i in range(0,genres):

                addition[i] = addition[i] + int(movieHash[movieID][i])
  
    clusterMatrix.append(addition)


#Non rated movies are not mentioned for a user. No rating is 0, if
#a movie was not rated, it just doesn't appear as a row.
#So we will treat half of the data as unrated and the other half will be
#left alone.
#First half of utility Matrix will be treated as unrated movies.
#Second half will be rated movies.


#####
#**
#Content Based filtering. Cosine Similarity algorithm.
#**
#####

#to count time ...

CoBa_start_time = time.clock()

#Create matrix that will store predicted ratings with content based filtering.
#  It's purpose: to later compare stored ratings with predicted ratings of other
#  methods, such as collaborative filtering and hybrid.

contentUtiMatrix = []

#It will be as big as the 1st half of utilityMatrix that is treating as unrated.

for i in range(0,int(len(unratedMatrix))):

    #Initialize matrix. Use userID and movieID from unratedMatrix but leave rating as 0.

    contentUtiMatrix.append([unratedMatrix[i][0],unratedMatrix[i][1],0])


#Loop to rate each movie of the 1st half of the utility matrix.

itemindex = 0

for i in range(0,len(unratedMatrix)):

    #print("running...")

    #Go through rows for each movie.
    #Search for movies rated by the same user (so check ratedHash by using userID as key)
    #Then calculate their cosine similarity and compare with previously calculated ones.
    #Keep the largest cosine similarity value.

    #Store userID of user we shall predict the rating for.

    userID = unratedMatrix[i][0]

    #Store movieID of unrated movie.

    movie1 = unratedMatrix[i][1]

    #############
    ###########
    ###NOTE!!! Have worry that it isn't recognizing any of the user IDs so it isn't predicting anything. Check userID results.
    ########

    if userID in ratedHash: #if the userID was in the rated section of the data, then proceed. if not, rating stays 0.
        
        for j in range(0,len(ratedHash[userID])): #go through movies rated by the user in question, ratedHash[userID] = a list of movie-rating tuples

            #Have variable with smallest possible cosine similarity value so to compare with calculated cosine similarities.
            #The purpose is to be able to determine for which movie we get the biggest cosine similarity.

            biggest = -1

            #store movieID of rated movie

            movie2 = ratedHash[userID][j][0]   #element of hash is of form: [(movieID,rating), (123, 4), ...]

            #store movie vectors into variables

            vector1 = movieHash[movie1] #gives vector with genre information

            vector2 = movieHash[movie2]

            #Calculate cosine similarity between movie in question (i) and rated movie (j).
            #Value is between -1 and 1, 1 meaning that movies are identical and -1 meaning that they are opposites.

            cosineSi = RecomHash.cosineSimilarity(vector1,vector2)

            if(cosineSi > biggest): #Best rating is biggest cosine similarity.

                biggest = cosineSi
                itemindex = j

        contentUtiMatrix[i][2] = ratedHash[userID][itemindex][1] #store rating prediction in new matrix.

        print("Predicted rating of Content Based filtering: ", contentUtiMatrix[i][2])
        

    #print(i)

#store end time
CoBa_end_time = time.clock()

#We have our predicted ratings! Woo! Now to calculate their accuracy by calculating RMSE (root meat square error)

rmse = RecomHash.RMSE(unratedMatrix, contentUtiMatrix)

print("RMSE of content based filtering: ", rmse) #RMSE ~ 1.4457

#display execution time of algorithm in minutes

CoBa_total_time = (CoBa_end_time - CoBa_start_time)/60

print("Total execution time for cosine similarity: ", CoBa_total_time)



#####
#**
#Clustering. Preparation for Collaborative filtering.
#**
#####

#Now we will put users into clusters based on movies they rated highly.
#We will do this so that we can run Collaborative Filtering more efficiently,
#because when we predict the rating for a user we will only base ourselves on
#ratings of other users that are in the same cluster as the user in question.

print("Create clusters ...")

#Create 10 clusters.
clusterid, error, nfound = Pycluster.kcluster(clusterMatrix, nclusters=10, transpose=0, 
                                       npass=10, method='a', dist='e')
#Create and store the centroids.
centroids, _ = Pycluster.clustercentroids(clusterMatrix, clusterid=clusterid)

#Store user cluster pair.
user_cluster = list(zip(clusterMatrix, clusterid))

#Now lets create 10 cluster sets! The elements of each set will be userIDs that belong
#in those sets. Each set will be an element in a cluster list. We will use the previosly
#created users list to determine the userIDs that will be stored in the 'sets'

cluster = []

#Initialize cluster list to have 10 lists corresponding to the 10 clusters.

for i in range(0,10):

    cluster.append([])

#Now to store userIDs into their respective clusters.

for i in range(0,len(users)):       #remember, each row in the clusterMatrix corresponds to one user
                                    #number of cluster  data rows = number of users

    index = user_cluster[i][1]      #cluster number, second value of tuple, becomes the index

    cluster[index].append(users[i])

print("The resulting generated clusters: ")

for i in range(0,len(cluster)):

    print("Cluster ", i, ": ", cluster[i])

#That's all we shall do for clustering! Now this will be incorporated into collaborative
#filtering! To decrease the run time!


#####
#**
#Collaborative filtering. Slope One algorithm.
#**
#####

#to count time ...

CoFi_start_time = time.clock()

#Create matrix that will store predicted ratings with collaborative filtering.
#  It's purpose: to later compare stored ratings with predicted ratings of other
#  methods, such as content based and hybrid.

collabUtiMatrix = []

#It will be as big as the 1st half of utilityMatrix that is treating as unrated.

for i in range(0,len(unratedMatrix)):

    #Do same as for the content based matrix.

    collabUtiMatrix.append([unratedMatrix[i][0],unratedMatrix[i][1],0])

    

for i in range(0,len(unratedMatrix)):

    #Start time of iteration.
    #ite_start_time = time.clock()

    addition = 0
    relevant = 0

    #Store userID of user we shall predict the rating for. user u

    userID = unratedMatrix[i][0]

    #Store movieID of unrated movie. movie j

    movie1 = unratedMatrix[i][1]

    if userID in ratedHash: #if the userID was in the rated section of the data, then proceed. if not, rating stays 0.

        #we are looking for different items to compare with. relevant items to compare with will be items same user rated. 
        #compare movie with other items rated by the SAME user. We count these to get 'relevant'.

        for j in range(0, len(ratedHash[userID])):   #number of movies rated by user userID

            movie2 = ratedHash[userID][j][0]    #movieID of movie j for user userID

            rating_ui = ratedHash[userID][j][1] #rating of movie j by user userID

            #movie_i is movie1, movie_j is movie2

            #figure out to which cluster this user belongs to and use it as a parameter for the deviation function

            own_cluster = []
            found = False
            i = 0

            while (not found) and (i < 10): #adding i < 10 for precaution but userID must be in one of the clusters

                if userID in cluster[i]:

                    own_cluster = cluster[i] #will be a list of userIDs
                    found = True

                i = i + 1

            #Now to calculate addition and call the deviation function.
            
            addition = addition + (int(rating_ui) - RecomHash.dev(movie1,movie2,ratedHash,own_cluster))

        relevant = len(ratedHash[userID]) #Relevant items for a user are items rated by the same user.

        prediction = addition / relevant   #a value for each unrated movie
    
        if(prediction < 1):

            collabUtiMatrix[j][2] = 1
            
        elif(prediction > 5):

            collabUtiMatrix[j][2] = 5

        else:    

            collabUtiMatrix[j][2] = round(prediction) #calculate rating for movie j

    #Calculate and print time it takes for iteration to be executed.
    #ite_end_time = time.clock()
    #ite_total_time = ite_end_time - ite_start_time
    #print("Iteration time for collaborative in seconds: ", ite_total_time)
        
    print("Predicted rating of Collaborative Filtering: ", collabUtiMatrix[j][2])
        

#store end time
CoFi_end_time = time.clock()

#We have our predicted ratings! Woo! Now to calculate their accuracy by calculating RMSE (root meat square error)

rmse = RecomHash.RMSE(unratedMatrix, collabUtiMatrix)

print("RMSE of collaborative filtering: ", rmse)

#display execution time of algorithm in minutes

CoFi_total_time = (CoFi_end_time - CoFi_start_time)/60

print("Total execution time for Slope One with Clustering: ", CoFi_total_time)


#####
#**
#Hybrid Filtering. Weighted Filtering.
#**
#####

#Last but not least, Hybrid Filtering! Woooooo!

            


        
