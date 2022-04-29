import random
import collections
import numpy as np
import pandas as pd


words = []
with open('data/words.txt') as f:
    for line in f:
        words.append(line.strip())


def internal_validate(answer, guess):
    colors = ['0', '0', '0', '0', '0']
    character_matches = dict(collections.Counter(list(answer)) & collections.Counter(list(guess)))
    for i in range(5):
        if answer[i] == guess[i]:
            colors[i] = '1'
            character_matches[guess[i]] -= 1

#         if guess[i] in character_matches and colors[i] == 'gray' and len(character_matches)>0:
#             character_matches.remove(guess[i])
#             colors[i] = 'yellow'

        if guess[i] in character_matches.keys() and colors[i] == '0':
            if character_matches[guess[i]] > 0:
                colors[i] = '2'
                character_matches[guess[i]] -= 1

    return "".join(colors)

def validate2(answer, guess):
    colors = list(internal_validate(answer, guess))
    flag = False
    if all(x == '1' for x in colors):
        flag = True
    return flag, "".join(colors)


def filteredSearch(df, constraints, guess):
    cols = []
    for col in np.arange(5):
        cols.append(f"c{col}")
    filtered = df
    searchList = {}
    for idx, constrain in enumerate(list(constraints)):
        
        if(constrain=="2"):
            filtered[filtered.eq(guess[idx]).any(1)]
            filtered = filtered[filtered[f"c{idx}"]!=guess[idx]]
        if(constrain=="1"):
            filtered = filtered[filtered[f"c{idx}"]==guess[idx]]
        if(constrain=="0"):
            if(guess[idx] not in searchList):
                filtered = filtered[filtered.eq(guess[idx]).any(1) == False]
        searchList[guess[idx]] = guess[idx]
    return filtered.reset_index()[cols]



def prepareWordDF():
    with open("./data/words.txt") as f:
        words = f.readlines()
        
    cols = []
    for col in np.arange(5):
        cols.append(f"c{col}")
    df = pd.DataFrame(columns = cols)
    for idx, word in enumerate(words):
        print(f"{idx+1}/{len(words)}", end="\r")
        df = pd.concat([df, pd.DataFrame([list(word.strip())], columns=cols)], ignore_index = True, axis = 0)
    
    return df