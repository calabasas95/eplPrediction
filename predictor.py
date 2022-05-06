#%%
#importing dependencies 
from numpy.random.mtrand import multinomial
import pandas as pd 
from sklearn.linear_model import LogisticRegression

#%%
#reading the data 
#all this data is taken from https://www.youtube.com/watch?v=6tQhoUuQrOw
#csv was generated from football_result_data_cleaned.py
#also credit to https://github.com/llSourcell/Predicting_Winning_Teams/blob/master/Prediction.ipynb
#and https://github.com/RudrakshTuwani/Football-Data-Analysis-and-Prediction
data = pd.read_csv('final_dataset2.csv')
# print(data.head())

#%%
#preparing the data 
# Separate into feature set and target variable
#X_all = data.drop(['FTR'],1), instead of using this, I created the set below as I noticed that the final_dataset had a lot more columns then what his print out came from 
X_all = data[['HTP', 'ATP', 'HM1', 'HM2', 'HM3', 'AM1', 'AM2', 'AM3', 'HTGD', 'ATGD', 'DiffFormPts', 'DiffLP']].copy()
y_all = data['FTR']

# Standardising the data.
from sklearn.preprocessing import scale

#Center to the mean and component wise scale to unit variance.
cols = [['HTGD','ATGD','HTP','ATP','DiffLP']]
for col in cols:
    X_all[col] = scale(X_all[col])
#%%
#last 3 wins for both sides
X_all.HM1 = X_all.HM1.astype('str')
X_all.HM2 = X_all.HM2.astype('str')
X_all.HM3 = X_all.HM3.astype('str')
X_all.AM1 = X_all.AM1.astype('str')
X_all.AM2 = X_all.AM2.astype('str')
X_all.AM3 = X_all.AM3.astype('str')

#we want continous vars that are integers for our input data, so lets remove any categorical vars
def preprocess_features(X):
    ''' Preprocesses the football data and converts catagorical variables into dummy variables. '''
    
    # Initialize new output DataFrame
    output = pd.DataFrame(index = X.index)
    
    # Investigate each feature column for the data
    for col, col_data in X.iteritems():

        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix = col)
                    
        # Collect the revised columns
        output = output.join(col_data)
    
    return output

X_all = preprocess_features(X_all)
# print("Processed feature columns ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns)))
#this gives me about 30 features instead of 24

#I might need to drop same of the features added by the functions above. 
X_all = X_all.drop(['HM1_M', 'HM2_M', 'HM3_M', 'AM1_M', 'AM2_M', 'AM3_M'], axis = 1)
# print("Processed feature columns now has ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns)))

#%%
from sklearn.model_selection import train_test_split

# Shuffle and split the dataset into training and testing set.
# X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,stratify = y_all)
X_train = X_all[:5700]
X_test = X_all[5700:]
y_train = y_all[:5700]
y_test = y_all[5700:]

#%%
#for measuring training time
from time import time 
# F1 score (also F-score or F-measure) is a measure of a test's accuracy. 
#It considers both the precision p and the recall r of the test to compute 
#the score: p is the number of correct positive results divided by the number of 
#all positive results, and r is the number of correct positive results divided by 
#the number of positive results that should have been returned. The F1 score can be 
#interpreted as a weighted average of the precision and recall, where an F1 score 
#reaches its best value at 1 and worst at 0.

# Initialize the three models (XGBoost is initialized later)
clf = LogisticRegression(random_state=14)
print("Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train)))
    
# Train the classifier
start = time()
clf.fit(X_train, y_train)
end = time()

print("Trained model in {:.4f} seconds".format(end - start))

# Print the results of prediction for both training and testing
start = time()
y_pred = clf.predict(X_train)

end = time()
print("Made predictions in {:.4f} seconds.".format(end - start))
print(y_pred[-10:])
print(y_train[-10:])
print(clf.predict_proba(X_train[-10:]))
from sklearn import metrics
print(metrics.accuracy_score(y_train,y_pred))


# print("F1 score and accuracy score for training set:", f1 , acc)
start = time()
y_pred = clf.predict(X_test)

end = time()
print("Made predictions in {:.4f} seconds.".format(end - start))
print(y_pred[:10])
print(y_test[:10])
print(clf.predict_proba(X_test[:10]))
print(metrics.accuracy_score(y_test,y_pred))
# print(X_test[:10])
print('')
print(clf.intercept_)
print('')
print(clf.coef_)
# %%
