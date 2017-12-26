#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from collections import Counter
import matplotlib.pyplot
from tester import *


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

## features_list without new features
# features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
#                  'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
#                  'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock',
#                  'director_fees','to_messages', 'from_poi_to_this_person', 'from_messages',
#                  'from_this_person_to_poi', 'shared_receipt_with_poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
print len(data_dict)
print 'features_count: ',len(data_dict['METTS MARK'])
poi_count = 0
non_poi_count = 0
nan_list = []
for key,value in data_dict.iteritems():
    for k,v in value.iteritems():
        if v == 'NaN':
            nan_list.append(k)
            data_dict[key][k] = 0

    if value['poi'] == True:
        print key
        poi_count = poi_count + 1
    else:
        non_poi_count = non_poi_count + 1

print 'poi count: ',poi_count
print 'non_poi_count: ',non_poi_count
print 'feature_nan_list: ',Counter(nan_list)

features = ["total_payments", "total_stock_value"]
data_dict.pop('TOTAL')
print 'Features count without outlier:',len(data_dict)

data = featureFormat(data_dict, features)
for point in data:
    total_payments= point[0]
    total_stock_value = point[1]
    # print point, '::',total_payments,':',total_stock_value
    matplotlib.pyplot.scatter( total_payments, total_stock_value )

matplotlib.pyplot.xlabel("total_payments")
matplotlib.pyplot.ylabel("total_stock_value")
matplotlib.pyplot.show()

for key,value in data_dict.iteritems():
     if value['total_payments'] > 100000000 and value['total_payments'] != 'NaN':
         print key

### Task 3: Create new feature(s)
def computeFraction( poi_messages, all_messages ):
    if poi_messages == 0 or all_messages == 0:
        fraction = 0
    else:
        fraction = float(poi_messages) / float(all_messages)

    return fraction

for name in data_dict:

    data_point = data_dict[name]
    from_poi_to_this_person = data_point["from_poi_to_this_person"]
    to_messages = data_point["to_messages"]
    fraction_from_poi = computeFraction( from_poi_to_this_person, to_messages )
    data_point["fraction_from_poi"] = fraction_from_poi
    from_this_person_to_poi = data_point["from_this_person_to_poi"]
    from_messages = data_point["from_messages"]
    fraction_to_poi = computeFraction( from_this_person_to_poi, from_messages )
    data_point["fraction_to_poi"] = fraction_to_poi


## features_list with new features
features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
                 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
                 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock',
                 'director_fees','to_messages', 'from_poi_to_this_person', 'from_messages',
                 'from_this_person_to_poi', 'shared_receipt_with_poi','fraction_from_poi','fraction_to_poi']



### Store to my_dataset for easy export below.
## for bayes and tree
# my_dataset = data_dict

## for SVM
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import pandas as pd
import numpy as np
df = pd.DataFrame.from_dict(data_dict,orient='index')
scaler = MinMaxScaler()
for feature in features_list:
    if feature != 'email_address'and feature != 'poi':
        df[feature] = scaler.fit_transform(df[feature])

my_dataset = df.to_dict(orient='index')

# for key,value in my_dataset.iteritems():
#     print value
# scaled_df = df.copy()
# scaled_df.ix[:,1:] = preprocessing.scale(scaled_df.ix[:,1:])
# my_dataset = scaled_df.to_dict(orient='index')
# df = scaler.fit_transform(df)

# features_list_1 = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus',
#                  'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses',
#                  'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock',
#                  'director_fees','to_messages', 'from_poi_to_this_person', 'from_messages',
#                  'from_this_person_to_poi', 'shared_receipt_with_poi'] # You will need to use more features
# for key,value in data_dict.iteritems():
#     for k, v in value.iteritems():
#         if k == 'salary':
#             data_dict[key][k] = scaler.fit_transform(v)

# my_dataset = data_dict


### Extract features and labels from dataset for local testing
# data = featureFormat(my_dataset, features_list2, sort_keys = True)
# data = featureFormat(my_dataset, features_list, sort_keys = True)

# labels, features = targetFeatureSplit(data)
#



from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2

# selector = SelectKBest(k=9).fit(features,labels)
# selector = SelectKBest(k=9).fit(rescale_features,labels)

# print selector.scores_
# print selector.pvalues_

# new_features = []
# for bool, feature in zip(selector.get_support(), features_list_add_new_features):
# for bool, feature in zip(selector.get_support(), features_list):
#     if bool:
#         new_features.append(feature)
# print new_features

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)

# from sklearn.model_selection import train_test_split
# features_train, features_test, labels_train, labels_test = train_test_split(features, labels,test_size=0.3,
#                                                                             random_state=42)


from sklearn.model_selection import GridSearchCV
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
# features_train = features_train[:len(features_train)/10]
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
n_features = np.arange(1, len(features_list))

# PineLine for bayes
# pipe = Pipeline([
#     ('select_features', SelectKBest()),
#     ('classify', GaussianNB())
# ])

