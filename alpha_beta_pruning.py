from tkinter import *
import math
import time 

#GLOBAL VARIBLES

#Types of moves
#------
PLAIN = 0
CANTER = 1
CAPTURE = 2
#------

#Types of spaces
#------
WHITE = -2
BLACK = 2
EMPTY = 0
INVALID = -1
#------

#Buttons array
buttons = []
board = []
whitePieces = []
blackPieces = []

#Useful globals
playerTurn = WHITE
startButtons = []
picking = 0
startPosition = []
currentMoveList = []
typeOfMove = INVALID
visited = []
minPruning = 0
maxPruning = 0
totalNodes = 0
root = None

#Difficulty
mode = 0
EASY = 1
MEDIUM = 2
HARD = 3
MAX_DEPTH = 0

theTime = time.time()

#Returns list of moves that can be made by the piece at the position given the board state
#Parameters: board = current game board
#            position = a (y,x) coordinate in the board
#            successive = only used if successive moves are made, (True, moveType,visitedList)
def getMoves(board, position, successive = (False,0,[])):
    moveList = []
    if(successive[0] == True and successive[1] == CANTER): #for successive cantering moves
        moveList += getCanteringMoves(board,position)
        removeVisited(moveList,successive[2])
    elif(successive[0] == True and successive[1] == CAPTURE): #for successive capturing moves
        moveList += getCapturingMoves(board,position)
        removeVisited(moveList,successive[2])
    else:
        moveList += getCapturingMoves(board,position)   #everything else
        if(len(moveList) == 0):
            moveList += getCanteringMoves(board,position)
            moveList += getAdjacentMoves(board,position)
    return moveList

#Removes positions already visited when cantering or capturing
def removeVisited(moveList,visited):
    toPop = []
    for x,y in visited:
        move = 0
        while( move < len(moveList)):
            if(x == moveList[move][0] and y == moveList[move][1]):
                moveList.pop(move)
            else:
                move+=1
                            

#Return type: list of tuples (yPosition,xPosition,PLAIN)
def getAdjacentMoves(board, position):
    moveList = []
    if(board[position[0]+1][position[1]] == EMPTY):    #ONE BELOW
       moveList.append((position[0]+1,position[1],PLAIN))
    if(board[position[0]-1][position[1]] == EMPTY):    #ONE ABOVE
       moveList.append((position[0]-1,position[1],PLAIN))
    if(board[position[0]][position[1]+1] == EMPTY):   #ONE TO THE RIGHT
       moveList.append((position[0],position[1]+1,PLAIN))
    if(board[position[0]][position[1]-1] == EMPTY):   #ONE TO THE LEFT
       moveList.append((position[0],position[1]-1,PLAIN))

    if(board[position[0]-1][position[1]-1] == EMPTY): #TOP LEFT
       moveList.append((position[0]-1,position[1]-1,PLAIN))
    if(board[position[0]-1][position[1]+1] == EMPTY): #TOP RIGHT
       moveList.append((position[0]-1,position[1]+1,PLAIN))

    if(board[position[0]+1][position[1]-1] == EMPTY): #BOTTOM LEFT
       moveList.append((position[0]+1,position[1]-1,PLAIN))
    if(board[position[0]+1][position[1]+1] == EMPTY): #BOTTOM RIGHT
       moveList.append((position[0]+1,position[1]+1,PLAIN))

    return moveList
    

