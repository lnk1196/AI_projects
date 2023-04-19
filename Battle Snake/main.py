# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math
import sys


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "lnk86",  # Your Battlesnake Username
    "color": "#9ebbba",  # Choose color
    "head": "silly",  # Choose head
    "tail": "hook",  # Choose tail
  }

# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  if (game_state["board"]["snakes"]):
    print("GAME OVER: Winner is: " + game_state["board"]["snakes"][0]["name"])
  else:
    print("GAME OVER: Draw")

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def get_next(current_head, next_move):
  """
  return the coordinate of the head if our snake goes that way
  """
  MOVE_LOOKUP = {"left":-1, "right": 1, "up": 1, "down":-1}
  # Copy first
  future_head = current_head.copy()

  if next_move in ["left", "right"]:
    # X-axis
    future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
  elif next_move in ["up", "down"]:
    future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]

  return future_head

def avoid_walls(future_head, board_width, board_height):
  result = True

  x = int(future_head["x"])
  y = int(future_head["y"])

  if x < 0 or y < 0 or x >= board_width or y >= board_height:
    result = False

  return result

def avoid_snakes(future_head, snake_bodies):
    for snake in snake_bodies:
      if future_head in snake["body"][:-1]:
        return False
    return True

# adapted from https://github.com/altersaddle/untimely-neglected-wearable
def get_safe_moves(possible_moves, body, board):
  safe_moves = []
  for guess in possible_moves:
    guess_coord = get_next(body[0], guess)
    if avoid_walls(guess_coord, board["width"], board["height"]) and avoid_snakes(guess_coord, board["snakes"]): 
      safe_moves.append(guess)
    elif len(body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
     # The tail is also a safe place to go... unless there is a non-tail segment there too
     safe_moves.append(guess)
  return safe_moves

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
  possible_moves = ["up", "down", "left", "right"]
  if not (game_over(game_state)):
    safe_moves = get_safe_moves(possible_moves, game_state["you"]["body"], game_state["board"])
    if game_state["board"]["snakes"][1] == game_state["you"]:
      max_player_index = 1
      min_player_index = 0
    else:
      max_player_index = 0
      min_player_index = 1
  
    if len(safe_moves)==1:
      next_move = safe_moves[0]
    elif len(safe_moves) > 1:
      #next_move = random.choice(safe_moves)
      x = minimax(game_state,[True,max_player_index,min_player_index],7)
      next_move = x[1]
    else: 
      next_move = random.choice(possible_moves)
    
      print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    print("tst5")
  return {"move": "none"}
#added to update all snake body, not just snake head
def nxt_move_state(snake_state,move):
  snake_state["head"] = get_next(snake_state["head"],move)
  snake_state["health"]-=1
  for i in range(len(snake_state["body"])):
    snake_state["body"][i] = get_next(snake_state["body"][i],move)
  return(snake_state)
  
#copied from a previous version
def manhattan_distance(pos1, pos2):
  return abs(pos1['x'] - pos2['x']) + abs(pos1['y'] - pos2['y'])

def pythag_distance(pos1,pos2):
  return (math.sqrt((pos1['x'] - pos2['x'])**2+(pos1['y'] - pos2['y'])**2))
  
#copied from a previous version
def game_over(game_state):
  # Check if your Battlesnake has died
  if game_state['you']['health'] <= 0:
    return True
  
  # Check if there is only one snake left on the board
  if len(game_state['board']['snakes']) == 1:
    return True
  
  # Check if all the food has been eaten
  if not game_state['board']['food']:
    return True
  
  return False

#JoJo's minimax. It needs a couple improvements, mainly that our heuristic needs to be a lot better. Specifically if there is a game state that would lead to a loss it needs to be returned as a very large negative number for the max or very large positive for the min. Currently, if i'm not mistaken, the heuristic is just calculating the distance between heads
def minimax (game_state,maximizing_player,depth,move="none"):
  possible_moves = ["up", "down", "left", "right"]
  if depth == 0 or game_over(game_state):  #base case of recursion, returns the heuristic
    #heuristic = manhattan_distance(game_state["board"]["snakes"][maximizing_player[1]]["head"],game_state["board"]["snakes"][maximizing_player[2]]["head"])
    if (maximizing_player):
      player_index = maximizing_player[1]
      opp_player_index = maximizing_player[2]
    else:
      player_index = maximizing_player[2]
      opp_player_index = maximizing_player[1]
      
    safe_moves = get_safe_moves(possible_moves, game_state["board"]["snakes"][player_index]["body"], game_state["board"])

    heuristic = 0
    numUnsafeMoves = 4
    
    for potential_move in safe_moves:
      numUnsafeMoves = numUnsafeMoves - 1
  
    if (numUnsafeMoves == 1):
      heuristic = heuristic - 5
    if (numUnsafeMoves == 2):
      heuristic = heuristic - 10
    if (numUnsafeMoves == 3):
      heuristic = heuristic - 15
    if (numUnsafeMoves == 4):
      heuristic = heuristic - 1000
  
    hunger = game_state['board']['snakes'][player_index]['health']
  
    if (hunger < 20):
      heuristic = heuristic - (20 - hunger)
    
    food = game_state['board']['food']
    head = game_state['board']['snakes'][player_index]['head']

    if not game_state['board']['food']:
      min_food_distance = 122
      for food_item in food:
        distance_from_food = abs(food['x'] - head['x']) + abs(food['y'] - head['y'])
        if distance_from_food < min_food_distance:
          min_food_distance = distance_from_food
            
      if (min_food_distance <= 3):
        heuristic = heuristic + (4 - min_food_distance)

    fren_snek_len = len(game_state["board"]["snakes"][player_index]["body"])
    op_snek_len = len(game_state["board"]["snakes"][opp_player_index]["body"])
          
    if (fren_snek_len > op_snek_len):
      heuristic = heuristic + ((fren_snek_len - op_snek_len) * 2)
  
    snake_len = len(game_state['board']['snakes'][player_index])
    heuristic = heuristic + (snake_len * 4)
    return([heuristic,move])
  elif maximizing_player[0]: #max function
    best_value = -1000
    safe_moves = get_safe_moves(possible_moves, game_state["board"]["snakes"][maximizing_player[1]]["body"], game_state["board"])
    best_move = "none"
    for potential_move in safe_moves: #loop through possible moves
      game_state["board"]["snakes"][maximizing_player[1]] = nxt_move_state(game_state["board"]["snakes"][maximizing_player[1]],potential_move) #calculates the next move
      x = minimax(game_state,[False,maximizing_player[1],maximizing_player[2]],depth-1,potential_move)
      value = x[0]
      if value > best_value:
        best_move = potential_move
        best_value = value
    return(best_value,best_move) #recursive call
  else: #same as max but opposite
    best_value = 1000
    best_move = "none"
    safe_moves = get_safe_moves(possible_moves, game_state["board"]["snakes"][maximizing_player[2]]["body"], game_state["board"])
    for potential_move in safe_moves:
      game_state["board"]["snakes"][maximizing_player[2]] = nxt_move_state (game_state["board"]["snakes"][maximizing_player[2]],potential_move)
      x = minimax(game_state,[True,maximizing_player[1],maximizing_player[2]],depth-1,potential_move)
      value = x[0]
      move = x[1]
      
      if value < best_value:
        best_move = move
        best_value = value

    return(best_value,best_move)

if __name__ == "__main__":
  from server import run_server

  run_server({
    "info": info, 
    "start": start, 
     "move": move, 
    "end": end
  })