# PineLine for SVM
pipe = Pipeline([
    ('select_features', SelectKBest()),
    ('classify', SVC())
])

#PineLine for tree
# pipe = Pipeline([
#     ('select_features', SelectKBest()),
#     ('classify',DecisionTreeClassifier())
# ])

param_grid = [
    {
        'select_features__k': n_features
    }
]

clf= GridSearchCV(pipe, param_grid=param_grid, scoring='f1', cv = 10)
clf.fit(features, labels)
print clf.best_estimator_
print clf.best_params_
# #
selector = SelectKBest(k=12).fit(features,labels)
#
# print selector.scores_
# print selector.pvalues_
#
def get_new_features(selector,features_list):
    new_features = []
    for bool, feature in zip(selector.get_support(), features_list):
        if bool:
            new_features.append(feature)
    return new_features
#
new_features = get_new_features(selector,features_list)
print 'new_features :',new_features

# parameters_tree = {'min_samples_split': [2,10,20,30,40],'max_depth': range(1,5),'min_samples_leaf': range(1,5),
#                   'criterion':['gini','entropy'],'max_features':[None,'sqrt','auto','log2']}
parameters_tree = {'min_samples_split': [2,10,20,30],'max_depth': range(1,5)}

# clf = GridSearchCV(DecisionTreeClassifier(),parameters_tree)

clf = DecisionTreeClassifier()
clf.fit(features,labels)
# print clf.best_params_
feature_importances = clf.feature_importances_

#Display the feature names and importance values
#
tree_important_features = []
tree_important_features_list = []
for feature in zip(sorted(feature_importances,reverse=True), features_list):
    if feature[0] > 0.1:
        tree_important_features.append(feature)
        tree_important_features_list.append(feature[1])
print 'tree_important_features :',tree_important_features
print 'tree_important_features_list :',tree_important_features_list
# new_features = tree_important_features_list

# data = featureFormat(my_dataset, new_features)
# labels, features = targetFeatureSplit(data)

# Find best parameters for tree
cv = StratifiedShuffleSplit(labels,1000,random_state=18)
clf_tree = GridSearchCV(DecisionTreeClassifier(),parameters_tree,cv=cv,scoring='f1')
clf_tree.fit(features,labels)
print clf_tree.best_params_
print clf_tree.best_estimator_



# data_for_svm = featureFormat(rescaled_dataset,features_list)
# svm_lables, svm_features = targetFeatureSplit(data_for_svm)
# selector_for_svm = SelectKBest(k=3).fit(svm_features,svm_lables)
# new_features_svm = get_new_features(selector_for_svm,features_list)
# print 'new_features_svm :',new_features_svm

# features_train, features_test, labels_train, labels_test = train_test_split(features, labels,test_size=0.3,
#                                                                             random_state=42)
# labels_train = labels_train[:len(labels_train)/10]

# parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
# svc = svm.SVC()
# clf = GridSearchCV(svc, parameters)
# param_grid = {'C': [1,10,100],
#               'gamma': [0.1,1,10,100], }
# clf = GridSearchCV(SVC(kernel='rbf'), param_grid)
# clf.fit(features_train, labels_train)

from sklearn.preprocessing import scale

#Train with Bayes









# TREE
# pred_svm = clf_svm.predict(features_test)
# print 'SVM Acc by GridSearchCV : ',accuracy_score(labels_test,pred_svm)
# recall = recall_score(labels_test, pred_svm )
# precision = precision_score(labels_test, pred_svm )
# print 'Recall,Precision :',recall,precision



# data = featureFormat(my_dataset, tree_important_features_list)
# print 'tree_important_features_list :',tree_important_features_list
# labels, features = targetFeatureSplit(data)
# features_train, features_test, labels_train, labels_test = train_test_split(features, labels,test_size=0.3,
#
#                                                                       random_state=42)






# import numpy as np
# from sklearn.model_selection import StratifiedShuffleSplit
# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
# param_grid = dict(gamma=gamma_range, C=C_range)
# cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
# grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
# grid.fit(features_train, labels_train)


# print("The best parameters are %s with a score of %0.2f"
#       % (grid.best_params_, grid.best_score_))



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

#
# clf = GaussianNB()
clf = DecisionTreeClassifier(min_samples_split= 2 , max_depth=4)
# test = ['fraction_from_poi','fraction_to_poi']
# new_features_test = ['poi', 'salary', 'deferral_payments', 'total_payments', 'loan_advances','fraction_from_poi','fraction_to_poi']

dump_classifier_and_data(clf,my_dataset,new_features)
print main()
print new_features


# print 'new_features: ',new_features
# clf_svm = SVC(kernel='rbf',C=10,gamma=1)
# dump_classifier_and_data(clf_svm, rescaled_dataset, new_features)
# print main()


# dump_classifier_and_data(clf_tree,data_dict,new_features)
# print main()
# print clf_tree.best_estimator_
# print clf_tree.best_params_



