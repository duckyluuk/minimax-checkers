# Import stuff
import math
from math import inf as infinity
import pygame
from copy import deepcopy

PLAYER = -1
COMPUTER = 1

# Game Configuration
aheadMoves = 6 # Maximum moves the bot thinks ahead
bigBoard = True # 8x8 or 10x10 board
hitBackwards = True # Whether normal pieces can hit backwards or not
startTurn = PLAYER # Define who starts the game
farJumpKing = True # Define whether the king can jump infinite tiles or not.

# Define python screen
pygame.init()

# Variables for screen drawing
screenWidth = 800
screenHeight = 800
size = (screenWidth, screenHeight)
screen = pygame.display.set_mode(size)

# Color variables
WHITE = (255,255,255)
LIGHTGRAY = (200, 200, 200)
DARKGRAY = (50, 50, 50)
BLACK = (0,0,0)
YELLOW = (255,255,0)
PLAYERCOLOR = (0,0,255)
COMPUTERCOLOR = (255,0,0)

# Define the starting position of the board
if bigBoard:
     gameBoard = [
        [0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,-1,0,-1,0,-1,0,-1,0,-1],
        [-1,0,-1,0,-1,0,-1,0,-1,0],
        [0,-1,0,-1,0,-1,0,-1,0,-1],
        [-1,0,-1,0,-1,0,-1,0,-1,0]
    ]
else:
    gameBoard = [
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [-1,0,-1,0,-1,0,-1,0],
        [0,-1,0,-1,0,-1,0,-1],
        [-1,0,-1,0,-1,0,-1,0]
    ]
    
# Render the board and pieces on the board
def renderBoard(board, highlightX, highlightY):
    height = screenHeight/len(board);
    width = screenWidth/len(board[0]);
    # Loop through each tile on the board
    for j in range(len(board)):
        for i in range(len(board[0])):
            # Board pattern
            if i%2 and not j%2 or not i%2 and j%2: # Odd tiles are black
                if i == highlightX and j == highlightY: color = DARKGRAY
                else: color = BLACK;
            else: # Even tiles are white
                if i == highlightX and j == highlightY: color = LIGHTGRAY
                else: color = WHITE;
            pygame.draw.rect(screen, color, (i*width,j*height,width,height), 0);

            # Piece rendering
            if gameBoard[j][i] != 0:
                if gameBoard[j][i] > 0: # Computer pieces are defined as 1 or 2
                    color = COMPUTERCOLOR;
                if gameBoard[j][i] < 0: # Player pieces are defined as -1 or -2
                    color = PLAYERCOLOR;

                # Draw the piece itself
                pygame.draw.circle(screen, color, (int(i*width+0.5*width), int(j*height+0.5*height)), int(0.4*width));
                # If the piece is a king, draw a gold outline around it
                if gameBoard[j][i] == 2 or gameBoard[j][i] == -2: 
                    pygame.draw.circle(screen, YELLOW, (int(i*width+0.5*width), int(j*height+0.5*height)), int(0.4*width), 5);
    # Update screen
    pygame.display.flip();

# Check if a space is empty and inside the board
def validMove(board, pX, pY, nX, nY):
    # First, check if the space is on the board
    if nX > -1 and nY > -1 and nX < len(board[0]) and nY < len(board):
        if board[nY][nX] == 0: # Then, check if it is empty
            return True;
    return False;

