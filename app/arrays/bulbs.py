"""
Given bulb_array,

Implement method
boolean isON(int i)

void toggle(int begin, int end) -> toggles all bulbs from off/on in between indices [begin, end]
In a naive array of switches implementation, isOn can be implemented in O(1) but toggle takes O(n)
How to balance the API times for both to be similar?

Important property of XOR. If you toggle one of the inputs, you toggle the output.

Use 2n switches arranged as a binary tree, with n leaves.

XOR of root to leaf path for the isOn function. This can be done in O(log n)

toggle(0,15) => just toggle the root switch
toggle(1,14) => toggle the root which turns on everything, then toggle the S0 leaf and S15.
Whats the maximum number of switches that I need to toggle?

"""