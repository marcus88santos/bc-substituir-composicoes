y = [1, 2, 3, 4, 5]
z = [3, 4]
x = 0
while x < len(y):
  print(x, y[x])
  for i in z:
    if y[x] == i:
      y.pop(x)
      x = -1
      break
  x += 1
  # input()