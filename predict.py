import warnings
import pandas as pd
import mysql.connector
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


warnings.filterwarnings("ignore", category=UserWarning)
# Connect to the MySQL database
connection = mysql.connector.connect(
    host='localhost', user='root', password='anm33918',database='jadiProject')

# Load data from MySQL database
df = pd.read_sql("SELECT * FROM houses", connection)

# Define preprocessing steps for categorical and numerical features
cat_preprocessing = OneHotEncoder()
num_preprocessing = 'passthrough'
preprocessor = ColumnTransformer(transformers=[
    ('cat', cat_preprocessing, ['neighbourhood']),
    ('num', num_preprocessing, ['roomsCount', 'area', 'builtYear']),
])

# Define the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42)),
])

# Train the model on the entire data
model.fit(df.drop(columns=['price']), df['price'])

# Use the model to predict the price of a new house
new_house = pd.DataFrame({
    'roomsCount': [input('Enter number of rooms: ')],
    'area': [input('Enter area: ')],
    'neighbourhood': [input('Enter neighbourhood: ')],
    'builtYear': [input('Enter built year: ')],
})

price = model.predict(new_house)
predicted_price = round(price[0])
print(f'Predicted price: {predicted_price:,.0f}  تومان')
