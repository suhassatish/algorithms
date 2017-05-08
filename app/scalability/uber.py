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

------------------------------------------------------------------------------------
MORE ON GEO-SPATIAL INDEXING, GEOHASHING AND GOOGLE'S S2 CELLS-

Google uses something called HILBERT CURVES. You can plot map points on this Hilbert curve.
When you stretch out this curve into a long string, and add an index to each entry, geographically
closer points come close together, in-terms of array indices. This means, you dont have to scan the
whole list of points to find ones that are close, just a few on either side of your starting
position.
-----
Implementation details of S2 cells - Google PPT - Geometry on the sphere
https://docs.google.com/presentation/d/1Hl4KapfAENAOf4gv-pSngKwvS_jwNVHRPZTTDzXXn6Q/view?pli=1#slide=id.i22
Main ideas -
1) Given a lat,long of the earth, place the sphere (Earth) inside a 3-D cube. Find the x,y,z co-ords
within the cube of the lat,long, ie (lat, long) -> (x, y, z) transform.

2) Project the inner point of the cube (x, y, z) onto a face of the cube
(x,y,z) -> (face, u, v) -> (face, s, t) -> S2_cell_id

u,v is in range (-1, +1) but (s, t) is in range (0,1).

3) Given a 64-bit integer and a known level (how fine-grained the google map is), every square
centimetre on earth can be represented by Hilbert curves and S2 cells. Key property is the symmetric
fractal nature of Hilbert curves that lets you achieve this.
Some stats -
Level|min_area |max_area |
0    |85M sq km|85M sq km|entire earth
1    |21M sq km|21M sq km|4 quarter-spheres of earth
12   |3.3 sq km|6.3 sq km|
30   |0.5 sq cm|0.9 sq cm|

64 bit= 1st 3 bits = which face of the cube; next 61 bits = position along hilbert curve,
index on [0: 2^level - 1] x [0: 2^level - 1] grid
For level2, [0:3] x [0:3] grid (4-bits)
For level30, [0:30] x [0:30] (60-bits)
------------------------------------------------------------------------------------
GEOHASH VS S2 PERFORMANCE COMPARISON -
http://blog.nobugware.com/post/2016/geo_db_s2_geohash_database/

1) Geohash has 12 different widths. When you lookup nearest neighbors of p = (x,y) within its
current geohash cell c1, and if p is close to the edge of c1, you will miss neighboring cells.
So you will have to look at neighboring geohash cells, which can be upto 3 different neighbors.
(rectangular window). Also, you may have to zoom-in or zoom-out and look at more fine-grained
or coarse-grained info 1 level up in geohash  width and 1 level down in geohash width.
So 4 cells in current level, 4 cells 1-level up and 4 cells 1-level down = 12 geohash lookups in DB
for nearest neighbors of 1 point p.

2) Space - The most precise geohash needs 12 bytes storage, but an S2 cell is just  a 64-bit int
(8 bytes), its convenient to store

3) In geohashing, there are discontinuities around lat-longs 0, +-90 degrees, +-180 degrees

4) Main advantage of S2 cell is the Region Coverer Algorithm. Given any region and the max_cells
as input, it will find different cells at different levels that cover your region with much fewer
DB range-queries. So less DB reads, less object unmarshalling. Implementation detail: Big endian
is required to store the S2 cell-id for lexicographical sort order.
------------------------------------------------------------------------------------
TODO -
HTTP://HIGHSCALABILITY.COM/BLOG/2015/9/14/HOW-UBER-SCALES-THEIR-REAL-TIME-MARKET-PLATFORM.HTML


"""
