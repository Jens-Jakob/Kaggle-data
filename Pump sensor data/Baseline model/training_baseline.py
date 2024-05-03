import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
import os

def evaluate_threshold(data, feature, threshold):
    # Check if the feature is 'RowIndex', and set the classification rule accordingly
    if feature == 'RowIndex':
        # Values over the threshold indicate danger for RowIndex
        predictions = (data[feature] > threshold).astype(int)
    else:
        # For WiFiSignalStrength and other features, values under or equal to the threshold indicate danger
        predictions = (data[feature] <= threshold).astype(int)
    
    # Calculate the F1 score comparing predictions to the actual danger_zone values
    f1 = f1_score(data['danger_zone'], predictions)
    return f1

def grid_search(data, feature, thresholds):
    best_threshold = None
    best_f1 = 0

    # Iterate over all given thresholds
    for threshold in thresholds:
        f1 = evaluate_threshold(data, feature, threshold)
        print(f"Threshold: {threshold}, F1 Score: {f1}")

        # Update the best threshold found so far
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    return best_threshold, best_f1

def main():
    # Load the training data
    path = os.path.join(os.path.dirname(__file__), 'train_data.csv')
    train_data = pd.read_csv(path)
    
    # Define the range of thresholds to test
    mean_thresholds = np.linspace(-100, 0, num=50)
    median_thresholds = np.linspace(-100, 0, num=50)
    row_index_thresholds = np.linspace(train_data['index_useinstance'].min(), train_data['index_useinstance'].max(), num=50)

    # Run grid search for median
    best_median_threshold, best_median_f1 = grid_search(train_data, 'Values.WiFiSignalStrengthN_median', median_thresholds)
    

    # Run grid search for RowIndex
    best_row_index_threshold, best_row_index_f1 = grid_search(train_data, 'index_useinstance', row_index_thresholds)
    
    print(f"Best Threshold for RowIndex: {best_row_index_threshold} with F1 Score: {best_row_index_f1}")
    print(f"Best Threshold for median: {best_median_threshold} with F1 Score: {best_median_f1}")
if __name__ == "__main__":
    main()