# Check in which directions a piece can move
def checkJump(board, turn, jumpList, moveHits, hitPieces, pX, pY, oX, oY):
    # Loop through each jump direction
    isKing = board[pY][pX] == 2*turn;
    if hitBackwards or isKing: jumpPositions = [[pX+2,pY+2,pX+1,pY+1],[pX-2,pY+2,pX-1,pY+1],[pX+2,pY-2,pX+1,pY-1],[pX-2,pY-2,pX-1,pY-1]]
    elif board[pY][pX] > 0: jumpPositions = [[pX+2,pY+2,pX+1,pY+1],[pX-2,pY+2,pX-1,pY+1]]
    else: jumpPositions = [[pX+2,pY-2,pX+1,pY-1],[pX-2,pY-2,pX-1,pY-1]]
    for jump in jumpPositions:
        # Set landing position and hit position
        nX = jump[0]
        nY = jump[1]
        hX = jump[2]
        hY = jump[3]
        # Check if the move is valid
        if validMove(board, pX, pY, nX, nY):
            jumpPiece = board[hY][hX]
            if jumpPiece == -turn or jumpPiece == -2*turn:
                # Add the move and hit piece to the list
                tempHitPieces = deepcopy(hitPieces)
                tempHitPieces.append([hX, hY])
                jumpList.append([oX, oY, nX, nY])
                moveHits.append(tempHitPieces)
                # Make copy of board for temporary move, then find all valid jumps from new position
                tempBoard = deepcopy(board);
                # Update the tested move on the board copy
                piece = tempBoard[pY][pX]
                tempBoard[pY][pX] = 0
                tempBoard[nY][nX] = piece
                tempBoard[hY][hX] = 0
                # Recursion for jumping over multiple pieces
                jumpList, moveHits = checkJump(tempBoard, turn, jumpList, moveHits, tempHitPieces, nX, nY, oX, oY)


    return jumpList, moveHits

# Get a list of moves from a King piece
def kingMoves(board, turn, pX, pY, oX, oY, validMoves, moveHits, curMoveHits, loop):
     onBoard = True
     moveDir = []
     # Find the directions the piece can move in
     if pX > 0 and pY > 0:
          moveDir.append([-1, -1])
     if pX > 0 and pY < len(board)-1:
          moveDir.append([-1, +1])
     if pX < len(board[0])-1 and pY > 0:
          moveDir.append([+1, -1])
     if pX < len(board[0])-1 and pY < len(board)-1:
          moveDir.append([+1, +1])

     for move in moveDir:
          stop = 0
          hit = False;
          # Temporarily copy board and hit list 
          tempMoveHits = deepcopy(curMoveHits)
          tempBoard = deepcopy(board)
          nX = pX
          nY = pY
          # Test in each direction until the piece hits an edge or blockade
          while stop < 2:
               
               nX = nX+move[0]
               nY = nY+move[1]
               # Stop if you hit the edge
               if nX<0 or nY< 0 or nX>=len(board[0]) or nY>=len(board): stop = 2
               if stop < 2:
                    if board[nY][nX] == 0:
                         # If you hit a piece, add the move as valid and recalculate each direction from new position
                         if hit:
                              # Add the move to the list of valid moves
                              validMoves.append([oX, oY, nX, nY])
                              moveHits.append(tempMoveHits)
                              # Update the tested move on the board copy
                              piece = tempBoard[pY][pX]
                              tempBoard[pY][pX] = 0
                              tempBoard[nY][nX] = piece
                              # Recursion, since a king piece can keep moving in a direction
                              validMoves, moveHits = kingMoves(tempBoard, turn, nX, nY, oX, oY, validMoves, moveHits, tempMoveHits, loop+1)
                         # If you are on the original first loop, each move that doesn't hit a piece is also valid
                         if loop == 0:
                              if not hit:
                                   # Add the move to the list of valid moves
                                   validMoves.append([oX, oY, nX, nY])
                                   moveHits.append([])
                                   # Update the tested move on the board copy
                                   piece = tempBoard[pY][pX]
                                   tempBoard[pY][pX] = 0
                                   tempBoard[nY][nX] = piece

                    # Check if you hit a piece          
                    elif board[nY][nX] == -turn or board[nY][nX] == -2*turn: # -turn will be a normal piece from the opponent player, 
                         stop = 1                                            # -2*turn will be a king piece from the opponent player.
                         # hX,hY are the coordinates of the hit piece
                         hX = nX
                         hY = nY
                         # nX, nY are updated to the spot behind the hit piece
                         nX = nX+move[0]
                         nY = nY+move[1]
                         # Check if the piece behind the hit piece is empty and inside the board
                         if nX<0 or nY< 0 or nX>=len(board[0]) or nY>=len(board):
                              stop = 2 # If the next spot is outside of the board, end the search
                         elif board[nY][nX] != 0:
                              stop = 2 # If there is another piece behind the hit piece, it cannot be hit, so end the search.
                         else:
                              # If nothing blocks the tile behind the hit piece, add the move to the list of valid moves.
                              stop = 0;
                              validMoves.append([oX, oY, nX, nY])
                              tempMoveHits.append([hX, hY])
                              moveHits.append(tempMoveHits)
                              hit = True
                              # Update temporary board
                              piece =  tempBoard[pY][pX]
                              tempBoard[pY][pX] = 0
                              tempBoard[nY][nX] = piece
                              tempBoard[hY][hX] = 0
                         # Undo the update to nX, nY
                         nX = nX-move[0]
                         nY = nY-move[1]
                    else: stop = 2 # If the piece is from the player that is moving, they cannot jump over it, so end the search.

     return validMoves, moveHits
