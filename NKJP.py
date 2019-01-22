import os
import xml.etree.ElementTree as ET
import json

def procent(gora,dol,buff):
    global buff_percent
    percent = int((gora / dol) * 100)
    # if (percent % 10 == 0 and percent != 0 and percent != buff):
    if (percent != 0 and percent != buff):
        # print(str(percent) + "%")
        print('{0}%\r'.format(percent)),
    return percent

def print_procent(i, length, indeks):
    procent = (indeks+1)*35 + (i+1)
    procent = int(procent * 100 / (length*35))
    # print('trwa przetwarzanie... {0}%\r'.format(procent))
    print("trwa przetwarzanie... " + str(procent) + "%")
    # sent = 'trwa przetwarzanie... {0}%\r'.format(procent)
    # print(sent, end='', flush=True)
    # print("trwa przetwarzanie... " + str(procent) + "%", end = '\r')

def load_xmls(nkjp_dir, number_of_files):

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
    for subdir, dirs, files in os.walk(nkjp_dir):
        if iterate_files <= number_of_files:
            for file in files:
                if subdir == nkjp_dir: break
                filepath = subdir + os.sep + file

                if filepath.endswith("ann_words.xml"):
                    buff = procent(iterate_files,number_of_files,buff)
                    iterate_files += 1
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    # ann_words_indexes_from.append(ann_words_index)
                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        ann_words_indexes_from.append(ann_words_index)
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                for key, _ in e_fs.attrib.items():
                                                    if key == "type":
                                                        for e_f in e_fs:

                                                            if e_f.attrib == {'name': 'orth'}:
                                                                w_orth.append(e_f[0].text)

                                                            if e_f.attrib == {'name': 'base'}:
                                                                w_base.append(e_f[0].text)

                                                            if e_f.attrib == {'name': 'ctag'}:
                                                                for _, value in e_f[0].attrib.items():
                                                                    w_tag.append(value)

                                                            if e_f.attrib == {'name': 'msd'}:
                                                                w_msd.append(e_f[0].attrib)

                                                        ann_words_index += 1

                                        ann_words_indexes_to.append(ann_words_index)
                    # ann_words_indexes_to.append(ann_words_index)

                if filepath.endswith("ann_named.xml"):
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    # ann_named_indexes_from.append(ann_named_index)
                    for e_tei in root:
                        for e_text in e_tei:
                            for e_body in e_text:
                                for e_p in e_body:
                                    for e_s in e_p:
                                        ann_named_indexes_from.append(ann_named_index)
                                        for e_seg in e_s:
                                            for e_fs in e_seg:
                                                for key, _ in e_fs.attrib.items():
                                                    if key == "type":
                                                        has_subtype = False
                                                        has_type = False
                                                        has_time = False
                                                        for e_f in e_fs:

                                                            if e_f.attrib == {'name': 'type'}:
                                                                for _, value in e_f[0].attrib.items():
                                                                    if value == "date" or value == "time":
                                                                        has_time = True
                                                                        break
                                                                    n_type.append(value)
                                                                if has_time: break
                                                                has_type = True

                                                            if e_f.attrib == {'name': 'subtype'}:
                                                                for _, value in e_f[0].attrib.items():
                                                                    n_subtype.append(value)
                                                                has_subtype = True

                                                            if e_f.attrib == {'name': 'orth'}:
                                                                n_orth.append(e_f[0].text)

                                                            if e_f.attrib == {'name': 'base'}:
                                                                n_base.append(e_f[0].text)

                                                        if has_time: break

                                                        ann_named_index += 1

                                                        if has_subtype != True:
                                                            n_subtype.append("O")

                                                        if has_type != True:
                                                            n_type.append("O")

                                        ann_named_indexes_to.append(ann_named_index)
                    # ann_named_indexes_to.append(ann_named_index)

    print("dane zostały wczytane")
    print("ropoczęto przetwarzanie wstępne")

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
                w_msd[i].append("O")

    # for i in range(len(n_base))[:]:
    #     print(n_base[i] + " - " + n_type[i] + " - " + n_subtype[i])

    w_type = []
    w_subtype = []
    for file_index in range(len(ann_words_indexes_from)):
        w_od = ann_words_indexes_from[file_index]
        w_do = ann_words_indexes_to[file_index]
        n_od = ann_named_indexes_from[file_index]
        n_do = ann_named_indexes_to[file_index]
        for w in range(w_od, w_do):
            found = False
            n_buff = 0
            for n in range(n_od, n_do):
                if w_base[w] == n_base[n] and w_orth[w] == n_orth[n] and n_subtype[n] != "O":
                    n_buff = n
                    found = True
            if found:
                w_type.append(n_type[n_buff])
                w_subtype.append(n_subtype[n_buff])
            else:
                for n in range(n_od, n_do):
                    if w_base[w] == n_base[n] and w_orth[w] == n_orth[n]:
                        n_buff = n
                        found = True
                if found:
                    w_type.append(n_type[n_buff])
                    w_subtype.append("O")
                else:
                    w_type.append("O")
                    w_subtype.append("O")

    # for i in range(len(w_base))[:100]:
    #     print(w_orth[i] + " - " + w_type[i] + " - " + w_subtype[i])

    # for i in range(len(ann_named_indexes_from)):
    #     print(str(ann_words_indexes_from[i]) + " - " + str(ann_words_indexes_to[i]-1))

    number_of_sentences = len(ann_words_indexes_from)
    number_of_tokens = len(w_base)

    BOS = []
    EOS = []
    for i in range(number_of_tokens):
        buff = procent(i, number_of_tokens, buff)
        for j in range(number_of_sentences):
            if i == ann_words_indexes_from[j]:
                BOS.append(True)
                EOS.append(False)
                break
            elif i == ann_named_indexes_to[j]-1:
                BOS.append(False)
                EOS.append(True)
                break
            else:
                BOS.append(False)
                EOS.append(False)
                break

    print("zakończono przetwarzanie wstępne")
    return w_orth, w_base, w_tag, w_msd, w_type, w_subtype, BOS, EOS, number_of_tokens, number_of_sentences, ann_words_indexes_from, ann_words_indexes_to

