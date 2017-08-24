def merge_sort(a):
    lo = 0
    hi = len(a) - 1
    mid = (lo + hi) / 2
    msort(a, lo, mid)
    msort(a, mid+1, hi)
    merge(a, lo, mid, hi)
    # recursive work before iterative, ie its not tail recursion


def msort(a, lo, hi):
    pass


def merge(a, lo, mid, hi):
    i = lo
    j = mid + 1
    b = []
    if a[i] <= a[j]:
        b.append(a[i])
        i += 1
    else:
        b.append(a[j])
        j += 1
    if i > mid:
        b.append(a[j:])
    if j > hi:
        b.append(a[i:mid+1])
    return b