from operator import attrgetter
#riprovo a fare push

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (f"{self.codice} - {self.tipo} {self.marca} "
                f"(anno {self.anno_acquisto}, {self.valore:.2f} euro)")


class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return (f"{self.codice} - strumento {self.id_strumento} "
                f"a {self.cognome_allievo} il {self.data}")

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = {}
        self.contatore_prestiti = 0

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()
                if riga == "":
                    continue
                campi = riga.split(",")
                codice = campi[0]
                if self._cerca_strumento(codice) is None:
                    self.strumenti.append(
                        Strumento(codice, campi[1], campi[2], int(campi[3]), float(campi[4])))

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        ultimo = 0
        for s in self.strumenti:
            numero = int(s.codice[1:])
            if numero > ultimo:
                ultimo = numero
        nuovo = Strumento(f"S{ultimo + 1}", tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo)
        return nuovo

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if self._cerca_strumento(id_strumento) is None:
            raise Exception("Strumento non presente nel sistema")
        for p in self.prestiti.values():
            if p.id_strumento == id_strumento:
                raise Exception("Strumento già in prestito")
        self.contatore_prestiti += 1
        codice = f"P{self.contatore_prestiti}"
        prestito = Prestito(codice, data, id_strumento, cognome_allievo)
        self.prestiti[codice] = prestito
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception("Prestito non esistente")
        del self.prestiti[id_prestito]
