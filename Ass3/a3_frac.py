class Node:
    def __init__(self, data, left, right):
        self.data = data
        self.l = left
        self.r = right


class PointDatabase:
    def __init__(self, pointlist: list):
        self.root = self.Construct_X(sorted(pointlist))

    def print_x(self, root: Node, space):
        if root == None:
            return
        space += 10
        self.print_x(root.r, space)
        print()
        for i in range(10, space):
            print(end=" ")
        print(root.data[0])

        self.print_x(root.l, space)

    def Construct_X(self, ordered_set: list):
        if len(ordered_set) == 0:
            return None
        if len(ordered_set) == 1:
            return Node((ordered_set[0], [[ordered_set[0], -1, -1]],), None, None)
        mid = (len(ordered_set) - 1)//2
        left = self.Construct_X(ordered_set[:mid+1])
        right = self.Construct_X(ordered_set[mid+1:])
        return Node((ordered_set[mid], self.MergeList_Y(left.data[1], right.data[1]), ), left, right)

    def MergeList_Y(self, arr1: list, arr2: list):
        merged = [[-1]*3 for i in range(len(arr1) + len(arr2))]
        p1 = 0
        p2 = 0
        pmerge = 0
        while p1 < len(arr1) and p2 < len(arr2):
            if arr1[p1][0][1] < arr2[p2][0][1]:
                merged[pmerge][0] = arr1[p1][0]
                p1 += 1
            else:
                merged[pmerge][0] = arr2[p2][0]
                p2 += 1
            pmerge += 1
        while p1 < len(arr1):
            merged[pmerge][0] = arr1[p1][0]
            p1 += 1
            pmerge += 1
        while p2 < len(arr2):
            merged[pmerge][0] = arr2[p2][0]
            p2 += 1
            pmerge += 1
        p1 = 0
        p2 = 0
        pmerge = 0
        while pmerge < len(merged) and p1 < len(arr1):
            if merged[pmerge][0][1] <= arr1[p1][0][1]:
                merged[pmerge][1] = p1
                pmerge += 1
            else:
                while p1 < len(arr1) and merged[pmerge][0][1] > arr1[p1][0][1]:
                    p1 += 1
        pmerge = 0
        while pmerge < len(merged) and p2 < len(arr2):
            if merged[pmerge][0][1] <= arr2[p2][0][1]:
                merged[pmerge][2] = p2
                pmerge += 1
            else:
                while p2 < len(arr2) and merged[pmerge][0][1] > arr2[p2][0][1]:
                    p2 += 1
        return merged

    def searchNearby(self, q, d):
        ans = []
        return self.Query_X(q[0]-d, q[0]+d, q[1] - d, q[1]+d, ans)

    def Query_X(self, x_low, x_high, y_low, y_high, ans):
        if self.root == None:
            return ans
        lower = self.LowerBound_Y(self.root.data[1], y_low)
        if lower == -1:
            return ans
        splitNode, lower = self.FindSplit(x_low, x_high, lower)
        if splitNode == None or lower == -1:
            return ans
        if splitNode.l == None and splitNode.r == None:
            if x_low <= splitNode.data[0][0] and splitNode.data[0][0] <= x_high and y_low <= splitNode.data[0][1] and splitNode.data[0][1] <= y_high:
                ans.append(splitNode.data[0])
            return ans
        currNode = splitNode.l
        currLower = splitNode.data[1][lower][1]
        while (currNode.l != None or currNode.r != None) and currLower != -1:
            if x_low <= currNode.data[0][0]:
                self.Query_Y(
                    currNode.r.data[1], currNode.data[1][currLower][2], y_low, y_high, ans)
                currLower = currNode.data[1][currLower][1]
                currNode = currNode.l
            else:
                currLower = currNode.data[1][currLower][2]
                currNode = currNode.r
        if x_low <= currNode.data[0][0] and currNode.data[0][0] <= x_high and y_low <= currNode.data[0][1] and currNode.data[0][1] <= y_high:
            ans.append(currNode.data[0])
        currNode = splitNode.r
        currLower = splitNode.data[1][lower][2]
        while currNode.l != None or currNode.r != None and currLower != -1:
            if currNode.data[0][0] < x_high:
                self.Query_Y(
                    currNode.l.data[1], currNode.data[1][currLower][1], y_low, y_high, ans)
                currLower = currNode.data[1][currLower][2]
                currNode = currNode.r
            else:
                currLower = currNode.data[1][currLower][1]
                currNode = currNode.l
        if x_low <= currNode.data[0][0] and currNode.data[0][0] <= x_high and y_low <= currNode.data[0][1] and currNode.data[0][1] <= y_high:
            ans.append(currNode.data[0])
        return ans

    def FindSplit(self, x_low, x_high, lower):
        currNode = self.root
        while currNode != None and (currNode.l != None or currNode.r != None) and (x_high <= currNode.data[0][0] or currNode.data[0][0] < x_low) and lower != -1:
            if x_high <= currNode.data[0][0]:
                lower = currNode.data[1][lower][1]
                currNode = currNode.l
            else:
                lower = currNode.data[1][lower][2]
                currNode = currNode.r
        return (currNode, lower)

    def Query_Y(self, arr: list, lower, y_low, y_high, ans):
        if lower == -1:
            return
        while lower < len(arr) and y_low <= arr[lower][0][1] and arr[lower][0][1] <= y_high:
            ans.append(arr[lower][0])
            lower += 1

    def LowerBound_Y(self, arr: list, y_low):
        idx = -1
        low = 0
        high = len(arr)-1
        while low <= high:
            mid = (low + high)//2
            if arr[mid][0][1] >= y_low:
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
            if arr[mid][0][1] <= y_high:
                idx = mid
                low = mid+1
            else:
                high = mid-1
        return idx


pointDbObject = PointDatabase([(1, 6), (2, 4), (3, 7), (4, 9), (5, 1), (6, 3), (7, 8), (8, 10),
                               (10, 5), (9, 2)])
pointDbObject.print_x(pointDbObject.root, 0)

# print(pointDbObject.searchNearby((5, 5), 1))
# print(pointDbObject.searchNearby((4, 8), 2))
# print(pointDbObject.searchNearby((10, 2), 1.5))
# print(pointDbObject.searchNearby((-1, -1), 100))