#Return type: list of tuples (yPosition,xPosition,CAPTURE,enemy_yposition,enemy_xposition )
def getCapturingMoves(board,position):
    player = board[position[0]][position[1]]
    enemy = -player
    moveList = []

    #ENEMY DIRECTLY ABOVE, EMPTY SPACE 2 SPACES ABOVE
    if(board[position[0]-1][position[1]] == enemy and board[position[0]-2][position[1]] == EMPTY):
        moveList.append((position[0]-2,position[1],CAPTURE, position[0]-1, position[1]))

    #ENEMY DIRECTLY BELOW, EMPTY SPACE 2 SPACES BELOW
    if(board[position[0]+1][position[1]] == enemy and board[position[0]+2][position[1]] == EMPTY):
        moveList.append((position[0]+2,position[1],CAPTURE, position[0]+1, position[1]))

    #ENEMY DIRECTLY LEFT, EMPTY SPACE 2 SPACES LEFT
    if(board[position[0]][position[1]-1] == enemy and board[position[0]][position[1]-2] == EMPTY):
        moveList.append((position[0],position[1]-2,CAPTURE, position[0], position[1]-1))

    #ENEMY DIRECTLY RIGHT, EMPTY SPACE 2 SPACES RIGHT
    if(board[position[0]][position[1]+1] == enemy and board[position[0]][position[1]+2] == EMPTY):
        moveList.append((position[0],position[1]+2,CAPTURE, position[0], position[1]+1))

    #ENEMY AT TOP LEFT, EMPTY SPACE 2 SPACES UP, 2 SPACES LEFT
    if(board[position[0]-1][position[1]-1] == enemy and board[position[0]-2][position[1]-2] == EMPTY):
        moveList.append((position[0]-2,position[1]-2,CAPTURE, position[0]-1, position[1]-1))

    #ENEMY AT TOP RIGHT, EMPTY SPACE 2 SPACES UP, 2 SPACES LEFT
    if(board[position[0]-1][position[1]+1] == enemy and board[position[0]-2][position[1]+2] == EMPTY):
        moveList.append((position[0]-2,position[1]+2,CAPTURE, position[0]-1, position[1]+1))
    
    #ENEMEY AT BOTTOM LEFT, EMPTY SPACE 2 SPACES DOWN, 2 SPACES LEFT
    if(board[position[0]+1][position[1]-1] == enemy and board[position[0]+2][position[1]-2] == EMPTY):
        moveList.append((position[0]+2,position[1]-2,CAPTURE, position[0]+1, position[1]-1))

    #ENEMY AT BOTTOM RIGHT, EMPTY SPACE 2 SPACES DOWN, 2 SPACES RIGHT
    if(board[position[0]+1][position[1]+1] == enemy and board[position[0]+2][position[1]+2] == EMPTY):
        moveList.append((position[0]+2,position[1]+2,CAPTURE, position[0]+1, position[1]+1))
        
    return moveList




#Return type: list of tuples (yPosition,xPosition,CANTER)
def getCanteringMoves(board,position):
    player = board[position[0]][position[1]]
    ally = player
    moveList = []

    #ALLY DIRECTLY ABOVE, EMPTY SPACE 2 SPACES ABOVE
    if(board[position[0]-1][position[1]] == ally and board[position[0]-2][position[1]] == EMPTY):
        moveList.append((position[0]-2,position[1],CANTER))

    #ALLY DIRECTLY BELOW, EMPTY SPACE 2 SPACES BELOW
    if(board[position[0]+1][position[1]] == ally and board[position[0]+2][position[1]] == EMPTY):
        moveList.append((position[0]+2,position[1],CANTER))

    #ALLY DIRECTLY LEFT, EMPTY SPACE 2 SPACES LEFT
    if(board[position[0]][position[1]-1] == ally and board[position[0]][position[1]-2] == EMPTY):
        moveList.append((position[0],position[1]-2,CANTER))

    #ALLY DIRECTLY RIGHT, EMPTY SPACE 2 SPACES RIGHT
    if(board[position[0]][position[1]+1] == ally and board[position[0]][position[1]+2] == EMPTY):
        moveList.append((position[0],position[1]+2,CANTER))

    #ALLY AT TOP LEFT, EMPTY SPACE 2 SPACES UP, 2 SPACES LEFT
    if(board[position[0]-1][position[1]-1] == ally and board[position[0]-2][position[1]-2] == EMPTY):
        moveList.append((position[0]-2,position[1]-2,CANTER))

    #ALLY AT TOP RIGHT, EMPTY SPACE 2 SPACES UP, 2 SPACES LEFT
    if(board[position[0]-1][position[1]+1] == ally and board[position[0]-2][position[1]+2] == EMPTY):
        moveList.append((position[0]-2,position[1]+2,CANTER))
    
    #ALLY AT BOTTOM LEFT, EMPTY SPACE 2 SPACES DOWN, 2 SPACES LEFT
    if(board[position[0]+1][position[1]-1] == ally and board[position[0]+2][position[1]-2] == EMPTY):
        moveList.append((position[0]+2,position[1]-2,CANTER))

    #ALLY AT BOTTOM RIGHT, EMPTY SPACE 2 SPACES DOWN, 2 SPACES RIGHT
    if(board[position[0]+1][position[1]+1] == ally and board[position[0]+2][position[1]+2] == EMPTY):
        moveList.append((position[0]+2,position[1]+2,CANTER))
        
    return moveList


