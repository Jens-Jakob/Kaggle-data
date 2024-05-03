import os
import pandas as pd


def list_subfolders(source_folder):
    """
    Description:
    ---------------------------
    A function that finds the name of subfolders within a source folder.
    Subfolders are the different cranes, each containing CSV-files.
    ---------------------------
    

    Parameters:
    ---------------------------
    - source_folder: Path to the source folder
    ---------------------------

    Returns:
    ---------------------------
    List of subfolder names
    ---------------------------
    """

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

def concatenate_dataframes(source_folder):
    """
    Description:
    ---------------------------
    A function that concatenates CSV-files.
    The function iterates through each subfolder, finding the CSV-files
    and concatenates the CSV-files from that subfolder
    ---------------------------

    Parameters:
    ---------------------------
    - source_folder: Path to the source folder
    ---------------------------

    Returns:
    ---------------------------
    DataFrame which consists of the concatenated CSV-files
    ---------------------------

    """
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder '{source_folder}' does not exist.")
        return

    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Get a list of all subfolders
    subfolders = [os.path.join(source_folder, item) for item in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, item))]

    # Iterate through each subfolder
    for subfolder in subfolders:
        # Find CSV file within the subfolder
        csv_files = [file for file in os.listdir(subfolder) if file.endswith('.csv')]

        # Check if a CSV file exists in the subfolder
        if csv_files:
            # Read CSV file into a DataFrame
            df = pd.read_csv(os.path.join(subfolder, csv_files[0]))
            dfs.append(df)
            print(f"Appended: {csv_files[0]} from {subfolder}!")
        else:
            print(f"No CSV file found in {subfolder}!")

    # Concatenate all DataFrames in the list
    if dfs:
        concatenated_df = pd.concat(dfs, ignore_index=True)
        print("The CSV files have successfully been concatenated!")
        return concatenated_df
    else:
        print("No CSV files found in the subfolders.")
        return None



def save_concatenated_df(output_path, df, file_name):
    """
    Description:
    ---------------------------
    A function that turns a DataFrame into a CSV-file and saves it
    ---------------------------

    Parameters:
    ---------------------------
    - output_path: The path where the new CSV-file gets saved
    - df: The DataFrame you wish to save
    - file_name: File name of the saved CSV-file
    ---------------------------
    
    """
    
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Write the concatenated DataFrame to a CSV file
    output_file = os.path.join(output_path, file_name)
    df.to_csv(output_file, index=False)

    print("Concatenated CSV saved to:", output_file)



def main():
    source_folder_path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Dataframes\Baseline model\Processed cranes' # Path to source folder
    output_path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Dataframes\Baseline model\concatenated cranes' # Output path

    # Concatenate and save as a new CSV-file
    df = concatenate_dataframes(source_folder_path) 
    save_concatenated_df(output_path, df, "concatenated_cranes.csv")

if __name__ == '__main__':
    main()