class Node:
    def __init__(self, data, left, right):
        self.data = data
        self.l = left
        self.r = right


class PointDatabase:
    def __init__(self, pointlist: list):
        length_leaf = 1
        while length_leaf*2 < len(pointlist):
            length_leaf *= 2
        self.tree = [[0]*2 for i in range(length_leaf-1 + len(pointlist))]
        self.Construct_X(sorted(pointlist), 0)

    def print_x(self, idx, space):
        if idx >= len(self.tree):
            return
        space += 10
        self.print_x(2*idx+2, space)
        print()
        for i in range(10, space):
            print(end=" ")
        print(self.tree[idx][0])

        self.print_x(2*idx+1, space)

    def Construct_X(self, ordered_set: list, idx):
        if len(ordered_set) == 0:
            return
        if len(ordered_set) == 1:
            self.tree[idx] = [ordered_set[0], [ordered_set[0]]]
            return
        mid = (len(ordered_set)-1)//2
        self.Construct_X(ordered_set[:mid+1], 2*idx+1)
        self.Construct_X(ordered_set[mid+1:], 2*idx+2)
        self.tree[idx] = [ordered_set[mid], self.MergeList_Y(
            self.tree[2*idx+1][1], self.tree[2*idx+2][1])]

    def MergeList_Y(self, arr1: list, arr2: list):
        merged = [0] * (len(arr1) + len(arr2))
        p1 = 0
        p2 = 0
        pmerge = 0
        while p1 < len(arr1) and p2 < len(arr2):
            if arr1[p1][1] < arr2[p2][1]:
                merged[pmerge] = arr1[p1]
                p1 += 1
            else:
                merged[pmerge] = arr2[p2]
                p2 += 1
            pmerge += 1
        while p1 < len(arr1):
            merged[pmerge] = arr1[p1]
            p1 += 1
            pmerge += 1
        while p2 < len(arr2):
            merged[pmerge] = arr2[p2]
            p2 += 1
            pmerge += 1
        return merged

    def searchNearby(self, q, d):
        ans = []
        return self.Query_X(q[0]-d, q[0]+d, q[1] - d, q[1]+d, ans)

    def Query_X(self, x_low, x_high, y_low, y_high, ans):
        splitNode = self.FindSplit(x_low, x_high)
        if splitNode == None:
            return ans
        if splitNode.l == None and splitNode.r == None:
            if x_low <= splitNode.data[0][0] and splitNode.data[0][0] <= x_high:
                self.Query_Y(splitNode.data[1], y_low, y_high, ans)
            return ans
        currNode = splitNode.l
        while currNode.l != None or currNode.r != None:
            if x_low <= currNode.data[0][0]:
                self.Query_Y(currNode.r.data[1], y_low, y_high, ans)
                currNode = currNode.l
            else:
                currNode = currNode.r
        if x_low <= currNode.data[0][0] and currNode.data[0][0] <= x_high:
            self.Query_Y(currNode.data[1], y_low, y_high, ans)
        currNode = splitNode.r
        while currNode.l != None or currNode.r != None:
            if currNode.data[0][0] < x_high:
                self.Query_Y(currNode.l.data[1], y_low, y_high, ans)
                currNode = currNode.r
            else:
                currNode = currNode.l
        if x_low <= currNode.data[0][0] and currNode.data[0][0] <= x_high:
            self.Query_Y(currNode.data[1], y_low, y_high, ans)
        return ans

    def FindSplit(self, x_low, x_high):
        currNode = self.root
        while currNode != None and (currNode.l != None or currNode.r != None) and (x_high <= currNode.data[0][0] or currNode.data[0][0] < x_low):
            if x_high <= currNode.data[0][0]:
                currNode = currNode.l
            else:
                currNode = currNode.r
        return currNode

    def Query_Y(self, arr: list, y_low, y_high, ans):
        lower = self.LowerBound_Y(arr, y_low)
        upper = self.UpperBound_Y(arr, y_high)
        if lower == -1 or upper == -1:
            return
        ans.extend(arr[lower:upper+1])
        return

    def LowerBound_Y(self, arr: list, y_low):
        idx = -1
        low = 0
        high = len(arr)-1
        while low <= high:
            mid = (low + high)//2
            if arr[mid][1] >= y_low:
                idx = mid
                high = mid-1
            else:
                low = mid+1
        return idx

    def UpperBound_Y(self, arr: list, y_high):
        idx = -1
        low = 0
        high = len(arr)-1
        while low <= high:
            mid = (low+high)//2
            if arr[mid][1] <= y_high:
                idx = mid
                low = mid+1
            else:
                high = mid-1
        return idx


pointDbObject = PointDatabase([(1, 6), (2, 4), (3, 7), (4, 9), (5, 1), (6, 3), (7, 8), (8, 10),
                               (10, 5), (9, 2)])
pointDbObject.print_x(0, 0)

# print(pointDbObject.FindSplit(30, 40).data)


# print(pointDbObject.searchNearby((5, 5), 1))
# print(pointDbObject.searchNearby((4, 8), 2))
# print(pointDbObject.searchNearby((10, 2), 1.5))
# print(pointDbObject.searchNearby((-1, -1), 100))
