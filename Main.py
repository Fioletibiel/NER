import NKJP as nkjp
import Train as load

wczytywanie_danych = False
if wczytywanie_danych:
    # nkjp_dir = "C:\\Users\p.kaminski4\Desktop\INL_korpus_10_samples"
    nkjp_dir = "C:\\Users\Paweł\Documents\INL_korpus"
    number_of_files = 5 # nie więcej niż 3889
    nkjp.prepare_dictionary(nkjp_dir, number_of_files)


# uczenie = True
# if uczenie:
#     load.train()
#
#
#
# sprawdzenie = False
# if uczenie:
#     load.check()