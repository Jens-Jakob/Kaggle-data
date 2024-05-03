import pandas as pd
from sklearn.metrics import f1_score, ConfusionMatrixDisplay, confusion_matrix
import os
import matplotlib.pyplot as plt

def apply_thresholds(data, threshold_row_index, threshold_median):
    # Apply both thresholds; predictions are danger if both conditions are true
    predictions = ((data['index_useinstance'] > threshold_row_index) & 
                   (data['Values.WiFiSignalStrengthN_median'] <= threshold_median)).astype(int)
    return predictions

def evaluate_model(data, threshold_row_index, threshold_median):
    # Generate predictions based on the dual thresholds
    predictions = apply_thresholds(data, threshold_row_index, threshold_median)
    
    # Calculate and return the F1 score
    f1 = f1_score(data['danger_zone'], predictions)

    cm = confusion_matrix(data['danger_zone'], predictions)
    display = ConfusionMatrixDisplay(confusion_matrix=cm)

    display.plot(cmap=plt.cm.Greens)

    plt.show()
    return f1

def main():
    # Load the training data
    path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    test_data = pd.read_csv(path)
   
    # Define thresholds as determined from the training set
    best_row_index_threshold = 207.6734693877551 #insert threshold value
    best_median_threshold = -65.3061224489796 #insert threshold value
    
    # Evaluate the model on the test set
    test_f1_score = evaluate_model(test_data, best_row_index_threshold, best_median_threshold)
    print(f"F1 Score on Test Set: {test_f1_score}")

if __name__ == "__main__":
    main()
