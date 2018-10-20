import re
import time

GOAL_STATE = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))


def misplaced_tile(board):
   n = 0
   for rows, ROWS in zip(board, GOAL_STATE):
      for cell, CELL in zip(rows, ROWS):
         if CELL != 0 and cell != CELL:
            n += 1
   return n


def manhattan_distance(board):
   table = ((0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1))
   n = 0
   for i, rows in enumerate(board):
      for j, cell in enumerate(rows):
         if cell != 0:
            (x, y) = table[cell - 1]
            n += abs(i-x) + abs(j-y)
   return n


def enqueue(queue, item, priority):
   queue.append((item, priority))
   i = len(queue) - 1
   while i > 0:
      p = (i - 1) // 2
      if queue[p][1] <= queue[i][1]:
         break
      queue[p], queue[i] = queue[i], queue[p]
      i = p


def dequeue(queue):
   length = len(queue) - 2
   i = 0
   left = 1
   right = 2
   queue[0], queue[-1] = queue[-1], queue[0] #send element to the back
   while left <= length:
      #swap = right if right exists, and right is smaller than left
      swap = right if right <= length and queue[right][1] < queue[left][1] else left
      if queue[i][1] <= queue[swap][1]:
         break
      queue[i], queue[swap] = queue[swap], queue[i]
      i = swap
      left = i * 2 + 1
      right = i * 2 + 2
   return queue.pop()


def valid_board(board):
   nums = set()
   for row in board:
      for b in row:
         if b < 0 or b >= 9: #invalid number
            return False
         if b not in nums:
            nums.add(b)
         else:
            return False
   return True


def operators(board):
   #linear search for 0, then yield left, right up, down
   m = len(board) - 1
   n = len(board[0]) - 1
   for i, rows in enumerate(board):
      for j, c in enumerate(rows):
         if c == 0:
            if i != 0:
               yield i, j, i-1, j #LEFT
            if i != m:
               yield i, j, i+1, j #RIGHT
            if j != 0:
               yield i, j, i, j-1 #UP
            if j != n:
               yield i, j, i, j+1 #DOWN        
            return


def queueing_function(queue, node, parent, cost, visited, heuristic = lambda x: 0):
   for i1, j1, i2, j2 in operators(node):
      #work-around for the way that sets are designed in python...
      #next node = node w/ value swapped:
      next_temp = [[node[0][0], node[0][1], node[0][2]], 
                   [node[1][0], node[1][1], node[1][2]], 
                   [node[2][0], node[2][1], node[2][2]]]
      next_temp[i1][j1], next_temp[i2][j2] = next_temp[i2][j2], next_temp[i1][j1]
      next_node = ((next_temp[0][0], next_temp[0][1], next_temp[0][2]), 
                   (next_temp[1][0], next_temp[1][1], next_temp[1][2]), 
                   (next_temp[2][0], next_temp[2][1], next_temp[2][2]))
      if next_node not in visited:
         enqueue(queue, (next_node, (node, parent)), cost + heuristic(next_node))


def search(initial, heuristic = lambda x: 0):
   queue   = [((initial, None), 0)] #make a queue w/ with the initial state
   visited = set()
   num_nodes_expanded = 0
   max_queue_length = 1
   while True:
      if not queue:
         return None
      ((node, parent), priority) = dequeue(queue) #remove front of list
      visited.add(node)
      if node == GOAL_STATE: #found solution to the problem, calculate/return the path to the destination
         path = [node]
         while parent != None:
            data, next_parent = parent
            path.append(data)
            parent = next_parent
         return reversed(path), num_nodes_expanded, max_queue_length

      queueing_function(queue, node, parent, priority + 1, visited, heuristic)
      num_nodes_expanded += 1
      max_queue_length = max(len(queue), max_queue_length)


nums_regex = re.compile('[0-9]+')
print('Welcome to Daniel Tan\'s 8-puzzle solver')
while True:
   string = input('Type \"1\" to use a default puzzle, \"2\" to enter your own puzzle, or \"exit\" to quit: ')
   if string == 'exit':
      break

   game = None
   if string == '1':
      while True:
         s0 = input('Using a default puzzle. Please enter a desired difficulty on a scale from 0-8: ')      
         if s0 == '0':
            game = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
            break
         elif s0 == '1':
            game = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
            break
         elif s0 == '2':
            game = ((1, 2, 0), (4, 5, 3), (7, 8, 6))
            break
         elif s0 == '3':
            game = ((1, 2, 3), (0, 4, 6), (7, 5, 8))
            break
         elif s0 == '4':
            game = ((1, 2, 3), (4, 5, 6), (0, 7, 8))
            break
         elif s0 == '5':
            game = ((1, 0, 3), (4, 2, 6), (7, 5, 8))
            break
         elif s0 == '6':
            game = ((0, 1, 2), (4, 5, 3), (7, 8, 6))
            break
         elif s0 == '7':
            game = ((8, 7, 1), (6, 0, 2), (5, 4, 3))
            break
         elif s0 == '8':
            game = ((1, 2, 3), (4, 5, 6), (8, 7, 0))
            break

   elif string == '2':
      print('Enter your puzzle, use a zero to represent the blank ')
      board = [[0,0,0], [0,0,0], [0,0,0]]
      while True:
         s0 = input('Enter the first row, use spaces or tabs between numbers: ')
         nums_string = nums_regex.findall(s0)
         if not nums_string or len(nums_string) != 3:
            continue

         board[0][0] = int(nums_string[0])
         board[0][1] = int(nums_string[1])
         board[0][2] = int(nums_string[2])
         break

      while True:
         s1 = input('Enter the second row, use spaces or tabs between numbers: ')
         nums_string = nums_regex.findall(s1)
         if not nums_string or len(nums_string) != 3:
            continue

         board[1][0] = int(nums_string[0])
         board[1][1] = int(nums_string[1])
         board[1][2] = int(nums_string[2])
         break
      
      while True:         
         s2 = input('Enter the third row, use spaces or tabs between number: ')
         nums_string = nums_regex.findall(s2)
         if not nums_string or len(nums_string) != 3:
            continue  

         board[2][0] = int(nums_string[0])
         board[2][1] = int(nums_string[1])
         board[2][2] = int(nums_string[2])
         break
      game = ((board[0][0], board[0][1], board[0][2]), 
              (board[1][0], board[1][1], board[1][2]),
              (board[2][0], board[2][1], board[2][2]))
   else:
      print('Invalid number input')
      continue

   if not valid_board(game):
      print('Invalid board')
      continue

   heuristic = None
   while True:
      string = input('Enter your choice of algorithm:\n'
                     '1. Uniform Cost Search\n'
                     '2. A* with the Misplaced Tile heuristic\n'
                     '3. A* with the Manhattan distance heuristic\n')
      if string == '1':
         heuristic = lambda x: 0
         break
      elif string == '2':
         heuristic = misplaced_tile
         break
      elif string == '3':
         heuristic = manhattan_distance
         break
   
   time_taken = time.time_ns()   
   answer = search(game, heuristic=heuristic)
   time_taken = time.time_ns() - time_taken
   if answer == None:
      print('Problem cannot be solved.')
   else:
      (path, nodes_expanded, max_queue_size) = answer
      print('Start:')
      for node in path:
         for row in node:
            print(row)
         print()
      print('Number of nodes expanded:', nodes_expanded)
      print('Max queue size:', max_queue_size)

   if time_taken < 1.0e6:
      print('Time taken: %.03f ms' % (time_taken / 1.0e6))
   else:
      print('Time taken: %.03f s (%.03f ms)' % (time_taken / 1.0e9, time_taken / 1.0e6))


