__author__      = 'akshaykulkarni'

'''
Recommendation algorithm implemented on MovieLens Data
'''

from math import sqrt

'''
Similarity between two entities based on eucledian-distance metric
'''
def sim_distance(prefs,p1,p2):

    sum_squares         = 0
    for item in prefs[p1]:
        if item in prefs[p2]:
            diff            = prefs[p1][item] - prefs[p2][item]
            sum_squares     = sum_squares   + pow(diff,2)

    return 1.0/(1+sum_squares)

'''
Similarity between two entities based on pearson-similarity metric
'''
def pearson_sim_distance(prefs,p1,p2):
    commons             = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            commons[item]   = 1

    n                   = len(commons)
    if 0 == n:
        return 0

    s1                  = sum([prefs[p1][item] for item in commons])
    s2                  = sum([prefs[p2][item] for item in commons])

    sqrs1               = sum([pow(prefs[p1][item],2) for item in commons])
    sqrs2               = sum([pow(prefs[p2][item],2) for item in commons])

    csum                = sum(prefs[p1][item]*prefs[p2][item] for item in commons)
    num                 = csum-(s1*s2/n)
    den                 = sqrt((sqrs1-pow(s1,2)/n)*(sqrs2-pow(s2,2)/n))

    if den==0:
        return 0

    return (num*1.0)/den

'''
Getting top matches for the given input person whose choice matches to others
'''

def topMatches(prefs,person,n=5,similarity=pearson_sim_distance):
    sim_values          = [(similarity(prefs,person,other),other) for other in prefs if other!= person]
    sim_values.sort()
    sim_values.reverse()
    return sim_values[0:n]

'''
Getting top movies for a user
'''
def getRecommendations(prefs,person,similarity=pearson_sim_distance):
    total_sims          = {}
    sum_sims            = {}

    for other in prefs:

        if other == person:
            continue

        sim             = similarity(prefs,person,other)
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                if item not in total_sims:
                    total_sims[item]    = 0

                total_sims[item]    = total_sims[item] + (prefs[other][item]*sim*1.0)

                if item not in sum_sims:
                    sum_sims[item]  = 0
                sum_sims[item]      = sum_sims[item] + sim


    rankings    = [(total/sum_sims[item],item) for item,total in total_sims.items()]
    rankings.sort()
    rankings.reverse()

    return rankings

def transformPrefs(prefs):
    result      = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person]    = prefs[person][item]

    return result

'''
loading Input MovieData
'''
def loadMovieLensData(input_path):

    movies          = {}
    for line in open(input_path+'/u.item'):
        (id,title)      = line.split('|')[0:2]
        movies[id]      = title

    prefs           = {}
    for line in open(input_path+'/u.data'):
        (userid,movieid,rating,ts)          = line.split("\t")
        prefs.setdefault(userid,{})
        prefs[userid][movies[movieid]]      = float(rating)

    return prefs


input_data_path     = "/Users/akshaykulkarni/Documents/gp/Recommendations/ml-100k"
prefs               = loadMovieLensData(input_data_path)
print getRecommendations(prefs,'87')[0:30]
print "------------------------"
print getRecommendations(prefs,'24')[0:30]