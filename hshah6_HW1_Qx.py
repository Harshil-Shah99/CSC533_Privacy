import re, sys
import math, random
import numpy as np
import operator

#### BEGIN----- functions to read movie files and create db ----- ####

def add_ratings(db, chunks, num):
    if not chunks[0] in db:
        db[chunks[0]] = {}
    db[chunks[0]][num] = int(chunks[2])

def read_files(db, num):
    movie_file = "movies/"+num
    ratings = []
    fo = open(movie_file, "r")
    r = 0
    for line in fo:
        chunks = re.split(",", line)
        chunks[len(chunks)-1] = chunks[len(chunks)-1].strip()
        add_ratings(db, chunks, num)

#### END----- functions to read movie files and create db ----- ####

def score(w, p, aux, r):
    '''
    Inputs: weights of movies, maximum possible difference in rating, auxiliary information, and a record,
    Returns the corresponding score
    '''
    #### ----- your code here ----- ####

    similarity_score = 0
    for rating in aux:
        if rating in r.keys():
            T = 1 - abs((aux[rating] - r[rating]))/p[rating]
            similarity_score += w[rating]*T/len(aux)

    return similarity_score



def compute_weights(db):
    '''
    Input: database of users
    Returns weights of all movies
    '''
    #### ----- your code here ----- ####
    weights = {}
    ## you can use 10 base log
    for user_id in db:
        for movie_id in db[user_id]:
            if movie_id in weights.keys():
                weights[movie_id] += 1
            else:
                weights[movie_id] = 1

    for weight in weights:
        weights[weight] = 1/(math.log10(abs(weights[weight])))

    print("Movie ID                      Weight")
    for weight in weights:
        print(str(weight) + "                     " + str(weights[weight]))

    return weights




def calcP(db, aux, movies):
    low = {}
    high = {}
    for movie in movies:
        low[movie] = 6
        high[movie] = -1

    ## you can use 10 base log
    for user_id in db:
        for movie_id in db[user_id]:
            low[movie_id] = min(low[movie_id], db[user_id][movie_id])
            high[movie_id] = max(high[movie_id], db[user_id][movie_id])

    for movie_id in aux:
        low[movie_id] = min(low[movie_id], aux[movie_id])
        high[movie_id] = max(high[movie_id], aux[movie_id])

    pvalues = {}
    for movie in movies:
        pvalues[movie] = high[movie] - low[movie]

    return pvalues
#### BEGIN----- additional functions ----- ####



#### END----- additional functions ----- ####

if __name__ == "__main__":

    db = {}
    files = ["03124", "06315", "07242", "16944", "17113",
            "10935", "11977", "03276", "14199", "08191",
            "06004", "01292", "15267", "03768", "02137"]

    for file in files:
        read_files(db, file)

    aux = { '03124': 4, '06315': 3.2, '07242': 3.9, '17113': 3.7,
            '10935': 4, '11977': 4.2, '03276': 3.8, '14199': 3.9,
            '08191': 3.8, '03768': 2.2, '02137': 3}

    w = compute_weights(db)
    p = calcP(db, aux, files)
    print(p)
    scores = {}
    for user in db:
        scores[user] = score(w, p, aux, db[user])
    top5 = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:5]
    print()
    for user in top5:
        print(user)
    print()
    print()
    for item in aux:
        print(item + ":   " + str(aux[item]) + " |        Top Similar User: " + str(db['716173'][item]))

    print()
    print("Difference in top 2: " + str(top5[0][1] - top5[1][1]))
    difference = top5[0][1] - top5[1][1]
    print()
    # question d part ii -> subsection a.
    M = 0
    for rating in aux:
        M += w[rating]/abs(len(aux))

    gamma = 0.1
    print("Gamma * M: ")
    print(gamma*M)
    if difference > gamma*M:
        print("Accepted")
    else:
        print("Not accepted")

    gamma = 0.05
    print()
    print("Gamma * M: ")
    print(gamma*M)
    if difference > gamma*M:
        print("Accepted")
    else:
        print("Not accepted")


    # question d part ii -> subsection b.
    #### ----- your code here ----- ####
