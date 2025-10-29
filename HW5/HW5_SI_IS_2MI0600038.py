from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
import csv

from sklearn import model_selection as ms


def extract_vocabulary(D : pd.DataFrame):
    return len(D.columns)-1

def count_docs(D : pd.DataFrame):
    return len(D)

def count_docs_in_class(D : pd.DataFrame, c):
    return len(D.loc[D['class'] == c])

def count_tokens_of_term(D: pd.DataFrame, c, atribute, term):
    
    return D.loc[(D['class'] == c) & (D[atribute] == term)].shape[0]

def train_BernoulliNB(classes, documents, attributes, vocabulary, _lambda=1):
    number_of_docs = count_docs(documents)
    prior = {}
    condprob = {c: {attribute: {} for attribute in attributes} for c in classes}
    for _class in classes:
        Nc = count_docs_in_class(documents, _class)
        prior[_class] = Nc / number_of_docs
        for attribute in attributes:
            for term in vocabulary:
                Nct = count_tokens_of_term(documents, _class, attribute, term)
                condprob[_class][attribute][term] = (Nct + _lambda) / (Nc + (len(vocabulary) * _lambda))
    
    return prior, condprob
    
def apply_BernoulliNB(classes,vocabulary, attributes, prior,condprob,documents : pd.DataFrame):
    predictions = []
    perfect_guesses = 0
    for index, row in documents.iterrows():
        doc = list(row)
        score = {}
        for _class in classes:    
            score[_class] = np.log(prior[_class])
            for attribute in range(len(attributes)-1):
                    term = doc[attribute + 1]
                    if term in vocabulary:
                        score[_class] += np.log(condprob[_class][attributes[attribute]][doc[attribute + 1]])
        prediction = max(score, key=score.get)
        if prediction == doc[0]:
            perfect_guesses += 1
        predictions.append(prediction)
    return predictions, perfect_guesses

def std_deviation(accuracies,mean_of_accuracies):
    for i in range(len(accuracies)):
        accuracies[i] -= mean_of_accuracies
        accuracies[i] *= accuracies[i]

    var = sum(accuracies)
    var /= len(accuracies)

    return np.sqrt(var)

def main():
    task_type = int(input("Enter 0 for 3 values or enter 1 for 2 values."))

    data = pd.read_csv("house-votes-84.data")
    classes = {"republican", "democrat"}
    attributes = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12", "a13", "a14", "a15", "a16"]
    vocabulary = {"y","n","?"}
    if task_type == 1:
        vocabulary = {"y","n"}
        data.replace("?","y", inplace=True)
    
    
    X_train, X_test, y_train, y_test = ms.train_test_split(data, data['class'], test_size=0.2,stratify=data["class"])
    
    prior,condprob = train_BernoulliNB(classes,X_train,attributes,vocabulary,1)
    res,guesses1 = apply_BernoulliNB(classes,vocabulary,attributes,prior,condprob,X_test)
    accuracy = (guesses1/(len(X_test)))*100
    print(f"Test Set Accuracy: {round(accuracy,2)}")
    print("")

    folds = ms.KFold(n_splits=10,shuffle=True,random_state=None)
    accuracies = []
    
    for i,(train_index, test_index) in enumerate(folds.split(data)):
        
        tenf_train, tenf_test = data.iloc[train_index], data.iloc[test_index]

        prior, condprob = train_BernoulliNB(classes, tenf_train, attributes, vocabulary, 1)
        
        _,guesses = apply_BernoulliNB(classes, vocabulary, attributes, prior, condprob, tenf_test)

        accuracy = (guesses / len(tenf_test)) * 100
        accuracies.append(accuracy)
        print(f"Accuracy Fold {i+1}: {round(accuracy,2)}")

    
    average_accuracy = np.mean(accuracies)
    print(f"Average Accuracy from 10-Fold Cross-Validation: {round(average_accuracy, 2)}%")
    std_dev = std_deviation(accuracies,average_accuracy)
    print(f"Standard Deviation: {round(std_dev, 2)}%")
    print("")
    
    res,guesses2 = apply_BernoulliNB(classes,vocabulary,attributes,prior,condprob,X_train)
    accuracy = (guesses2/(len(X_train)))*100
    print(f"Train Set Accuracy: {round(accuracy,2)}")

if __name__ == "__main__":
    main()

