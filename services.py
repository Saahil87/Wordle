import random
import collections


words = []
with open('data/words.txt') as f:
    for line in f:
        words.append(line.strip())

answer = random.choice(words)


def validate(guess):
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