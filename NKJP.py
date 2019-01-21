import os
from xml.dom import minidom
import xml.etree.ElementTree as ET

# def remove_duplicates_1(list):
#     list2 = []
#     for i in range(len(list)):
#         powtarzasie = False
#         for j in range(i):
#             if(list[i]==list[j]):
#                 powtarzasie = True
#         if(powtarzasie==False):
#             list2.append(list[i])
#         # procent = int((i / len(list)) * 100)
#         # if (procent % 10 == 0 and procent != 0):
#         #     print(str(50 + procent/2) + "%")
#         print(str(50+((i/len(list))*100))+"%")
#     return list2
#
# def remove_duplicates_2(list1, list2):
#     list3 = []
#     list4 = []
#     for i in range(len(list1)):
#         powtarzasie = False
#         for j in range(i):
#             if(list1[i]==list1[j]):
#                 powtarzasie = True
#         if(powtarzasie==False):
#             list3.append(list1[i])
#             list4.append(list2[i])
#         # procent = int((i / len(list1)) * 100)
#         # if (procent % 10 == 0 and procent != 0):
#         #     print(str(procent/2) + "%")
#         print(str((i/len(list1))*50)+"%")
#     return list3, list4

def procent(gora,dol,buff):
    global buff_percent
    percent = int((gora / dol) * 100)
    # if (percent % 10 == 0 and percent != 0 and percent != buff):
    if (percent != 0 and percent != buff):
        # print(str(percent) + "%")
        print('{0}%\r'.format(percent)),
    return percent

def load_xmls(rootdir, number_of_files):

    tekst = []  # lista zdań

    w_orth = []
    w_base = []
    w_tag = []
    w_msd = []

    n_orth = []
    n_base = []
    n_type = []
    n_subtype = []

    ann_words_indexes_from = []
    ann_words_indexes_to = []
    ann_named_indexes_from = []
    ann_named_indexes_to = []
    print("wczytywanie danych...")
    iterate_files = 1
    buff = 0
    ann_words_index = 0
    ann_named_index = 0
    for subdir, dirs, files in os.walk(rootdir):
        if (iterate_files <= number_of_files):
            for file in files:
                if(subdir==rootdir): break
                filepath = subdir + os.sep + file

                # [('Melbourne', 'NP', 'B-LOC'),
                #  ('(', 'Fpa', 'O'),
                #  ('Australia', 'NP', 'B-LOC'),
                #  (')', 'Fpt', 'O'),
                #  (',', 'Fc', 'O'),
                #  ('25', 'Z', 'O'),
                #  ('may', 'NC', 'O'),
                #  ('(', 'Fpa', 'O'),
                #  ('EFE', 'NC', 'B-ORG'),
                #  (')', 'Fpt', 'O'),
                #  ('.', 'Fp', 'O')]

                # {'1)+1:postag': 'Fpa',
                #  '2)+1:postag[:2]': 'Fp',
                #  '3)+1:word.istitle()': False,
                #  '4)+1:word.isupper()': False,
                #  '5)+1:word.lower()': '(',
                #  '6)BOS': True,
                #  '7)bias': 1.0,
                #  '8)postag': 'NP',
                #  '9)postag[:2]': 'NP',
                #  '10)word.isdigit()': False,
                #  '11)word.istitle()': True,
                #  '12)word.isupper()': False,
                #  '13)word.lower()': 'melbourne',
                #  '14)word[-2:]': 'ne',
                #  '15)word[-3:]': 'rne'}

                if filepath.endswith("text.xml"):
                    mydoc = minidom.parse(filepath)
                    items_tekst = mydoc.getElementsByTagName('ab')
                    for elem in items_tekst:
                        tekst.append(elem.firstChild.data)
                    buff = procent(iterate_files,number_of_files,buff)
                    iterate_files += 1

                if filepath.endswith("ann_words.xml"):
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    ann_words_indexes_from.append(ann_words_index)
                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                for e_f in e_fs:

                                                    if (e_f.attrib == {'name': 'orth'}):
                                                        w_orth.append(e_f[0].text)

                                                    if (e_f.attrib == {'name': 'base'}):
                                                        w_base.append(e_f[0].text)

                                                    if (e_f.attrib == {'name': 'ctag'}):
                                                        for _, value in e_f[0].attrib.items():
                                                            w_tag.append(value)

                                                    if (e_f.attrib == {'name': 'msd'}):
                                                        w_msd.append(e_f[0].attrib)

                                                    ann_words_index += 1

                    ann_words_indexes_to.append(ann_words_index)

                if filepath.endswith("ann_named.xml"):
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    ann_named_indexes_from.append(ann_named_index)
                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                has_subtype = False
                                                has_type = False
                                                for e_f in e_fs:

                                                    if (e_f.attrib == {'name': 'orth'}):
                                                        n_orth.append(e_f[0].text)

                                                    if (e_f.attrib == {'name': 'base'}):
                                                        n_base.append(e_f[0].text)

                                                    if(e_f.attrib=={'name': 'type'}):
                                                        for _, value in e_f[0].attrib.items():
                                                            n_type.append(value)
                                                        has_type = True

                                                    if(e_f.attrib=={'name': 'subtype'}):
                                                        for _, value in e_f[0].attrib.items():
                                                            n_subtype.append(value)
                                                        has_subtype = True

                                                    ann_named_index += 1

                                                if (has_subtype != True):
                                                    n_subtype.append("")
                                                if (has_type != True):
                                                    n_type.append("")

                    ann_named_indexes_to.append(ann_named_index)

    # tekst_string = ""
    # for word in w_orth:
    #     tekst_string += word + " "
    # #print(tekst_string)

    w_msd_list = []
    for elem in w_msd:
        for _, value in elem.items():
            w_msd_list.append(value)
    w_msd = w_msd_list
    for i in range(len(w_msd)):
        temp = w_msd[i].replace(":", " ")
        temp = temp.split()
        w_msd[i] = temp
    for i in range(len(w_msd)):
        for j in range(10):
            if(j >= len(w_msd[i])):
                w_msd[i].append("")

    for i in range(len(n_base)):
        print(n_base[i] + " - " + n_type[i] + " - " + n_subtype[i])

    # new_n_type = []
    # for i in range(len(n_subtype)):


    w_type = []
    w_subtype = []

    # for file_index in range(len(number_of_files)):
    #     w_od = ann_words_indexes_from[file_index]
    #     w_do = ann_words_indexes_to[file_index]
    #     n_od = ann_named_indexes_from[file_index]
    #     n_do = ann_named_indexes_to[file_index]
    #     for i in range(w_od,w_do):
    #         for j in range(n_od,n_do):
    #             if(w_base[i]==n_base[i] and w_orth[i]==n_orth[i] and ):




    return tekst, w_orth, w_base, w_tag, w_msd, n_orth, n_base, n_type, n_subtype

