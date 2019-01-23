import NKJP as nkjp
import Train as train

wczytywanie_danych = False
if wczytywanie_danych:
    nkjp_dir = "C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples"
    # nkjp_dir = "C:\\Users\Paweł\Documents\INL_korpus"
    number_of_files = 10 # nie więcej niż 3889
    nkjp.prepare_dictionary(nkjp_dir, number_of_files)
if not wczytywanie_danych:
    daneU, nerU, daneR, nerR, daneT, nerT = train.load_data()

    algorytmy = ["lbfgs", "l2sgd", "ap", "pa", "arow"]
    indeks_najlepszego_algorytmu = train.f1_max(daneU, nerU, daneR, nerR, algorytmy)

    print("\n\nWYNIKI:")
    f1, precision, recall, labels, y_pred = train.train(daneU, nerU, daneT, nerT, algorytmy[indeks_najlepszego_algorytmu])
    print("\nEntities:", end=" ")
    for elem in labels: print(elem, end=", ")
    print("\nMiara F1: " + str(round(f1, 2)) + "\nPrecyzja: " + str(round(precision, 2)) + "\nPełność: " + str(round(recall, 2)) + "\n")

    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(train.metrics.flat_classification_report(nerT, y_pred, labels=sorted_labels, digits=3))


    print("\nTeraz dane zostaną wyświetlone wg klucza: token - nkjp - sklearn\n")
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

    # print("\nDane, dla których sklearn przypisało jakąś wartość:\n")
    # for i in range(len(tokens)):
    #     if eskalern[i] != 'O':
    #         print(str(tokens[i]) + " - " + str(nkjp_korpus[i]) + " - " + str(eskalern[i]))

    licz = 0
    for i in range(len(tokens)):
        if eskalern[i] == nkjp_korpus[i] and eskalern[i] != "O": licz += 1
    print("\nDane, dla których sklearn przypisało poprawną wartość: " + str(licz) + "\n")
    for i in range(len(tokens)):
        if eskalern[i] == nkjp_korpus[i] and eskalern[i] != "O":
            print(str(tokens[i]) + " - " + str(nkjp_korpus[i]) + " - " + str(eskalern[i]))

    licz = 0
    for i in range(len(tokens)):
        if eskalern[i] != nkjp_korpus[i]: licz += 1
    print("\nDane, dla których sklearn przypisało błędną wartość: " + str(licz) + "\n")
    for i in range(len(tokens)):
        if eskalern[i] != nkjp_korpus[i]:
            print(str(tokens[i]) + " - " + str(nkjp_korpus[i]) + " - " + str(eskalern[i]))