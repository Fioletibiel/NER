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
    return features, predictions
features, predictions = load_data()

mikser_danych = 0
daneUR, daneT, nerUR, nerT = train_test_split(features, predictions, test_size=0.1, random_state=0)
daneU, daneR, nerU, nerR = train_test_split(daneUR, nerUR, test_size=0.11, random_state=mikser_danych)

for elem in daneU[0]:
    print(elem)
print(daneU[0])



crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(daneU, nerU)



labels = list(crf.classes_)
labels.remove("")
print(labels)


print("")

# y_pred = crf.predict(X_test)
# metrics.flat_f1_score(y_test, y_pred,
#                       average='weighted', labels=labels)
#
#
# # group B and I results
# sorted_labels = sorted(
#     labels,
#     key=lambda name: (name[1:], name[0])
# )
# print(metrics.flat_classification_report(
#     y_test, y_pred, labels=sorted_labels, digits=3
# ))

print("")
print("")
print("")

# def train(dane, ner, mikser_danych):
#     daneU, daneR, nerU, nerR = train_test_split(dane, ner, test_size=0.11, random_state=mikser_danych)      # daneU i nerU to dane uczące, zaś daneR i nerR to dane rozwojowe
#
#     polish_corpus = ""
#     for i in range(len(daneU)):
#         polish_corpus += (str(daneU[i]) + " " + str(nerU[i]) + "\n")
#     filepath = "./stanford-ner-2018-10-16/train/"
#     filename = "polish-corpus" + ".tsv"
#     with open(os.path.join(filepath, filename), 'w') as temp_file:
#         temp_file.write(polish_corpus)
#
#
#     subprocess.call("java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -prop train/prop.prop", cwd = "D:/Programy/JetBrains/PyCharm/PycharmProjects/NER/stanford-ner-2018-10-16/")
#
#
#     jar = "./stanford-ner-2018-10-16/stanford-ner.jar"
#     model = "./stanford-ner-2018-10-16/classifiers/ner_model-polish.ser.gz"
#
#     ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
#
#     stanford_przypisanie = ner_tagger.tag(daneR)
#     stanford_przypisanie = list(map(list, zip(*stanford_przypisanie)))
#     # stanford_dane = stanford_przypisanie[0]   # stanford_dane są takie same jak daneR
#     stanford_ner = stanford_przypisanie[1]
#
#
#     # teraz trzeba obliczyć ilosc dobrze dopasowanych entities w stanford_ner w stosunku do nerR
#     licz = 0
#     for i in range(len(nerR)):
#         if(stanford_ner[i] == nerR[i] and stanford_ner[i]!='O'): licz+=1
#     dobrze_dopasowane_entities_w_stanford_ner = licz
#
#     # precyzja = dobrze dopasowane entities w stanford_ner / wszystkie entities w stanford_ner
#     licz = 0
#     for i in range(len(stanford_ner)):
#         if(stanford_ner[i]!='O'): licz+=1
#     wszystkie_entities_w_stanford_ner = licz
#     if(wszystkie_entities_w_stanford_ner!=0): precyzja = dobrze_dopasowane_entities_w_stanford_ner / wszystkie_entities_w_stanford_ner
#     else: precyzja = 0
#
#     # pelnosc = dobrze dopasowane entities w stanford_ner / wszystkie entities w nerR
#     licz = 0
#     for i in range(len(nerR)):
#         if(nerR[i]!='O'): licz+=1
#     wszystkie_entities_w_nerR = licz
#     if(wszystkie_entities_w_nerR!=0): pelnosc = dobrze_dopasowane_entities_w_stanford_ner / wszystkie_entities_w_nerR
#     else: pelnosc = 0
#
#     # miara F1
#     if(precyzja==0 or pelnosc==0): F1 = 0
#     else: F1 = 2* precyzja * pelnosc / (precyzja + pelnosc)
#
#     return precyzja, pelnosc, F1
#
# def check(dane, ner, mikser_danych, number_of_mixes):
#     daneU, daneR, nerU, nerR = train_test_split(dane, ner, test_size=0.11, random_state=mikser_danych)      # daneU i nerU to dane uczące, zaś daneR i nerR to dane rozwojowe
#     print("inicjowanie uczenia...")
#     print("liczba tokenów uczących: " + str(len(daneU)))
#     # print("\n\n\n")
#     # print("daneU")
#     # print(daneU)
#     # print("\n\n\n")
#     # print("daneR")
#     # print(daneR)
#     # print("\n\n\n")
#     # print("nerU")
#     # print(nerU)
#     # print("\n\n\n")
#     # print("nerR")
#     # print(nerR)
#     # print("\n\n\n")
#
#     if(number_of_mixes>1):
#         polish_corpus = ""
#         for i in range(len(daneU)):
#             polish_corpus += (str(daneU[i]) + " " + str(nerU[i]) + "\n")
#
#         filepath = "./stanford-ner-2018-10-16/train/"
#         filename = "polish-corpus" + ".tsv"
#         with open(os.path.join(filepath, filename), 'w') as temp_file:
#             temp_file.write(polish_corpus)
#
#         java_path = "C:/Program Files/Java/jdk1.8.0_202/bin/"
#         os.environ['JAVA_HOME'] = java_path
#         classpath_path = "D:/Programy/JetBrains/PyCharm/PycharmProjects/NER/stanford-ner-2018-10-16/*"
#         os.environ['CLASSPATH'] = classpath_path
#         stanfordmodels_path = "D:/Programy/JetBrains/PyCharm/PycharmProjects/NER/stanford-ner-2018-10-16/classifiers"
#         os.environ['STANFORD_MODELS'] = stanfordmodels_path
#
#         subprocess.call("java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -prop train/prop.prop", cwd = "D:/Programy/JetBrains/PyCharm/PycharmProjects/NER/stanford-ner-2018-10-16/")
#
#     jar = "./stanford-ner-2018-10-16/stanford-ner.jar"
#     model = "./stanford-ner-2018-10-16/classifiers/ner_model-polish.ser.gz"
#
#     ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
#
#     unique = list(set(nerU))
#     number_of_entities = len(unique)-1
#     print("liczba nazw obiektów wg danych uczących: "+str(number_of_entities))
#     print("trening został zakończony")
#     return ner_tagger
#
# def source():
#
#     dane, ner, daneT, nerT = load_data()     # daneT i nerT to dane testowe
#     # print("\n\n\n")
#     # for i in range(len(daneT)):
#     #     print(str(daneT[i])+" - "+str(nerT[i]))
#     # print("\n\n\n")
#
#     # Dokonujemy uczenia dla różnych potasowań danych i dla każdego liczymy F1, z czego wyciągamy to uczenie, dla którego wychodzi największe F1
#     print("inicjowanie wykonywania miksów danych...")
#     precyzja = []
#     pelnosc = []
#     F1 = []
#     for i in range(number_of_mixes):
#         precyzja.append(0)
#         pelnosc.append(0)
#         F1.append(0)
#     for i in range(number_of_mixes):
#         precyzja[i], pelnosc[i], F1[i] = podzial_danych(dane, ner, i)
#         print("wykonano miks: "+str(i+1))
#     F1_max_index = 0
#     for i in range(number_of_mixes-1):
#         if(F1[i+1]>F1[i]):
#             F1_max_index = i+1
#     print("wybrano najbardziej wydajny miks")
#     print("miara F1 przy uczeniu wyniosła: " + str(F1[F1_max_index]) + " (precyzja = " + str(precyzja[F1_max_index]) + ", pełnosć = " + str(pelnosc[F1_max_index]) + ")")
#
#     # W tym miejscu wykonujemy trening danych dla mikser_danych = F1_max_index i sprawdzamy na danychT
#     ner_tagger = trening(dane, ner, F1_max_index, number_of_mixes)
#     print("przypisywanie nazw obiektów...")
#     stanford_przypisanie = ner_tagger.tag(daneT)
#     stanford_przypisanie = list(map(list, zip(*stanford_przypisanie)))
#     stanford_ner = stanford_przypisanie[1]
#     print("przypisywanie nazw zostało zakończone")
#
#     # precyzja, pelnosc i F1 w stosunku do danychT
#     print("sprawdzanie jakości przypisania...")
#     licz = 0
#     for i in range(len(nerT)):
#         if (stanford_ner[i] == nerT[i] and stanford_ner[i] != 'O'): licz += 1
#     dobrze_dopasowane_entities_w_stanford_ner = licz
#     licz = 0
#     for i in range(len(stanford_ner)):
#         if (stanford_ner[i] != 'O'): licz += 1
#     wszystkie_entities_w_stanford_ner = licz
#     if (wszystkie_entities_w_stanford_ner != 0):
#         precyzjaT = dobrze_dopasowane_entities_w_stanford_ner / wszystkie_entities_w_stanford_ner
#     else:
#         precyzjaT = 0
#     licz = 0
#     for i in range(len(nerT)):
#         if (nerT[i] != 'O'): licz += 1
#     wszystkie_entities_w_nerR = licz
#     if (wszystkie_entities_w_nerR != 0):
#         pelnoscT = dobrze_dopasowane_entities_w_stanford_ner / wszystkie_entities_w_nerR
#     else:
#         pelnoscT = 0
#     if (precyzjaT == 0 or pelnoscT == 0):
#         F1_T = 0
#     else:
#         F1_T = 2 * precyzjaT * pelnoscT / (precyzjaT + pelnoscT)
#     print("sprawdzanie jakości przypisania zakończone")
#     print("miara F1 przy sprawdzeniu wyniosła: " + str(F1_T) + " (precyzja = " + str(precyzjaT) + ", pełność = " + str(pelnoscT) + ")")
#
#     # Drukowanie tokenów, przypisań nkjp i przypisań stanforda
#     print("teraz dane zostaną wyświetlone wg klucza: token - nkjp - stanford\n")
#     for i in range(len(daneT)):
#         if(nerT[i]!='O' and stanford_ner[i]!='O'):
#             print(str(daneT[i]) + " - " + str(nerT[i]) + " - " + str(stanford_ner[i]) + "\n")
#
#
#

