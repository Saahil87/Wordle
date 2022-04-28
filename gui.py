"""
Source: https://www.youtube.com/watch?v=TsnovVfkafI
"""
import random
from collections import Counter
import pygame

words = []
with open('data/allowed_words.txt') as f:
    for line in f:
        words.append(line.strip())

possible_answers = []
with open('data/words.txt') as f:
    for line in f:
        possible_answers.append(line.strip())

ANSWER = random.choice(possible_answers)
print(ANSWER)


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


WIDTH = 600
HEIGHT = 700
MARGIN = 10
T_MARGIN = 100
B_MARGIN = 100
LR_MARGIN = 100

WHITE = (255, 255, 255)
GREY = (70, 70, 80)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)

INPUT = ""
GUESSES = []
COLORS = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

SQ_SIZE = (WIDTH-4*MARGIN-2*LR_MARGIN) // 5
FONT = pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQ_SIZE//2)


def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters = ""
    for l in ALPHABET:
        if l not in guessed_letters:
            unguessed_letters = unguessed_letters+l
    return unguessed_letters

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# animation loop
animating = True
while animating:

    # background
    screen.fill("black")
    letters = FONT_SMALL.render(UNGUESSED, False, WHITE)
    surface = letters.get_rect(center=(WIDTH // 2, T_MARGIN // 2))
    screen.blit(letters, surface)

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
        letters = FONT.render(ANSWER.upper(), False, WHITE)
        surface = letters.get_rect(center=(WIDTH//2, HEIGHT-B_MARGIN//2 - MARGIN))
        screen.blit(letters, surface)

    # update the screen
    pygame.display.flip()

    # track user interaction
    for event in pygame.event.get():

        # closing the window stops the animation
        if event.type == pygame.QUIT:
            animating = False
        elif event.type == pygame.KEYDOWN:
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
                    UNGUESSED = determine_unguessed_letters(GUESSES)
                    GAME_OVER = True if INPUT == ANSWER.upper() else False
                    INPUT = ""

            # space bar to restart
            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                ANSWER = random.choice(words)
                print(ANSWER)
                GUESSES = []
                COLORS = []
                UNGUESSED = ALPHABET
                INPUT = ""

            # regular text input
            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()
                # print(INPUT)
