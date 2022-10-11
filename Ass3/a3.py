class Node:
    __slots__ = 'node', 'y_list', 'l', 'r'

    def __init__(self, node, y_list, left, right):
        self.node = node
        self.y_list = y_list
        self.l = left
        self.r = right


class PointDatabase:
    __slots__ = 'root'

    def __init__(self, pointlist: list):
        self.root = self.Construct_X(sorted(pointlist), 0, len(pointlist)-1)

    # construct BST sorted by xcoord where each node contains all nodes in its subtree sorted by ycoord
    def Construct_X(self, ordered_set: list, low, high):
        if low > high:
            return None
        if low == high:
            return Node(ordered_set[low], [ordered_set[low]], None, None)
        mid = (high - low)//2 + low
        left = self.Construct_X(ordered_set, low, mid)
        right = self.Construct_X(ordered_set, mid+1, high)
        return Node(ordered_set[mid], self.MergeList_Y(left.y_list, right.y_list), left, right)

    # merge sorted arr1 and sorted arr2 into another sorted array
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
        # find last common node
        splitNode = self.FindSplit(x_low, x_high)
        #tree is empty
        if splitNode == None:
            return ans

        # splitNode is a leaf
        if splitNode.l == None:
            if x_low <= splitNode.node[0] <= x_high and y_low <= splitNode.node[1] <= y_high:
                ans.append(splitNode.node)
            return ans

        # traverse from splitNode to x_low
        currNode = splitNode.l
        while currNode.l != None:
            if x_low <= currNode.node[0]:            # include whole r subtree
                self.Query_Y(currNode.r.y_list, y_low, y_high, ans)
                currNode = currNode.l
            else:
                currNode = currNode.r
        # currNode is a leaf
        if x_low <= currNode.node[0] <= x_high and y_low <= currNode.node[1] <= y_high:
            ans.append(currNode.node)

        # traverse from splitNode to x_high
        currNode = splitNode.r
        while currNode.l != None:
            if currNode.node[0] < x_high:  # include whole l subtree
                self.Query_Y(currNode.l.y_list, y_low, y_high, ans)
                currNode = currNode.r
            else:
                currNode = currNode.l
        # currNode is a leaf
        if x_low <= currNode.node[0] <= x_high and y_low <= currNode.node[1] <= y_high:
            ans.append(currNode.node)
        return ans

    # find last common node on the path from root to x_low and x_high
    def FindSplit(self, x_low, x_high):
        currNode = self.root
        while currNode != None and currNode.l != None:
            if x_high <= currNode.node[0]:
                currNode = currNode.l
            elif currNode.node[0] < x_low:
                currNode = currNode.r
            else:
                break
        return currNode

    def Query_Y(self, arr: list, y_low, y_high, ans):  # 1d range query using binary search
        lower = self.LowerBound_Y(arr, y_low)
        upper = self.UpperBound_Y(arr, y_high)
        if lower == -1 or upper == -1:  # no element in range
            return
        ans.extend(arr[lower:upper+1])
        return

    def LowerBound_Y(self, arr: list, y_low):  # binary search first geq element
        if arr[-1][1] < y_low:
            return -1
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

    def UpperBound_Y(self, arr: list, y_high):  # binary search last leq element
        if arr[0][1] > y_high:
            return -1
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


# pointDbObject = PointDatabase(
#     [(1, 6), (2, 4), (3, 7), (4, 9), (5, 1), (6, 3), (7, 8), (8, 10), (10, 5), (9, 2)])
# print(pointDbObject.searchNearby((5, 5), 1))
# print(pointDbObject.searchNearby((4, 8), 2))
# print(pointDbObject.searchNearby((10, 2), 1.5))
# print(pointDbObject.searchNearby((-1, -1), 100))
# print(pointDbObject.searchNearby((4, 9), 0))
