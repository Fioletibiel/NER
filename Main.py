import Train as load

# wpisujemy:
rootdir = "C:\\Users\Paweł\Documents\INL_korpus"
number_of_files = 100     # nie więcej niż 3889
number_of_mixes = 5      # dowolny int

load.source(rootdir, number_of_files, number_of_mixes)