#Changes board,and pieces array to match the move made
def makeMove(board, position,move,whitePieces,blackPieces):
    
    player = board[position[0]][position[1]]
    if(move[2] == PLAIN):
        board[position[0]][position[1]] = 0
        board[move[0]][move[1]] = player
        
    elif(move[2] == CANTER):
        board[position[0]][position[1]] = 0
        board[move[0]][move[1]] = player

    elif(move[2] == CAPTURE):
        board[position[0]][position[1]] = 0
        board[move[0]][move[1]] = player
        board[move[3]][move[4]] = 0
        if(player == WHITE):
            removePiece(blackPieces, (move[3],move[4]))
        elif(player == BLACK):
            removePiece(whitePieces, (move[3],move[4]))

    if(player == WHITE):
        removePiece(whitePieces, position)
        whitePieces.append((move[0],move[1]))
    elif(player == BLACK):
        removePiece(blackPieces, position)
        blackPieces.append((move[0],move[1]))

    

#Used to connect final move position to the other information in a move
def findMoveInMoveList(moveList, position):
    for move in moveList:
        if (move[0] == position[0] and move[1] == position[1]):
            return move

#Removes a single item from a playerpieces array
def removePiece(pieceList,position):
    index = -1
    for piece in range(len(pieceList)):
        if(pieceList[piece][0] == position[0] and pieceList[piece][1] == position[1]):
            index = piece
    pieceList.pop(index)


#All the checks to see if a game should continue or end
def checkToContinue(board, whitePieces, blackPieces):
    
    if(board[1][3] == BLACK and board[1][4] == BLACK): #CHECK WHITE CASTLE
        return (False,BLACK)
    elif(board[14][4] == WHITE and board[14][5] == WHITE):  #CHECK BLACK CASTLE
        return (False, WHITE)

    if(len(whitePieces) == 0):  #CHECK WHITE PIECES REMAINING
        return (False,BLACK)
    elif(len(blackPieces) == 0): #CHECK BLACK PIECES REMAINING
        return (False,WHITE)

    if(len(whitePieces) == 1 and len(blackPieces) == 1): #CHECK IF TIE
        return (False,INVALID)

    return (True,INVALID)

#Checks which buttons to enable since only capture buttons should be enabled
def buttonsToEnable(board,pieces):
    canCapture = False
    availablePieces = []
    for move in pieces:
        if(getMoves(board,move)[0][2] == CAPTURE):  #gets the first move and type of that move
            canCapture = True
            availablePieces.append(move)

    if(canCapture == True):
        return availablePieces
    else:
        return pieces
    

#Ends the game and declares the winner
def endTheGame(text):
    print("Game ended. " + text)
    root.destroy()

#Makes the black player move its pieces
def makeBlackPlayerMove(board,whitePieces,blackPieces):
    result = alphaBetaSearch(board,whitePieces,blackPieces)
    makeMove(board,result[0],result[1],whitePieces,blackPieces)

    if(result[1][2] == CAPTURE):
        
        return (CAPTURE,result[0],result[1])
    else:
        return (INVALID,result[0],result[1])
    

#The alpha beta search used to make black player's moves
def alphaBetaSearch(board,whitePieces,blackPieces):
    global minPruning, maxPruning, totalNodes
    minPruning = 0
    maxPruning = 0
    treeDepth = 0
    totalNodes = 0
    theTime = time.time()
    v = maxValue(board,whitePieces,blackPieces,float("-inf"),float("inf"),0)
    print("Min Pruned", minPruning)
    print("Max pruned", maxPruning)
    print("Total Nodes", totalNodes)
    print("Depth limit", MAX_DEPTH)
    print()
    return (v[2],v[1])
    
