import iris_tree as iris
from sklearn.ensemble import GradientBoostingClassifier

boosting = GradientBoostingClassifier(n_estimators=10, learning_rate=1.0,max_depth=3,random_state=1)

iris.tree(boosting)

