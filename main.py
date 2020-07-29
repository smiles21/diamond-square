import numpy as np


def create_grid(side_length):
  """
  Create a square grid of all zeros of size side_length
  """
  return np.zeros((side_length, side_length))


def generate_step_lengths(n):
  """
  Create a list of side lengths to help with running this iteratively
  instead of recursively.  

  n = 2: returns [4, 2]
  n = 3: returns [8, 4, 2]
  n = n: returns [2^n, 2^(n-1), ..., 2^2, 2^1]
  """
  return [2**i for i in np.arange(n, 0, -1)]


def generate_internal_squares(t_l, b_r, side_length):
  """
  Create the internal squares from top left to bottom right
  with side lengths of side_length
  """
  squares = []

  for i in range(b_r[0] // side_length):
    for j in range(b_r[1] // side_length):
      square = {
        't_l': (t_l[0] + (i * side_length), t_l[0] + (j * side_length)),
        't_r': (t_l[0] + (i * side_length), t_l[0] + ((j + 1) * side_length)),
        'b_l': (t_l[0] + ((i + 1) * side_length), t_l[0] + (j * side_length)),
        'b_r': (t_l[0] + ((i + 1) * side_length), t_l[0] + ((j + 1) * side_length)),
      }
      squares.append(square)

  return squares


def generate_noise(noisiness = 0):
  if noisiness == 0:
    return 0

  return np.random.normal(0, 0.01) * noisiness


def set_corners(grid, min_val = 0, max_val = 10):
  """
  Set the values of the corners to random values
  """
  values = np.random.randint(min_val, max_val, 4)
  edge_val = len(grid) - 1

  grid[0, 0] = values[0]
  grid[0, edge_val] = values[1]
  grid[edge_val, 0] = values[2]
  grid[edge_val, edge_val] = values[3]

  return grid


def calc_midpoint(top_left, bottom_right):
  """
  Calculate the coorindates of the midpoint given the top-left and
  bottom-right corners of the square
  """
  midpoint_x = ((bottom_right[0] - top_left[0]) // 2) + top_left[0]
  midpoint_y = ((bottom_right[1] - top_left[1]) // 2) + top_left[1]

  return (midpoint_x, midpoint_y)


def calc_midpoint_on_side(c0, c1, orientation):
  """
  Calculate the midpoint between two corners on the side of a the square

  c0 will be the top or left point
  c1 will be the bottom or right point
  orientation will either be 'vertical' or 'horizontal' to determine
    which coordinate to change
  """
  if orientation == 'vertical':
    return (((c1[0] - c0[0]) // 2) + c0[0], c0[1])

  return (c0[0], ((c1[1] - c0[1]) // 2) + c0[1])


def diamond_step(grid, t_l, t_r, b_l, b_r, noisiness):
  """
  Perform the diamond-step on grid given the coordinates of the corners.

  The corners are arranged by:
  t_l, t_r
  b_l, b_r
  """
  midpoint = calc_midpoint(t_l, b_r)
  midpoint_value = np.average(list(grid[x, y] for (x, y) in (t_l, t_r, b_l, b_r)))

  grid[midpoint[0], midpoint[1]] = midpoint_value + generate_noise(noisiness)
  return grid


def square_step(grid, t_l, t_r, b_l, b_r, noisiness):
  """
  Perform the square-step on grid given the coordinates of the corners.

  The corners are arranged by:
  t_l, t_r
  b_l, b_r
  """
  middle_point = calc_midpoint(t_l, b_r)

  sides = [
    { 'c0': t_l, 'c1': t_r, 'orientation': 'horizontal' },
    { 'c0': t_l, 'c1': b_l, 'orientation': 'vertical' },
    { 'c0': b_l, 'c1': b_r, 'orientation': 'horizontal' },
    { 'c0': t_r, 'c1': b_r, 'orientation': 'vertical' },
  ]

  for side in sides:
    (c0, c1, orientation) = side.values()
    top_midpoint = calc_midpoint_on_side(c0, c1, orientation)
    top_midpoint_value = np.average(list(grid[x, y] for (x, y) in (c0, c1, middle_point)))
    grid[top_midpoint[0], top_midpoint[1]] = top_midpoint_value + generate_noise(noisiness)

  return grid


def generate(size, noisiness = 0):
  """
  The runner for generating a random terrain
  """
  side_length = (2 ** size) + 1
  grid = create_grid(side_length)
  grid = set_corners(grid)

  t_l = (0, 0),
  b_r = (side_length - 1, side_length - 1)
  step_lengths = generate_step_lengths(size)

  for step_length in step_lengths:
    squares = generate_internal_squares(t_l, b_r, step_length)
    
    for sq in squares:
      grid = diamond_step(grid, sq['t_l'], sq['t_r'], sq['b_l'], sq['b_r'], noisiness)
      grid = square_step(grid, sq['t_l'], sq['t_r'], sq['b_l'], sq['b_r'], noisiness)

  return grid


if __name__ == '__main__':
  result = generate(2)

  print(result)
