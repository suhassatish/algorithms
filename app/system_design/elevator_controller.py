"""
Call button (up/down)

Inside elevator buttons -
    door open/close
    emergency alarm bell
    floor #

load/capacity
camera (security)

order of floor requests (internal priority queue with priority to current direction)


Elevator controller -> command_to_go -> elevator

Flow chart:
Start
Sensors notify elevatro fir a stop at floor-x
elevator matches x with the next in the queue
if match:
    make stop
else:
    continue
end

Strategy for controller:
1) Always choose the nearest elevator as long as its not moving in opposite direction of request.
2) Choose an elevator thats not moving (ie, its Q is empty)

Make sure strategy is pluggable so that depending on peak traffic patterns at different times of
day, you can program it to pick different strategies at different times.
This is the most important design pattern to demonstrate in this problem.
Eg - In the morning, when you are on ground floor, and door is closing, you dont want to re-open
and allow new person, because that way elevator will be stuck on ground floor forever.
"""