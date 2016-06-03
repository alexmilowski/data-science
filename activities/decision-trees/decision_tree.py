import iris_tree as iris
from sklearn.tree import DecisionTreeClassifier


dtree = DecisionTreeClassifier(criterion='gini',max_depth=3,random_state=0)

iris.tree(dtree)

