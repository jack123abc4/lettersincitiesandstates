import matplotlib.pyplot as plt
import numpy as np
import csv

wordFile = open("words.txt")
wordLines = wordFile.readlines()
wordFile.close()

NUMERICS_ALLOWED = False
HYPHENS_ALLOWED = False
NO_VOWELS_ALLOWED = False
MULTIPLE_CAPITALS_ALLOWED = False
SPACES_ALLOWED = True

def freqListToPercents(valList, is_printing):
    sum = 0
    retStr = ""
    for i in valList:
        sum += i

    for i in range(0,len(valList)):
        letterFreq = float(valList[i]) / sum
        retStr += (chr(i+97) + ": " + str("%.2f" % (letterFreq*100))+ "%\n")
        valList[i] = letterFreq
    if is_printing:
        print(retStr)
    return valList

index = 1
beginningLetters_allWords = [0]*26
for line in wordLines:
    line = line.strip()
    valid = True
    contains_numeric = False
    contains_hyphen = False
    contains_space = False
    contains_vowel = False
    contains_one_capital = False
    contains_multiple_capitals = False

    for char in line:
        if not char.isalpha():
            if char == "-":
                contains_hyphen = True
            elif char == " ":
                contins_space = True
            else:
                contains_numeric = True
        if char in ["a","e","i","o","u","y"]:
            contains_vowel = True
        if char != char.lower():
            if contains_one_capital == False:
                contains_one_capital = True
            else:
                contains_multiple_capitals = True

    if (NUMERICS_ALLOWED == False and contains_numeric == True) or (HYPHENS_ALLOWED == False and contains_hyphen == True) or (NO_VOWELS_ALLOWED == False and contains_vowel == False) or (MULTIPLE_CAPITALS_ALLOWED == False and contains_multiple_capitals == True) or (SPACES_ALLOWED == False and contains_space == True):
        valid = False

    if valid:
        #97 = "a"
        beginningLetters_allWords[ord(line[0].lower())-97] += 1
        #beginningLetters_allWords.append(line[0])
        index += 1

stateFile = open("listOfStates.txt")
stateLines = stateFile.readlines()
stateFile.close()
beginningLetters_states = [0]*26
for line in stateLines:
    beginningLetters_states[ord(line[0].lower())-97] += 1

cityLines = []
beginningLetters_cities = [0]*26
with open('simplemaps_uscities_basicv1.74/uscities.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        cityName = row[0].split(",")[0]
        cityName.replace('"', "")
        cityLines.append(cityName.replace('"',""))

cityLines.pop(0)
for line in cityLines:
    beginningLetters_cities[ord(line[0].lower())-97] += 1

#cityFile = open("simplemaps_uscities_basicv1.74/uscities.csv")
#cityLines = cityFile.readLines(cityFile)
#cityFile.close()

allWordsFreq = freqListToPercents(beginningLetters_allWords, True)
statesFreq = freqListToPercents(beginningLetters_states, True)
citiesFreq = freqListToPercents(beginningLetters_cities, True)


x_labels = [""] * 26
for i in range(26):
    x_labels[i] = chr(i+97)

x_axis = np.arange(len(x_labels))
plt.bar(x_axis, allWordsFreq, width=0.2, label = 'All Words')
plt.bar(x_axis - 0.2, statesFreq, width=0.2, label = 'States')
plt.bar(x_axis + 0.2, citiesFreq, width=0.2, label = 'Cities')

plt.xticks(x_axis, x_labels)
plt.xlabel("Letters")
plt.ylabel("Frequency")
plt.title("Beginning Letters - U.S. States + Cities to All Words")
plt.legend()
plt.show()
