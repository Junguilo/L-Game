class gameState:
    def __init__(self, prevState = None):
        if prevState != None:
            self.empty = prevState.empty.copy()
            self.full = prevState.full.copy()
            #Gets both L shapes
            self.Lshapes = {k: v.copy() for k, v in prevState.Lshapes.items()}
            self.neutrals = prevState.neutrals.copy()
            self.turn = prevState.turn
        else:
            self.initialize()
    def initialize(self):
        self.empty = set([(1,4),(2,1),(2,4),(3,1),(3,4),(4,1)])
        self.full = set([(1,1),(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(4,2),(4,3),(4,4)])
        self.Lshapes = {0: self.simpleCoords(1,3,'N'), 1: self.simpleCoords(4,2,'S')}
        self.neutrals = set([(1,1),(4,4)])
        self.turn = 0
    
    #able to add Lshape to board
    def simpleCoords(self, x, y, direction):
        Lshape = set()
        Lshape.add((x, y))
        #print((x, y))
        if direction == 'N':
            Lshape.add((x, y-1))
            if(x <=2):
                Lshape.add((x+1, y)) 
                Lshape.add((x+2, y))
            else:
                Lshape.add((x-1, y)) 
                Lshape.add((x-2, y)) 
        if direction == 'S':
            Lshape.add((x, y+1))
            if(x <=2):
                Lshape.add((x+1, y)) 
                Lshape.add((x+2, y))
            else:
                Lshape.add((x-1, y)) 
                Lshape.add((x-2, y)) 
        if direction == 'E':
            Lshape.add((x+1, y))
            if(y <=2):
                Lshape.add((x, y+1)) 
                Lshape.add((x, y+2))
            else:
                Lshape.add((x, y-1)) 
                Lshape.add((x, y-2)) 
        if direction == 'W':
            Lshape.add((x-1, y))
            if(y <=2):
                Lshape.add((x, y+1)) 
                Lshape.add((x, y+2))
            else:
                Lshape.add((x, y-1)) 
                Lshape.add((x, y-2))
        
        #print(Lshape)
        return Lshape 
    

    #will be used for the minimax, && 
    #Our win condition will be if the other player has 0 moves left in the board
    def checkValid(self, x, y, dir, old1 = None, old2 = None, new1 = None, new2 = None, player = None):
        if player is None:
            player = self.turn
       
        #chooses which player turn, either 0 or 1
        oldLshape = self.Lshapes[player]

        #tests input if its in bound of game space
        if not (1 <= x <= 4 and 1 <= y <= 4):
            #print("Coords out of bound")
            return False
        
        #Testing direction if its in bounds of game space
        newLshape = self.simpleCoords(x, y, dir)
        for pos in newLshape:
            if not (1 <= pos[0] <= 4 and 1 <= pos[1] <= 4):
                #print("Invalid placement: L-shape overlaps or is out of bounds.")
                return False
        
        #Checks if its the same as the old position now that we see that the new position is valid
        #clear old Lshape pos in prep for new pos
        for pos in oldLshape:
            self.empty.add(pos)
            self.full.discard(pos)
        #needs to place old Lshape back before every false

        #Checks if newpos is occupying any areas
        for pos in newLshape:
            if pos in self.full:
                #print("Cannot move to occupied area")

                #restore old Lshape
                for pos in oldLshape:
                    self.empty.discard(pos)
                    self.full.add(pos)
                return False

        #make sure new Lshape is different than old, not in any full spots, or the same as the other shape
        if newLshape == oldLshape:
            #restore old Lshape if move fails
            for pos in oldLshape:
                self.empty.discard(pos)
                self.full.add(pos)
            return False

        # Check neutral piece validity, if provided
        if old1 and old2:
            if not (1 <= new1 <= 4 and 1 <= new2 <= 4):
                #print("Coordinates for new neutral piece out of bounds.")
                #restore lshape
                for pos in oldLshape:
                    self.empty.discard(pos)
                    self.full.add(pos)
                return False
            if (new1, new2) in self.full:
                #print("Neutral piece cannot be placed inside another piece.")
                #restore lshape
                for pos in oldLshape:
                    self.empty.discard(pos)
                    self.full.add(pos)
                return False
            if (old1, old2) not in self.neutrals:
                #print("Original neutral piece position is invalid.")
                #restore lshape
                for pos in oldLshape:
                    self.empty.discard(pos)
                    self.full.add(pos)
                return False
            for pos in newLshape:
                if (new1, new2) == pos:
                    #restore lshape
                    for pos in oldLshape:
                        self.empty.discard(pos)
                        self.full.add(pos)
                    return False

        #restore old Lshape, since this is just a check, it will be modified in the play function
        for pos in oldLshape:
            self.empty.discard(pos)
            self.full.add(pos)

        
        return True

    # (x, y, dir) will move L block. (x1, y1, x2, x2) moves neutral piece from old spot to new
    def play(self, x, y, direction, old1 = None, old2 = None, new1 = None, new2 = None, changeTurn = True, player = None):
        if player is None:
            player = self.turn

        #Checks valid position
        if not self.checkValid(x, y, direction, old1, old2, new1, new2, player=player):
            return False

        # Remove old L-shape positions
        oldLshape = self.Lshapes[player]
        for pos in oldLshape:
            self.full.discard(pos)
            self.empty.add(pos)

        #generate Lshape
        newLshape = self.simpleCoords(x, y, direction)
        
        #Update Lshape and Board Positions
        self.Lshapes[player] = newLshape
        for pos in newLshape:
            self.empty.discard(pos)
            self.full.add(pos)

        #Update neutrals
        if old1 and old2:
            #update board pos in empty and full
            self.full.add((new1, new2))
            self.full.discard((old1, old2))
            self.empty.add((old1, old2))
            self.empty.discard((new1, new2))

            self.neutrals.discard((old1,old2))
            self.neutrals.add((new1,new2))

        #Change turn if we move an L piece
        if changeTurn:
            self.turn = (self.turn + 1) % 2
        return True
    
    #Checks every single empty space on the board
    #will return a num, will run on the game loop
    def checkPossible(self, player = None):
        if player is None:
            player = self.turn

        currentPlayer = self.Lshapes[player] 
        possibleMoves = []

        allEmptyBlocks = self.empty.union(currentPlayer)
        #allEmptyBlocksNeutral = self.allEmptyBlocks.union(neutral)
        directions = ['N', 'S', 'E', 'W']

        #Checks every single space on the board at every single direction if its possible to move
        #Checks emptyblocks + current block, will return list of actions the player can do
        for pos in allEmptyBlocks:
            x, y = pos
            for dir in directions:
                #First check if we are able to move the rectangle before dealing with neutral pieces
                if self.checkValid(pos[0], pos[1], dir, player=player):
                    possibleMoves.append((pos[0], pos[1], dir))

                for neutral in self.neutrals:
                    old1, old2 = neutral
                    for new_pos in self.empty:
                        if new_pos == (old1, old2):
                            continue
                        new1, new2 = new_pos
                        if self.checkValid(x, y, dir, old1, old2, new1, new2, player=player):
                            possibleMoves.append((x, y, dir, old1, old2, new1, new2))
    

        return possibleMoves


    def visualize(self):
        for i in range(1,5): # y board
            for j in range(1,5): # x board
                if (j,i) in self.empty:
                    print('#  ', end='')
                if (j,i) in self.Lshapes[0]:
                    print('1  ', end='')
                if (j,i) in self.Lshapes[1]:
                    print('2  ', end='')
                if (j,i) in self.neutrals:
                    print('N  ', end='')
                if j == 4:
                    print('\n', end='')
                    pass
    

    def isGameOver(self):
        return len(self.checkPossible()) == 0


    #Currently this only works for Player vs AI 
    # The CheckPossible is hardcoded
    def getAction(self, depth=3, player = None):
        if player is None:
            player = self.turn

        bestScore = float('-inf')
        bestAction = None
        alpha = float('-inf')
        beta = float('inf')


        for action in self.checkPossible(player = player):
            nextGameState = gameState(self)
            nextGameState.play(*action, changeTurn = False, player = player)
            nextGameState.turn = (player + 1) % 2

            score = nextGameState.minimax(depth - 1, alpha, beta, player = (player + 1) % 2)
            print(f"Evaluated action {action} with score {score}")
            
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)

        return bestAction

    def minimax(self, depth, alpha=float('-inf'), beta=float('inf'), player = None):
        if player is None:
            player = self.turn

        if self.isGameOver() or depth == 0:
            return self.evaluate()
        
        if player == 1:  #The Maximizing Player (usually AI)
            return self.Max(depth, alpha, beta, player)
        else:
            return self.Min(depth,alpha, beta, player)

    def Max(self, depth, alpha, beta, player):
        maxScore = float('-inf')

        possibleMoves = self.checkPossible(player=player)
        # # Evaluate and sort moves
        # scoredMoves = []
        # for action in possibleMoves:
        #     nextGameState = gameState(self)
        #     nextGameState.play(*action, changeTurn=False, player=player)
        #     score = nextGameState.evaluate()
        #     scoredMoves.append((score, action))

        # # Sort in descending order
        # scoredMoves.sort(reverse=True)


        for action in possibleMoves:
            nextGameState = gameState(self)
            #print(action)
            nextGameState.play(*action, changeTurn = False, player = player)
            nextGameState.turn = (player + 1) % 2
            score = nextGameState.minimax(depth - 1, player = (player + 1) % 2)
            maxScore = max(maxScore, score)
            alpha = max(alpha, maxScore)

            #prune
            if beta <= alpha:
                break

        return maxScore

    def Min(self, depth, alpha, beta, player):
        minScore = float('inf')

        possibleMoves = self.checkPossible(player=player)
        # # Evaluate and sort moves
        # scoredMoves = []
        # for action in possibleMoves:
        #     nextGameState = gameState(self)
        #     nextGameState.play(*action, changeTurn=False, player=player)
        #     score = nextGameState.evaluate()
        #     scoredMoves.append((score, action))

        # # Sort in ascending order
        # scoredMoves.sort()
        # #print("MIN", scoredMoves)


        for action in possibleMoves:
            nextGameState = gameState(self)
            #print(action)
            nextGameState.play(*action, changeTurn=False, player=player)
            nextGameState.turn = (player + 1) % 2
            score = nextGameState.minimax(depth - 1, player = (player + 1) % 2)
            minScore = min(minScore, score)

            beta = min(beta, minScore)

            if beta <= alpha:
                break

        return minScore

    def evaluate(self):
        aiMoves = len(self.checkPossible(player=1))
        humanMoves = len(self.checkPossible(player=0))
        return aiMoves - humanMoves



    #Will handle human v human
    def playGame(self):
        while True: 
            possibleMoves = self.checkPossible()
            possibleMovesLen = len(possibleMoves)
            if possibleMovesLen == 0:
                print("Player ", ((self.turn + 1) % 2) + 1, " Has Won!, Player ", ((self.turn + 2) % 2)+1, "has no available moves!")
                return False
            print("Possible Moves:", possibleMoves, '\n', "Possible Moves:" , possibleMovesLen)
            print("Player ", self.turn + 1, " turn: ")
            self.visualize()
            #input
            inp = input("Enter your input:").split()
            if len(inp) == 3:
                posX, posY = int(inp[0]), int(inp[1])
                dir = inp[2]
                self.play(posX, posY, dir)
            elif len(inp) == 7:
                posX, posY, NposX, NposY, NewNposX, NewNposY = int(inp[0]), int(inp[1]), int(inp[3]), int(inp[4]), int(inp[5]), int(inp[6])
                dir = inp[2]
                #NposX, NposY, NewNposX, NewNposY = input
                self.play(posX, posY, dir, NposX, NposY, NewNposX, NewNposY)
            #gotta add possible moves the player or the amount of moves the player can have
            #self.visualize()
        pass

    #Human V AI
    def playHumanVsAI(self):
        while True:
            #Game Print Statements
            possibleMoves = game.checkPossible()
            possibleMovesLen = len(possibleMoves)
            if possibleMovesLen == 0:
                print("Player ", ((self.turn + 1) % 2) + 1, " Has Won!, Player ", ((self.turn + 2) % 2)+1, "has no available moves!")
                return False
            print("Possible Moves:", possibleMoves, '\n', "Possible Moves:" , possibleMovesLen)
            print("Player ", self.turn + 1, " turn: ")

            self.visualize()

            if self.turn == 0:  # Human player
                inp = input("Enter your input:").split()
                if len(inp) == 3:
                    posX, posY = int(inp[0]), int(inp[1])
                    dir = inp[2]
                    game.play(posX, posY, dir, player = 0)
                elif len(inp) == 7:
                    posX, posY, NposX, NposY, NewNposX, NewNposY = int(inp[0]), int(inp[1]), int(inp[3]), int(inp[4]), int(inp[5]), int(inp[6])
                    dir = inp[2]
                    #NposX, NposY, NewNposX, NewNposY = input
                    game.play(posX, posY, dir, NposX, NposY, NewNposX, NewNposY, player = 0)
            else:  # AI player
                action = self.getAction(depth=2, player = self.turn)
                if action:
                    self.play(*action, player = self.turn)
                    print(f"AI plays: {action}")
                    self.visualize()
                else:
                    print("AI has no moves left. You win!")
                    break
    
    
    def playAIVsAI(self):
        while True:
            #Game Print Statements
            possibleMoves = self.checkPossible()
            possibleMovesLen = len(possibleMoves)
            if possibleMovesLen == 0:
                print("Player ", ((self.turn + 1) % 2) + 1, " Has Won!, Player ", ((self.turn + 2) % 2)+1, "has no available moves!")
                self.visualize()
                return False
            print("Possible Moves:", possibleMoves, '\n', "Possible Moves:" , possibleMovesLen)
            print("AI ", self.turn + 1, " turn: ")

            self.visualize()
            action = self.getAction(depth = 2, player = self.turn)
            if action:
                self.play(*action, player = self.turn)
                print(f"AI {self.turn + 1} plays: {action}")
            # else:
            #     print(f"AI {self.turn + 1} has no moves left. AI {((self.turn + 1) % 2) + 1} wins!")
            #     break


#init game state
game = gameState()
#game.visualize()
#game.playHumanVsAI()
#game.playGame()
game.playAIVsAI()


#To lose we play
# 3 4 N 1 1 3 1
# 1 1 E 3 1 1 4

