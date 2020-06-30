from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk, Image
from tkinter.ttk import Combobox
from tkinter import filedialog

from data import *




class Gui(Tk):

    def __init__(self, localdata):
        super().__init__()

        self.__data = localdata

        self.__lbo = ""
        self.__ime = ""
        self.__prezime = ""
        self.__datumrodj = "%m-%d-%Y"

        self.__pacijent = ""
        self.__datum_i_vreme = " %m-%d-%Y %H:%M:%S "
        self.__izvestaj = ""
        self.__lekar = ""
        self.__tip = ""
        self.__snimak = ""


        self.geometry("640x480")

        self.__main_frame = Frame(self, relief=GROOVE, padx=10, pady=10)

        self.__patient_frame = Frame(self, height=480, width=640)
        self.__all_patients_frame = Frame(self.__patient_frame, borderwidth=2, relief="ridge")
        self.__patient_details_frame = Frame(self.__patient_frame, borderwidth=2)
        self.__patient_details_frame_container = Frame(self.__patient_details_frame, borderwidth=10)

        self.__recordings_frame = Frame(self, height=480, width=640)
        self.__all_recordings_frame = Frame(self.__recordings_frame, borderwidth=2, relief="ridge")
        self.__recordings_details_frame = Frame(self.__recordings_frame, borderwidth=2)
        self.__recordings_details_frame_container = Frame(self.__recordings_details_frame, borderwidth=10)

        self.__lbo_label = Label(self.__patient_details_frame_container)
        self.__ime_label = Label(self.__patient_details_frame_container)
        self.__prezime_label = Label(self.__patient_details_frame_container)
        self.__datumrodj_label = Label(self.__patient_details_frame_container)

        self.__pacijent_label = Label(self.__recordings_details_frame_container)
        self.__date_n_time_label = Label(self.__recordings_details_frame)
        self.__izvestaj_label = Label(self.__recordings_details_frame_container)
        self.__lekar_label = Label(self.__recordings_details_frame)
        self.__tip_label = Label(self.__recordings_details_frame_container)
        self.__snimak_label = Label(self.__recordings_details_frame_container)


        self.__listbox = Listbox(self.__all_patients_frame, activestyle="none")
        self.__search = Entry(self.__all_patients_frame)


        self.__main_frame.pack(fill=NONE, expand=TRUE)

        self.__logo = ImageTk.PhotoImage(Image.open("klinika.png"))

        self.podesiMeni(self.__main_frame)
        self.prikaziPocetnu(self.__main_frame)

        self.__main_frame.mainloop()

    def prikaziPocetnu(self, master):
        panel = Label(master, image=self.__logo)
        panel.pack()

    def prikaziPacijente(self):
        self.__main_frame.forget()

        self.__patient_frame.pack(fill=BOTH, expand=TRUE)
        self.__all_patients_frame.grid(sticky="nsew", row=0, column=0)
        self.__patient_details_frame.grid(sticky="nsew", row=0, column=1)

        # kopirano sa SO
        self.__patient_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.__patient_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.__patient_frame.grid_rowconfigure(0, weight=1)

        self.__patient_details_frame_container.pack(fill=NONE, expand=TRUE)

        Label(self.__patient_details_frame_container, text="LBO: ").grid(row=0, sticky=E)
        Label(self.__patient_details_frame_container, text="Ime: ").grid(row=1, sticky=E)
        Label(self.__patient_details_frame_container, text="Prezime: ").grid(row=2, sticky=E)
        Label(self.__patient_details_frame_container, text="Datum rodjenja: ").grid(row=3, sticky=E)

        self.__lbo_label.grid(row=0, column=1, sticky=W)
        self.__ime_label.grid(row=1, column=1, sticky=W)
        self.__prezime_label.grid(row=2, column=1, sticky=W)
        self.__datum_label.grid(row=3, column=1, sticky=W)

        Label(self.__all_patients_frame, text="Pretraga").pack()
        self.__search.pack(fill=X)
        self.__search.bind("<Key>", self.keyPressed)

        self.__listbox.bind("<<ListboxSelect>>", self.listboxSelect)
        self.listboxInsertData(self.__data, self.__listbox)

        self.__listbox.pack(fill=BOTH, expand=TRUE)

    def keyPressed(self, event=None):
        upisano = self.__search.get().lower()

        if upisano == "":
            self.listboxInsertData(patientData, self.__listbox)
            return

        bazaImena = {}
        for pacijent in patientData:
            bazaImena[pacijent.ime.lower() + pacijent.prezime.lower()] = pacijent

        returnValues = []
        for imeprezime in bazaImena.keys():
            if upisano in imeprezime:
                returnValues.append(bazaImena.get(imeprezime))

        self.listboxInsertData(returnValues, self.__listbox)

    def listboxSelect(self, event=None):
        if not self.__listbox.curselection():
            self.ocistiLabele()
            return

        indeks = self.__listbox.curselection()[0]
        pacijent = self.__data[indeks]
        self.popuniLabele(pacijent)

    def listboxInsertData(self, pacijenti, listbox):
        listbox.delete(0, END)
        for pacijent in pacijenti:
            listbox.insert(END, pacijent.ime + " " + pacijent.prezime)

        self.ocistiLabele()

    def ocistiLabele(self):
        self.__lbo_label["text"] = ""
        self.__ime_label["text"] = ""
        self.__prezime_label["text"] = ""
        self.__datum_label["text"] = ""

    def popuniLabele(self, pacijent):
        self.__lbo_label["text"] = pacijent.LBO
        self.__ime_label["text"] = pacijent.ime
        self.__prezime_label["text"] = pacijent.prezime
        self.__datum_label["text"] = pacijent.datumrodj

    def prikaziSnimke(self):
        self.__main_frame.forget()

        self.__recordings_frame.pack(fill=BOTH, expand=TRUE)
        self.__all_recordings_frame.grid(sticky="nsew", row=0, column=0)
        self.__recordings_details_frame_container.grid(sticky="nsew", row=0, column=1)

        # kopirano sa SO nije mi bas jasno zasto ali samo je tako je uspelo da radi :)
        self.__recordings_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.__recordings_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.__recordings_frame.grid_rowconfigure(0, weight=1)

        self.__recordings_details_frame_container.pack(fill=NONE, expand=TRUE)

        Label(self.__recordings_details_frame_container, text="Pacijent: ").grid(row=0, sticky=E)
        Label(self.__recordings_details_frame_container, text="Datum i vrene: ").grid(row=1, sticky=E)
        Label(self.__recordings_details_frame_container, text="Ime lekara: ").grid(row=2, sticky=E)
        Label(self.__recordings_details_frame_container, text="Tip: ").grid(row=3, sticky=E)

        self.__pacijent_label.grid(row=0, column=1, sticky=W)
        self.__datum_i_vreme_label.grid(row=1, column=1, sticky=W)
        self.__lekar_label.grid(row=2, column=1, sticky=W)
        self.__tip_label.grid(row=3, column=1, sticky=W)





    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Upozorenje", "Da li ste sigurni da želite da napustite aplikaciju?",
                                         icon="warning")
        if odgovor:
            self.destroy()

    def podesiMeni(self, master):
        menu = Menu(self)
        self.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="Pacijenti", menu=subMenu)
        subMenu.add_command(label="Prikaz pacijenata", command=self.prikaziPacijente)
        subMenu.add_command(label="Dodavanje pacijenata", command=lambda: self.NewPatientWindow(master))
        subMenu.add_command(label="Izmena pacijenata")

        snimakMenu = Menu()
        menu.add_cascade(label="Snimanja", menu=snimakMenu)
        snimakMenu.add_command(label="Lista snimanja", command=self.prikaziSnimke)
        snimakMenu.add_command(label="Dodavanje snimanja")
        snimakMenu.add_command(label="Izmena ili brisanje snimanja")

        izlazMenu = Menu()
        menu.add_cascade(label="Izlaz", menu=izlazMenu)
        izlazMenu.add_command(label="Izlaz", command=self.komanda_izlaz)

    class NewPatientWindow:
        def __init__(self, master):
            window = Toplevel(master)

            window.title("Dodaj pacijenta")
            window.geometry("240x120")

            Label(window, text="LBO: ").grid(row=0, sticky=E)
            Label(window, text="Ime: ").grid(row=1, sticky=E)
            Label(window, text="Prezime: ").grid(row=2, sticky=E)
            Label(window, text="Datum rodjenja: ").grid(row=3, sticky=E)

            self.__lbo_entry = Entry(window)
            self.__ime_entry = Entry(window)
            self.__prezime_entry = Entry(window)
            self.__datum_entry = Entry(window)

            btn = Button(window, text="Dodaj", command=self.saveNewPatient)
            btn.grid(row=4, columnspan=2)

            self.__lbo_entry.grid(row=0, column=1, sticky=W)
            self.__ime_entry.grid(row=1, column=1, sticky=W)
            self.__prezime_entry.grid(row=2, column=1, sticky=W)
            self.__datum_entry.grid(row=3, column=1, sticky=W)


        def saveNewPatient(self):
            noviPacijent = Pacijent(self.__lbo_entry.get(), self.__ime_entry.get(), self.__prezime_entry.get(),
                                    self.__datum_entry.get())
            data.sacuvajPacijenta(noviPacijent)



if __name__ == '__main__':
    data = Data()
    patientData = data.ucitaj()

    gui = Gui(patientData)
