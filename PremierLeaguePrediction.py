import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv('final_dataset.csv')

# Preprocess the data
le = preprocessing.LabelEncoder()
data['FTR'] = le.fit_transform(data['FTR'])

# Specify the range of years for training the model
start_year = int(input("Enter the start year: "))
end_year = int(input("Enter the end year: "))

# Filter the dataset based on the specified range of years
filtered_data = data.loc[(data['Date'].str[-2:] >= str(start_year)[-2:]) & (data['Date'].str[-2:] <= str(end_year)[-2:])]

# Split the data into features and target variable
X = filtered_data[['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP']].values
y = filtered_data['FTR'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the decision tree model
decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)

# GUI for Match Prediction
while True:
    print("Enter the Home Team:")
    home_team = input()

    print("Enter the Away Team:")
    away_team = input()

    # Prepare the input features for prediction
    home_stats = filtered_data.loc[filtered_data['HomeTeam'] == home_team].tail(1)[['HTGS', 'HTGC', 'HTP']].values
    away_stats = filtered_data.loc[filtered_data['AwayTeam'] == away_team].tail(1)[['ATGS', 'ATGC', 'ATP']].values
    input_features = np.concatenate((home_stats, away_stats), axis=1)

    # Predict the match outcome
    predicted_result = le.inverse_transform(decision_tree.predict(input_features))[0]

    print("Predicted Result: " + predicted_result)
    print("------------------------")
