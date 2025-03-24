# 15 Puzzle Game

The 15 Puzzle is a classic sliding puzzle that consists of a 4x4 grid with 15 numbered tiles and one empty space. The objective is to arrange the tiles in ascending numerical order by making sliding moves that use the empty space.

![15 Puzzle Screenshot 1](screenshots/en/01.png)
![15 Puzzle Screenshot 2](screenshots/en/03.png)

## How to Play

1. **Starting the Game:**
   - Launch the 15 Puzzle game application.&#8203;:contentReference[oaicite:0]{index=0}
   - :contentReference[oaicite:1]{index=1}&#8203;:contentReference[oaicite:2]{index=2}

2. **Objective:**
   - :contentReference[oaicite:3]{index=3}&#8203;:contentReference[oaicite:4]{index=4}

3. **Controls:**
   - :contentReference[oaicite:5]{index=5}&#8203;:contentReference[oaicite:6]{index=6}
   - :contentReference[oaicite:7]{index=7}&#8203;:contentReference[oaicite:8]{index=8}

4. **Winning the Game:**
   - :contentReference[oaicite:9]{index=9}&#8203;:contentReference[oaicite:10]{index=10}

How to use?
===========

Fifteen Puzzle game can be run on the Sugar desktop. Please refer to;

* [How to Get Sugar on sugarlabs.org](https://sugarlabs.org/),
* [How to use Sugar](https://help.sugarlabs.org/)


How to run?
=================

Dependencies:- 
- Python >= 3.10
- PyGObject >= 3.42
- PyGame >= 2.5
  
These dependencies need to be manually installed on Debian, Ubuntu and Fedora distributions.


**Running outside Sugar**


- Install the dependencies

- Clone the repo and run -
```
git clone https://github.com/Bishoywadea/FifteenPuzzle
cd FifteenPuzzle
python main.py
```

**Running inside Sugar**

- Open Terminal activity and change to the Fifteen Puzzle activity directory
```
cd activities\FifteenPuzzle.activity
```
- To run
```
sugar-activity3 .
```
