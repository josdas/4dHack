def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def sca(a, b, c):
    return (c[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (c[1] - a[1]) < 0


# Return true if line segments ab and cd intersect
def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def rel_error(x, y):
    return (x - y) / max(y, 1)
