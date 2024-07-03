import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the modello, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAlbum = None

    def handleCreaGrafo(self, e):
        try:
            durata = float(self._view._txtInDurata.value)
        except ValueError:
            self._view.create_alert("Inserire un valore numerico!")
            return
        self._model.buildGraph(durata)
        nodes = self._model.getNodes()
        nodes.sort(key=lambda x: x.Title)
        listDD = map(lambda x: ft.dropdown.Option(data=x,
                                                  text=x.Title,
                                                  on_click=self.getSelectedAlbum),
                     nodes)

        self._view._ddAlbum.options = listDD
        numNodi, numArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numNodi} nodi e {numArchi} archi."))
        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data
        print(self._choiceAlbum)

    def handleAnalisiComp(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceAlbum is None:
            self._view.create_alert("Selezionare un album prima!")
            return
        lunghezzaCC, totDurata = self._model.getConnessaDetails(self._choiceAlbum)
        self._view.txt_result.controls.append(ft.Text(f"La lunghezza della componente connessa"
                                                      f" che include {self._choiceAlbum} è {lunghezzaCC}"))
        self._view.txt_result.controls.append(ft.Text(f"La durata complessiva di tutti gli album connessi"
                                                      f" è {totDurata:.2f} minuti"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        a1 = self._choiceAlbum
        try:
            dTot = int(self._view._txtInSoglia.value)
        except ValueError:
            self._view.create_alert("Inserisci un valore intero!!")
            return

        if self._choiceAlbum is None:
            self._view.create_alert("Attenzione, album non selezionato!")
            return

        self._view.txt_result.controls.clear()
        setAlbum = self._model.getSetAlbum(a1, dTot)
        self._view.txt_result.controls.append(ft.Text(f"Set di album ottimo trovato di lunghezza {len(setAlbum)}"))
        for album in setAlbum:
            self._view.txt_result.controls.append(ft.Text(f"{album}"))

        self._view.update_page()



