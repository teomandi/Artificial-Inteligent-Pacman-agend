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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newPos = successorGameState.getPacmanPosition()	#8esi m
        newFood = successorGameState.getFood() #as list me ta fai
        newGhostStates = successorGameState.getGhostStates()	# [0]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        import time
        foodlist = newFood.asList()
        if(len(foodlist) ==0 ):return 1000	#winState
        score = successorGameState.getScore();
        
        xyG = util.manhattanDistance(newPos,newGhostStates[0].getPosition())
        print "Ghost Distanse: " , xyG
        if (xyG > 2):
        	score += xyG
        else:
        	score += 0
        if(currentGameState.getNumFood() > successorGameState.getNumFood()):
        	score +=100
        min = util.manhattanDistance(newPos,foodlist[0])        
        sum=0;
        for i in foodlist:
        	dist = util.manhattanDistance(newPos,i)
        	if(dist < min):
        		min = dist
        print " Min dist from food: ",min
        score -= min
        if  action == Directions.STOP:		#if stop bad move
        	score -= 3
        print score
        return score

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
		"""
		"*** YOUR CODE HERE ***"
		print"*minimax:START*"
		def MAXi(state, depth):
			if state.isWin() or state.isLose():			#always check
				return state.getScore()
			actions = state.getLegalActions(0) #agent 0 is our pacman
			maxscore = float("-inf")		
			score = maxscore
			maxaction = Directions.STOP
			for i in actions:
				score = MINi(state.generateSuccessor(0, i), depth, 1)
				if score > maxscore:
					maxscore=score
					maxaction= i
			if depth == 0 :
				return maxaction
			else :
				return maxscore

		def MINi(state, depth, ghostAgent):
			if state.isLose() or state.isWin():
				return state.getScore()
			if(ghostAgent ==  state.getNumAgents() - 1):
				nextAgent = 0
			else:
				nextAgent = ghostAgent + 1
			actions = state.getLegalActions(ghostAgent)
			minscore = float("inf")
			score = minscore
			for i in actions:
				if (nextAgent == 0):
					if(depth == (self.depth-1)):
						score = self.evaluationFunction(state.generateSuccessor(ghostAgent, i)) #last one
					else:
						score = MAXi(state.generateSuccessor(ghostAgent, i), depth + 1)
				else:
					score = MINi(state.generateSuccessor(ghostAgent, i), depth, nextAgent)
				if(score < minscore):
					minscore = score
			return minscore

		score= MAXi(gameState,0)
		return score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
		"""
          Returns the minimax action using self.depth and self.evaluationFunction
		"""
		print"*AlphaBeta:START*"
		def MAXi(state, depth, a, b):
			if state.isWin() or state.isLose():			#always check
				return state.getScore()
			actions = state.getLegalActions(0) #agent 0 is our pacman
			maxscore = float("-inf")		
			score = maxscore
			maxaction = Directions.STOP
			for i in actions:
				score = MINi(state.generateSuccessor(0, i), depth, 1, a, b)
				if score > maxscore:
					maxscore=score
					maxaction= i
				a = max(a, maxscore)
				if(maxscore > b):
					return maxscore
			if depth == 0 :
				return maxaction
			else :
				return maxscore

		def MINi(state, depth, ghostAgent, a , b):
			if state.isLose() or state.isWin():
				return state.getScore()
			if(ghostAgent ==  state.getNumAgents() - 1):
				nextAgent = 0
			else:
				nextAgent = ghostAgent + 1
			actions = state.getLegalActions(ghostAgent)
			minscore = float("inf")
			score = minscore
			for i in actions:
				if (nextAgent == 0):
					if(depth == (self.depth-1)):
						score = self.evaluationFunction(state.generateSuccessor(ghostAgent, i)) #last one
					else:
						score = MAXi(state.generateSuccessor(ghostAgent, i), depth + 1, a, b)
				else:
					score = MINi(state.generateSuccessor(ghostAgent, i), depth, nextAgent, a, b)
				if(score < minscore):
					minscore = score
				b = min(minscore, b)
				if (minscore < a):
					return minscore
			return minscore
		score= MAXi(gameState, 0, float("-inf"), float("inf"))
		return score

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
		print"*Expectimax:START*"
		def MAXi(state, depth):
			if state.isWin() or state.isLose():			#always check
				return state.getScore()
			actions = state.getLegalActions(0) #agent 0 is our pacman
			maxscore = float("-inf")		
			score = maxscore
			maxaction = Directions.STOP
			for i in actions:
				score = MINi(state.generateSuccessor(0, i), depth, 1)
				if score > maxscore:
					maxscore=score
					maxaction= i
			if depth == 0 :
				return maxaction
			else :
				return maxscore

		def MINi(state, depth, ghostAgent):
			if state.isLose() or state.isWin():
				return state.getScore()
			if(ghostAgent ==  state.getNumAgents() - 1):
				nextAgent = 0
			else:
				nextAgent = ghostAgent + 1
			actions = state.getLegalActions(ghostAgent)
			score = 0
			for i in actions:
				if (nextAgent == 0):
					if(depth == (self.depth-1)):
						score1 = self.evaluationFunction(state.generateSuccessor(ghostAgent, i)) #last one
					else:
						score1 = MAXi(state.generateSuccessor(ghostAgent, i), depth + 1)
				else:
					score1 = MINi(state.generateSuccessor(ghostAgent, i), depth, nextAgent)
				score += score1
			return score/len(actions)

		score= MAXi(gameState,0)
		return score

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman_pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()


# Abbreviation
better = betterEvaluationFunction




