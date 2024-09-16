import os 
import pickle


with open(os.path.join("", "src", "baseDatos","guias"), 'rb') as f:
    destinos = pickle.load(f)
    for i in destinos:
        print(i._nombre)