#Max Value function of alphabetasearch
#returns (utility_value, moveChosen, pieceChosen)
def maxValue(board,whitePieces,blackPieces,alpha,beta,treeDepth):
    global maxPruning, theTime, totalNodes
    totalNodes+=1
    
    
    #Checks terminal nodes
    answer = checkToContinue(board,whitePieces,blackPieces)
    if(answer[0] == False):
        if(answer[1] == BLACK):
            return (100,0)
        elif(answer[1] == WHITE):
            return (-100,0)
        elif(answer[1] == INVALID):            
            return (0,0)

    #Implements the depth limit
    if(treeDepth >= MAX_DEPTH):
        evaluate = evaluationFunction(board,whitePieces,blackPieces)
        return (evaluate,1)
    
    v = float("-inf")
    movable = buttonsToEnable(board,blackPieces)
    moveList = []
    
    for piece in movable:   #gets all the pieces that can be moved
        moveList += getMoves(board,piece)
        for action in moveList:       #gets all the moves that a single piece can make  
            tempBoard = []
            for a in board:           #creates copies of board, and pieces
                tempBoard.append(a[:])
                
            tempWhite = whitePieces[:]
            tempBlack = blackPieces[:]
            
            makeMove(tempBoard,(piece[0],piece[1]),action,tempWhite,tempBlack)
            res = minValue(tempBoard,tempWhite,tempBlack,alpha,beta,treeDepth+1)

            if(v < res[0]):
                v = res[0]
                move = action
                finalPosition = piece
                
            if v >= beta:   #prunes in the max function
                maxPruning += 1
                return (v,move,finalPosition)
            
            alpha = max(alpha,v)
            
        moveList = []

    
        
    return (v,move,finalPosition)
        

#Min value function of alpha beta search
#Returns (utility_value, moveChosen, pieceChosen) 
def minValue(board,whitePieces,blackPieces,alpha,beta,treeDepth):
    global minPruning, theTime, totalNodes
    totalNodes += 1
    
    
    
    answer = checkToContinue(board,whitePieces,blackPieces)
    if(answer[0] == False):
        if(answer[1] == BLACK):
            return (100,0)
        elif(answer[1] == WHITE):
            return (-100,0)
        elif(answer[1] == INVALID):
            return (0,0)

    #Implements the depth limit
    if(treeDepth >= MAX_DEPTH):
        evaluate = evaluationFunction(board,whitePieces,blackPieces)
        return (evaluate,1)
        
    v = float("inf")
    movable = buttonsToEnable(board,whitePieces)
    moveList = []
    
    for piece in movable:            #gets the pieces that can move
        moveList += getMoves(board,piece)

        for action in moveList:      #finds all the moves of each piece
            tempBoard = []
            for a in board:             #creates copies of the board and pieces
                tempBoard.append(a[:])
                
            tempWhite = whitePieces[:]
            tempBlack = blackPieces[:]

            makeMove(tempBoard, (piece[0],piece[1]),action,tempWhite,tempBlack)
            res = maxValue(tempBoard,tempWhite,tempBlack,alpha,beta,treeDepth+1)

            if(res[0] < v):
                v = res[0]
                move = action
                finalPosition = piece
                
            if v <= alpha:      #prunes in the min function
                minPruning+=1
                return (v,move,finalPosition)
            
            beta = min(beta,v)
            
        moveList = []
    
    return (v,move,finalPosition)


#Function used to calculate utility value when depth limit is reached
def evaluationFunction(board,whitePieces,blackPieces):
    num = 30                    #a starting value for the evaluation function
    num += len(blackPieces)*5   #higher when more black pieces are present
    num += len(whitePieces)*-5  #higher when less white pieces are present

    min1 = 16    
    for black in blackPieces: #finds the minimum in the y axis
        if(black[0] < min1):
            min1 = black[0]

    min2 = 16
    for black in blackPieces:   #finds the 2nd lowest minimum on the y axis
        if(black[0] < min2 and black[0] > min1):
            min2 = black[0]

    num += 10/(min1+min2)   #higher when the pieces are closer to the enemy castle

    return num
    
    
    

