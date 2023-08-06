"""
class:

ListNode(val=0, next=None)

method:

None     <- printList(head: ListNode, style=[None, 1], limit=100)
ListNode <- fromArray(a: list)
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return "<ListNode {}>".format(self.val)
    

def printList(head, style=None, limit=100):
    """
    if style is anything but None, then output using arrow style.
    """
    curr = head
    c = 0
    print('[', end='')
    while curr and c < limit:
        if style:
            print(curr.val, end=' -> ')
        else:
            print(curr.val, end=', ')
        curr = curr.next
        c += 1
    print(']')


def fromArray(a):
    """
    Return the head, construct a linkedlist from an array
    """
    dummy = ListNode(0, None)
    curr = dummy
    for e in a:
        curr.next = ListNode(e)
        curr = curr.next
    return dummy.next
