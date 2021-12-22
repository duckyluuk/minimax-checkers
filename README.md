# minimax-checkers

This program can play checkers against a human player, using the minimax algorithm with alpha-beta pruning.

## Playing the game

- run the python file. Make sure you have the [pygame](https://www.pygame.org/) library installed. 
- When it is your turn, select one of your pieces by clicking it.
- After selecting a piece, click a tile to move this piece to.
- Only valid moves will be executed, if a move is invalid nothing will happen.
- To unselect a piece, click it again.
- The last made move will be highlighted, as well as the pieces killed by that move.

## Settings

The game has various settings that can be changed. These can be edited near the top of the python file. The different settings are:

- aheadMoves: Change the amount of moves that the bot can look ahead.
  - The higher this is set, the further the bot looks ahead and the harder it will be to win.
  - It is reccomended to set this value between 3 and 8. Depending on how strong your computer is, values above 6 can take a long time to calculate a move.
- bigBoard: Change the size of the game board.
  - If this is set to True, the game will be played on a 10x10 board. (International Checkers / Draughts)
  - If this is set to False, the game will be played on an 8x8 board. (American Checkers)
- hitBackwards: Define whether normal pieces can hit backwards or not. (This rule varies between different checkers variants)
- startTurn: Defines which player starts. Set to either PLAYER or COMPUTER.
- farJumpKing: Define whether a king piece can jump infinite tiles or not.
  - If this is set to True, a king piece can jump for any distance diagonally in any direction, as long as normal movement rules apply. (International Checkers / Draughts)
  - If this is set to false, a king piece can move like a normal piece, with the only difference being that it can also move backwards by one tile. ( American Checkers)
