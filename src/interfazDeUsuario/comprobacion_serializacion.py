import os 
import pickle
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
with open(os.path.join("src", "baseDatos","guias"), 'rb') as f:
    destinos = pickle.load(f)
    for i in destinos:
        print(i._nombre)