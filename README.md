## Python Connect Four AI 
#### Nichil Stewart

### Overview:
Connect 4 game built in Python using Pygame graphics library. Game AI developed using 
Minimax algorithm with further optimized depth-traversal time using alpha-beta pruning. 

### Files:
To run: cd to game directory and type `python3 connect4_AI.py` in terminal.

Select difficult (depth-level of Minimax algorithm) 1-5 in console before launching 
graphical game interface. 

### Visuals:
<img src="https://raw.githubusercontent.com/nichilstewart/connect4-game-ai/main/imgs/ui.png" alt="Your image title" width="450"/>

<img src="https://raw.githubusercontent.com/nichilstewart/connect4-game-ai/main/imgs/game1.png" alt="Your image title" width="450"/>

<img src="https://raw.githubusercontent.com/nichilstewart/connect4-game-ai/main/imgs/game2.png" alt="Your image title" width="450"/>
 
### AI:
AI is developed using the Minimax algorithm with a custom heuristic scoring model. 
The game-tree traversal process if further optimized using Alpha-beta bruning to 
only select the best paths in evaluating the best move. Moves are scored using 
greatest sequence of adjacent pieces, even-odd positioning, and prioritizing the 
lower rows and center column positions.