#Preliminary code to set up a game board and GUI for player
def makeGameBoard():
    global buttons,board,whitePieces,blackPieces,playerTurn,startButtons, root

    
    root = Tk()
    topFrame = Frame(root)

    #Buttons for player to choose if they are first or second
    goFirstButton = Button(topFrame,width=5,height=2,background="white",command=lambda:chooseGoingFirst(1),text="First")
    goSecondButton = Button(topFrame,width=5,height=2,background="white",command=lambda:chooseGoingFirst(2),text="Second")

    easyDifficulty = Button(topFrame,width=5,height=2,background="white",command=lambda:chooseDifficulty(EASY),text="Easy",state=DISABLED)
    mediumDifficulty = Button(topFrame,width=5,height=2,background="white",command=lambda:chooseDifficulty(MEDIUM),text="Medium",state=DISABLED)
    hardDifficulty = Button(topFrame,width=5,height=2,background="white",command=lambda:chooseDifficulty(HARD),text="Hard",state=DISABLED)
    
    startButtons.append(goFirstButton)
    startButtons.append(goSecondButton)
    startButtons.append(easyDifficulty)
    startButtons.append(mediumDifficulty)
    startButtons.append(hardDifficulty)

    topFrame.pack(side=TOP)
    goFirstButton.pack(side=LEFT)
    goSecondButton.pack(side=LEFT)
    easyDifficulty.pack(side=LEFT)
    mediumDifficulty.pack(side=LEFT)
    hardDifficulty.pack(side=LEFT)
    
    
    #Makes array of buttons for GUI
    botFrame = Frame(root)
    botFrame.pack(side=BOTTOM)
    for y in range(16):
        buttons.append([])
        for x in range(10):
            aButton = Button(botFrame,width=4,height=2,background="white")
            aButton.grid(row=y,column=x)
            b = lambda row=y, column=x : onButtonPress((row,column))
            aButton.config(command=b,state=DISABLED)
            buttons[y].append(aButton)

    
    #THIS IS A (Y,X) GRID
    
    board = [[-1,-1,-1,-1, -1,-1, -1,-1,-1,-1],   #0
             [-1,-1,-1,-1,  0,0,  -1,-1,-1,-1],   #1
             [-1,-1,-1,   0,0,0,0,   -1,-1,-1],   #2
             [-1,-1,    0,0,0,0,0,0,    -1,-1],   #3
             [-1,     0,0,0,0,0,0,0,0,  -1],   #4
             [-1,     0,0,1,1,1,1,0,0,  -1],   #5
             [-1,     0,0,0,1,1,0,0,0,  -1],   #6
             [-1,     0,0,0,0,0,0,0,0,  -1],   #7
             [-1,     0,0,0,0,0,0,0,0,  -1],   #8
             [-1,     0,0,0,2,2,0,0,0,  -1],   #9
             [-1,     0,0,2,2,2,2,0,0,  -1],   #10
             [-1,     0,0,0,0,0,0,0,0,  -1],   #11
             [-1,-1,    0,0,0,0,0,0,    -1,-1],   #12
             [-1,-1,-1,   0,0,0,0,   -1,-1,-1],   #13
             [-1,-1,-1,-1,  0,0,  -1,-1,-1,-1],   #14
             [-1,-1,-1,-1, -1,-1, -1,-1,-1,-1]]   #15

    #loop below is to change all 1's to -2's. One looks better for formatting, but -2 is better for code
    for y in range(len(board)):  
        for x in range(len(board[y])):
            if(board[y][x] == 1):
                board[y][x] = -2

    
    root.mainloop()


    
