from sklearn.model_selection import train_test_split
import os
import json
import sklearn_crfsuite
from sklearn_crfsuite import metrics

import scipy.stats
from sklearn.model_selection  import RandomizedSearchCV
from sklearn.metrics import make_scorer

def load_data():

    filepath = "./venv/Input_file/"
    filename = "input_data" + ".json"
    with open(os.path.join(filepath, filename), 'r') as temp_file:
        features = json.load(temp_file)
    filename = "predictions" + ".json"
    with open(os.path.join(filepath, filename), 'r') as temp_file:
        predictions = json.load(temp_file)
        # predictions_binarized = json.load(temp_file)
        # predictions_binarized = np.load(temp_file)
    # filename = "factors" + ".json"
    # with open(os.path.join(filepath, filename), 'r') as temp_file:
    #     factors = json.load(temp_file)
    # w_orth, w_base, w_tag, w_msd, w_type, w_subtype, BOS, EOS, number_of_tokens, number_of_sentences, od, do = factors

    # predictions_sentences = []
    # for sent_i in range(number_of_sentences):
    #     predictions_sentences.append(list())
    #     for indeks in range(od[sent_i], do[sent_i]):
    #         predictions_sentences[sent_i].append(predictions_binarized[indeks])
    # #print(predictions_sentences)
    # print("\n\n")
    # predictions_binarized = predictions_sentences
    # # for i in range(len(predictions_binarized)):
    # #     for j in range(len(predictions_binarized[i])):
    # #         predictions_binarized[i][j] = np.int32(predictions_binarized[i][j])
    # # predictions_binarized_array = np.array([np.array(xi) for xi in predictions_binarized])
    # # print(predictions_binarized_array)
    # for sent_i in range(number_of_sentences):
    #     for token_i in range(len(predictions_binarized[sent_i])):
    #         predictions_binarized[sent_i][token_i] = np.int32(predictions_binarized[sent_i][token_i])
    #
    # lista = list()
    # for sent_i in range(number_of_sentences):
    #     lista.append(np.array([np.array(xi) for xi in predictions_binarized]))
    # # predictions_binarized_array = np.array([np.array(xi) for xi in predictions_binarized])
    # # print(predictions_binarized_array)
    # lista = np.array(lista)
    # print(type(lista))
    # print(type(lista[0]))
    # print(type(lista[0][0]))
    # print(type(lista[0][0][0]))
    # print(type(lista[0][0][0][0]))
    #
    # # predictions = np.array()
    # # for sent_i in range(number_of_sentences):
    # #     np.append()
    # #     for indeks in range(od[sent_i], do[sent_i]):
    # #         predictions[sent_i].append(dict())
    # #         predictions[sent_i][indeks-od[sent_i]] = {}

    # daneUR, daneT, nerUR, nerT = train_test_split(features, predictions, test_size=0.1, random_state=0)
    # daneU, daneR, nerU, nerR = train_test_split(daneUR, nerUR, test_size=0.11, random_state=0)
    daneU, daneRT, nerU, nerRT = train_test_split(features, predictions, test_size=0.2, random_state=0)
    daneR, daneT, nerR, nerT = train_test_split(daneRT, nerRT, test_size=0.5, random_state=0)
    # print(len(daneU))
    # print(len(nerU))
    # print("")
    # print(len(daneR))
    # print(len(nerR))
    # print("")
    # print(len(daneT))
    # print(len(nerT))
    # print("")

    return daneU, nerU, daneR, nerR, daneT, nerT

def procent(gora,dol,buff):
    global buff_percent
    percent = int((gora / dol) * 100)
    if (percent != 0 and percent != buff):
        print('{0}%\r'.format(percent)),
    return percent

def hyperparameter_optimization(X_train, y_train):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        max_iterations=100,
        all_possible_transitions=True
    )
    params_space = {'c1': scipy.stats.expon(scale=0.5), 'c2': scipy.stats.expon(scale=0.05)}

    f1_scorer = make_scorer(metrics.flat_f1_score, average='weighted', )

    rs = RandomizedSearchCV(crf, params_space,
                            cv=3,
                            verbose=1,
                            n_jobs=-1,
                            n_iter=50,
                            scoring=f1_scorer)
    rs.fit(X_train, y_train)

    # print('best params:', rs.best_params_)
    # print('best CV score:', rs.best_score_)
    # print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))

    # for key, value in rs.best_params_.item():
    print("best params: ")
    print(len(rs.best_params_))
    print(type(rs.best_params_))
    print(rs.best_params_)
    # best params:
    # 2
    # <class 'dict'>
    # {'c1': 0.0016129636757673464, 'c2': 0.005536036011289631}

    # [Parallel(n_jobs=-1)]: Done 34 tasks | elapsed: 58.1s
    # [Parallel(n_jobs=-1)]: Done 150 out of 150 | elapsed: 4.1min finished
    # Traceback(most recent call last):
    # File "C:/Users/p.kaminski4/PycharmProjects/NER/Main.py", line 16, in < module >
    # best params:
    # 2
    # <class 'dict'>
    # {'c1': 0.0016129636757673464, 'c2': 0.005536036011289631}
    # indeks_najlepszego_algorytmu = train.f1_max(daneU, nerU, daneR, nerR, algorytmy)
    # File "C:\Users\p.kaminski4\PycharmProjects\NER\Train.py", line 167, in f1_max
    # f1, _, _, _, _ = train(daneU, nerU, daneR, nerR, algorytm[indeks])
    # File "C:\Users\p.kaminski4\PycharmProjects\NER\Train.py", line 123, in train
    # ce1, ce2 = hyperparameter_optimization(daneU, nerU)
    # TypeError: 'NoneType' object is not iterable

def train(daneU, nerU, daneR, nerR, algorytm):

    # algorytmy:
    # 'lbfgs' - Gradient descent using the L-BFGS method
    # 'l2sgd' - Stochastic Gradient Descent with L2 regularization term
    # 'ap' - Averaged Perceptron
    # 'pa' - Passive Aggressive (PA)
    # 'arow' - Adaptive Regularization Of Weight Vector (AROW)
    if algorytm == "lbfgs":
        ce1, ce2 = hyperparameter_optimization(daneU, nerU)
        crf = sklearn_crfsuite.CRF(
            algorithm=algorytm,
            c1=0.1,     # 0.1,
            c2=0.1,     # 0.1,
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
    print("\n\nAlgorytm: " + str(algorytm))
    print("\nTraining labels:", end=" ")
    for elem in labels: print(elem, end=", ")
    print("\nPrecyzja: " + str(round(precision, 2)) + "\nPełność: " + str(round(recall, 2)) + "\nMiara F1: " + str(round(f1, 2)) + "\n")
    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(metrics.flat_classification_report(nerR, y_pred, labels=sorted_labels, digits=3))
    print("---------------------------------------------------------")
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
