import pandas as pd
import numpy as np
from sklearn import model_selection as ms

def calculate_entropy(proportions):
    
    entropy = 0
    for i in range(len(proportions)):
        if proportions[i] > 0:
            entropy -= proportions[i]*np.log2(proportions[i])
    
    return entropy

def calculate_proportions(data,attribute,num_of_rows):
    
    classes = data[attribute].unique()
    props = [0] * len(classes)
    index = 0

    for c in classes:
        all_c_count = data[data[attribute] == c].shape[0]
        proportion = all_c_count/num_of_rows
        props[index] = proportion
        index += 1

    return props

def calculate_counts_with_classes(data, attribute, main_classes, num_of_rows):
    
    classes = data[attribute].unique()
    props = [[0, 0] for _ in range(len(classes))]
    index = 0

    for c in classes:
        index_mc = 0
        for mc in main_classes:
            count = data[(data[attribute] == c) & (data["class"] == mc)].shape[0]
            props[index][index_mc] = count
            index_mc += 1
        index += 1

    return props

def calculate_gains(data,attributes,num_of_rows,entropy_s):

    main_classes = data["class"].unique()
    #removed ->  attribute = atributes[1:]
    gains = []

    for atr in attributes:       
        counts = calculate_counts_with_classes(data,atr,main_classes,num_of_rows)
        entropy_atr_class = 0

        for i in range(len(counts)):
            total = counts[i][0] + counts[i][1]  
            if total > 0:
                proportions = [counts[i][0] / total, counts[i][1] / total]
                entropy_for_value = calculate_entropy(proportions)
                entropy_atr_class += (total / num_of_rows) * entropy_for_value
        
        gain = entropy_s - entropy_atr_class
        gains.append([atr,gain])

    return gains


def create_dtree(data,num_of_rows,attributes,entropy_s):
    
    
    if len(attributes) == 0:
        return data["class"].mode()[0]
    
    best_gain  = max(calculate_gains(data,attributes,num_of_rows,entropy_s), key=lambda x: x[1])
    values = data[best_gain[0]].unique()
    
    tree = {best_gain[0] : {}}

    for v in values:
        sub_data = data[data[best_gain[0]] == v]
        if len(sub_data) == 0:
            tree[best_gain[0]][v] = data[best_gain[0]].mode()[0]
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_gain[0]]
            tree[best_gain[0]][v] = create_dtree(sub_data,num_of_rows,remaining_attributes,entropy_s)

    return tree

def create_dtree_with_arg(data,num_of_rows,attributes,entropy_s,N,K,G,depth):
    if depth >= N and N > 0:
        return data["class"].mode()[0]
    if len(attributes) == 0:
        return data["class"].mode()[0]
    if len(data) < K and K > 0:
        return data["class"].mode()[0]

    best_gain  = max(calculate_gains(data,attributes,num_of_rows,entropy_s), key=lambda x: x[1])
    if best_gain[1] < G and G > 0:
        return data["class"].mode()[0]
    
    values = data[best_gain[0]].unique()
    
    tree = {best_gain[0] : {}}

    for v in values:
        sub_data = data[data[best_gain[0]] == v]
        if len(sub_data) == 0:
            tree[best_gain[0]][v] = data[best_gain[0]].mode()[0]
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_gain[0]]
            tree[best_gain[0]][v] = create_dtree_with_arg(sub_data,num_of_rows,remaining_attributes,entropy_s,N,K,G,depth+1)

    return tree

def apply_dtree(row,dtree):
    
    if type(dtree) != dict:
        return dtree
    
    for root_attribute in dtree:
        attribute_value = row[root_attribute]

        if attribute_value in dtree[root_attribute]:
            return apply_dtree(row, dtree[root_attribute][attribute_value])
        else:
            return None 
        
def test_dtree(data,tree):

    correct_ans_count = 0
    results = []
    for _, row in data.iterrows():

        result = apply_dtree(row, tree)
        if result == row["class"]:
            correct_ans_count += 1
        results.append(result)

    return results,correct_ans_count

