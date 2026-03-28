# from numpy import array
from random import choices
from time import sleep

# arr = array([[1,2,3,4],[1,2,3,4],[1,2,3,4]])
# di = {"happy":1,"sad":2}
# for i in di:
#     print(i)

# print( [di[i] for i in di][0])

# HIDDEN VARS = 1: good, 2:Bad

data = ["Blue","Green", "Green"]

# Challenge: Find the probabable moods on each day
# BONUS:  Find the probable mood on the next day.

class HMM:
    def __init__(self):
        self.hiddenVars = {"Happy":{"Happy": 0.7,"Sad": 0.3},"Sad":{"Happy": 0.5,"Sad": 0.5}}
        self.Vars = {
                    "Red":{"Happy": 0.6,"Sad": 0.2},
                    "Green":{"Happy": 0.3,"Sad": 0.3 },
                    "Blue":{"Happy": 0.1,"Sad": 0.5}
                    }
        self.StOut = {"Happy":0.3,"Sad":0.7}
        self.mood_list = []
        self.correctness = 0
# Starting from the start of the dataset but only using the highest probabilities without actually doing them.
    def transition_emission(self,data, previousMood, currentDay):
        # Make list(self.hiddenVariables.keys()) into a student variable
        # Find a way to make this function undependant on the self.mood_list variable

        cache = []
        for i in range(2):
            # print(self.hiddenVars[previousMood])
            cache.append([p for p in self.hiddenVars[previousMood]][i] * [p for p in self.Vars[data[currentDay]]][i])
        if cache[0] > cache[1]:
            self.mood_list.append("Happy")
            mood = "Happy"
            if currentDay == len(data) - 1:
                return
            currentDay += 1
            self.transition_emission(data,mood,currentDay)
        else:
            self.mood_list.append("Sad")
            mood = "Sad"
            if currentDay == len(data) - 1:
                return
            currentDay += 1
            self.transition_emission(data,mood,currentDay)

# Starting from the end of the dataset
    def official_transitionEmission(self, current_day):
        if current_day == 0:

            top = [0 for num in range(3)]
            for i in range(len(self.hiddenVars)):
                temp = [self.StOut[mood] * self.Vars[data[current_day]][x] * self.hiddenVars[mood][i] for x,mood in enumerate(self.StOut) ]
                probs = [ list(self.hiddenVars.keys())[temp.index(max(temp))], list(self.hiddenVars.keys())[i], max(temp) ]
                if probs[2] > top[2]:
                    top = probs

            self.mood_list.append(top[0])
            self.mood_list.append(top[1])

            self.correctness += top[2]
            return top[1]
            
        previous_mood = self.official_transitionEmission(current_day - 1)
        current_mood_probList = [ y * self.Vars[data[current_day]][x] for x,y in enumerate(self.hiddenVars[previous_mood]) ]
        current_mood = list(self.hiddenVars.keys())[current_mood_probList.index(max(current_mood_probList))]
        self.correctness += max(current_mood_probList)
        self.mood_list.append(current_mood)
        return current_mood

# Starting from the start of the dataset and actually running the probabilities and going from there.
# TIP: Maybe use the self.correctness thing from official_transitionEmission here to try and see which path is better as well
    def base_TE(self,current_day, list_mood):
        # if len(data) == 0:
        #     return list_mood
        if current_day == 0:
            startMood = choices([mood for mood in self.StOut],[self.StOut[p] for p in self.StOut])[0]
            list_mood.append(startMood)
        
        try:
            probabilties = [ p * self.Vars[data[current_day]][x] for x,p in enumerate(self.hiddenVars[list_mood[current_day]]) ]
            # choices function should normalize the probabilites but make sure to do it myself anyway.
            mood = choices( [mood for mood in self.hiddenVars], probabilties )[0]
            list_mood.append(mood)
        except IndexError:
            return list_mood
        
        current_day +=1

        list_mood = self.base_TE( current_day, list_mood)

        return list_mood

        # [ return_currentMood(previous_mood) for ]
# MAIN PROBLEM: IM not even sure if this is a true HMM, an HMM or at least the algorithm for the HMM I'm trying to make is supposed to find the maximum assignment value across the entire data set.  My algorithm only finds the maximum current value of each day as they go by, which doesn't guarantee the maximum probable set of moods.

