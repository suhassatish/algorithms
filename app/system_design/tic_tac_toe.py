"""
3 by 3 tic-tac-toe game design
Requirement:
You want to build a library for tic-tac-toe where you can put it on hardware and have a kiosk
with gaming console.

Your engine should enforce the rules of the game.

X,O are markers.

|X|O|X|
|O|X|O|
|O|X|O|

Rules:
1) Players cannot take each-other's turn away.
2) Cannot put marker on taken spot
3) Cannot allow any more moves once someone wins or if all slots are filled

Outcomes -
1 player wins or there is a draw

State machine:
Start -> in progress -> over
             U
         self-loop

class Board(object):
    pass

You need a RuleEngine to isolate who executes the rule vs who implements the rule.
eg - Financial risk - if some IP address and some geographic region and some transaction
and some limited credit history, then flag as fraud!
Here, for this problem, it may be overkill.

"""