# {'1)+1:w_tag': 'Fpa',
#  '2)+1:w_tag[:2]': 'Fp',
#  '3)+1:w_base.istitle()': False,
#  '4)+1:w_base.isupper()': False,
#  '5)+1:w_base.lower()': '(',
#  '6)-1:w_tag': 'Fpa',
#  '7)-1:w_tag[:2]': 'Fp',
#  '8)-1:w_base.istitle()': False,
#  '9)-1:w_base.isupper()': False,
#  '10)-1:w_base.lower()': '(',
#  '11)BOS': True,
#  '12)EOS': True,
#  '13)w_tag': 'NP',
#  '14)w_tag[:2]': 'NP',
#  '15)w_base.isdigit()': False,
#  '16)w_base.istitle()': True,
#  '17)w_base.isupper()': False,
#  '18)w_base.lower()': 'melbourne',
#  '19)w_orth.lower()': 'melbourne',
#  '20)w_base[-2:]': 'ne', # można spróbować polepszyć jakość uczenia dodając ficzery 20-23 także dla tokenów o indeksie +-1
#  '21)w_base[-3:]': 'rne'
#  '22)w_orth[-2:]': 'ne',
#  '23)w_orth[-3:]': 'rne'
#  '24)w_msd_1': cośtam
#  '24)w_msd_2': cośtam
#  '24)...
#  '24)w_msd_10': cośtam
#  '25)w_type':
#  '26)w_subtype':}

def feat1(w_tag, indeks):
    print_procent(1,len(w_tag),indeks)
    if(indeks+1<len(w_tag)): return w_tag[indeks+1]
    else: return "O"

def feat2(w_tag, indeks):
    print_procent(2, len(w_tag),indeks)
    if(indeks+1<len(w_tag)): return w_tag[indeks+1][0:2]
    else: return "O"

def feat3(w_base, indeks):
    print_procent(3, len(w_base),indeks)
    if(indeks+1<len(w_base)):
        return w_base[indeks+1].istitle()
    else: return "O"

