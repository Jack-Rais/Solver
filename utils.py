import pickle
import os


def get_file():

    files = [file for file in os.listdir() if file.startswith("graph_saved")]

    if len(files) == 0:
        print("Non ci sono grafi salvati impossibile caricare")
        os.abort()

    
    print("-" * 40)
    for n, file in enumerate(files):

        print(f"{n}] -- {file}")


    inp = int(input("Inserire il numero corrispondente al file che si vuole caricare: "))
    with open(files[inp], 'rb') as file:
        out = pickle.load(file)
    
    return out