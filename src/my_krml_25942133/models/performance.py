# Solution:
def print_classification_metrics(y_preds, y_actuals, set_name=None):
    """Print the confusion matrix along with precision, recall, and F1-score

    Parameters
    ----------
    y_preds : array-like
        Predicted labels
    y_actuals : array-like
        Actual labels
    set_name : str, optional
        Name of the set to be printed

    Returns
    -------
    None
    """
    from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
    import pandas as pd

    # Confusion Matrix
    cm = confusion_matrix(y_actuals, y_preds)
    print(f"\nConfusion Matrix {set_name}:")
    print(pd.DataFrame(cm,
                       index=[f"Actual_{i}" for i in range(cm.shape[0])],
                       columns=[f"Pred_{i}" for i in range(cm.shape[1])]))

    # Precision, Recall, F1
    precision = precision_score(y_actuals, y_preds, average='weighted', zero_division=0)
    recall = recall_score(y_actuals, y_preds, average='weighted', zero_division=0)
    f1 = f1_score(y_actuals, y_preds, average='weighted', zero_division=0)

    print(f"\nPrecision {set_name}: {precision:.4f}")
    print(f"Recall {set_name}:    {recall:.4f}")
    print(f"F1-score {set_name}:  {f1:.4f}")
