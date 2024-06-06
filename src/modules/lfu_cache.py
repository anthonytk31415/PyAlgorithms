

class ValueNode:
    def __init__(self, key=None, val=None):
        self.val = val 
        self.key = key
        self.next = None
        self.prev = None
        self.frequencyNode = None

class FrequencyNode: 
    def __init__(self, val=None):
        self.val = val 
        self.count = 0
        self.next = None
        self.prev = None
        self.head = ValueNode()
        self.tail = ValueNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    ## Inserting and deletig will increment/decrement count
    ## when count == 0, we remove

# Frequency Nodes : from head , 1, 2, ..., tail
# hash table will contian key: valueNode

class LFUCache: 
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = {}               # key:value where value points to the valueNode
        self.frequencyHead = FrequencyNode()
        self.frequencyTail = FrequencyNode()
        self.frequencyHead.next = self.frequencyTail
        self.frequencyTail.prev = self.frequencyHead
        
    def get(self, key):
        if key not in self.storage: return -1
        valueNode = self.storage[key]
        # remove valueNode associated FrequencyNode
        self.removeListNode(valueNode)
        oldFrequencyNode = valueNode.frequencyNode        


        # if next FrequencyNode doesnt exist, create one
        if oldFrequencyNode.next.val == None or oldFrequencyNode.next.val != oldFrequencyNode.val + 1: 
             self.createFrequencyNodeAfterCurrentFrequencyNode(oldFrequencyNode)

        # insert valueNode at beginning of the next frequency node
        self.insertValueNodeAtBeginningOfFrequencyNode(valueNode, oldFrequencyNode.next)

        valueNode.frequencyNode = oldFrequencyNode.next
        
        # remove oldFrequencyNode if required
        self.decrementFrequencyNodeCount(oldFrequencyNode)
        return valueNode.val

    def put(self, key, value):
        if key in self.storage: 
            self.storage[key].val = value 
            self.get(key)           
            return 
        newValueNode = ValueNode(key, value)
        self.storage[key] = newValueNode
        if len(self.storage) > self.capacity: self.evictValueNode()
        if self.frequencyHead.next.val == None or self.frequencyHead.next.val != 1: self.createFrequencyNodeAtBeginning()
        firstFrequencyNode = self.frequencyHead.next
        newValueNode.frequencyNode = firstFrequencyNode
        self.insertValueNodeAtBeginningOfFrequencyNode(newValueNode, firstFrequencyNode)
        return 
    
    def insertValueNodeAtBeginningOfFrequencyNode(self, valueNode, frequencyNode):
        frequencyNode.count += 1
        newNext = frequencyNode.head.next
        frequencyNode.head.next = valueNode
        valueNode.prev = frequencyNode.head
        valueNode.next = newNext
        newNext.prev = valueNode

    # used for put requests 
    def createFrequencyNodeAtBeginning(self): 
        newFrequencyNode = FrequencyNode(val=1)
        newNext = self.frequencyHead.next
        self.frequencyHead.next = newFrequencyNode
        newFrequencyNode.prev = self.frequencyHead
        newFrequencyNode.next = newNext
        newNext.prev = newFrequencyNode

    # used for get requests; creates a node after freqNode; reattaches pointers
    def createFrequencyNodeAfterCurrentFrequencyNode(self, frequencyNode):     
        newFrequencyNode = FrequencyNode(frequencyNode.val + 1)
        newNext = frequencyNode.next
        newNext.prev = newFrequencyNode
        newFrequencyNode.next = newNext
        newFrequencyNode.prev = frequencyNode
        frequencyNode.next = newFrequencyNode

    # when removing valueNode, detatch the pointers, and null the node pointers
    def removeListNode(self, node):
        curPrev = node.prev
        curNext = node.next
        curPrev.next, curNext.prev = curNext, curPrev 
        node.prev, node.next = None, None

    ## if frequencyNode is empty after removal, then remove the node 
    def removeFrequencyNode(self, frequencyNode):
        oldPrev = frequencyNode.prev
        oldNext = frequencyNode.next
        oldPrev.next, oldNext.prev = oldNext, oldPrev
        frequencyNode.prev, frequencyNode.next = None, None

    # requires storage length > 0
    def evictValueNode(self):
        smallestFrequencyNode = self.frequencyHead.next
        nodeToRemove = smallestFrequencyNode.tail.prev
        self.removeListNode(nodeToRemove)            
        del self.storage[nodeToRemove.key]
        self.decrementFrequencyNodeCount(smallestFrequencyNode)


    def decrementFrequencyNodeCount(self, frequencyNode):
        frequencyNode.count -= 1
        if frequencyNode.count == 0: self.removeFrequencyNode(frequencyNode)

    # if removing valueNode causes frequencyNode to be empty, remove the FN

# c = LFUCache(2)
# c.put(1,1)
# c.put(2,2)
# print("GET 1: ", c.get(1))
# c.put(3,3)
# print("GET 2 should be -1: ", c.get(2))
# c.get(3) ## now theres only FN of 2 and that's it
# c.put(4,4) ## 1 gets evicted 
# # print(c.get(1))
# # print(c.get(3))
# # print(c.get(4))

# print(c.frequencyHead.next.next.val)


c = LFUCache(2)
c.put(3,1)
c.put(2,1)
c.put(2,2)
c.put(4,4)
c.get(2)



print("---- now iterating through the FN's -----")

fNode = c.frequencyHead
while fNode: 
    print(fNode.val)
    fNode = fNode.next

print("------now looking at LL's------")
node = c.frequencyHead.next.head
while node: 
    print(node.val)
    node = node.next