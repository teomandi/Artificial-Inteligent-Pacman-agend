# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    print "!!!! DFS !!!!"

    result = [] #list with moves
    visited = []
    order = []
    s = util.Stack()
    t = problem.getStartState()
    visited.append(t)
    order.append(("null", t,"null"))		#init order #list to help me find the path (father,son,move)
    while not problem.isGoalState(t):
        nodes = problem.getSuccessors(t)
        for i in range(len(nodes)):
            if nodes[i][0] not in visited:
                visited.append(nodes[i][0])
                order.append((t,nodes[i][0],nodes[i][1]))
                s.push(nodes[i])
                print "done" , t , " ", nodes[i][1]
        x = s.pop()
        t=x[0]
    temp=t
    while not (temp == 'null'):
       for i in range(len(order)):                          #until we found the node with the same father
            if temp == order[i][1] :
                result.append(order[i][2])
                temp = order[i][0]
    result.reverse()
    del result[0]
    print result
    return result

def breadthFirstSearch(problem):

    print "!!!! BFS !!!!"
    result = []                                 							#list with moves
    visited = []
    q = util.Queue()
    t = problem.getStartState()
    order=[]
    order.append(("null", t,"null"))
    print " S-T-A-R-T"
    while not problem.isGoalState(t):	  
        nodes = problem.getSuccessors(t)
        for i in range(len(nodes)):
            if nodes[i][0] not in visited:
            	visited.append(nodes[i][0])
                q.push(nodes[i][0])
                order.append((t,nodes[i][0],nodes[i][1]))					#(father, node, move2go)
        if q.isEmpty():         #just in case
            print "EMPTY"
            q.push(t)
            visited=[]
        else:
            t = q.pop()
    temp = t
    print result, temp
    order.reverse()
    while not (temp == "null" ):
       for i in range(len(order)):                          				#until we found the node with the same father
            if temp == order[i][1] :										
                result.append(order[i][2])
                temp = order[i][0]
    result.reverse()
    del result[0]
    print "MOVES: ", result
    return result



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    print "!!!! UFS !!!!"


    result = [] #list with moves
    visited = []
    value = []
    order = []
    pq = util.PriorityQueue()
    t = problem.getStartState()
    pq.push(t, 0)
    value.append((t,0))
    item = pq.pop()
    while not problem.isGoalState(t):
        nodes = problem.getSuccessors(t)
        visited.append(t)
        for i in range(len(value)):
            if value[i][0] == t:
                priority = value[i][1]
        for i in range(len(nodes)):
            if nodes[i][0] not in visited:
                pr = nodes[i][2] + priority
                pq.push(nodes[i][0],pr)
                value.append((nodes[i][0],pr))
                order.append((t,nodes[i][0],nodes[i][1]))
        t = pq.pop()
    temp = t
    while not temp == problem.getStartState():
        for i in range(len(order)):
            if temp== order[i][1]:
                result.append(order[i][2])
                temp = order[i][0]
    result.reverse()

    print "MOVES: ", result
    print value
    return result

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

 
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print "!!!!A*!!!!!"
    pq =  util.PriorityQueue()   #priority queue
    nodeinfo = []   #this list has the info for the nodes ( node, fathernode, move)
    result = []
    visited = []
    t = problem.getStartState()
    x = (t, "null", 0, "null")
    nodeinfo.append(x)
    while not problem.isGoalState(t):
        nodes = problem.getSuccessors(t)
        for i in range(len(nodes)):
            if nodes[i][0] in visited: #if visited dont visit again
                continue
            h = heuristic(nodes[i][0],problem)
            print "H = ", h
            f = nodes[i][2] + h   #calculate f
            visited.append(nodes[i][0])
            pq.update(nodes[i][0], f)
            x = (nodes[i][0], t, nodes[i][1])
            fl = False
            for i in range(len(nodeinfo)):  #if already exist we update it
                if nodeinfo[i][0]==x[0]:
                    fl = True
                    if x[2] < nodeinfo[i][2]:
                        nodeinfo.append(x)
            if not fl:
                nodeinfo.append(x)
        t = pq.pop()
    temp = t
    while not temp == problem.getStartState(): #create result 
        for i in range(len(nodeinfo)):
            if temp == nodeinfo[i][0]:
                result.append(nodeinfo[i][2])
                temp = nodeinfo[i][1]
    print "PRIN : " , result
    result.reverse()
    print result
    return result


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
