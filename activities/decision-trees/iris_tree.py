import regions
import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split,cross_val_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt


def tree(alg):
   
   iris = datasets.load_iris()
   X = iris.data[:,[2,3]]
   y = iris.target

   # Create a training set with a 30% sample and initial random_state so we get similar results
   X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)

   # fit our algorithm to the training data
   alg.fit(X_train,y_train)

   # print out the cross validation score
   scores = cross_val_score(alg,X,y)
   print('accuracy {:0.2f} (± {:0.2f})'.format(scores.mean(),scores.std()))

   # recombine our data
   X_combined = np.vstack((X_train,X_test))
   y_combined = np.hstack((y_train,y_test))

   # plot the regions and data
   regions.plot(X_combined,y_combined,classifier=alg,test_idx=range(105,150))

   # label our plot
   plt.xlabel('petal length [cm]')
   plt.ylabel('petal width [cm]') 
   plt.legend(loc='upper left')
   plt.show()

