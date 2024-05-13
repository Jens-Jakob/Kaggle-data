import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix



def preprocess(path):
    df = pd.read_csv(path)

    # Drop index column
    for feature in df.columns:
        if "index" in feature:
            df.drop([feature], axis=1, inplace=True)
    
    # Define input/target
    X = df.drop(['y'], axis=1)
    y = df['y']
    return X, y

classifiers = {
    'XGB': XGBClassifier(),
    'RF': RandomForestClassifier()
}

def evaluate_model(X_train, y_train, X_test, y_test, name, ml_model):
    model = ml_model
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print(f"Classificationreport for {name}: ")
    print(classification_report(y_test, pred))
    print("")
    print(f"Confusion matrix for {name}: ")
    print(confusion_matrix(y_test, pred))




def main():
    train_path = r"C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Kaggle data\Controlled anomalies\train_df.csv"
    test_path = r"C:\Users\marti\Desktop\Uni\Design og Anvendelse af AI\2. semester\P2\Kaggle data\Controlled anomalies\test_df.csv"

    X_train, y_train = preprocess(train_path)
    X_test, y_test = preprocess(test_path)

    for name, model in classifiers.items():
        evaluate_model(X_train, y_train, X_test, y_test, name, model)
    


if __name__ == '__main__':
    main()