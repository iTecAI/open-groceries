from open_groceries import *

groc = OpenGrocery(features=["wegmans"])
groc.set_nearest_stores("Rochester Institute of Technology")
print(groc.search("fear", ignore_errors=True))
