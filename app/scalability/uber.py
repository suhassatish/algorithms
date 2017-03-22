"""
Requirements:
rider{(latitude, longitude), seats, destination, pool/X/wheelchair-accessible/child-seats}

How to match supply-demand in few seconds as soon as a user logs-in?

First find all cars within a radius, then filter out cars that dont meet the criteria of user
requirements.

If cars are static and parked in parking lots, each car is talking to uber app and sending out a
heart-beat time of last-known-location.

|car_id|last_known_location|capacity_seats|latitude|longitude|
Geo-spatial indexing is an application in itself. Elastic search supports radius as an off-the-shelf
computation. Google has done something called S2. It uses entire earth as bunch of grid cells.
Breaks out everything as an S2 cell. Given a lat-long, it tells all S2 cells associated with a
particular radius.

Interview question: Given a bunch of rectangles, a point and a particular radius,  give all the
rectangles that touches the circle of that radius around that point. Then find grids that are
fully encompassed.

Given cars are moving with a certain velocity, how do we solve the problem?
hashing. what do we hash on? Based on lat-long, we get the S2 cell and thats my key.
Drivers hash-map
|key   |value
S2_cell|car1 ->car2 -> car3

How to honor the most-recent heart-beat and discard cell-locations that have stale timestamps.
Keeping updating the hash-map is not ideal.

For this you need a reverse hash of
driver -> cell he's in.

Once this is done, dispatch_service says these are the 10 potential drivers.
Then there is a ranking algo based on drivers_response_time, nearness, etc
Its a bad driver experience to make them take an action to "accept passenger" which will then get
rejected. So there is not a broadcast, but a unicast, and then if driver doesnt accept within a
certain time frame, send request to next driver, and so on.
"""
