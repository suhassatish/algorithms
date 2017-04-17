#
# Your previous Plain Text content is preserved below:
#
# image = [
#   [1, 1, 1, 1, 1, 1, 1],
#   [1, 1, 1, 1, 1, 1, 1],
#   [1, 1, 1, 0, 0, 0, 1],
#   [1, 1, 1, 0, 0, 0, 1],
#   [1, 1, 1, 1, 1, 1, 1],
# ];
#
# 1 = background
# 0 = GUARANTEED exactly one rectangle
#
# image ≥ 1x1 (image == MxN)
# 1x1 ≤ rectangle ≥ MxN
#
# Write a function to return the coordinates of the rectangle:
#   input - image
#   output - top-left and bottom-right corners OR
#            top-left corner, width, and height
#
# def say_hello():
#     print 'Hello, World'

# for i in xrange(5):
#     say_hello()


#
# Your previous Plain Text content is preserved below:
#
# image = [
#   [1, 1, 1, 1, 1, 1, 1],
#   [1, 1, 1, 1, 1, 1, 1],
#   [1, 1, 1, 0, 0, 0, 1],
#   [1, 1, 1, 0, 0, 0, 1],
#   [1, 1, 1, 1, 1, 1, 1],
# ];
#
# 1 = background
# 0 = GUARANTEED exactly one rectangle
#
# image ≥ 1x1 (image == MxN)
# 1x1 ≤ rectangle ≥ MxN
#
# Write a function to return the coordinates of the rectangle:
#   input - image
#   output - top-left and bottom-right corners OR
#            top-left corner, width, and height
#


def get_rectangle_coordinates(matrix):
    """
    returns top-left corner's co-ordinate assuming top-left of input = (0,0)
    height, width as a tuple
    :param matrix: 2D array of booleans
    :output: tuple of ((inner_rect_coordinate_x, inner_rect_coordinate_y), height,width)

    """
    if matrix is None or len(matrix) == 0 :
        return None
    rows = len(matrix)
    cols = len(matrix[0])
    start_x = None
    start_y = None
    height = width = None
    for row in xrange(len(matrix)):
        for col in xrange(len(matrix[0])):
            if matrix[row][col] == 1:
                continue
            else:
                start_x,start_y = row, col
                break
        if start_x is not None:
            break
    if start_x is not None:
        width = height = 0
        col = start_y
        row = start_x
        while col < cols:
            if matrix[start_x][col] == 0:
                width += 1
                col += 1
            else:
                break
        while row < rows:
            if matrix[row][start_y] == 0:
                height += 1
                row += 1
            else:
                break
    return ((start_x, start_y), height, width)


def get_rectangle_coordinates2(matrix):
    """
    Note: this method does not work for overlapping rectangles. The time complexity is O(n^2 * m^2)

    :param matrix:
    :return:
    """
    if matrix is None or len(matrix) == 0 :
        return None
    rows = len(matrix)
    cols = len(matrix[0])
    start_x = None
    start_y = None
    height = width = None
    visited = [[0 for col in xrange(cols)] for row in xrange(rows)]
    rectangles = []
    for row in xrange(len(matrix)):
        for col in xrange(len(matrix[0])):
            if visited[row][col]:
                continue

            if matrix[row][col] == 1:
                visited[row][col] = 1
                continue
            else:
                start_x,start_y = row, col
                visited[row][col] = 1

            if start_x is not None:
                width = height = 0
                c = col
                r = row
                while c < cols:
                    if matrix[start_x][c] == 0:
                        visited[start_x][c] = 1
                        width += 1
                        c += 1
                    else:
                        break
                while r < rows:
                    if matrix[r][start_y] == 0:
                        visited[r][start_y] = 1
                        height += 1
                        r += 1
                    else:
                        break
                for x in xrange(start_x,start_x + height):
                    for y in xrange(start_y, start_y + width):
                        visited[x][y] = 1
                rectangles.append(((start_x, start_y), height,  width))
                start_x = start_y = height = width = None
    return rectangles

if __name__ == '__main__':
    image = [
      [1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 0, 0, 0, 1],
      [1, 0, 1, 0, 0, 0, 1],
      [1, 0, 1, 1, 1, 1, 0],
      [1, 0, 1, 0, 0, 1, 1],
      [1, 1, 1, 0, 0, 1, 1],
      [1, 1, 1, 1, 1, 1, 1],
    ]
    print get_rectangle_coordinates2(image)
    #  [((2, 3), 2, 3), ((3, 1), 3, 1), ((4, 6), 1, 1), ((5, 3), 2, 2)]
    #  worst-case time complexity = O(n^2 * m^2); space complexity = O(mn)

    # for get_rectangle_coordinates(image), worst-case time = O(mn); space = O(1)