def feat4(w_base, indeks):
    print_procent(4, len(w_base),indeks)
    if(indeks+1<len(w_base)):
        return w_base[indeks+1].isupper()
    else: return "O"

def feat5(w_base, w_tag, indeks):
    print_procent(5, len(w_base),indeks)
    if(indeks+1<len(w_base)):
        if w_tag[indeks + 1] == "Interp": return "O"
        else: return w_base[indeks+1].lower()
    else: return "O"

def feat6(w_tag, indeks):
    print_procent(6, len(w_tag),indeks)
    if(indeks-1>=0): return w_tag[indeks-1]
    else: return "O"

def feat7(w_tag, indeks):
    print_procent(7, len(w_tag),indeks)
    if(indeks-1>=0): return w_tag[indeks-1][0:2]
    else: return "O"

def feat8(w_base, indeks):
    print_procent(8, len(w_base),indeks)
    if(indeks-1>= 0):
        return w_base[indeks-1].istitle()
    else: return "O"

def feat9(w_base, indeks):
    print_procent(9, len(w_base),indeks)
    if(indeks-1>= 0):
        return w_base[indeks-1].isupper()
    else: return "O"

def feat10(w_base, w_tag, indeks):
    print_procent(10, len(w_base),indeks)
    if(indeks-1>= 0):
        if w_tag[indeks - 1] == "Interp": return "O"
        else: return w_base[indeks-1].lower()
    else: return "O"

def feat11(BOS, indeks):
    print_procent(11, len(BOS),indeks)
    return BOS[indeks]

def feat12(EOS, indeks):
    print_procent(12, len(EOS),indeks)
    return EOS[indeks]

def feat13(w_tag, indeks):
    print_procent(13, len(w_tag),indeks)
    return w_tag[indeks]

def feat14(w_tag, indeks):
    print_procent(14, len(w_tag),indeks)
    return w_tag[indeks][0:2]

def feat15(w_base, indeks):
    print_procent(15, len(w_base),indeks)
    return w_base[indeks].isdigit()

def feat16(w_base, indeks):
    print_procent(16, len(w_base),indeks)
    return w_base[indeks].istitle()

def feat17(w_base, indeks):
    print_procent(17, len(w_base),indeks)
    return w_base[indeks].isupper()

