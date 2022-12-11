class MinPriorityQueue:
    '''Minimum Priority Queue Implementation using Min-Heap.

    Heap is stored in an array where left child = 2*i+1 and right child is 2*i+2. This convention is followed to allow 0-indexing'''
    __slots__ = '_arraysize', '_size', '_array'

    def min_heapify(self, idx):
        '''send value at idx to correct position and maintain heap property'''
        minimum = -1
        left = -1
        right = -1
        while idx != minimum:
            left = 2*idx+1
            right = 2*idx+2
            minimum = idx
            if left < self._size and self._array[left] < self._array[minimum]:
                minimum = left
            if right < self._size and self._array[right] < self._array[minimum]:
                minimum = right
            if minimum != idx:
                self._array[minimum], self._array[idx] = self._array[idx], self._array[minimum]
                idx = minimum
                minimum = -1

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
        return self._array[0]

    def pop(self):
        '''return the minimum value and removes it from priority queue'''
        minimum = self._array[0]
        self._array[0] = self._array[self._size-1]
        self._size -= 1
        if self._size > 0:
            self.min_heapify(0)
        return minimum

    def decrease_value(self, idx, value):
        '''decrease the key at position idx and set it to value'''
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

# __________________________________________________________________________________________________________


def findMaxCapacity(n, links, s, t):
    graph = [[] for i in range(n)]  # stores the graph in an adjacency list
    INT_MAX = links[0][2]  # holds the value of inf, calculated by max of all edges +10
    for u, v, cap in links:  # build adjacency list
        graph[u].append((v, cap))
        graph[v].append((u, cap))
        INT_MAX = max(cap, INT_MAX)
    MaxCapacity = [-1] * n  # holds the value of maximum packet size from source to ith node
    MaxCapacity[s] = INT_MAX + 10
    backtrack = [-1] * n  # holds the parent of most optimum path according to Dijkstra's
    visited = [False]*n  # true if node is already visited
    pqueue = MinPriorityQueue([(-INT_MAX - 10, s)])  # insert negative capacities because its a min-priority queue
    while not pqueue.is_empty():
        curr = pqueue.pop()[1]
        if curr == t:  # once t is selected, its MaxCapacity is final. so we can break
            break
        if visited[curr]:
            continue
        visited[curr] = True
        for node, capacity in graph[curr]:
            if MaxCapacity[node] < min(MaxCapacity[curr], capacity):  # contract the path
                MaxCapacity[node] = min(MaxCapacity[curr], capacity)
                pqueue.insert((-MaxCapacity[node], node))
                backtrack[node] = curr
    # restore optimum path
    node = t
    path = []
    while node != -1:
        path.append(node)
        node = backtrack[node]
    return MaxCapacity[t], path[::-1]  # path is restored in reverse order
