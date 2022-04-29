"""
Source: https://www.youtube.com/watch?v=TsnovVfkafI
"""
import random
from collections import Counter
import pygame

# AI Imports
import pandas as pd
from services2 import validate2
import numpy as np
import threading

import time


# AI True/False
AI = True

# FORCE FIRST WORD
FORCE = True


words = []
with open('data/allowed_words.txt') as f:
    for line in f:
        words.append(line.strip())

possible_answers = []
with open('data/words.txt') as f:
    for line in f:
        possible_answers.append(line.strip())

ANSWER = random.choice(possible_answers)
# ANSWER = "nerve"
print(ANSWER)


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

wordDF = prepareWordDF()
searchSpace = wordDF.copy()

xGBoard = pd.read_csv("xGTable.csv")

AI_GUESS = ""

WIDTH = 600
HEIGHT = 800
MARGIN = 10
T_MARGIN = 65
B_MARGIN = 100
LR_MARGIN = 100

WHITE = (255, 255, 255)
GREY = (58, 58, 60)
LIGHT_GREY = (129, 131, 132)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)

INPUT = ""
GUESSES = []
COLORS = []
TRINARY_COLORS = []
KEYBOARD = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
ALPHABET_DICT = {}

GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

SQ_SIZE = (WIDTH-4*MARGIN-2*LR_MARGIN) // 5
FONT = pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQ_SIZE//2)


def validate(guess):
    colors = [GREY, GREY, GREY, GREY, GREY]
    character_matches = dict(Counter(list(ANSWER)) & Counter(list(guess)))
    for i in range(5):
        if ANSWER[i] == guess[i]:
            colors[i] = GREEN
            character_matches[guess[i]] -= 1

        if guess[i] in character_matches.keys() and colors[i] == GREY:
            if character_matches[guess[i]] > 0:
                colors[i] = YELLOW
                character_matches[guess[i]] -= 1
    return colors


def color2trinary(colors):
    trinary_colors = [0, 0, 0, 0, 0]
    for i in range(len(colors)):
        if colors[i] == GREY:
            trinary_colors[i] = 0
        elif colors[i] == GREEN:
            trinary_colors[i] = 1
        elif colors[i] == YELLOW:
            trinary_colors[i] = 2

    return "".join(str(e) for e in trinary_colors)


def filteredSearch(df, constraints, guess):
    
    cols = []
    for col in np.arange(5):
        cols.append(f"c{col}")
    filtered = df
    searchList = {}
    for idx, constrain in enumerate(list(constraints)):
        
        if(constrain=="2"):
            filtered = filtered[filtered.eq(guess[idx]).any(1)]
            filtered = filtered[filtered[f"c{idx}"]!=guess[idx]]
        if(constrain=="1"):
            filtered = filtered[filtered[f"c{idx}"]==guess[idx]]
        if(constrain=="0"):
            if(guess[idx] not in searchList):
                filtered = filtered[filtered.eq(guess[idx]).any(1) == False]
            else:
                filtered = filtered[filtered[f"c{idx}"]!=guess[idx]]
        searchList[guess[idx]] = guess[idx]
    return filtered.reset_index()[cols]


def xMap(guess, df):
    fbMap = {}
    for _, row in df.iterrows():
        word = "".join(row)
        _, fb = validate2(word, guess)
        if(fb in fbMap):
            fbMap[fb] +=1
        else:
            fbMap[fb] = 1
    return fbMap

def getxG(guess, df):
    fbMap = xMap(guess, df)
    x = 0
    for info in fbMap:
        p = fbMap[info]/df.shape[0]
        x += p* - np.log2(p)
    return x


def getBestWords(df):
    xGBoard = pd.DataFrame(columns=["word", "xG"])
    
    for idx, row in df.iterrows():
#         clear_output(wait = True)
#         print(f"{idx+1}/{df.shape[0]}")
        word = "".join(row)
        xG = getxG(word, df)
        xGBoard = xGBoard.append({"word": word, "xG": xG}, ignore_index = True)
    return xGBoard


def infoTheorySolver(df, word):
    xGBoard = pd.read_csv("xGTable.csv")
    guesses = 0
    isDone = False
    while(isDone == False):
        guess = xGBoard.sort_values(by="xG", ascending=False).iloc[0]["word"]
        isDone, fb = validate(word, guess)
        df = filteredSearch(df, fb, guess)
        xGBoard = getBestWords(df)
        guesses +=1
    return guesses


