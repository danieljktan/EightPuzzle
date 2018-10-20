import random

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
      if queue[i][1] < queue[swap][1]:
         break
      queue[i], queue[swap] = queue[swap], queue[i]
      i = swap
      left = i * 2 + 1
      right = i * 2 + 2

   return queue.pop()


def check_heap(queue, i):
   left = i * 2 + 1
   right = i * 2 + 2
   if left >= len(queue):
      return True
   if queue[i][1] <= queue[left][1] and check_heap(queue, left):
      if right >= len(queue):
         return True
      elif queue[i][1] <= queue[right][1] and check_heap(queue, right):
         return True
   return False


queue = []
for i in range(1000000):
   enqueue(queue, 'i', random.randint(1, 200000))

num = -1000
while queue:
   p, n = dequeue(queue)
   print(p, n)
   if num > n:
      print('fail')
   else:
      num = n


'''while True:
   r = random.randint(0, 1)
   if r == 0 or not queue:
      enqueue(queue, 'item', random.randint(1, 20))
   else:
      item, priority = dequeue(queue)
      print('item:', item, 'priority:', priority)
   print(queue)
   if not check_heap(queue, 0):
      break

print('fail', queue)
'''




