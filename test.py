from open_groceries import *

groc = OpenGrocery()
groc.set_nearest_stores("Rochester Institute of Technology")
#print(groc.search("beans", include=["costco"]))
print([i.categories for i in groc.search("beans")])