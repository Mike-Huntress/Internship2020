
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def predictive_accuracy(signal, objective, n=10):
    """Return a tuple (accuracy, confusion matrix) for predicting an objective with signal."""
    X = signal.long_form().dropna()
    X.date += pd.DateOffset(months=3)
    X = X.set_index(['date', 'country'])
    X = X.dropna()
    Y = objective.long_form().dropna().set_index(['date', 'country']).loc[X.index].dropna()
    X = X.loc[Y.index]
    confusion_matrix = pd.DataFrame({-1: {-1: 0, 1: 0}, 1: {-1: 0, 1: 0}})
    for country in objective.data.columns:
        X_train, X_test = X.query('country != @country'), X.query('country == @country')
        Y_train, Y_test = Y.query('country != @country'), Y.query('country == @country')
        clf = RandomForestClassifier(n_estimators=n)
        clf.fit(X_train, Y_train)
        Y_pred = clf.predict(X_test)
        my_c_mat = pd.crosstab(
            Y_test['value'], Y_pred, rownames=['Actual'], colnames=['Predicted']
        )
        confusion_matrix += my_c_mat / my_c_mat.sum().sum()
    confusion_matrix /= confusion_matrix.sum().sum()
    accuracy = confusion_matrix.loc[-1, -1] + confusion_matrix.loc[1, 1]
    return accuracy, confusion_matrix