def feat1(w_tag, indeks):
    if(indeks+1<len(w_tag)): return w_tag[indeks+1]
    else: return "0"

def feat2(w_tag, indeks):
    if(indeks+1<len(w_tag)): return w_tag[indeks+1][0:2]
    else: return "0"

def feat3(w_base, indeks):
    if(indeks+1<len(w_base)):
        return w_base[indeks+1].istitle()
    else: return False

def feat4(w_base, indeks):
    if(indeks+1<len(w_base)):
        return w_base[indeks+1].isupper()
    else: return False

def feat5(w_base, indeks):
    if(indeks+1<len(w_base)):
        return w_base[indeks+1].lower()

def feat6(w_tag, indeks):
    if(indeks-1>=0): return w_tag[indeks-1]
    else: return "0"

def feat7(w_tag, indeks):
    if(indeks-1>=0): return w_tag[indeks-1][0:2]
    else: return "0"

def feat8(w_base, indeks):
    if(indeks-1>= 0):
        return w_base[indeks-1].istitle()
    else: return False

def feat9(w_base, indeks):
    if(indeks-1>= 0):
        return w_base[indeks-1].isupper()
    else: return False

def feat10(w_base, indeks):
    if(indeks-1>= 0):
        return w_base[indeks-1].lower()
    else: return False

# def szukaj(tekst, w_orth, indeks):
#     licz = 0
#
#     return
#
# def feat11():
#
#     return
#
# def feat12():
#
#     return

def feat13(w_tag, indeks):
    return w_tag[indeks]

def feat14(w_tag, indeks):
    return w_tag[indeks][0:2]

def feat15(w_base, indeks):
    return w_base[indeks].isdigit()

def feat16(w_base, indeks):
    return w_base[indeks].istitle()

def feat17(w_base, indeks):
    return w_base[indeks].isupper()

def feat18(w_base, indeks):
    return w_base[indeks].lower()

def feat19(w_orth, indeks):
    return w_orth[indeks].lower()

def feat20(w_base, indeks):
    return w_base[indeks][-2:]

def feat21(w_base, indeks):
    return w_base[indeks][-3:]

def feat22(w_orth, indeks):
    return w_orth[indeks][-2:]

def feat23(w_orth, indeks):
    return w_orth[indeks][-3:]

def feat24(w_msd, indeks, zero_dziewiec):
    return w_msd[indeks][zero_dziewiec]

