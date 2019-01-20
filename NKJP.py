import os
from xml.dom import minidom
import xml.etree.ElementTree as ET

def remove_duplicates_1(list):
    list2 = []
    for i in range(len(list)):
        powtarzasie = False
        for j in range(i):
            if(list[i]==list[j]):
                powtarzasie = True
        if(powtarzasie==False):
            list2.append(list[i])
        # procent = int((i / len(list)) * 100)
        # if (procent % 10 == 0 and procent != 0):
        #     print(str(50 + procent/2) + "%")
        print(str(50+((i/len(list))*100))+"%")
    return list2

def remove_duplicates_2(list1, list2):
    list3 = []
    list4 = []
    for i in range(len(list1)):
        powtarzasie = False
        for j in range(i):
            if(list1[i]==list1[j]):
                powtarzasie = True
        if(powtarzasie==False):
            list3.append(list1[i])
            list4.append(list2[i])
        # procent = int((i / len(list1)) * 100)
        # if (procent % 10 == 0 and procent != 0):
        #     print(str(procent/2) + "%")
        print(str((i/len(list1))*50)+"%")
    return list3, list4

# buff_percent = 0
# def procent(gora,dol):
#     global buff_percent
#     percent = int((gora / dol) * 100)
#     if (percent % 10 == 0 and percent != 0 and percent!= buff_percent):
#         print(str(percent) + "%")
#     buff_percent = percent
def procent(gora,dol,buff):
    global buff_percent
    percent = int((gora / dol) * 100)
    # if (percent % 10 == 0 and percent != 0 and percent != buff):
    if (percent != 0 and percent != buff):
        # print(str(percent) + "%")
        print('{0}%\r'.format(percent)),
    return percent

def preprocess(rootdir, number_of_files):
    # this.rootdir = rootdir # "C:\\Users\Paweł\Documents\INL_korpus"
    # this.number_of_files = number_of_files # 1
    tekst = []
    objects = []
    # tokens = []
    ner = []
    objects_all = []
    # tokens_all = []
    print("wczytywanie danych...")
    iterate_files = 1
    it_obj = 0
    buff = 0
    for subdir, dirs, files in os.walk(rootdir):
        if (iterate_files <= number_of_files):
            for file in files:
                if(subdir==rootdir): break
                filepath = subdir + os.sep + file

                if filepath.endswith("text.xml"):
                    mydoc = minidom.parse(filepath)

                    items_tekst = mydoc.getElementsByTagName('ab')
                    for elem in items_tekst:
                        tekst.append(elem.firstChild.data)

                    # procent = int((iterate_files / number_of_files)*100)
                    # if (procent % 10 == 0 and procent != 0):
                    #     print(str(procent) + "%")
                    buff = procent(iterate_files,number_of_files,buff)

                    iterate_files += 1

                if filepath.endswith("ann_words.xml"):
                    tree = ET.parse(filepath)
                    root = tree.getroot()

                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                for e_f in e_fs:

                                                    if (e_f.attrib == {'name': 'base'}):
                                                        objects_all.append(e_f[0].text)

                                                    # if (e_f.attrib == {'name': 'orth'}):
                                                    #     tokens_all.append(e_f[0].text)

                if filepath.endswith("ann_named.xml"):
                    tree = ET.parse(filepath)
                    root = tree.getroot()

                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                for e_f in e_fs:

                                                    if (e_f.attrib == {'name': 'base'}):
                                                        objects.append(e_f[0].text)

                                                    # if (e_f.attrib == {'name': 'orth'}):
                                                    #     tokens.append(e_f[0].text)

                                                    if(e_f.attrib=={'name': 'type'}):
                                                        ner.append(e_f[0].attrib)

                                                    if(e_f.attrib=={'name': 'subtype'}):
                                                        ner[it_obj] = e_f[0].attrib

                                            it_obj += 1

    print("dane zostały wczytane")
    print("trwa preprocessing... 1/7")
    ner2 = []
    for elem in ner:        # zmienia formatowanie tablicy ner - usuwa wyświetlanie klucza 'value' i zostawia samą nazwę dopasowania ner
        for key, value in elem.items():
            ner2.append(value)
    ner = ner2
    print("trwa preprocessing... 2/7")
    objects2 = []
    ner3 = []
    for i in range(len(objects)-1):     # jeśli obiekty powtarzają się zaraz po sobie, to wywalenie tych bardziej ogólnie zinterpretowanych
        if(objects[i] != objects[i+1]):
            objects2.append(objects[i])  # jeśli chcemy mieć w słowniku formę morfologiczną to używamy objects2.append(tokens[i])
            ner3.append(ner[i])         # a jeśli formę podstawową, wówczas używamy objects2.append(objects[i])
    objects = objects2
    ner = ner3
    print("trwa preprocessing... 3/7")
    # objects, ner = remove_duplicates_2(objects, ner)      # usuwa duplikaty
    # objects_all = remove_duplicates_1(objects_all)        # warto sprawdzić czy algorytm lepiej uczy się na formach podstawowych
    # tokens_all = remove_duplicates_1(tokens_all)          # czy morfologicznych...
    print("trwa preprocessing... 4/7")
    ner4 = []
    objects3 = []
    for i in range(len(ner)):                       # usuwa ze słownika etykiety date i time oraz odpowiadające im obiekty
        if(ner[i] != "date" and ner[i] != "time"):
            ner4.append(ner[i])
            objects3.append(objects[i])
    ner = ner4
    objects = objects3

    # print("\n\n\n")
    # for i in range(len(objects)):
    #     print(str(objects[i])+" - "+str(ner[i]))
    # print("\n\n\n")

    print("trwa preprocessing... 5/7")
    # Dalej trzeba stagować tekst tak, aby każdemu jego tokenowi dopasować wartość przypisaną w dictionary, a jeśli takiej nie ma, wówczas zero.
    # W ten sposób uzyskujemy dane wstępne do trenowania.
    tekst_ner = []
    bufor = 0
    count = 0
    buff = 0
    for token in objects_all:
        entity = False
        for i in range(len(objects)):
            if(token==objects[i]):
                entity = True
                bufor = i
        if(entity==True):
            tekst_ner.append(ner[bufor])
        else:
            tekst_ner.append("O")
        count +=1
        # percent = int((count/len(objects_all))*100)
        # if(percent%10==0 and percent!=0):
        #     print(str(percent)+"%")
        buff = procent(count,len(objects_all), buff)


    print("trwa preprocessing... 6/7")
    tekst2 = []
    ner2 = []
    daneT = []
    nerT = []
    for i in range(len(objects_all)):
        if(i<int(0.9*len(objects_all))):
            tekst2.append(objects_all[i])
            ner2.append(tekst_ner[i])
        if(i>=int(0.9*len(objects_all))):
            daneT.append(objects_all[i])
            nerT.append(tekst_ner[i])

    print("trwa preprocessing... 7/7")
    for i in range(len(tekst2)):
        tekst2[i] = tekst2[i].replace(' ', '-')

    for i in range(len(daneT)):
        daneT[i] = daneT[i].replace(' ', '-')

    print("preprocessing został zakończony")
    return tekst2, ner2, daneT, nerT
