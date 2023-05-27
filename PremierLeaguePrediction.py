import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
import tkinter as tk
from tkinter import ttk

# Load the dataset
data = pd.read_csv('final_dataset.csv')

# Preprocess the data
le = preprocessing.LabelEncoder()
data['FTR'] = le.fit_transform(data['FTR'])

# Function to handle the match prediction
def predict_match():
    home_team = home_team_combobox.get()
    away_team = away_team_combobox.get()

    # Prepare the input features for prediction
    home_stats = filtered_data.loc[filtered_data['HomeTeam'] == home_team].tail(1)[['HTGS', 'HTGC', 'HTP']].values
    away_stats = filtered_data.loc[filtered_data['AwayTeam'] == away_team].tail(1)[['ATGS', 'ATGC', 'ATP']].values
    input_features = np.concatenate((home_stats, away_stats), axis=1)

    # Predict the match outcome using the decision tree model
    predicted_result = le.inverse_transform(decision_tree.predict(input_features))[0]

    # Display the predicted result in the GUI
    winning_team = home_team if predicted_result == 'H' else away_team
    result_label.config(text="Predicted Winner: " + winning_team)

# Function to train the model
def train_model():
    start_year = int(start_year_var.get())
    end_year = int(end_year_var.get())

    # Filter the dataset based on the specified range of years
    global filtered_data
    filtered_data = data.loc[(data['Date'].str[-2:] >= str(start_year)[-2:]) & (data['Date'].str[-2:] <= str(end_year)[-2:])]

    # Get the list of teams
    teams = sorted(set(filtered_data['HomeTeam']) | set(filtered_data['AwayTeam']))

    # Update the team dropdown menus
    home_team_combobox['values'] = teams
    away_team_combobox['values'] = teams

    # Train a decision tree model for all matches
    X = filtered_data[['HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP']].values
    y = filtered_data['FTR'].values

    global decision_tree
    decision_tree = DecisionTreeClassifier(random_state=42)
    decision_tree.fit(X, y)

    # Display a message indicating that a new model is generated
    result_label.config(text="New model generated.")

# Create the GUI window
window = tk.Tk()
window.title("Match Prediction")
window.geometry("400x300")

# Specify the range of years for training the model
start_year_var = tk.StringVar()
end_year_var = tk.StringVar()

# Create the range of years input
start_year_label = ttk.Label(window, text="Start Year:")
start_year_label.pack()
start_year_entry = ttk.Entry(window, textvariable=start_year_var)
start_year_entry.pack()

end_year_label = ttk.Label(window, text="End Year:")
end_year_label.pack()
end_year_entry = ttk.Entry(window, textvariable=end_year_var)
end_year_entry.pack()

train_button = ttk.Button(window, text="Train Model", command=train_model)
train_button.pack()

# Create the team selection dropdown menus
home_team_label = ttk.Label(window, text="Home Team:")
home_team_label.pack()
home_team_combobox = ttk.Combobox(window, state="readonly")
home_team_combobox.pack()

away_team_label = ttk.Label(window, text="Away Team:")
away_team_label.pack()
away_team_combobox = ttk.Combobox(window, state="readonly")
away_team_combobox.pack()

# Create the predict button
predict_button = ttk.Button(window, text="Predict", command=predict_match)
predict_button.pack()

# Create the result label
result_label = ttk.Label(window, text="Predicted Winner: ")
result_label.pack()

window.mainloop()