# Get a list of valid moves for a single piece
def moveListPiece(board, turn, pX, pY):
    # validMoves stores all positions for valid moves
    validMoves = [];
    # moveHits stores the amount of pieces each valid move kills
    moveHits = [];

    # Check if the piece is a king
    isKing = board[pY][pX] == 2*turn;
    if not farJumpKing or not isKing:
         
         # Normal moves
         if validMove(board, pX, pY, pX+1, pY+turn):
             validMoves.append([pX, pY, pX+1, pY+turn]);
             moveHits.append([]);
         if validMove(board, pX, pY, pX-1, pY+turn):
             validMoves.append([pX, pY, pX-1, pY+turn]);
             moveHits.append([]);
         # King moves
         if isKing:
             if validMove(board, pX, pY, pX+1, pY-turn):
                 validMoves.append([pX, pY, pX+1, pY-turn]);
                 moveHits.append([]);
             if validMove(board, pX, pY, pX-1, pY-turn):
                 validMoves.append([pX, pY, pX-1, pY-turn]);
                 moveHits.append([]);
         
         # Attack moves
         tempBoard = deepcopy(board)
         jumpList, jumpMoveHits = checkJump(tempBoard, turn, [], [], [], pX, pY, pX, pY)
         for jump in jumpList:
             validMoves.append(jump)
         for hits in jumpMoveHits:
             moveHits.append(hits)
    else:
         validMoves, moveHits = kingMoves(board, turn, pX, pY, pX, pY, [], [], [], 0)
    return validMoves, moveHits;
    
# Get a list of valid moves for a player
def moveList(board, turn):
     validMoves = [];
     moveHits = []
     mostHits = 0;
     # Loop through the entire board
     for j in range(len(board)):
          for i in range(len(board[0])):
               # If the position on the board has a piece from the playing player,
               # find all the moves it can make.
               if board[j][i] == turn or board[j][i] == 2*turn:
                    # Find the moves for the piece
                    pieceMoves, pieceMoveHits = moveListPiece(board, turn, i, j);
                    # Add the moves to the list of total moves
                    for move in pieceMoves:
                         validMoves.append(move);
                    for hits in pieceMoveHits:
                         moveHits.append(hits)
                         if len(hits) > mostHits:
                              mostHits = len(hits)


     # Filter the moves for moves that are actually valid
     # Valid moves are only the moves which have the most hits.
     filterMoves = []
     filterHits = []
     
     for i in range(len(validMoves)):
          if len(moveHits[i]) == mostHits:
               filterMoves.append(validMoves[i])
               filterHits.append(moveHits[i])
     
     
     return filterMoves, filterHits;

# Turn of player
def playerTurn(board):
    # Get the list of valid moves
    validMoves, moveHits = moveList(board, PLAYER);
    startX = -1;
    startY = -1;
    endX = -1;
    endY = -1;
    
    move = [startX, startY, endX, endY];
    
    # Width and height of a cell
    height = screenHeight/len(board);
    width = screenWidth/len(board[0]);
    index = -1
    
    # Repeat until the player enters a valid move
    while index < 0:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                # Get click position
                pos = pygame.mouse.get_pos()
                xCell = math.floor(pos[0]/width)
                yCell = math.floor(pos[1]/height)
                # If no tile is selected yet, select the clicked tile
                if startX == -1 or startY == -1:
                    startX = xCell
                    startY = yCell
                # If the selected tile is clicked, unselect it
                elif xCell == startX and yCell == startY:
                    startX = -1
                    startY = -1
                # If a piece is already selected, and an unselected tile is clicked, do the move
                else:
                    endX = xCell
                    endY = yCell


                move = [startX, startY, endX, endY];

                # Check if the move is valid
                try: index = validMoves.index(move)
                except ValueError: index = -1
                # If the move is not valid, reset the selected end position
                if index < 0 and startX > -1 and startY > -1 and endX > -1 and endY > -1:
                    endX = -1
                    endY = -1
                # Redraw the board to update the selected tiles
                renderBoard(board, startX, startY)

    # Execute the move
    move = validMoves[index];
    hitPieces = moveHits[index];
    board = makeMove(board, move, hitPieces);
    # Draw the board
    renderBoard(board, -1, -1);
    print(boardString(board))
    # Start the computer turn
    computerTurn(board);