# {'1)+1:w_tag': 'Fpa',
#  '2)+1:w_tag[:2]': 'Fp',
#  '3)+1:word.istitle()': False,
#  '4)+1:word.isupper()': False,
#  '5)+1:word.lower()': '(',
#  '6)-1:w_tag': 'Fpa',
#  '7)-1:w_tag[:2]': 'Fp',
#  '8)-1:word.istitle()': False,
#  '9)-1:word.isupper()': False,
#  '10)-1:word.lower()': '(',
#  # '11)BOS': True,
#  # '12)EOS': True,
#  '13)w_tag': 'NP',
#  '14)w_tag[:2]': 'NP',
#  '15)word.isdigit()': False,
#  '16)word.istitle()': True,
#  '17)word.isupper()': False,
#  '18)w_base.lower()': 'melbourne',
#  '19)w_orth.lower()': 'melbourne',
#  '20)w_base[-2:]': 'ne',
#  '21)w_base[-3:]': 'rne'
#  '22)w_orth[-2:]': 'ne',
#  '23)w_orth[-3:]': 'rne'
#  '24)w_msd_1': cośtam
#  '24)w_msd_2': cośtam
#  '24)...
#  '24)w_msd_10': cośtam
#  '25) ':
#  '26) ':
#  '27) ':
#  '28) ':
#  '29) ':
#  '30) ': }

def feat25():
    return

tekst, w_orth, w_base, w_tag, w_msd_list, n_orth, n_base, n_type, n_subtype = load_xmls("C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples", 3)

#print(tekst[:1])






















#
# def preprocessing():
#
#     print("dane zostały wczytane")
#     print("trwa preprocessing... 1/7")
#     ner2 = []
#     for elem in ner:        # zmienia formatowanie tablicy ner - usuwa wyświetlanie klucza 'value' i zostawia samą nazwę dopasowania ner
#         for key, value in elem.items():
#             ner2.append(value)
#     ner = ner2
#     print("trwa preprocessing... 2/7")
#     objects2 = []
#     ner3 = []
#     for i in range(len(objects)-1):     # jeśli obiekty powtarzają się zaraz po sobie, to wywalenie tych bardziej ogólnie zinterpretowanych
#         if(objects[i] != objects[i+1]):
#             objects2.append(objects[i])  # jeśli chcemy mieć w słowniku formę morfologiczną to używamy objects2.append(tokens[i])
#             ner3.append(ner[i])         # a jeśli formę podstawową, wówczas używamy objects2.append(objects[i])
#     objects = objects2
#     ner = ner3
#     print("trwa preprocessing... 3/7")
#     # objects, ner = remove_duplicates_2(objects, ner)      # usuwa duplikaty
#     # objects_all = remove_duplicates_1(objects_all)        # warto sprawdzić czy algorytm lepiej uczy się na formach podstawowych
#     # tokens_all = remove_duplicates_1(tokens_all)          # czy morfologicznych...
#     print("trwa preprocessing... 4/7")
#     ner4 = []
#     objects3 = []
#     for i in range(len(ner)):                       # usuwa ze słownika etykiety date i time oraz odpowiadające im obiekty
#         if(ner[i] != "date" and ner[i] != "time"):
#             ner4.append(ner[i])
#             objects3.append(objects[i])
#     ner = ner4
#     objects = objects3
#
#     print("trwa preprocessing... 5/7")
#     # Dalej trzeba stagować tekst tak, aby każdemu jego tokenowi dopasować wartość przypisaną w dictionary, a jeśli takiej nie ma, wówczas zero.
#     # W ten sposób uzyskujemy dane wstępne do trenowania.
#     tekst_ner = []
#     bufor = 0
#     count = 0
#     buff = 0
#     for token in objects_all:
#         entity = False
#         for i in range(len(objects)):
#             if(token==objects[i]):
#                 entity = True
#                 bufor = i
#         if(entity==True):
#             tekst_ner.append(ner[bufor])
#         else:
#             tekst_ner.append("O")
#         count +=1
#
#         buff = procent(count,len(objects_all), buff)
#
#
#     print("trwa preprocessing... 6/7")
#     tekst2 = []
#     ner2 = []
#     daneT = []
#     nerT = []
#     for i in range(len(objects_all)):
#         if(i<int(0.9*len(objects_all))):
#             tekst2.append(objects_all[i])
#             ner2.append(tekst_ner[i])
#         if(i>=int(0.9*len(objects_all))):
#             daneT.append(objects_all[i])
#             nerT.append(tekst_ner[i])
#
#     print("trwa preprocessing... 7/7")
#     for i in range(len(tekst2)):
#         tekst2[i] = tekst2[i].replace(' ', '-')
#
#     for i in range(len(daneT)):
#         daneT[i] = daneT[i].replace(' ', '-')
#
#     print("preprocessing został zakończony")
#     return tekst2, ner2, daneT, nerT
