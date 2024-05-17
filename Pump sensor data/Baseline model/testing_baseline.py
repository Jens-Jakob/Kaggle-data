import pandas as pd
from sklearn.metrics import f1_score, ConfusionMatrixDisplay, confusion_matrix
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def apply_thresholds(data, thresholds):
    predictions = None  # Initialize predictions
    
    for feature, threshold in thresholds.items():
        predictions = ((data[feature] <= threshold)).astype(int)

        # Apply threshold for the current feature
        current_predictions = (data[feature] <= threshold).astype(int)
        
        # Combine predictions using logical AND
        if predictions is None:
            predictions = current_predictions
        else:
            predictions &= current_predictions

    return predictions

def evaluate_model(data, thresholds):
    # Generate predictions based on the dual thresholds
    predictions = apply_thresholds(data, thresholds)
    
    # Calculate and return the F1 score
    f1 = f1_score(data['machine_status'], predictions)

    cm = confusion_matrix(data['machine_status'], predictions)
    # Calculate percentages
    total = cm.sum()
    cm_percentages = cm / total * 100
    cm_percentages = np.round(cm_percentages, 2)

    # Display the confusion matrix as percentages of total with % symbol
    plt.figure(figsize=(7, 7))
    ax = sns.heatmap(cm_percentages, annot=True, fmt='.2f', cmap='Greens', cbar=False, 
                     annot_kws={"size": 12}, linewidths=.5, linecolor='black')
    for t in ax.texts: 
        t.set_text(t.get_text() + " %")

    plt.title(f'Baseline model (Pump sensor) - Confusion Matrix (Percentages)')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

    return f1

def main():
    # Load the training data
    path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    test_data = pd.read_csv(path)
   
    thresholds = {
        'Feature_1': 44.96173497439016,
        'Feature_2': 74.43398326530611,
        'Feature_3': 8.016534489795918,
        'Feature_4': 301.2525530816326,
        'Feature_5': 561.0782371428571,
        'Feature_6': 842.896331632653,
        'Feature_7': 395.2719642857143,
        'Feature_8': 40.85901918367347
    }

    
    # Evaluate the model on the test set
    test_f1_score = evaluate_model(test_data, thresholds)
    print(f"F1 Score on Test Set: {test_f1_score}")

if __name__ == "__main__":
    main()
