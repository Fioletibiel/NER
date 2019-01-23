import NKJP as nkjp
import Train as train

wczytywanie_danych = False
if wczytywanie_danych:
    # nkjp_dir = "C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples"
    nkjp_dir = "C:\\Users\Paweł\Documents\INL_korpus"
    number_of_files = 2000      # nie więcej niż 3889
    nkjp.prepare_dictionary(nkjp_dir, number_of_files)
if not wczytywanie_danych:
    daneU, nerU, daneR, nerR, daneT, nerT = train.load_data()

    algorytmy = ["lbfgs", "l2sgd", "ap", "pa", "arow"]
    indeks_najlepszego_algorytmu = train.f1_max(daneU, nerU, daneR, nerR, algorytmy)

    print("\n\n\n\n------------------------------------------------------------------------------------------------------------------\nWYNIKI:")
    f1, precision, recall, labels, y_pred = train.train(daneU, nerU, daneT, nerT, algorytmy[indeks_najlepszego_algorytmu])
    # print("\nLabels in training data:", end=" ")
    # for elem in labels: print(elem, end=", ")
    # print("\nMiara F1: " + str(round(f1, 2)) + "\nPrecyzja: " + str(round(precision, 2)) + "\nPełność: " + str(round(recall, 2)) + "\n")
    # sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    # print(train.metrics.flat_classification_report(nerT, y_pred, labels=sorted_labels, digits=3))

    dane_uczace = []
    for sent in daneU:
        for token in sent:
            dane_uczace.append(token)
    dane_rozwojowe = []
    for sent in nerR:
        for token in sent:
            dane_rozwojowe.append(token)
    tokens = []
    for sent in daneT:
        for token in sent:
            for key, value in token.items():
                if key == "27)": tokens.append(value)
    nkjp_korpus = []
    for sent in nerT:
        for token in sent:
            nkjp_korpus.append(token)
    eskalern = []
    for sent in y_pred:
        for token in sent:
                eskalern.append(token)

    print("\n\nIlość tokenów uczących: " + str(len(dane_uczace)))
    print("Ilość tokenów rozwojowych: " + str(len(nkjp_korpus)))
    print("Ilość tokenów testowych: " +str(len(eskalern)))
    labelsR = set(dane_rozwojowe)
    labelsT = set(nkjp_korpus)
    labelsZ = set(eskalern)
    print("\nLabels rozwojowe: " + str(labelsR))
    print("Labels testowe: " + str(labelsT))
    print("Labels rozpoznane: " + str(labelsZ))

    print("\nDane zostaną wyświetlone wg klucza: token - nkjp - sklearn")
    good = 0
    for i in range(len(tokens)):
        if eskalern[i] == nkjp_korpus[i] and eskalern[i] != "O": good += 1
    bad = 0
    for i in range(len(tokens)):
        if eskalern[i] != nkjp_korpus[i]: bad += 1
    print("\nDane, dla których sklearn przypisało poprawną wartość: " + str(good) + "/" + str(good+bad) + "\n")
    for i in range(len(tokens)):
        if eskalern[i] == nkjp_korpus[i] and eskalern[i] != "O":
            print(str(tokens[i]) + " - " + str(nkjp_korpus[i]) + " - " + str(eskalern[i]))
    print("\nDane, dla których sklearn przypisało błędną wartość: " + str(bad) + str(good+bad) + "\n")
    for i in range(len(tokens)):
        if eskalern[i] != nkjp_korpus[i]:
            print(str(tokens[i]) + " - " + str(nkjp_korpus[i]) + " - " + str(eskalern[i]))
