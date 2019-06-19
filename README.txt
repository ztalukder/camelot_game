Zami Talukder
12/12/17
Instructions on AI Project
1. Install Python 3.5.1 through python website
2. Install idle with python 3.5.1
3. Run code on idle with python 3.5.1
4. Player must choose to go first or second before other options are made available
5. Player must choose difficulty of the AI
6. Player must pick on their piece and click on the highlighted places to move to
7. If cantering is possible, player has option to click highlighted position or click the same
piece again to stop moving
8. If player can capture, only the pieces that can capture will be enabled
9. Player can choose to capture multiple times or stop after one capture

High Level Description

This project uses Tkinter to implement graphics. A 2d array is used to store the
information in the board. Another 2d array is used to store the actual buttons that correspond
to the board array. The game starts by allowing players to click on the white pieces. After a
player chooses a white piece, they can click highlighted pieces to move to. Specific functions are
used to calculate which pieces can move and where those pieces can move to. After a player
moves to a position, the buttons are re-enabled after the black player moves. The color of the
buttons change to indicate that a piece has moved, actual buttons are not swapped in the
array.

The evaluation function looks at the black pieces and the number of white pieces. It
favors having more black pieces and having two of them being closer to the white castle. It
lowers the utility value when more white pieces are present. It largely favors looking at number
of pieces over looking at the position of the pieces.The levels of difficulty differ in the maximum depth level of the alpha beta search. The
hardest difficulty mode looks at a depth limit of 5, which takes around 10 seconds to calculate.
Looking at a depth level of 6 takes much longer than 10 seconds as the number of nodes in the
alpha beta search increases exponentially. Easy mode makes the depth limit 1 and medium
makes the depth limit 3. With this implementation, the AI differs in how many steps into the
future it looks into. The more it looks into the future, the better the AI is. Ideally, the AI would
be able to look at the terminal states in each turn, but searching to get to the terminal states
take much too long.

Successive canters and captures are also implemented. If the players wants to
successfully canter, the piece is already chosen and the board shows where the player can
move. The player cannot move to a place that they were previously in, in that same turn. The
turn ends when the player chooses to stop canter or stop capturing. If the player is capturing,
they can only do successive captures and no canters. If the player is cantering, they can only do
successive canters and no captures. The player can end their turn prematurely if they click on
the piece again.