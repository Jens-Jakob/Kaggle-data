import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    """
    Description:
    ---------------------------
    A function that extracts statistical features from a DataFrame
    ---------------------------

    Parameters:
    ---------------------------
    - df_usecase: Dataframe containing original features for each use instance
    - non_binary_features: List of non-binary features
    - binary_features: List of binary features

    Returns:
    ---------------------------
    - df_features: DataFrame containing the extracted statistical features for each use instance
    ---------------------------
    """
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

def main():
    # load data
    path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Kaggle data\data.csv'
    df = pd.read_csv(path)
    # Drop irrelevant features
    df.drop(['aimp','adbr','adfl','category'], axis=1, inplace=True)

    # Dataset already ordered by time, therefore drop time-column
    df.drop(['timestamp'], axis=1, inplace=True) 

    # Slice dataset for easier computation
    train_df = df[1000000:1300000] # Train
    train_df = train_df.reset_index()
    test_df = df[4300000:4350000] # Test
    test_df = test_df.reset_index()

    # Map target column
    print(train_df['y'].value_counts())
    print(test_df['y'].value_counts())

    # Visualize feature
    # visualise_single_feature('arnd', train_df)



if __name__ == '__main__':
    main()