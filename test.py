from open_groceries import *

groc = OpenGrocery()
groc.set_nearest_stores("Rochester Institute of Technology")
print(groc.suggest("pot"))