def getGuess(idx):
    global searchSpace
    global xGBoard
    global AI_GUESS
    print(idx)
    if(idx == 0):
        AI_GUESS = xGBoard.sort_values(by="xG", ascending=False).iloc[0]["word"]
    else:
        print(searchSpace.shape)
        print(TRINARY_COLORS[-1])
        print(GUESSES[-1])
        print(GUESSES)
        print(TRINARY_COLORS)
        searchSpace = filteredSearch(searchSpace, str(TRINARY_COLORS[-1]), GUESSES[-1].lower())
        # print(searchSpace.shape)
        xGBoard = getBestWords(searchSpace)
        
        AI_GUESS = xGBoard.sort_values(by="xG", ascending=False).iloc[0]["word"]
        

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# animation loop
animating = True

while animating:
    # background
    screen.fill("black")
    letters = pygame.font.SysFont("cambria", SQ_SIZE//2, bold=True).render("Wordle", False, WHITE)
    surface = letters.get_rect(center=(WIDTH // 2, 25))
    screen.blit(letters, surface)
    pygame.draw.line(screen, LIGHT_GREY, (0, 50), (WIDTH, 50))

    y = T_MARGIN
    for i in range(6):
        x = LR_MARGIN
        for j in range(5):
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, GREY, square, width=2)

            if i < len(GUESSES):
                color = COLORS[i][j]
                pygame.draw.rect(screen, color, square, border_radius=3)
                letter = FONT.render(GUESSES[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center = (x+SQ_SIZE//2, y+SQ_SIZE//2))
                screen.blit(letter, surface)

            # user text input next guess
            if i == len(GUESSES) and j < len(INPUT):
                letter = FONT.render(INPUT[j], False, WHITE)
                surface = letter.get_rect(center = (x+SQ_SIZE//2, y+SQ_SIZE//2))
                screen.blit(letter, surface)

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN

    # show the correct ANSWER after a game over
    if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
        GAME_OVER = True
        letters = pygame.font.SysFont("cambria", SQ_SIZE//3, bold=True).render(ANSWER.upper(), False, WHITE)
        surface = letters.get_rect(center=(WIDTH//2, y + SQ_SIZE//6))
        screen.blit(letters, surface)

    y = y + SQ_SIZE // 2
    for keys in KEYBOARD:
        x = 250 + ((LR_MARGIN - (len(keys) * 50)) // 2)
        for char in keys:
            color = LIGHT_GREY
            if char in ALPHABET_DICT.keys():
                color = ALPHABET_DICT[char]
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 45, 55), border_radius=3)
            letter = FONT_SMALL.render(char, False, (255, 255, 255))
            surface = letter.get_rect(center=(x + 45/2, y + 55/2))
            screen.blit(letter, surface)
            x += 50
        y += 60

    # update the screen
    pygame.display.flip()

    for event in pygame.event.get():
        # closing the window stops the animation
        if event.type == pygame.QUIT:
            animating = False
        elif event.type == pygame.KEYDOWN:
            if AI and not GAME_OVER:
                
                # Integrate AI HERE
                INPUT = random.choice(words).upper()
                print("Shape in here")
                print(searchSpace.shape)
                print("Done")
                x = threading.Thread(target=getGuess, args=(len(GUESSES),))
                x.start()
                pygame.display.flip()
                x.join()
                INPUT = AI_GUESS.upper()
#                 print(color2trinary(validate(INPUT.lower())))

            # escape key to quit animation
            if event.type == pygame.K_ESCAPE:
                animating = False

            # backspace to correct user input
            if event.key == pygame.K_BACKSPACE:
                if len(INPUT) > 0:
                    INPUT = INPUT[:len(INPUT)-1]

            # return key to submit a guess
            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and INPUT.lower() in words:
                    GUESSES.append(INPUT)
                    COLORS.append(validate(INPUT.lower()))
                    TRINARY_COLORS.append(color2trinary(validate(INPUT.lower())))
                    for g, c in zip(GUESSES, COLORS):
                        for letter, rgb in zip(g, c):
                            if letter not in ALPHABET_DICT.keys():
                                ALPHABET_DICT[letter] = rgb
                    
                    # 
                    GAME_OVER = True if INPUT == ANSWER.upper() else False
                    INPUT = ""

            # space bar to restart
            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                ANSWER = random.choice(possible_answers)
                print(ANSWER)
                GUESSES = []
                COLORS = []
                TRINARY_COLORS = []
                ALPHABET_DICT = {}
                INPUT = ""
                searchSpace = wordDF.copy()
                if(not FORCE):
                    AI_GUESS = "RAISE"

            # regular text input
            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()


