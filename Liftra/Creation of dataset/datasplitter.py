import random
import pandas as pd
import os

def create_train_test_split(df, train_ratio=0.8, random_state=None):
    random.seed(random_state)
    total_cranes = [crane for crane in df['craneID'].unique()]

    # Separate machines into two groups based on label
    label_1_machines = df[df['danger_zone'] == 1]['craneID'].unique()

    # Create a copy of total_cranes to iterate over
    total_cranes_copy = total_cranes.copy()

    for other_crane in total_cranes_copy:
        if other_crane in label_1_machines:
            total_cranes.remove(other_crane) # Remove label_1 cranes from the total crane list
    
    
    # Randomly shuffle the machines in each group
    random.shuffle(label_1_machines)
    random.shuffle(total_cranes)
    
    # Determine number of machines for training and testing
    num_train_label_1_machines = int(len(label_1_machines) * train_ratio)
    num_test_label_1_machines = len(label_1_machines) - num_train_label_1_machines
    
    num_train_other_machines = int(len(total_cranes) * train_ratio)
    num_test_other_machines = len(total_cranes) - num_train_label_1_machines  # Subtract label_1_machines
    
    # Assign machines to training and testing sets
    train_label_1_machines = label_1_machines[:num_train_label_1_machines]
    test_label_1_machines = label_1_machines[num_train_label_1_machines:]
 
    
    train_other_machines = total_cranes[:num_train_other_machines]
    # print(train_other_machines)
    test_other_machines = total_cranes[num_train_other_machines:]  
    
    # Combine machines from both groups for training and testing sets
    train_machines = list(train_label_1_machines) + list(train_other_machines)
    test_machines = list(test_label_1_machines) + list(test_other_machines)
    
    # Filter data for train and test sets
    train_df = df[df['craneID'].isin(train_machines)]
    test_df = df[df['craneID'].isin(test_machines)]
    
    return train_df, test_df

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

def main():
    path = r'C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Dataframes\Baseline model\concatenated cranes\concatenated_cranes.csv'
    df = pd.read_csv(path)
    train_df, test_df = create_train_test_split(df, random_state=42)

    output_path = os.path.dirname(path)  # Get the directory of the original CSV file
    
    # Save train_df and test_df as CSV files in the same directory
    save_concatenated_df(output_path, train_df, 'train_data.csv')
    save_concatenated_df(output_path, test_df, 'test_data.csv')


if __name__ == '__main__':
    main()