# Turn of computer
def computerTurn(board):
    # Find the best move
    best = minimax(board, aheadMoves, COMPUTER, -infinity, infinity)
    move = best[0]
    hitPieces = best[1]

    # Make the found move
    board = makeMove(board, move, hitPieces)

    # Draw the board
    renderBoard(board, -1, -1);
    print(boardString(board))

    # Start the player turn
    playerTurn(board);

# Evaluate how good a board state is for the bot
def evaluate(board):
    score = 0;
    # Calculate the sum of all values on the board
    for row in board:
        for value in row:
            score += value;
    return score;

def minimax(board, layers, turn, alpha, beta):
    if layers == 0:
        score = evaluate(board);
        return [[], [], score];
    # When it is the computer's turn, higher score is better,
    #when it is the player's turn, lower score is better
    if turn == COMPUTER: best = [[], [], -infinity];
    else: best = [[], [], +infinity];

    validMoves, moveHits = moveList(board, turn)
    # Loop through each move
    for i in range(len(validMoves)):
        # Make a temporary copy of the board and make the move on this copy
        tempBoard = deepcopy(board)
        move = validMoves[i]
        hitPieces = moveHits[i]
        tempBoard = makeMove(tempBoard, move, hitPieces)
        # Evaluate new board
        score = minimax(tempBoard, layers-1, -turn, alpha, beta);
        score[0] = move;
        score[1] = hitPieces;
        # When it is the computer's turn, higher score is better
        if turn == COMPUTER:
            alpha = max(alpha, score[2])
            if score[2] > best[2]:
                best = score
            if beta <= alpha: break;
        # When it is the player's turn, lower score is better
        else:
            beta = min(beta, score[2])
            if score[2] < best[2]:
                best = score
            if beta <= alpha: break;
    # Return the best move
    return best;

# Execute the given move
def makeMove(board, move, hitPieces):
    # Find the piece being moved
    piece = board[move[1]][move[0]];
    # Remove the piece from the old position
    board[move[1]][move[0]] = 0;
    # Promote the piece to a king if it is on the end of the board
    if piece == 1 and move[3] == len(board) - 1:
        piece = 2
    if piece == -1 and move[3] == 0:
        piece = -2
    # Place the piece in the new position
    board[move[3]][move[2]] = piece;

    # Remove the pieces that were hit from the board
    for piece in hitPieces:
        board[piece[1]][piece[0]] = 0;
    
    return board;
    
# Turn the board into a single string (unique per board configuration)
def boardString(board):
    string = ""
    last = 0
    same = 0
    types = ["O","o","_","x","X"]
    # Loop through each tile on the board
    for y in range(len(board)):
         for x in range(len(board[y])):
              # Only check for tiles on the board that can actually be played on
              if x%2 and not y%2 or not x%2 and y%2:
                   # Get the symbol for the piece in the position of the board
                   piece = types[board[y][x] + 2]
                   # Check if the last piece was the same as the current piece
                   if last == 0:
                        # If this is the first piece, start counting
                        last = piece
                        same = 1
                   elif last == piece:
                        same += 1 # Increase sum of same pieces
                   # If this piece is different from the previous one,
                   # Add the previous one to the string and start counting for the new piece
                   else:
                        if same > 1:
                             string = string + str(same)
                        string = string + last
                        last = piece
                        same = 1
    # Add last piece to the string
    if same > 1:
        string = string + str(same)
        string = string + last                     
    return string;

# Initiate the game
renderBoard(gameBoard, -1, -1)
if startTurn == PLAYER:
     playerTurn(gameBoard)
else:
     computerTurn(gameBoard)

