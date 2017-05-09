# Data-Mining-Project
UKY Data Mining project

To run program in Windows' cmd: C:\Python33\python.exe program.py
other python libraries as reference: http://www.lfd.uci.edu/~gohlke/pythonlibs/

Have to run program in terminal/cmd. Running it in IDLE will make it slow
and it will stop responding.
http://stackoverflow.com/questions/17219490/idle-not-responding-when-building-a-dictionary

Next approach to try: don't store data in matrices, get data continuously
from the files

Input is u.data and u.item files. 100,000 entries

Will have a matrix (list with list elements) to store first half of matrix, 50,000
entries, which will be the entries we will predict ratings for.
We will store the second half in a hash table where the key is the user ID and the element
is a list of 2-tuples. We will use the information in the hash table to calculate rating
predictions for the entries in the previously created matrix.

While we read u.data and store the unrated and rated information into a matrix and hash,
store rating and movie data into matrix for clustering, where the position will correspond
to the position in the u.data file. Will inly store second half of file into the cluster
matrix, so i = 0 will correspond to i = 0 + 50,000.

When creating the cluster matrix...
Each element of the cluster will be the addition of the genre elements of the movies rated by a user.
We only add the genre info of movies that were given a rating of 3 or higher by a user.
In the future I may use the average value of ratings per user to decide what rating is a high enough
or good enough rating.

Non rated movies are not mentioned for a user. No rating is 0, if
a movie was not rated, it just doesn't appear as a row.
So we will treat half of the data as unrated and the other half will be
left alone.
First half of utility Matrix will be treated as unrated movies.
Second half will be rated movies.

***more info within comments of program