def feat18(w_base, w_tag, indeks):
    print_procent(18, len(w_base), indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    else: return w_base[indeks].lower()

def feat19(w_orth, w_base, w_tag, indeks):
    print_procent(19, len(w_orth),indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    return w_orth[indeks].lower()

def feat20(w_base, w_tag, indeks):
    print_procent(20, len(w_base),indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    return w_base[indeks][-2:]

def feat21(w_base, w_tag, indeks):
    print_procent(21, len(w_base),indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    return w_base[indeks][-3:]

def feat22(w_orth, w_base, w_tag, indeks):
    print_procent(22, len(w_orth),indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    return w_orth[indeks][-2:]

def feat23(w_orth, w_base, w_tag, indeks):
    print_procent(23, len(w_orth),indeks)
    if w_tag[indeks] == "Interp": return w_base[indeks]
    return w_orth[indeks][-3:]

def feat24(w_msd, indeks, zero_dziewiec):
    if zero_dziewiec == 0: print_procent(24, len(w_msd),indeks)
    if zero_dziewiec == 1: print_procent(25, len(w_msd),indeks)
    if zero_dziewiec == 2: print_procent(26, len(w_msd),indeks)
    if zero_dziewiec == 3: print_procent(27, len(w_msd),indeks)
    if zero_dziewiec == 4: print_procent(28, len(w_msd),indeks)
    if zero_dziewiec == 5: print_procent(29, len(w_msd),indeks)
    if zero_dziewiec == 6: print_procent(30, len(w_msd),indeks)
    if zero_dziewiec == 7: print_procent(31, len(w_msd),indeks)
    if zero_dziewiec == 8: print_procent(32, len(w_msd),indeks)
    if zero_dziewiec == 9: print_procent(33, len(w_msd),indeks)
    return w_msd[indeks][zero_dziewiec]

def feat25(w_type, indeks):
    print_procent(34, len(w_type),indeks)
    return w_type[indeks]

def feat26(w_subtype, indeks):
    print_procent(35, len(w_subtype),indeks)
    return w_subtype[indeks]

def prepare_dictionary(nkjp_dir, number_of_files):

    w_orth, w_base, w_tag, w_msd, w_type, w_subtype, BOS, EOS, number_of_tokens, number_of_sentences, od, do = load_xmls(nkjp_dir, number_of_files)

    print("inicjowanie przetwarzania danych...")
    features = []
    for sent_i in range(number_of_sentences):
        features.append(list())
        for indeks in range(od[sent_i], do[sent_i]):
            features[sent_i].append(dict())
            features[sent_i][indeks-od[sent_i]] = {
                '1)': feat1(w_tag, indeks),
                '2)': feat2(w_tag, indeks),
                '3)': feat3(w_base, indeks),
                '4)': feat4(w_base, indeks),
                '5)': feat5(w_base, w_tag, indeks),
                '6)': feat6(w_tag, indeks),
                '7)': feat7(w_tag, indeks),
                '8)': feat8(w_base, indeks),
                '9)': feat9(w_base, indeks),
                '10)': feat10(w_base, w_tag, indeks),
                '11)': feat11(BOS, indeks),
                '12)': feat12(EOS, indeks),
                '13)': feat13(w_tag, indeks),
                '14)': feat14(w_tag, indeks),
                '15)': feat15(w_base, indeks),
                '16)': feat16(w_base, indeks),
                '17)': feat17(w_base, indeks),
                '18)': feat18(w_base, w_tag, indeks),
                '19)': feat19(w_orth, w_base, w_tag, indeks),
                '20)': feat20(w_base, w_tag, indeks),
                '21)': feat21(w_base, w_tag, indeks),
                '22)': feat22(w_orth, w_base, w_tag, indeks),
                '23)': feat23(w_orth, w_base, w_tag, indeks),
                '24-0)': feat24(w_msd, indeks, 0),
                '24-1)': feat24(w_msd, indeks, 1),
                '24-2)': feat24(w_msd, indeks, 2),
                '24-3)': feat24(w_msd, indeks, 3),
                '24-4)': feat24(w_msd, indeks, 4),
                '24-5)': feat24(w_msd, indeks, 5),
                '24-6)': feat24(w_msd, indeks, 6),
                '24-7)': feat24(w_msd, indeks, 7),
                '24-8)': feat24(w_msd, indeks, 8),
                '24-9)': feat24(w_msd, indeks, 9),
                # '25)': feat25(w_type, indeks),
                # '26)': feat26(w_subtype, indeks)
            }
    predictions = []
    for sent_i in range(number_of_sentences):
        predictions.append(list())
        for indeks in range(od[sent_i], do[sent_i]):
            predictions[sent_i].append(w_subtype[indeks])

            # predictions[sent_i].append(w_type[indeks])
            # predictions[sent_i].append(w_subtype[indeks])

            # predictions[sent_i].append(dict())
            # predictions[sent_i][indeks - od[sent_i]] = {
            #     'Type': feat25(w_type, indeks),
            #     'Subtype': feat26(w_subtype, indeks)}
    print("przetwarzanie danych zostało zakończone")

    # for feature in features:
    #     for key, value in feature.items():
    #         print(key, value)
    #     print("")

    print("eksportowanie danych do pliku...")
    filepath = "./venv/Input_file/"
    filename = "input_data" + ".json"
    with open(os.path.join(filepath, filename), 'w') as temp_file:
        json.dump(features, temp_file)
    filepath = "./venv/Input_file/"
    filename = "predictions" + ".json"
    with open(os.path.join(filepath, filename), 'w') as temp_file:
        json.dump(predictions, temp_file)
    print("dane zostały eksportowane do pliku")


# nkjp_dir = "C:\\Users\Paweł\Documents\INL_korpus"
# nkjp_dir = "C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples"
# number_of_files = 1 # nie więcej niż 3889
# prepare_dictionary(nkjp_dir, number_of_files)