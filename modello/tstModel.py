from time import time

from modello.model import Model

myModel = Model()
start_time = time()
myModel.buildGraph(120)
numNodi, numArchi = myModel.getGraphDetails()
setAlbum = myModel.getSetAlbum(myModel.getNodeI(261), 2000)
end_time = time()
print(f"Elapsed time: {end_time - start_time} seconds")
print(f"Numero nodi: {numNodi}")
print(f"Numero archi: {numArchi}")
print(f"Lunghezza setAlbum: {len(setAlbum)}")
for album in setAlbum:
    print(f"{album}")

