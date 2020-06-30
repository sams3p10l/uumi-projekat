import pickle


class Pacijent:
    @property
    def LBO(self):
        return self.__LBO

    @LBO.setter
    def LBO(self, LBO):
        self.__LBO = LBO

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, ime):
        self.__ime = ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, prezime):
        self.__prezime = prezime

    @property
    def datumrodj(self):
        return self.__datumrodj

    @datumrodj.setter
    def datumrodj(self, datumrodj):
        self.__datumrodj = datumrodj

    def __init__(self, LBO, ime, prezime, datumrodj):
        self.__LBO = LBO
        self.__ime = ime
        self.__prezime = prezime
        self.__datumrodj = datumrodj

    def __str__(self):
        format_linije = "{:>14}: {}"
        return "\n".join([
            "",
            format_linije.format("LBO", self.__LBO),
            format_linije.format("Ime", self.__ime),
            format_linije.format("Prezime", self.__prezime),
            format_linije.format("Datum rođenja", self.__datumrodj)]
        )

    @classmethod
    def prikazi_pacijente(cls, pacijenti):
        format_linije = "{:5} {:20} {:9} {:10}"

        print()
        # zaglavlje
        print(format_linije.format("LBO", "Ime", "Prezime", "Datum rodjenja"))
        print(format_linije.format("-" * 5, "-" * 20, "-" * 9, "-" * 10))
        # podaci
        for pacijent in pacijenti:
            print(format_linije.format(
                pacijent.__LBO,
                pacijent.__ime,
                pacijent.__prezime,
                pacijent.__datumrodj
            ))


class Snimanje:
    @property
    def datum_i_vreme(self):
        return self.__datum_i_vreme

    @datum_i_vreme.setter
    def datum_i_vreme(self, datum_i_vreme):
        self.__datum_i_vreme = datum_i_vreme

    @property
    def izvestaj(self):
        return self.__izvestaj

    @izvestaj.setter
    def izvestaj(self, izvestaj):
        self.__izvestaj = izvestaj

    @property
    def lekar(self):
        return self.__lekar

    @lekar.setter
    def lekar(self, lekar):
        self.__lekar = lekar

    @property
    def snimak(self):
        return self.__snimak

    @snimak.setter
    def snimak(self, snimak):
        self.__snimak = snimak

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, tip):
        self.__tip = tip


    def __init__(self, pacijent, datum_i_vreme, izvestaj, lekar, snimak, tip):
        self.__pacijent = pacijent
        self.__datum_i_vreme = datum_i_vreme
        self.__izvestaj = izvestaj
        self.__lekar = lekar
        self.__snimak = snimak
        self.__tip = tip

    def __str__(self):
        format_linije = "{:>14}: {}"
        return "\n".join([
            "",
            format_linije.format("Pacijent", self.__pacijent.LBO, self.__pacijent.ime, self.__pacijent.prezime, self.__pacijent.datumrodj),
            format_linije.format("Datum i vreme", self.__datum_i_vreme),
            format_linije.format("Izvestaj", self.__izvestaj),
            format_linije.format("Lekar", self.__lekar),
            format_linije.format("Snimak", self.__snimak),
        ]
        )


class Data:
    __patientDataStorage = "patient_data_storage"

    def __init__(self):
        self.__pacijenti = []
        self.__snimci = []

    def createMockPatients(self):
        pacijent1 = Pacijent("111", "Petar", "Petrovic", "31839198")
        pacijent2 = Pacijent("112", "Petra", "Jovanovic", "31839414")
        pacijent3 = Pacijent("113", "Milos", "Markovic", "31525198")
        pacijent4 = Pacijent("114", "Zoran", "Petrovic", "82828282")

        self.__pacijenti.append(pacijent1)
        self.__pacijenti.append(pacijent2)
        self.__pacijenti.append(pacijent3)
        self.__pacijenti.append(pacijent4)

    @property
    def getPacijenti(self):
        return self.__pacijenti

    @classmethod
    def sacuvaj(cls, podaci):
        file = open(cls.__patientDataStorage, "wb")
        pickle.dump(podaci, file)
        file.close()

    def ucitaj(self):
        try:
            file = open(self.__patientDataStorage, "rb")
            podaci = pickle.load(file)
            file.close()
        except FileNotFoundError:
            self.createMockPatients()

        return podaci

    @classmethod
    def sacuvajPacijenta(cls, pacijent):
        file = open(cls.__patientDataStorage, "r+b")
        podaci = pickle.load(file)
        file.close()

        podaci.append(pacijent)

        file = open(cls.__patientDataStorage, "wb")
        pickle.dump(podaci, file)
        file.close()

    def ocistiPacijente(self):
        file = open(self.__patientDataStorage, "wb")
        pickle.dump(None, file)
        file.close()
