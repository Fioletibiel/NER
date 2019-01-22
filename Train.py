from sklearn.model_selection import train_test_split
import os
import json
import sklearn_crfsuite
from sklearn_crfsuite import metrics

def load_data():
    filepath = "./venv/Input_file/"
    filename = "input_data" + ".json"
    with open(os.path.join(filepath, filename), 'r') as temp_file:
        features = json.load(temp_file)
    # for elem in features:
    #     for key, value in elem.items():
    #         print(str(key) + " - " + str(value))
    #     print("")
    filepath = "./venv/Input_file/"
    filename = "predictions" + ".json"
    with open(os.path.join(filepath, filename), 'r') as temp_file:
        predictions = json.load(temp_file)
    # for elem in predictions:
    #     for key, value in elem.items():
    #         print(str(key) + " - " + str(value))
    #     print("")

    daneUR, daneT, nerUR, nerT = train_test_split(features, predictions, test_size=0.1, random_state=0)
    daneU, daneR, nerU, nerR = train_test_split(daneUR, nerUR, test_size=0.11, random_state=0)

    return daneU, nerU, daneR, nerR, daneT, nerT

def procent(gora,dol,buff):
    global buff_percent
    percent = int((gora / dol) * 100)
    if (percent != 0 and percent != buff):
        print('{0}%\r'.format(percent)),
    return percent

def train(daneU, nerU, daneR, nerR, algorytm):

    # algorytmy:
    # 'lbfgs' - Gradient descent using the L-BFGS method
    # 'l2sgd' - Stochastic Gradient Descent with L2 regularization term
    # 'ap' - Averaged Perceptron
    # 'pa' - Passive Aggressive (PA)
    # 'arow' - Adaptive Regularization Of Weight Vector (AROW)
    if algorytm == "lbfgs":
        crf = sklearn_crfsuite.CRF(
            algorithm=algorytm,
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True)
    elif algorytm == "l2sgd":
        crf = sklearn_crfsuite.CRF(
            algorithm=algorytm,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True)
    else:
        crf = sklearn_crfsuite.CRF(
            algorithm=algorytm,
            max_iterations=100,
            all_possible_transitions=True)

    crf.fit(daneU, nerU)
    labels = list(crf.classes_)
    labels.remove("O")
    # print(labels)
    y_pred = crf.predict(daneR)
    f1 = metrics.flat_f1_score(nerR, y_pred, average='weighted', labels=labels)
    precision = metrics.flat_precision_score(nerR, y_pred, average='weighted', labels=labels)
    recall = metrics.flat_recall_score(nerR, y_pred, average='weighted', labels=labels)
    # sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    # print(metrics.flat_classification_report(nerR, y_pred, labels=sorted_labels, digits=3))
    return f1, precision, recall, labels, y_pred

def f1_max(daneU, nerU, daneR, nerR, algorytm):

    f1_list = list()
    buff = 0
    for indeks in range(len(algorytm)):
        f1, _, _, _, _ = train(daneU, nerU, daneR, nerR, algorytm[indeks])
        buff = procent(indeks+1, len(algorytm), buff)
        f1_list.append(f1)
    max_f1_value = max(f1_list)
    max_f1_index = f1_list.index(max_f1_value)
    for indeks in algorytm:
        if indeks == max_f1_index:
            print(str(algorytm[indeks] + ", f1: " + str(max_f1_value)))
    return max_f1_index
