import NKJP as nkjp
import Train as train

wczytywanie_danych = False
if wczytywanie_danych:
    # nkjp_dir = "C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples"
    nkjp_dir = "C:\\Users\Paweł\Documents\INL_korpus"
    number_of_files = 20 # nie więcej niż 3889
    nkjp.prepare_dictionary(nkjp_dir, number_of_files)
if not wczytywanie_danych:
    daneU, nerU, daneR, nerR, daneT, nerT = train.load_data()

    algorytmy = ["lbfgs", "l2sgd", "ap", "pa", "arow"]
    indeks_najlepszego_algorytmu = train.f1_max(daneU, nerU, daneR, nerR, algorytmy)

    f1, precision, recall, labels, y_pred = train.train(daneU, nerU, daneT, nerT, algorytmy[indeks_najlepszego_algorytmu])
    print(labels)
    print("Miara F1: " + str(f1) + "\nPrecyzja: " + str(precision) + "\nPełność: " + str(recall))
    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(train.metrics.flat_classification_report(nerT, y_pred, labels=sorted_labels, digits=3))

    # print("\nteraz dane zostaną wyświetlone wg klucza: token - nkjp - sklearn\n")
    # for i in range(len(daneT)):
    #     if(nerT[i]!='O' and stanford_ner[i]!='O'):
    #         print(str(daneT[i]) + " - " + str(nerT[i]) + " - " + str(stanford_ner[i]) + "\n")
