# Listing - apartment or home
# Host - owner of a listing(s)

# Query (location + date + guests + ...) -> list of listings

# Improve:
# 1. Paginate
# 2. At most one results from each host per page

# # "host_id,listing_id,score,city",
inp = [
    "1,28,300.1,San Francisco",  # <- one listing / result
    "4,5,209.1,San Francisco",
    "20,7,208.1,San Francisco",
    "23,8,207.1,San Francisco",
    "16,10,206.1,Oakland",
    "1,16,205.1,San Francisco",
    "1,31,204.6,San Francisco",
    "6,29,204.1,San Francisco",
    "7,20,203.1,San Francisco",
    "8,21,202.1,San Francisco",
    "2,18,201.1,San Francisco",
    "2,30,200.1,San Francisco",
    "15,27,109.1,Oakland",
    "10,13,108.1,Oakland",
    "11,26,107.1,Oakland",

    "12,9,106.1,Oakland",
    "13,1,105.1,Oakland",
    "22,17,104.1,Oakland",
    "1,2,103.1,Oakland",
    "28,24,102.1,Oakland",
    "18,14,11.1,San Jose",
    "6,25,10.1,Oakland",
    "19,15,9.1,San Jose",
    "3,19,8.1,San Jose",

    "3,11,7.1,Oakland",
    "27,12,6.1,Oakland",
    "1,3,5.1,Oakland",
    "25,4,4.1,San Jose",
    "5,6,3.1,San Jose",
    "29,22,2.1,San Jose",
    "30,23,1.1,San Jose"
]

expected_out = [
    "0 1,28,300.1,San Francisco",
    "0 4,5,209.1,San Francisco",
    "0 20,7,208.1,San Francisco",
    "0 23,8,207.1,San Francisco",
    "0 16,10,206.1,Oakland",
    "0 6,29,204.1,San Francisco",
    "0 7,20,203.1,San Francisco",
    "0 8,21,202.1,San Francisco",
    "0 2,18,201.1,San Francisco",
    "0 15,27,109.1,Oakland",
    "0 10,13,108.1,Oakland",
    "0 11,26,107.1,Oakland",

    "1 1,16,205.1,San Francisco",
    "1 2,30,200.1,San Francisco",
    "1 12,9,106.1,Oakland",
    "1 13,1,105.1,Oakland",
    "1 22,17,104.1,Oakland",
    "1 28,24,102.1,Oakland",
    "1 18,14,11.1,San Jose",
    "1 6,25,10.1,Oakland",
    "1 19,15,9.1,San Jose",
    "1 3,19,8.1,San Jose",
    "1 27,12,6.1,Oakland",
    "1 25,4,4.1,San Jose",

    "2 1,31,204.6,San Francisco",
    "2 3,11,7.1,Oakland",
    "2 5,6,3.1,San Jose",
    "2 29,22,2.1,San Jose",
    "2 30,23,1.1,San Jose",

    "3 1,2,103.1,Oakland"
]
NUM_RESULTS_PER_PAGE = 12


def display_pages_buggy(a):
    shown = set()
    total_shown = 0
    i = 0
    out = []
    page_contents = []

    while total_shown < len(a):
        # i = 0
        while i in shown:
            i += 1
            continue

        if len(page_contents) % NUM_RESULTS_PER_PAGE == 0:  # start of a new page
            host_st = set()
            page_contents = []
            i = 0

        if i >= len(a):
            return out

        e = a[i]
        # if i == 5:
        #     print shown, total_shown, host_st, page_contents

        host_id = e.split(',')[0]
        if host_id in host_st:  # skip
            i += 1
            continue
        else:
            host_st.add(host_id)
            page_contents.append(e)
            shown.add(i)
            total_shown += 1
            i += 1

        if len(page_contents) == 12:
            out.append(page_contents)

    return out


def display_pages_working(a):
    i = 0
    out = list()
    page_contents = []
    host_st = set()

    while a:  # in python, you can iterate over a list and still delete its elements
        # without getting a ConcurrentModificationException unlike java

        if (page_contents and len(page_contents) % NUM_RESULTS_PER_PAGE == 0)\
                or i >= len(a):  # start of a new page
            out.append(page_contents)
            host_st.clear()
            page_contents = []
            i = 0

        e = a[i]

        host_id = e.split(',')[0]
        if host_id in host_st:  # skip
            i += 1
            continue
        else:
            host_st.add(host_id)
            page_contents.append(e)
            a.remove(e)  # this is the critical step which simplifies the code, so that additional
            # state variables and data structures like `total_shown` and `shown` are not needed

    return out


for page_number, page in enumerate(display_pages_working(inp)):
    for result in page:
        print page_number, result
