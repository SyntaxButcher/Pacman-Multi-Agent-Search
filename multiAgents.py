# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        FoodL = newFood.height
        FoodW = newFood.width
        foodD = []
        for i in range(FoodW):
            for j in range(FoodL):
                if newFood[i][j] == True:
                    foodD.append(util.manhattanDistance(newPos,(i,j)))
        if len(foodD) >= 1:
            minFoodD = min(foodD)
        else:
            minFoodD = 99999
    
        ghostPos = successorGameState.getGhostPositions()
        ghostD = []
        ghostDangerDist = 0
        for i in ghostPos:
            ghostD.append(util.manhattanDistance(newPos,i))
        if min(ghostD) == 4:
            ghostDangerDist = -200
        elif min(ghostD) == 3:
            ghostDangerDist = -400
        elif min(ghostD) == 2:
            ghostDangerDist = -600
        elif min(ghostD) == 1:
            ghostDangerDist = -800
        elif min(ghostD) == 0:
            ghostDangerDist = -1000

        evaluation = successorGameState.getScore() + min(ghostD)/(minFoodD*minFoodD) + ghostDangerDist

        return evaluation
        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        return self.minimax(gameState, 0, 0)[1]
    
    def minimax(self, gameState, depth, agentIndex):
        
        numOfAgents = gameState.getNumAgents()

        if depth == (self.depth*numOfAgents) or gameState.isWin() or gameState.isLose():
            return (gameState.getScore(),'')

        if agentIndex == 0:
            Max = float("-inf")
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimax(j, depth + 1, agentIndex + 1)[0]
                if Val > Max:
                    Action = i
                Max = max(Max,Val)
            return (Max, Action)

        elif agentIndex == (numOfAgents-1):
            Min = float('inf')
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimax(j, depth + 1, 0)[0]
                if Val < Min:
                    Action = i
                Min = min(Min, Val)
            return (Min, Action)
        
        else:
            Min = float('inf')
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimax(j, depth + 1, agentIndex + 1)[0]
                if Val < Min:
                    Action = i
                Min = min(Min, Val)
            return (Min, Action)
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxAlphaBeta(gameState, 0, 0, float('-inf'), float('inf'))[1]

        util.raiseNotDefined()
    
    def minimaxAlphaBeta(self, gameState, depth, agentIndex, alpha, beta):
        
        numOfAgents = gameState.getNumAgents()

        if depth == (self.depth*numOfAgents) or gameState.isWin() or gameState.isLose():
            return (gameState.getScore(),'')

        if agentIndex == 0:
            Max = float("-inf")
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimaxAlphaBeta(j, depth + 1, agentIndex + 1, alpha, beta)[0]
                alpha = max(alpha, Val)
                if Val > Max:
                    Action = i
                Max = max(Max,Val)
                if beta < alpha:
                    break           
            return (Max, Action)

        elif agentIndex == (numOfAgents-1):
            Min = float('inf')
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimaxAlphaBeta(j, depth + 1, 0, alpha, beta)[0]
                beta = min(beta, Val)
                if Val < Min:
                    Action = i
                Min = min(Min, Val)
                if beta < alpha:
                    break      
            return (Min, Action)
        
        else:
            Min = float('inf')
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.minimaxAlphaBeta(j, depth + 1, agentIndex + 1, alpha, beta)[0]
                beta = min(beta, Val)
                if Val < Min:
                    Action = i
                Min = min(Min, Val)
                if beta < alpha:
                    break         
            return (Min, Action)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"    
        return self.expectimax(gameState, 0, 0)[1]
        util.raiseNotDefined()
    
    def expectimax(self, gameState, depth, agentIndex):
        
        numOfAgents = gameState.getNumAgents()

        if depth == (self.depth*numOfAgents) or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),'')

        if agentIndex == 0:
            Max = float("-inf")
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.expectimax(j, depth + 1, agentIndex + 1)[0]
                if Val > Max:
                    Action = i
                Max = max(Max,Val)
            return (Max, Action)

        elif agentIndex == (numOfAgents-1):
            avg = 0
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.expectimax(j, depth + 1, 0)[0]
                avg += (Val/len(gameState.getLegalActions(agentIndex)))
            return (avg, i)
        
        else:
            avg = 0
            for i in gameState.getLegalActions(agentIndex):
                j = gameState.generateSuccessor(agentIndex, i)
                Val = self.expectimax(j, depth + 1, agentIndex + 1)[0]
                avg += (Val/len(gameState.getLegalActions(agentIndex)))
            return (avg, i)
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    We calculated the Food, Capsule and Ghost positions along with Ghost scared timers when a capsule is consumed
    The formula was to add game score + (all ghost distances/closest food squared * closest capsule) + ghost chase promoting score when a capsule was consumed
    to keep the code from crashing we added conditions such as len(foodD) >= 1 so the code doesn't crash when there is no food or capsule left and also set closest capsuleD value to 1 incase there are no capsules left since it is in the denominator.
    Also added a ghost Panic variable "ghostDangerDist" to make pacman move away from ghosts if they come anywhere 4 blocks close
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood()
    capPos = currentGameState.getCapsules()
    ghostPos = currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    #Food Score
    FoodL = foodPos.height
    FoodW = foodPos.width
    foodD = []
    for i in range(FoodW):
        for j in range(FoodL):
            if foodPos[i][j] == True:
                foodD.append(util.manhattanDistance(position,(i,j)))
    if len(foodD) >= 1:
        minFoodD = min(foodD)
        maxFoodD = max(foodD)
    else:
        minFoodD = float('inf')
        maxFoodD = float('inf')
    
    #Ghost score
    ghostD = []
    ghostTotalD = 0
    ghostDangerDist = 0
    for i in ghostPos:
        ghostD.append(util.manhattanDistance(position,i))
        ghostTotalD += util.manhattanDistance(position,i)
    if min(ghostD) in range(3):
        ghostDangerDist = float('-inf')
    
    #Capsule score
    capsuleD = []
    for i in capPos:
        capsuleD.append(util.manhattanDistance(position,i))
    if len(capsuleD) >= 1:
        minCapsuleD = min(capsuleD)
    else:
        minCapsuleD = 1
    
    #Ghost Chase score
    ghostChase = 0
    for i in scaredTimes:
        if i > 0:
            if min(ghostD) in range(10):
                ghostChase = float('inf')
    
    Formula = currentGameState.getScore() + (ghostTotalD/(minFoodD*minFoodD*minCapsuleD)) + ghostChase 

    return Formula
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
