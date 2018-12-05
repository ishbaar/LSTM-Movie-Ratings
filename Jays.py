import numpy as np
import pandas
import random
#source: https://stackoverflow.com/questions/37793118/load-pretrained-glove-vectors-in-python

#This function takes in the path to the glove 50d pretrained vectors that is
#originally stored as a .txt and then converts it into a dictionary. To access
#a certain vector of a certain word, use the word as the key, and the dictionary
#will return the vector.
def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r',encoding="utf-8")
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model

#This function takes in the path to our modified csv file and returns individual
#lists containing title, summary, and score, respectively. 
#
#Example: title[k] returns the movie at index k's title in the form of a string
#
#@ Params: csvFile - the path to our modified csv file containing only the usable
#                    movies
#
#@ Return: title - a list of all the movie titles inside of csvFile
#          summary - a list of all the summaries inside of csvFile
#          score - a list of all the scores (voter averages) inside of csvFile
def parseCSV(csvFile):
    #define the column names
    columns = ['title', 'summary', 'score']
    
    #reading the file to parse
    csv_data = pandas.read_csv(csvFile, names = columns)
    
    #stores the respective data in lists
    title = csv_data.title.tolist()
    summary = csv_data.summary.tolist()
    score = csv_data.score.tolist()
    
    #because the first index of each list is the header, we get rid of
    #the first element in each list
    title.pop(0)
    summary.pop(0)
    score.pop(0)
    
    return title, summary, score

#This function takes in the summary list and then randomly generates a test
#set and a training set. The hardcoded value is 80 percent training and 20
#percent test. This returns a trainingSet, a testSet, a testSetIndex, and
#a trainingSetIndex list. 
#
#@ Params: summary - the summary list generated by the function parseCSV
#@ Return: trainingSet - the summaries inside of the parameter summary to be used
#                        as training data
#          testSet - the summaries inside of the parameter summary to be used for
#                    testing purposes
#          testSetIndex - a list of integers that represent which indices inside
#                         summary are being used for testing purposes
#          trainingSetIndex - a list of integers that represent which indices inside
#                             summary are being used for training purposes.
def generateSets(summary):
    #definition of constants throughout this function
    training_percentage = .8
    list_size = len(summary)
    
    #initialize the things to return
    testSetIndex = []
    testSet = []
    trainingSet = []
    trainingSetIndex = []
    
    #Steps to generate the test set:
    #1. Randomly generate an integer between 0 and list_size
    #2. Check to see if this index is already within our test set
    #3. If it isn't, document this index inside our testSetIndex and go on
    #4. If it is, generate another random number until we find one that isn't
    #5. Repeat until testSetIndex is of size (1-training_percentage)
    for i in range(int(list_size * (1-training_percentage))):
        rand_index = random.randint(0, list_size)
        
        #keep generating until it is NOT inside of testSetIndex
        while(rand_index in testSetIndex):
            rand_index = random.randint(0, list_size)
            
        testSetIndex.append(rand_index)
        testSet.append(summary[rand_index])
        
    #After this, we will have int[(1-training_percentage)*list_size] elements
    #inside of testSet. Training set is everything else. 
    for k in range(list_size):
        
        if(k not in testSetIndex):
            trainingSet.append(summary[k])
            trainingSetIndex.append(k)
            
    return trainingSet, testSet, testSetIndex, trainingSetIndex


#taken and modified from: 
#https://stackoverflow.com/questions/9797357/dividing-a-string-at-various-punctuation-marks-using-split

#This function splits the sentence by spaces and punctuation marks. Punctuation
#marks refer to non-alphanumeric characters that can appear validly inside
#of the English sentence. One exception to this rule is the string "'s" as this
#has it's own vector inside of the glove pretrained vector set. Therefore, this
#particular string will get it's own index. 
#@Param: text- the text to be parsed. This must a valid English block of text,
#              as in, it must be readable to the everyday person
#@Retuen: sentence - a list containing the parsed version of the input text.
#                    Each index of this will contain either a punctuation mark
#                    by itself, the string "'s" by itself, or an English word.
def parseSentence(text):
    sentence = ("".join((char if char.isalnum() else (" "+ char + " ")) for char in text).split())
    
    #join the instances of "'s" and ONLY "'s"
    i = 0
    while i in range (len(sentence)):
        if(sentence[i] == "'" and sentence[i+1] == 's'):
            sentence[i] = "'s"
            sentence.pop(i+1)
            i += 1
            
    #join the rest of the punctuation marks. AKA non-alphanumeric characters
    j = 0
    while j in range (len(sentence)): 
        if(sentence[j] != "'s" and not sentence[j].isalnum()):
            k = j+1
            while (k in range (len(sentence)) and not sentence[k].isalnum()):
                sentence[j] = sentence[j] + sentence[k]
                sentence.pop(k)
        
        j += 1
    
    return sentence
    