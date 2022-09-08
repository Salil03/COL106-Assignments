# ______________________________________________________________________________________________
class MinPriorityQueue:
    '''Minimum Priority Queue Implementation using Min-Heap. 

    Heap is stored in an array where left child = 2*i+1 and right child is 2*i+2. This convention is followed to allow 0-indexing'''

    def min_heapify(self, idx):
        '''send value at idx to correct position and maintain heap property'''
        if idx >= self._size:
            raise Exception("Index out of range of heap")
        left = 2*idx+1
        right = 2*idx + 2
        minimum = idx
        if left < self._size and self._array[left] < self._array[minimum]:
            minimum = left
        if right < self._size and self._array[right] < self._array[minimum]:
            minimum = right
        if minimum != idx:
            self._array[minimum], self._array[idx] = self._array[idx], self._array[minimum]
            min_heapify(self, minimum)

    def __init__(self, array):
        '''initialize the heap in O(n)

        _size: size of the heap
        _arraysize: size of the container array
        _array: reference to container array
        '''
        self._arraysize = len(array)
        self._size = len(array)
        self._array = array
        for i in range(self._size//2 - 1, -1, -1):
            self.min_heapify(i)

    def top(self):
        '''returns the minimum value in priority queue'''
        if self.is_empty():
            raise Exception("Top called on empty Priority Queue")
        return self._array[0]

    def pop(self):
        '''return the minimum value and removes it from priority queue'''
        if self.is_empty():
            raise Exception("Pop called on empty Priority Queue")
        minimum = self._array[0]
        self._array[0] = self._array[self._size-1]
        self._size -= 1
        if self._size > 0:
            self.min_heapify(0)
        return minimum

    def decrease_value(self, idx, value):
        '''decrease the key at position idx and set it to value'''
        if idx >= self._size:
            raise Exception("Index out of Range")
        self._array[idx] = value
        while idx > 0 and self._array[(idx-1)//2] > self._array[idx]:
            self._array[(
                idx-1)//2], self._array[idx] = self._array[idx], self._array[(idx-1)//2]
            idx = (idx-1)//2

    def insert(self, value):
        '''insert new element in priority queue'''
        self._size += 1
        if self._arraysize >= self._size:
            self._array[self._size-1] = (float('inf'), -1, -1,)
        else:
            self._array.append((float('inf'), -1, -1,))
            self._arraysize += 1
        self.decrease_value(self._size-1, value)

    def is_empty(self):
        return (self._size == 0)

# ______________________________________________________________________________________________


def listCollisions(M, x, v, m, T):
    '''Takes n points and simulates m collisions or till time T

    M: a list of positive floats, where M[i] is the mass of the ith object,
    x: a sorted list of floats, where x[i] is the initial position of the ith object,
    v: a list of floats, where v[i] is the initial velocity of the ith object,
    m: a non-negative integer,
    T: a non-negative float,
    '''
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

        ans.append((float('%.4f' % (time)), idx, float('%.4f' % (pos)),))

        # update all parameters of idx and idx+1
        x[idx], x[idx+1] = pos, pos
        v[idx], v[idx+1] = (M[idx] - M[idx+1])/(M[idx] + M[idx+1]) * v[idx] + 2*M[idx+1] * v[idx+1]/(
            M[idx]+M[idx+1]), 2*M[idx]*v[idx]/(M[idx] + M[idx+1]) - (M[idx] - M[idx+1])*v[idx+1]/(M[idx] + M[idx+1])
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


# print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
# print(listCollisions([1.0, 1.0, 1.0, 1.0],
#       [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5, 5.0))
# print(listCollisions([10000.0, 1.0, 100.0], [
#       0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
# print(listCollisions([10000.0, 1.0, 100.0], [
#       0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))
