import os
import pandas as pd


def calculate_statistical_features(df_useinstance, feature):
    """
    Calculate statistical features for each feature in a dataframe.

    Parameters:
    - df_usecase: Dataframe containing original features for each use case
    - non_binary_features: List of non-binary features
    - binary_features: List of binary features

    Returns:
    - df_features: DataFrame containing the extracted statistical features for each use case.
    """
    # Initialize an empty list to store statistical features for each use case
    useinstance_features = []

    # Calculate statistical features for the use case
    statistical_features = {}
    
    # Extract statistical features for non-binary features
    statistical_features[f'{feature}_median'] = df_useinstance[feature].median()

    # Append statistical features for the use case to the list
    useinstance_features.append(statistical_features)

    # Create a DataFrame from the list of statistical features
    df_features = pd.DataFrame(useinstance_features)

    return df_features


def create_dataframe(folder_path, crane_number):
    """
    A function that concatenates multiple csv-files into a single DataFrame.

    Features included in the DataFrame:
    - Statistical features (for binary and non-binary features)
    - date: The date of the use-case
    - danger_zone: Feature that shows if the crane is in danger zone or not. 
                   1 if usecase is in danger zone, 0 otherwise. By default it's 0
    - usecase_length: Feature that shows how many rows the usecase contains.
        

    Parameters:
    - folder_path: The path to the folder that contains the csv-files
    - features_to_keep: List that contains all of the feature's that you want to keep
    - binary_features: List that contains all of the binary features of features_to_keep
    - non_binary_features: List that contains all of the non-binary features of features_to_keep
    - crane_number: Serial number of crane (crane ID)
    Returns:
    - concatenated_df: The concatenated DataFrame sorted by the date.
    """
    
    # Get list of CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Iterate through each CSV file
    for file in csv_files:
        # Read CSV file into a DataFrame
        df = pd.read_csv(os.path.join(folder_path, file))

        # Specify which features to keep
        df = df[['Values.WiFiSignalStrengthN']]

        # Number of rows in the usecase
        rows_in_usecase = len(df)

        # Extract statistical features from binary and non-binary features
        new_df = calculate_statistical_features(df, 'Values.WiFiSignalStrengthN')
        try:
            # Add 'danger_zone' column
            new_df['danger_zone'] = 0

            date_str = '_'.join(file.split('_')[:3])  # Assuming date is at the beginning and separated by underscores
            new_df['date'] = date_str

            # Add 'date' column
            new_df['date'] = pd.to_datetime(new_df['date'], format='%Y_%m_%d')  # Adjust the format accordingly

            # Add usecase length feature
            new_df['usecase_length'] = rows_in_usecase

            # Add craneID feature
            new_df['craneID'] = crane_number
            
            # Append DataFrame to the list
            dfs.append(new_df)
            print(f"Appended: {file}!")
        except Exception as e:
            print(f"An error has occurred: {e}")
        
        
    
    print("Conversion to datetime: Complete")
    print("Sorting the df by date: Complete")

    # Concatenate all DataFrames in the list
    df = pd.concat(dfs, ignore_index=True)
    print("The csv-files have successfully been concatenated!")

    # Remove use instances that are less than 300
    df = df.drop(df[df['usecase_length'] < 300].index)

    # Sort dataframe by date
    df = df.sort_values(by='date')

    # Reset the index to generate a new index
    df.reset_index(inplace=True, drop=True)

    # Add num of useinstance
    df['index_useinstance'] = df.index+1

    return df

    

def label_danger_zone(dataframe, start_date, end_date):
    """
    Function that labels 'danger_zone' to 1 in specified days
    """
    # Mark the danger_zone cases to 1
    # dataframe.loc[dataframe["date"].isin(list), "danger_zone"] = 1


    # start_date = start_date
    # end_date = end_date
    dataframe['date'] = pd.to_datetime(dataframe['date'])

        # Create a boolean mask to locate rows within the date range
    date_mask = (dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)

    # Set 'danger zone' to 1 for rows within the date range
    dataframe.loc[date_mask, 'danger_zone'] = 1

    print("Dataset has been labeled!")
    return dataframe

def save_concatenated_df(output_path, df, file_name):
    """
    Function that turns a DataFrame into a CSV-file and saves it in specified folder

    Parameters:
    - output_path: Path to location where you want to save the CSV-file
    - df: The DataFrame that'll get saved as a CSV-file
    - file_name: Filename of the CSV-file when it gets saved.
    """
    
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Write the concatenated DataFrame to a CSV file
    output_file = os.path.join(output_path, file_name)
    df.to_csv(output_file, index=False)

    print("Concatenated CSV saved to:", output_file)

def list_subfolders(source_folder):
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder '{source_folder}' does not exist.")
        return

    # Get a list of all items (files and folders) in the source folder
    items = os.listdir(source_folder)

    # Filter out only the subfolders
    subfolders = [item for item in items if os.path.isdir(os.path.join(source_folder, item))]

    # Print the names of the subfolders
    if subfolders:
        print("Subfolders within", source_folder, ":")
        for folder in subfolders:
            print(folder)
    else:
        print("There are no subfolders within", source_folder)
    return subfolders


danger_cranes = ['LT1200-1-P02-002_uncompressed','LT1200-2-P01-002_uncompressed','LT1200-2-P03-001_uncompressed',
               'Kran 4 uncompressed','Kran 7 uncompressed']

def main():
    print("---------- Create concatenated dataframe --------")
    # source_folder_path = r'm:\UNI Daki\2. semester\P2\Samlet data_NoKeyword_NoKeyword_2' # Change path to source folder that contains subfolders (different cranes)
    source_folder_path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Samlet data_NoKeyword_2'
    subfolders = list_subfolders(source_folder_path)
    for folder in subfolders:
        # folder_path = f'm:/UNI Daki/2. semester/P2/Samlet data_NoKeyword_NoKeyword_2/{folder}' 
        folder_path = f'C:/Users/marti/Desktop/Uni/Design og Anvendelse af AI/2. semester/P2/Samlet data_NoKeyword_2/{folder}'

        df = create_dataframe(folder_path, folder)
        print("DataFrame created!")
        # print("Length of df before removal: ", len(df))



        if folder in danger_cranes:
            if folder == 'LT1200-1-P02-002_uncompressed':
                df = label_danger_zone(df, '2023-08-01', '2023-08-05')
            elif folder == 'LT1200-2-P01-002_uncompressed':
                df = label_danger_zone(df, '2024-01-12','2024-01-31')
                df = label_danger_zone(df, '2023-06-05','2023-07-02')
            elif folder == 'LT1200-2-P03-001_uncompressed':
                df = label_danger_zone(df,'2022-04-21','2022-05-17')
            elif folder == 'Kran 4 uncompressed':
                df = label_danger_zone(df, '2023-07-21','2023-08-18')
            elif folder == 'Kran 7 uncompressed':
                df = label_danger_zone(df, '2023-10-10','2023-11-08')
                df = label_danger_zone(df, '2023-04-26','2023-05-17')
        print("Labeling complete")
        

        # Save the DataFrame in specified folder path
        # output_path = f'm:/UNI Daki/2. semester/P2/Dataframes/Use instances/{folder}'
        output_path = f'C:/Users/marti/Desktop/Uni/Design og Anvendelse af AI/2. semester/P2/Dataframes/Baseline model/Processed cranes/{folder}'
        save_concatenated_df(output_path, df, "useinstance.csv")


if __name__ == '__main__':
    main()