def onButtonPress(position):
    global buttons,board,whitePieces,blackPieces,playerTurn,picking, startPosition, currentMoveList,typeOfMove,visited
    #Statement below runs when it is the player's turn and they want to pick a piece to move
    if(playerTurn == WHITE and picking == 0):
        moveList = getMoves(board,position)
      
        for move in moveList:
            buttons[move[0]][move[1]].config(background="brown",state=NORMAL)


        startPosition = position

        for piece in whitePieces:
            buttons[piece[0]][piece[1]].config(state=DISABLED)
            
        buttons[startPosition[0]][startPosition[1]].config(background="cyan", state=NORMAL)
        currentMoveList = moveList
        picking = 1

    #Runs when player picked a piece to move and now wants to move it to a spot
    elif(playerTurn == WHITE and picking == 1):
        #When a player picked a piece and clicked that same piece again
        if(position[0] == startPosition[0] and position[1] == startPosition[1]):
            #If the player was successively cantering or capturing and they click the piece again, they stop moving
            if(typeOfMove == CANTER or typeOfMove == CAPTURE):
                buttons[position[0]][position[1]].config(background="white",state=DISABLED)
                visited = []
                picking = 0
                playerTurn = BLACK
            #If player wants to move a different piece instead
            else:
                buttons[position[0]][position[1]].config(background="white")
                whiteButtons = buttonsToEnable(board,whitePieces)
                for piece in whiteButtons:
                    buttons[piece[0]][piece[1]].config(state=NORMAL)

            picking = 0
            for move in currentMoveList:
                buttons[move[0]][move[1]].config(background="purple",state=DISABLED)
            
            
        #Once the player has clicked a different place to move to
        else:
            theMove = findMoveInMoveList(currentMoveList,position)
            for move in currentMoveList:
                buttons[move[0]][move[1]].config(background="purple",state=DISABLED)
            makeMove(board,startPosition,theMove,whitePieces,blackPieces)
    
            buttons[startPosition[0]][startPosition[1]].config(background="purple",state=DISABLED)
            typeOfMove = theMove[2]
            currentMoveList = []
            
            #Checks if the game should end at the end of each activity            
            results = checkToContinue(board,whitePieces,blackPieces)
            if(results[0] == False):
                if(results[1] == WHITE):
                    endTheGame("WHITE WINS!")
                else:
                    endTheGame("BLACK WINS!")
                return


            
            #If the type of move was a canter of capture move, they can go again
            if(typeOfMove == CANTER or typeOfMove == CAPTURE):
                visited.append(startPosition)
                currentMoveList = getMoves(board,position,(True,typeOfMove,visited))

            
            if(typeOfMove == CANTER):
                #Type of move was a canter and more canters are available
                if(len(currentMoveList) > 0):
                    for move in currentMoveList:
                        buttons[move[0]][move[1]].config(background="brown",state=NORMAL)
                        
                    buttons[position[0]][position[1]].config(background="cyan",state=NORMAL)
                    startPosition = position
                    
                #No more moves are available, so move is basically a plain move
                else:
                    typeOfMove = PLAIN
                    
            if(typeOfMove == CAPTURE):
                buttons[theMove[3]][theMove[4]].config(background="purple",state=DISABLED) #Removes button color
                if(len(currentMoveList) > 0):
                    for move in currentMoveList:
                        buttons[move[0]][move[1]].config(background="brown",state=NORMAL)
                        
                    buttons[position[0]][position[1]].config(background="cyan",state=NORMAL)
                    startPosition = position
                else:
                    typeOfMove = PLAIN
                
                    
            if(typeOfMove == PLAIN):
                buttons[position[0]][position[1]].config(background="white",state=DISABLED)
                visited = []
                picking = 0
                playerTurn = BLACK

            

            


    if(playerTurn == BLACK):
        
        blackMove = makeBlackPlayerMove(board,whitePieces,blackPieces)
        buttons[blackMove[1][0]][blackMove[1][1]].config(background="purple")
        buttons[blackMove[2][0]][blackMove[2][1]].config(background="black")
        if(blackMove[0] == CAPTURE):
            buttons[blackMove[2][3]][blackMove[2][4]].config(background="purple")

        #Checks if the game should end at the end of each activity            
        results = checkToContinue(board,whitePieces,blackPieces)
        if(results[0] == False):
            if(results[1] == WHITE):
                endTheGame("WHITE WINS!")
            else:
                endTheGame("BLACK WINS!")
            return
        
        whiteButtons = buttonsToEnable(board,whitePieces)
        for piece in whiteButtons:
            buttons[piece[0]][piece[1]].config(state=NORMAL)


        playerTurn = WHITE
    
               
    
    
#Button command to allow player to go first or second
def chooseGoingFirst(turn):
    global buttons,board,whitePieces,blackPieces,playerTurn,startButtons

    if(turn == 1):
        playerTurn = WHITE
    else:
        playerTurn = BLACK

    startButtons[0].config(state=DISABLED)
    startButtons[1].config(state=DISABLED)
    startButtons[2].config(state=NORMAL)
    startButtons[3].config(state=NORMAL)
    startButtons[4].config(state=NORMAL)
    
    
#Button command to handle all difficulty buttons
def chooseDifficulty(difficulty):
    global buttons,board,whitePieces,blackPieces,playerTurn,startButtons, mode, MAX_DEPTH

    mode = difficulty
    MAX_DEPTH = mode*2-1

    #Loops through board array and populates whitePiece,blackPiece list.
    #Changes button configs(color,active) according to board array
    for y in range(len(board)):
        for x in range(len(board[y])):
            if(board[y][x] == -1):
                buttons[y][x].config(background="gray",state=DISABLED)
            elif(board[y][x] == -2):
                buttons[y][x].config(background="white")
                whitePieces.append((y,x))
                    
            elif(board[y][x] == 2):
                buttons[y][x].config(background="black")
                blackPieces.append((y,x))
                
            else:
                buttons[y][x].config(background="purple",state=DISABLED)

    
    startButtons[2].config(state=DISABLED)
    startButtons[3].config(state=DISABLED)
    startButtons[4].config(state=DISABLED)
    
    if(playerTurn == WHITE):
        whiteButtons = buttonsToEnable(board,whitePieces)
        for y,x in whiteButtons:
            buttons[y][x].config(state=NORMAL)
    else:
        onButtonPress(0)

                
    

makeGameBoard()



