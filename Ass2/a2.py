# Minimum Priority Queue Implementation using Min-Heap. Heap is stored in an array where left child = 2*i+1 and right child is 2*i+2
# ______________________________________________________________________________________________

class MinPriorityQueue:
    def MinHeapify(self, idx):
        if idx >= self.size:
            raise Exception("Index out of Range")
        left = 2*idx+1
        right = 2*idx + 2
        minimum = idx
        if left < self.size and self.array[left] < self.array[minimum]:
            minimum = left
        if right < self.size and self.array[right] < self.array[minimum]:
            minimum = right
        if minimum != idx:
            self.array[minimum], self.array[idx] = self.array[idx], self.array[minimum]
            MinHeapify(self, minimum)

    def __init__(self, array):
        self.size = len(array)
        self.array = array
        for i in range(self.size//2 - 1, -1, -1):
            self.MinHeapify(i)

    def top(self):
        if self.is_empty():
            raise Exception("Top called on empty Priority Queue")
        return self.array[0]

    def pop(self):
        if self.is_empty():
            raise Exception("Pop called on empty Priority Queue")
        minimum = self.array[0]
        self.array[0] = self.array[self.size-1]
        self.array.pop()
        self.size -= 1
        if self.size > 0:
            self.MinHeapify(0)
        return minimum

    def decrease_value(self, idx, value):
        if idx >= self.size:
            raise Exception("Index out of Range")
        self.array[idx] = value
        while idx > 0 and self.array[(idx-1)//2] > self.array[idx]:
            self.array[(
                idx-1)//2], self.array[idx] = self.array[idx], self.array[(idx-1)//2]
            idx = (idx-1)//2

    def insert(self, value):
        self.size += 1
        self.array.append((float('inf'), -1, -1))
        self.decrease_value(self.size-1, value)

    def is_empty(self):
        return (self.size == 0)

# ______________________________________________________________________________________________


'''
listCollisions(M, x,v,m,T): Takes n points with mass M[i], initial position x[i], initial velocity v[i] and simulates m collisions or till time T
'''


def listCollisions(M, x, v, m, T):
    n = len(M)
    collisions = []  # holds all future collisions
    # how many collisions involving ith ball have happened
    collision_cnt = [0]*n
    # when was velocity and position of ith ball last updated
    last_update = [0]*n
    ans = []  # final output of list of collisions

    # calculate all initial collisions
    for i in range(n-1):
        if(v[i] - v[i+1] > 0):
            collisions.append(
                ((x[i+1]-x[i])/(v[i] - v[i+1]), i, x[i] + v[i] * (x[i+1]-x[i])/(v[i] - v[i+1]), collision_cnt[i], collision_cnt[i+1],))
    # create priority queue in O(n)
    pqueue = MinPriorityQueue(collisions)

    # Main simulation
    while not pqueue.is_empty() and m > 0:
        time, idx, pos, coll1, coll2 = pqueue.pop()
        # break if time T has passed
        if time > T:
            break
        # discard old collisions which won't happen
        if coll1 < collision_cnt[idx] or coll2 < collision_cnt[idx+1]:
            continue
        ans.append((time, idx, pos, ))

        # update all parameters of idx and idx+1
        x[idx], x[idx+1] = pos, pos
        v[idx], v[idx+1] = (M[idx] - M[idx+1])/(M[idx] + M[idx+1]) * v[idx] + 2*M[idx+1] * v[idx+1]/(
            M[idx]+M[idx+1]), 2*M[idx]*v[idx]/(M[idx] + M[idx+1]) - (M[idx] - M[idx+1])*v[idx+1]/(M[idx] + M[idx+1])  # calculate new velocities using formula
        last_update[idx], last_update[idx+1] = time, time
        collision_cnt[idx] += 1
        collision_cnt[idx+1] += 1

        # update parameters of idx-1 and idx+2
        if idx-1 >= 0:
            x[idx-1] += v[idx-1] * (time - last_update[idx-1])
            last_update[idx-1] = time
        if idx+2 < n:
            x[idx+2] += v[idx+2] * (time - last_update[idx+2])
            last_update[idx+2] = time
        m -= 1
        # calculate new collisions
        for i in range(max(0, idx-1), min(idx+2, n-1)):
            if(v[i] - v[i+1] > 0):
                pqueue.insert((time + (x[i+1]-x[i])/(v[i] - v[i+1]), i,
                               x[i] + v[i] * (x[i+1]-x[i])/(v[i] - v[i+1]), collision_cnt[i], collision_cnt[i+1],))
    return ans


print(listCollisions([10000.0, 1.0, 100.0], [
      0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