def prune_dtree(dtree,data):

    if type(dtree) != dict: 
            return dtree
    
    attribute = list(dtree.keys())[0] 
    subtrees = dtree[attribute] 
    pruned_dtree = {}

    for v in list(subtrees.keys()):
        subtrees[v] = prune_dtree(subtrees[v],data)

    c_accuracy = test_dtree(data, dtree)
    
    majority_class = data["class"].mode()[0]
    pruned_dtree = majority_class

    p_accuracy = test_dtree(data, pruned_dtree)
    
    if p_accuracy[1] >= c_accuracy[1]:
        return pruned_dtree
    
    return dtree

def main():
    data = pd.read_csv("filleddata.data",header=None)
    columns = ["class","age","menopause","tumor-size","inv-nodes",
           "node-caps","deg-malig","breast","breast-quad","irradiat"]
    data.columns = columns
    
    X_train, X_test, y_train, y_test = ms.train_test_split(data, data['class'], test_size=0.2,stratify=data["class"])
    X_train.columns = columns
    X_test.columns = columns
    props = calculate_proportions(X_train,"class",len(X_train))
    entropy_s = calculate_entropy(props)

    
    mode = int(input("Plese enter 0,1,2 for mode."))
    if mode == 0:
        #pre
        N = int(input("Enter N, if you don not want to enter negative number."))
        K = int(input("Enter K, if you don not want to enter negative number."))
        G = float(input("Enter G, if you don not want to enter negative number."))
        
        dtree = create_dtree_with_arg(X_train,len(X_train),columns[1:],entropy_s,N,K,G,0)

    elif mode == 1:
        #post
        tree = create_dtree(X_train,len(X_train),columns[1:],entropy_s)
        dtree = prune_dtree(tree,X_train)
    elif mode == 2:
        #pre
        #post
        N = int(input("Enter N, if you don not want to enter negative number."))
        K = int(input("Enter K, if you don not want to enter negative number."))
        G = float(input("Enter G, if you don not want to enter negative number."))

        tree = create_dtree_with_arg(X_train,len(X_train),columns[1:],entropy_s,N,K,G,0)
        dtree = prune_dtree(tree,X_train)

    else:
        print("run again")

    
    res,guesses1 = test_dtree(X_test,dtree)
    accuracy = (guesses1/(len(X_test)))*100
    print(f"Test Set Accuracy: {round(accuracy,2)}")
    print("")

    folds = ms.KFold(n_splits=10,shuffle=True,random_state=None)
    accuracies = []
    
    for i,(train_index, test_index) in enumerate(folds.split(data)):
        
        tenf_train, tenf_test = data.iloc[train_index], data.iloc[test_index]

        if mode == 0:
            dtree = create_dtree_with_arg(tenf_train,len(tenf_train),columns[1:],entropy_s,N,K,G,0)
        elif mode == 1:
            dtree = create_dtree(tenf_train,len(tenf_train),columns[1:],entropy_s)
        elif mode == 2:
            tree = create_dtree_with_arg(tenf_train,len(tenf_train),columns[1:],entropy_s,N,K,G,0)
            dtree = prune_dtree(tree,tenf_train)
        
        res,guesses = test_dtree(tenf_test,dtree)
        accuracy = (guesses/(len(X_test)))*100
        accuracies.append(accuracy)
        print(f"Accuracy Fold {i+1}: {round(accuracy,2)}")


    average_accuracy = np.mean(accuracies)
    print(f"Average Accuracy from 10-Fold Cross-Validation: {round(average_accuracy, 2)}%")
    std_dev = np.std(accuracies)
    print(f"Standard Deviation: {round(std_dev, 2)}%")
    print("")
    res,guesses2 = test_dtree(X_train,dtree)
    accuracy = (guesses2/(len(X_train)))*100
    print(f"Train Set Accuracy: {round(accuracy,2)}")
    
    #import pprint
    #pprint.pprint()
if __name__ == "__main__":
    main()
 