# True algorithm, returns the probability of the path given occuring, not the best path of the hidden variables of the path.
# Not made entirely efficient though since there are still a lot of repeating lines: Add cache like that one guy did in that one stanford lesson
    def forward_algorithm(self, current_day, var):
        ans = 0
        if current_day == 0:
            ans = self.StOut[var] * self.Vars[data[current_day]][var]
        # This has to go unfortunately, it doesn't include the last element in data list so its an incomplete inference model.
        elif current_day == (len(data) - 1):
            for variable in self.hiddenVars:
                ans += self.forward_algorithm(current_day-1,variable)
        else:
            for variable in self.hiddenVars:
                ans += self.forward_algorithm(current_day-1, variable) * self.Vars[data[current_day]][variable] * self.hiddenVars[variable][var] 
            
        return ans

# 
    def inference(self, data):
        # startMood = choices([mood for mood in self.StOut],[self.StOut[p] for p in self.StOut])[0]
        # self.mood_list.append(startMood)
        # num = 0
        # if len(data) == 0:
        #     return self.mood_list

        return self.forward_algorithm(len(data) -1, 0)
        
        # self.transition_emission(data, startMood, num)
        # self.official_transitionEmission(len(data) -1)

        # return self.mood_list
        # return self.mood_list

        # poss = dict()
        # Something is wrong with this for loop for both transition/emission functions, fix it.
        # for i in range(5000):

        #     self.mood_list = self.base_TE(0,[])

        #     if " ".join(self.mood_list) in list(poss.keys()):
        #         poss[" ".join(self.mood_list)] += 1
        #     else:
        #         poss[" ".join(self.mood_list)] = 1


        # Make a lil thing here to get the top three highest paths (just find the max, and remove it from the dict (3x)
        # top_three = dict()
        # for i in range(3):
        #     top_three[max(poss, key=poss.get)] = max(poss.values())
        #     del poss[max(poss, key=poss.get)]

        # return top_three

test_run = HMM()
print(test_run.inference(data))
# start -> p(mood|start) * p(mood|shirtColor) -> 

# start:
# startMood = choices([mood for mood in self.StOut],[self.StOut(p) for p in self.StOut])
# mood_list.append(startMood)
# num = 0

# p(mood|start) * p(mood|shirtColor):
# cache = []
#for i in range(2):
#  cache.append([self.hiddenVars(p) for p in self.hiddenVars[startMood]][i] * [self.Vars(p) for p in self.Vars[data[num]]][i])
# if cache[0] > cache[1]:
#    mood_list.append("Happy")
#    startMood = "Happy"
#    if num == len(data) - 1:
#       return
#    num += 1
#    p(mood|start) * p(mood|shirtColor)
# else:
#    mood_list.append("Sad")
#    startMood = "Sad"
#    if num == len(data) - 1:
#       return
#    num += 1
#    p(mood|start) * p(mood|shirtColor)

# Need to make the first teacher's mood dependant on the mood of the second day in a way.  for ex. if second day she's likely to be happy then that indicates she was likely happy on the second day and vice versa.

# Official Version
#  p(shirt color| mood) * p(mood| prevoius mood) -> p(previous shirt color| previous mood) * p(previous mood | 2 previous moods) -> ... p(n previous moods| shirt color) * p(n previous moods| start mood)  -> p(start mood)

# transition_emission(self, current_day)
# Use the first data point in the data in conjuction with self.stout to help find the most likelihood mood of the teacher on the day before the dataset and their mood on the first day of the data set (which is index 0)
#   if current_day == 0:
# 
#      top = [0 for i in range(2)]
#      for i in len(self.hiddenVars):
#           temp = [self.StOut[mood] * self.Vars[data[current_day]][x] * self.hiddenVars[mood][i] for x,mood in enumerate(self.StOut) ]
#           probs = [ self.hiddenVars[temp.index(max(temp))], self.hiddenVars[i], max(temp) ]
#           if probs[2] > top[2]:
#                top = probs
# 
#      self.mood_list.append(top[0])
#      self.mood_list.append(top[1])
#      return top[1]
#      
#   previous_mood = transition_emission(current_day - 1)
#   current_mood_probList = [ y * self.Vars[data[current_day]][x] for x,y in enumerate(self.hiddenVars[previous_mood]) ]
#   current_mood = self.hiddenVars[current_mood_probList.index(max(current_mood_problList))]
#   self.mood_list.append(current_mood)
#   return current_mood
