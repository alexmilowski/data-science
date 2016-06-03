import iris_tree as iris
from sklearn.ensemble import AdaBoostClassifier

boosting = AdaBoostClassifier(n_estimators=10, learning_rate=1.0,random_state=1)

iris.tree(boosting)

