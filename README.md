<h1 align="center">IS 597 - Data Structures and Algorithms: Final Project - Wordle </h1>

## Background

<p align="center">
<img src = "./resources/ss.png" width="300">
</p>



Wordle is a web-based word game created and developed by Welsh software engineer Josh Wardle, and owned and published by The New York Times Company since 2022. Players have six attempts to guess a five-letter word, with feedback given for each guess in the form of colored tiles indicating when letters match or occupy the correct position. (description sourced from Wikipedia)

## Rising Popularity


Wordle has gained much popularity since the start of 2022. According to an <a href="https://theconversation.com/codecracking-community-and-competition-why-the-word-puzzle-wordle-has-become-a-new-online-obsession-174878"> article </a> by The Conversation. Wordle has nearly 3 million players across the world and versions of it are appearing in other languages. 


## Solving Wordle: Human Performance

With the growing popularity, the conversation of solving Wordle is a highly by individuals from various circles. A topic of much debate within the community is the choice of starting word. 


Below is a visualisation map depicting the average attempts it takes for a player to solve Wordle by country:


<p align="center">
<img src = "https://images.prismic.io/wordtips/1533ed82-0c9c-4953-a025-2aed8cc6e050_01-Wordle-Wizards_World-Map_Hi-RES.png?auto=compress,format&rect=0,0,2400,2127&w=800&h=709" width="600">
</p>


Below is a visualisation depicting the average attempts it takes for a player to solve Wordle on a city level:

<p align="center">
<img src = "https://images.prismic.io/wordtips/0464f2e0-f69f-458b-9a8f-80140f6da459_02_Wordle-Wizards_Top-10-Global-Cities.png?auto=compress,format&rect=0,0,1201,1904&w=800&h=1268" width="600">
</p>

Image Sources: <a href="https://word.tips/wordle-wizards/"> Word Tips </a>

## Solving Wordle: An Algorithmic Approach

For our final project we attempt to build an algorithm to solve Wordle.

### Iteration 0: The Naive Approach

For our first iteration, we attempted solve Wordle in the most naive possible way - Random Guessing. The approach is simple enough and easy to implement, but unsurprisingly performs poorly in practise. We performed simulations of all 2316 games (the size of the Wordle dictionary), and the solver was able to win very few games.

### Iteration 1: Constrained Filtering with Random Guessing

An improvement to build on our previous iteration involved solving the game more tactfully. This approach involved using the feedback (the letter colours) to reduce the search space for the next guess, thereby reducing the search space after every step and making guesses with slightly more finesse. While we reduced the search space with signficant effect, there was still an element of "randomness" with regards to choosing a word from the pool for the next guess.

Below we see a histogram depicting the performance of a simulation of this approach for all games:

<p align="center">
<img src = "./resources/info_constrained_filtering_histogram.jpg">
</p>
