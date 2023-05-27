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

# Get the list of teams
teams = sorted(set(filtered_data['HomeTeam']) | set(filtered_data['AwayTeam']))

# Train a decision tree model for all matches
X = filtered_data[['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP']].values
y = filtered_data['FTR'].values

decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X, y)

# GUI for Match Prediction
while True:
    print("Enter the Home Team:")
    home_team = input()
    if home_team not in teams:
        print("Invalid home team. Please select from the available teams.")
        continue

    print("Enter the Away Team:")
    away_team = input()
    if away_team not in teams:
        print("Invalid away team. Please select from the available teams.")
        continue

    # Prepare the input features for prediction
    home_stats = filtered_data.loc[filtered_data['HomeTeam'] == home_team].tail(1)[['HTGS', 'HTGC', 'HTP']].values
    away_stats = filtered_data.loc[filtered_data['AwayTeam'] == away_team].tail(1)[['ATGS', 'ATGC', 'ATP']].values
    input_features = np.concatenate((home_stats, away_stats), axis=1)

    # Predict the match outcome using the decision tree model
    predicted_result = le.inverse_transform(decision_tree.predict(input_features))[0]

    # Print the predicted result
    print("Predicted Result: " + predicted_result)
    print("Key Numbers:")
    print("Home Team: " + home_team)
    print("Away Team: " + away_team)
    print("Home Team Goals Scored: " + str(home_stats[0][0]))
    print("Away Team Goals Scored: " + str(away_stats[0][0]))
    print("Home Team Goals Conceded: " + str(home_stats[0][1]))
    print("Away Team Goals Conceded: " + str(away_stats[0][1]))
    print("Home Team Points: " + str(home_stats[0][2]))
    print("Away Team Points: " + str(away_stats[0][2]))
    print("------------------------")
