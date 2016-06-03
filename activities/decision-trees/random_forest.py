import iris_tree as iris
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(criterion='gini',n_estimators=10,max_depth=3,random_state=1,n_jobs=2)

iris.tree(forest)

