import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
 


#Load data
data = pd.read_csv('./cars-data3.csv', index_col=None)
test = pd.read_csv('./test-data.csv',  index_col=None)


# Remove Id column
data = data.drop(['id'],axis='columns')
data.price.hist()
# Dropping some columns
data = data.drop(['color'],axis='columns')
data = data.drop(['kms'],axis='columns')
data = data.drop(['euro'],axis='columns')

test = test.drop(['color'],axis='columns')
test = test.drop(['kms'],axis='columns')
test = test.drop(['euro'],axis='columns')

# Remove brands that are seen less than 200 times
data = data.groupby('brand').filter(lambda x :len(x)>200)

#Format BMW model
def format_bmw_model(model_name):
  if 'X' in model_name or 'i' in model_name:
    return model_name
  return model_name[0]

# Trim model to just 1 letter except if it is X or i ex.(318 to 3)
data.loc[data['brand'] == 'BMW', ['model']] = data[data.brand == 'BMW'].model.apply(lambda x: format_bmw_model(x))

# Remove models that are met less than 9 times
data = data.groupby('model').filter(lambda x :len(x)>9)

# Impute missing kms with the median
#data.kms.fillna(data.kms.median(), inplace = True)

# Impute missing categorical variables with the the most common value
data = data.fillna(data.mode().iloc[0])

#data.kms = np.log(data.kms)
#test.kms = np.log(test.kms)

print("Old Shape before trimming: ", data.shape)
data = data[(data.hp >30) & (data.hp < 480)]
data = data[(data.price >100) & (data.price < 60000)]
data = data[(data.displacement >100) & (data.displacement < 8000)]



print("New Shape after trimming: ", data.shape)

# Log the price variable so it is normally distributed
# data.price = np.log(data.price)

# Put a flag on premium brands
premium_brands = ["Porsche", "Audi","Mercedes-Benz","BMW"]

data['premium'] = np.where(data['brand'].isin(premium_brands), 1, 0)
test['premium'] = np.where(test['brand'].isin(premium_brands), 1, 0)

# Concatenate brand and model columns and remove model col
data["brand"] = data['brand'].astype(str) +"-"+ data["model"]
test["brand"] = test['brand'].astype(str) +"-"+ test["model"]

data = data.drop(['model'],axis='columns')
test = test.drop(['model'],axis='columns')

# Flag for new cars
data['new'] = np.where(data['year']>2018, 1, 0)
test['new'] = np.where(test['year']>2018, 1, 0)

# Define columns to be ordinal and one hot encoded
ordinal_enc_cols = ['brand','type']
one_hot_columns = ['fuel']

# Fit ordinal encoder
ordinal_encoder = OrdinalEncoder()
data[ordinal_enc_cols] = ordinal_encoder.fit_transform(data[ordinal_enc_cols])
test[ordinal_enc_cols] = ordinal_encoder.transform(test[ordinal_enc_cols])

# Apply one-hot encoder to fuel column
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
oh_columns_data = pd.DataFrame(OH_encoder.fit_transform(data[one_hot_columns]))
oh_columns_test = pd.DataFrame(OH_encoder.transform(test[one_hot_columns])) 

# One-hot encoding removed index; put it back
oh_columns_data.index = data.index
oh_columns_test.index = test.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_data = data.drop(one_hot_columns, axis=1)
num_X_test = test.drop(one_hot_columns, axis=1)

# Add one-hot encoded columns to numerical features
data = pd.concat([num_X_data, oh_columns_data], axis=1)
test = pd.concat([num_X_test, oh_columns_test], axis=1)

# Train set without price variable
X = data.drop(['price'],axis='columns')

# Train set price variable
y = data.price

X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.25, random_state=42)

# Define model
model = XGBRegressor(random_state=1,objective='reg:squarederror',
                         learning_rate = 0.1,
                         max_depth = 6,
                         colsample_bytree = 0.5,
                         n_estimators =300)

# Fit model
model.fit(X_train, y_train)

print("Model score: ",model.score(X_train,y_train))

# Calculate error 
mae_train = -1 * cross_val_score(model, X_train, y_train,
                                  cv=3,
                                  scoring='neg_mean_absolute_error')


mae_test = -1 * cross_val_score(model, X_test, y_test,
                                  cv=3,
                                  scoring='neg_mean_absolute_error')

# Supress scientific notation
pd.options.display.float_format = '{:.10f}'.format

print("Mean absolute error CV train: ", mae_train.mean())

print("Mean absolute error CV test: ", mae_test.mean())


#Predict 
preds =  model.predict(test)

# Calculate the exponential of the y variable
# preds = np.exp(preds)

print("Predictions: \n", preds)

