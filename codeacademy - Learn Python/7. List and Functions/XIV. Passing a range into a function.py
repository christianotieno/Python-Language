def my_function(x):
  for i in range(0, len(x)):
    x[i] = x[i]
  return x

print (my_function(range(3))) # Adding your range between the parentheses!
