import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapAlbum = {}
        self._bestSet = None
        self._bestScore = 0

    def buildGraph(self, durata):
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAlbumNodes(durata))
        self._idMapAlbum = {a.AlbumId: a for a in list(self._grafo.nodes)}

        self._grafo.add_edges_from(DAO.getAllEdges(self._idMapAlbum))

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        return list(self._grafo.nodes)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._grafo, v0)
        totDurata = 0
        for album in conn:
            totDurata += album.durataAlbum
        return len(conn), totDurata

    def getSetAlbum(self, a1, dTot):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale = {a1}
        connessa.remove(a1)

        self._ricorsione(parziale, connessa, dTot)

        return self._bestSet

    def _ricorsione(self, parziale, connessa, dTot):
        # Verificare se parziale è una soluzione ammissibile
        if self.durataComplessiva(parziale) > dTot:
            return

        # Verificare se parziale è migliore del best
        if self.getScore(parziale) > self._bestScore:
            self._bestScore = self.getScore(parziale)
            self._bestSet = copy.deepcopy(self._bestSet)

        # Ciclo su nodi aggiungibili -- ricorsione
        for album in connessa:
            if album not in parziale:
                parziale.add(album)
                self._ricorsione(parziale, connessa, dTot)
                parziale.remove(album)

    def getNodeI(self, i):
        return self._idMapAlbum[i]

    @staticmethod
    def durataComplessiva(listOfAlbums):
        somma = 0
        for album in listOfAlbums:
            somma += album.durataAlbum
        return somma

    @staticmethod
    def getScore(listOfAlbums):
        return len(listOfAlbums)
