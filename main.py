
"""
This is a full implementation of a user-user collaborative filtering system
My issue with this is the crossover between Pandas and OOP, its confusing 
Can solve this when implementing with Django with a SQL DB, can do it all in SQL
"""

import numpy as np
import pandas as pd
import math
import operator

class People:

    def __init__(self):
        """
        Need vectors df then movies df to make rec
        """
        self.columns = ["ID", "Action", "Comedy", "Romance", "Drama"]
        self.data = pd.DataFrame() 

        # for movies rec - list of people objects
        self.people_list = []

    def add(self, person):
        """
        add a new person to the data frame
        """
        ID = person.ID
        vec = person.vector
        rec = np.array([[ID, vec[0], vec[1], vec[2], vec[3]]])
        df = pd.DataFrame(data=rec, columns=self.columns)
        self.data = self.data.append(df, ignore_index=True)

        # add a person to the list of objects
        self.people_list.append(person)

    def recommend(self, person):
        """
        find recommendations for the person given
        """
        # all of the similarities
        sims = {}
        top = 0 # most similar user cos sim

        # isolate the user we want to find rec for - going to have to change this
        vec = person.vector
        euc = np.linalg.norm(vec)

        # need to loop through the other vectors and find each DP
        # how to not include user * user ?
        for i in range(0,len(self.data)):
            x = 1
            if person.ID == self.data['ID'].loc[i]:
                x = 0
            y = np.array(self.data.loc[i])
            vec_i = y[1:] # don't include the ID
            num = np.dot(vec, vec_i) * x # dot product, if same user then will be 0
            denom = np.linalg.norm(vec_i) # euclidean distance
            cos = num / (denom * euc) # cos similarity
            sims[self.data['ID'].loc[i]] = cos # need the ID for the row were on
            top = max(cos, top)

        top_ID = max(sims.items(), key=operator.itemgetter(1))[0] # ID of the most similar user - next step will be max heap

        # recommend from the top ID 
        # find the person with ID == top ID and store
        people = self.people_list
        for p in people:
            if p.ID == top_ID:
                target = p
                break
        activities = target.activity_IDs

        # loop through activities and find the ones the given user has not seen
        activities_ = []
        for a in activities:
            if a not in person.activity_IDs:
                activities_.append(a)
        
        return activities_

    def print(self):
        print(self.data)

class Person:

    count = 1 # need a static variable for unique IDs

    def __init__(self, name):
        """
        each person has a name and vector 
        vector prime is so we can update
        """
        self.name = name 
        self.vector = np.array([0,0,0,0])
        self.vectorprime = np.array([0,0,0,0])
        self.ID = Person.count
        self.activity_IDs = []
        Person.count += 1 
        
    def update(self, activity):
        """
        when a new activity is added
            add the new activities vector to the total (prime)
            divide the sums for each category by the sum of vector
        """
        self.vectorprime = np.add(self.vectorprime, activity.vector)
        self.vector = self.vectorprime / np.sum(self.vectorprime)
        self.activity_IDs.append(activity.ID) # add the activity ID to persons activity IDs

    def print(self):
        print(self.vector)


class Activity:

    count = 1

    def __init__(self, name, vector):
        """
        Each activity has a name and a vectors that defines it's characteristics
        Added an ID for recommendations
        """
        self.name = name 
        self.vector = vector
        self.ID = Activity.count
        Activity.count += 1

# testing 

# movies 

Movie1 = Activity("Dark Knight", np.array([9, 2, 5, 7]))
Movie2 = Activity("Dark Knight Rises", np.array([10, 1, 4, 8]))
Movie3 = Activity("Pineapple Express", np.array([6, 9, 1, 3]))
Movie4 = Activity("The Other Guys", np.array([8, 8, 1, 1]))
Movie5 = Activity("Interstellar", np.array([7, 1, 3, 9]))
Movie6 = Activity("Goon", np.array([8, 7, 5, 1]))
Movie7 = Activity("Waterworld", np.array([9, 1, 7, 6]))

# people

charlie = Person("Charlie")
charlie.update(Movie1)
charlie.update(Movie2)

sarah = Person("Sarah")
sarah.update(Movie2)
sarah.update(Movie3)

jack = Person("Jack")
jack.update(Movie1)
jack.update(Movie3)

nicole = Person("Nicole")
nicole.update(Movie7)
nicole.update(Movie6)

tom = Person("Tom")
tom.update(Movie3)
tom.update(Movie4)

will = Person("Will")
will.update(Movie7)
will.update(Movie5)

julia = Person("Julia")
julia.update(Movie7)
julia.update(Movie6)

jordan = Person("Jordan")
jordan.update(Movie4)
jordan.update(Movie5)

# list of people

first = People()
first.add(charlie)
first.add(sarah)
first.add(nicole)
first.add(jordan)
first.add(julia)
first.add(tom)
first.add(will)
first.add(jack)

# recommend

IDs = first.recommend(sarah)
print(IDs)










