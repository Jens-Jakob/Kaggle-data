import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def visualise_single_feature(feature, df):
    """
    Function that visualizes a scatterplot of specified feature
    """
    # Extract the values of the chosen feature
    feature_values = df[feature]
    
    # Extract the danger zone values
    target = df['y']

    # Create a list to store colors based on danger zone values
    colors = ['red' if dz == 1 else 'blue' for dz in target]


    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df.index, feature_values, c=colors)
    plt.xlabel("Row Number")
    plt.ylabel(f"{feature}")
    plt.title(f"Plot of {feature}")
    plt.grid(True)
    plt.show()

def calculate_statistical_features(df_usecase, features):
    # Initialize an empty list to store statistical features for each use case
    use_case_features = []

    # Calculate statistical features for the use case
    statistical_features = {}


    # Extract statistical features for non-binary features
    for feature in features:
        # Calculate the change from the first value to the last value
        first_value = df_usecase[feature].iloc[0]  # Get the first value
        last_value = df_usecase[feature].iloc[-1]  # Get the last value
        change_from_first_to_last = last_value - first_value

        # Calculate the absolute difference between min and max values
        absolute_diff = abs(df_usecase[feature].max() - df_usecase[feature].min())

        statistical_features[f'{feature}_median'] = df_usecase[feature].median()
        statistical_features[f'{feature}_mean'] = df_usecase[feature].mean()
        statistical_features[f'{feature}_skewness'] = df_usecase[feature].skew()
        statistical_features[f'{feature}_minimum'] = df_usecase[feature].min()
        statistical_features[f'{feature}_maximum'] = df_usecase[feature].max()
        statistical_features[f'{feature}_standard_deviation'] = df_usecase[feature].std()
        statistical_features[f'{feature}_variance'] = df_usecase[feature].var()
        statistical_features[f'{feature}_mean_abs_change'] = df_usecase[feature].diff().abs().mean()
        statistical_features[f'{feature}_abs_diff_minmax'] = absolute_diff
        statistical_features[f'{feature}_changes_from_first_to_last'] = change_from_first_to_last

    # Append statistical features for the use case to the list
    use_case_features.append(statistical_features)

    # Create a DataFrame from the list of statistical features
    df_features = pd.DataFrame(use_case_features)

    return df_features

def feature_engineering(interval_df, exclude_features=['y']):
    features_for_extraction = []
    for feature in interval_df.columns:
        if feature not in exclude_features:
            features_for_extraction.append(feature)
    
    # Extract statistical features for the interval
    statistical_features = calculate_statistical_features(interval_df, features=features_for_extraction)

    # Determine the majority value for 'date' and 'danger_zone' within the segment
    majority_y = interval_df['y'].mode()[0] if 'y' in interval_df.columns else None
    
    # Replace NaN values with the majority value
    if majority_y is not None:
        interval_df['y'].fillna(majority_y, inplace=True)

    # Append the statistical features along with majority date and majority danger_zone
    statistical_features['y'] = majority_y
    return statistical_features


def create_segmented_dataframe(df, df_name, segment_size=7, stride=1):
    # Initialize an empty list to store DataFrames
    dfs = []
    try:
        """Use for-loop below to do striding, i.e. rolling segmentation"""
        # Roll the intervals with overlapping segments
        for i in range(0, len(df) - segment_size + 1, stride):
            start_idx = i
            end_idx = min(i + segment_size, len(df))  # Adjust end index to handle the last segment
            interval_df = df.iloc[start_idx:end_idx]
            # visualise_single_feature('Values.WiFiSignalStrengthN_median',interval_df)

            statistical_features = feature_engineering(interval_df)

            dfs.append(statistical_features)
            print(f"Calculated statistical features for {df_name}")
    except Exception as e:
        print(f"Error: {e}")

    if dfs:
        # Concatenate the list of DataFrames
        segmented_df = pd.concat(dfs, ignore_index=True)
        return segmented_df
    else:
        # Skip segmentation and return None
        print("No segmentation performed as dfs is empty.")
        return None
    
def save_concatenated_df(output_path, df, file_name):  
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Write the concatenated DataFrame to a CSV file
    output_file = os.path.join(output_path, file_name)
    df.to_csv(output_file, index=False)

    print("Concatenated CSV saved to:", output_file)

def main():
    # load data
    path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Kaggle data\Controlled anomalies\data.csv'
    df = pd.read_csv(path)
    # Drop irrelevant features
    df.drop(['aimp','adbr','adfl','category'], axis=1, inplace=True)

    # Dataset already ordered by time, therefore drop time-column
    df.drop(['timestamp'], axis=1, inplace=True) 

    # Slice dataset for easier computation
    train_df = df[1000000:1080000] # Train
    train_df = train_df.reset_index()
    test_df = df[4310000:4326000] # Test
    test_df = test_df.reset_index()

    # Map target column
    print(train_df['y'].value_counts())
    print(test_df['y'].value_counts())
    train_df.drop(['index'], axis=1, inplace=True)
    test_df.drop(['index'], axis=1, inplace=True)

    # Visualize feature
    # visualise_single_feature('arnd', train_df)
    # visualise_single_feature('arnd', test_df)
    
    # Save df
    output_path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Kaggle data\Controlled anomalies'
    train_df = create_segmented_dataframe(train_df, 'train_df')
    save_concatenated_df(output_path, train_df, 'train_df.csv')

    test_df = create_segmented_dataframe(test_df, 'test_df')
    save_concatenated_df(output_path, test_df, 'test_df.csv')
    




if __name__ == '__main__':
    main()