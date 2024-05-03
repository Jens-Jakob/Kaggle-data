import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')


def grouping_averages(df):   
    df2 = df.copy()
    df2['group_1_avg'] = df2[['sensor_01', 'sensor_02']].mean(axis=1)
    df2['group_2_avg'] = df2[['sensor_03', 'sensor_04', 'sensor_05', 'sensor_06', 'sensor_07', 'sensor_08']].mean(axis=1)
    df2['group_3_avg'] = df2[['sensor_09', 'sensor_10', 'sensor_11']].mean(axis=1)
    df2['group_4_avg'] = df2[['sensor_13', 'sensor_16', 'sensor_17']].mean(axis=1)
    df2['group_5_avg'] = df2[['sensor_18', 'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23']].mean(axis=1)
    df2['group_6_avg'] = df2[['sensor_24', 'sensor_25', 'sensor_27', 'sensor_28', 'sensor_29', 'sensor_30', 'sensor_31', 'sensor_32']].mean(axis=1)
    df2['group_7_avg'] = df2[['sensor_33', 'sensor_34']].mean(axis=1)
    df2['group_8_avg'] = df2[['sensor_37', 'sensor_38', 'sensor_39', 'sensor_40', 'sensor_41', 'sensor_42', 'sensor_44', 'sensor_45', 'sensor_46']].mean(axis=1)
    df_average = df2[['group_1_avg', 'group_2_avg', 'group_3_avg', 'group_4_avg', 'group_5_avg', 'group_6_avg', 'group_7_avg', 'group_8_avg','machine_status']]

    return df_average

# #rename features 
def rename_features(df):
    df = df.rename(columns={'group_1_avg': 'Feature_1', 
                            'group_2_avg': 'Feature_2', 
                            'group_3_avg': 'Feature_3', 
                            'group_4_avg': 'Feature_4',
                            'group_5_avg': 'Feature_5', 
                            'group_6_avg': 'Feature_6', 
                            'group_7_avg': 'Feature_7', 
                            'group_8_avg': 'Feature_8'})
    return df

def define_label(df):
    df['machine_status'] = df['machine_status'].map({'NORMAL': 0, 'BROKEN': 1, 'RECOVERING': 1})
    return df

def split_data(df, test_size=0.5):
    length_data = len(df)

    # Define split-index
    split_idx = int(len(df) * test_size)
    split_idx_2 = split_idx * 0.3

    # Define end_index for test set (Remove last 30% of test set)
    end_idx = int(length_data - split_idx_2)

    # Define train and test set
    training_df = df[:split_idx]
    test_df = df[split_idx:end_idx]
    return training_df, test_df





def main():
    # load df
    path = r"C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\sensor.csv"
    df = pd.read_csv(path)

    # Replace MV's with 0
    df.fillna(0,inplace=True)

    # Reduce features
    df_average = grouping_averages(df)

    # Rename features
    df_renamed = rename_features(df_average)

    # Define label
    df_labeled = define_label(df_renamed)

    train_df, test_df = split_data(df_labeled)

    # Save train_df and test_df as CSV files in the same directory
    train_df.to_csv('train_data.csv', index=False)
    test_df.to_csv('test_data.csv', index=False)




if __name__ == '__main__':
    main()
