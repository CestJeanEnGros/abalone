from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random as rd
import math
import time

class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float=60*15,*args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type,name,time_limit,*args)
        self.maxDepthTable = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        # self.maxDepthTable = [1,2,2,2,3,3,3,3,3,3,4,4,4,4,4,3,3,3,3,3,3,2,2,2,1]
        # self.maxDepthTable =   [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        #Initialisation de l'alpha beta
        alpha = -math.inf
        beta = math.inf
        depth = 0
        max_depth = self.maxDepthTable[int(current_state.step // 2)] #La profondeur s'adapte à l'avancement de la partie
        #Lancement de l'alpha beta
        value, action = alpha_beta(current_state, alpha, beta, depth, max_depth)

        return action


def alpha_beta(current_state: GameState, alpha, beta, depth, max_depth):
    #Condition d'arrêt de l'exploration de l'arbre
    if current_state.is_done() or depth >= max_depth:
        return heuristic(current_state), None #On renvoit l'estimation de l'heuristique
    #Boucle min
    elif current_state.get_player_id(current_state.next_player.get_id()).piece_type == "W":
        best_v = math.inf
        best_a = None
        possible_actions = current_state.get_possible_actions()
        for a in possible_actions:
            v,_ = alpha_beta(a.get_next_game_state(), alpha, beta, depth+1, max_depth)
            if v < best_v:
                best_v = v
                best_a = a
            if v < alpha: return best_v, best_a
            beta = min(beta, v) #Mise à jour de beta
    #Boucle max
    elif current_state.get_player_id(current_state.next_player.get_id()).piece_type == "B":
        best_v = -math.inf
        best_a = None
        possible_actions = current_state.get_possible_actions()
        for a in possible_actions:
            v,_ = alpha_beta(a.get_next_game_state(), alpha, beta, depth+1, max_depth)
            if v > best_v:
                best_v = v
                best_a = a
            if v > beta: return best_v, best_a
            alpha = max(alpha, v) #Mise à jour de alpha
    else:
        raise TypeError
    
    return best_v, best_a

def heuristic(current_state: GameState) -> float:
    #Poids des heuristiques
    a = 3
    b = 10
    c = 0.5
    d = 0.1
    e = 0.05

    #Calcul de l'heuristique
    value = a*h1(current_state) + b*h2(current_state) + c*h3(current_state) + d*h4(current_state) + e*h5(current_state)
    
    return value
    

def h1(current_state): #Cf rapport pour explication
    #Score des cases
    weigh = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 2, 2, 2, 2, 1, 0, 0],
            [0, 1, 2, 3, 3, 3, 2, 1, 0],
            [1, 2, 3, 4, 4, 3, 2, 1, 0],
            [1, 2, 3, 4, 5, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 3, 3, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0]]
    #Initialisation
    grid = current_state.rep.get_grid()
    value = 0
    #Parcours du board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "W" :
                value -= weigh[i][j] 
            elif grid[i][j] == "B" :
                value += weigh[i][j]
                
    return value

def h2(current_state):#Cf rapport pour explication
    value = (current_state.get_player_score(current_state.get_players()[1]) - current_state.get_player_score(current_state.get_players()[0]))
    
    return value

def h3(current_state): #Cf rapport pour explication
    #Eloignements des cases
    weigh = [[0, 0, 5, 5, 5, 5, 5, 0, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [5, 4, 3, 2, 1, 2, 3, 4, 5],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0]]
    #Initialisation
    grid = current_state.rep.get_grid()
    v_w = 0
    v_b = 0
    n_w = 0
    n_b = 0
    #Parcours du board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "W":
                n_w += 1
                for k in range(i,9):
                    for l in range(9):
                        if k != i or l >= j+1:
                            if grid[k][l] == "W":
                                v_w += abs(weigh[i][j]-weigh[k][l])
            elif grid[i][j] == "B":
                n_b += 1
                for k in range(i,9):
                        for l in range(9):
                            if k != i or l >= j+1:
                                if grid[k][l] == "B":
                                    v_b -= abs(weigh[i][j]-weigh[k][l])
    #Normalisation
    value = v_w/n_w + v_b/n_b          

    return value

def h4(current_state): #Cf rapport pour explication
    #Eloignements des cases
    weigh = [[0, 0, 5, 5, 5, 5, 5, 0, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [5, 4, 3, 2, 1, 2, 3, 4, 5],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0]]
    #Initialisation
    grid = current_state.rep.get_grid()
    value = 0
    #Parcours du board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "W" and weigh[i][j] == 5:
                value += 1
            elif grid[i][j] == "B" and weigh[i][j] == 5:
                value -= 1

    return value

def h5(current_state): #Cf rapport pour explication
    #Eloignements des cases
    weigh = [[0, 0, 5, 5, 5, 5, 5, 0, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [5, 4, 3, 2, 1, 2, 3, 4, 5],
            [5, 4, 3, 2, 2, 3, 4, 5, 0],
            [0, 5, 4, 3, 3, 3, 4, 5, 0],
            [0, 5, 4, 4, 4, 4, 5, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0]]
    #Initialisation
    grid = current_state.rep.get_grid()
    value = 0
    #Parcours du board
    for i in range(9):
        for j in range(9):
            if grid[i][j] == "W" and (weigh[i][j] == 1 or weigh[i][j] == 2) :
                value -= 1
            elif grid[i][j] == "B" and (weigh[i][j] == 1 or weigh[i][j] == 2):
                value += 1

    return value

