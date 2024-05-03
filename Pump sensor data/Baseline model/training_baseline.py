import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
import os

def evaluate_threshold(data, feature, threshold):
    
    predictions = (data[feature] <= threshold).astype(int)
    
    # Calculate the F1 score comparing predictions to the actual danger_zone values
    f1 = f1_score(data['machine_status'], predictions)
    return f1

def grid_search(data, feature, thresholds):
    best_threshold = None
    best_f1 = 0

    # Iterate over all given thresholds
    for threshold in thresholds:
        f1 = evaluate_threshold(data, feature, threshold)
        # print(f"Threshold: {threshold}, F1 Score: {f1}")

        # Update the best threshold found so far
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    return best_threshold, best_f1

def main():
    # Load the training data
    path = os.path.join(os.path.dirname(__file__), 'train_data.csv')
    train_data = pd.read_csv(path)
    
    for feature in train_data.columns:
        threshold_range = np.linspace(train_data[feature].min(), train_data[feature].max(), num=50)
        best_threshold, best_f1 = grid_search(train_data, feature, threshold_range)
        print(f"Best Threshold for {feature}: {best_threshold} with F1 Score: {best_f1}")


if __name__ == "__main__":
    main()
