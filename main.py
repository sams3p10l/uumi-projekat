from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image
from data import *

from datetime import datetime
import pydicom
import snimanjaDICOM
import os

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
        self.__datum_label = Label(self.__patient_details_frame_container)

        self.__pacijent_label = Label(self.__recordings_details_frame_container)
        self.__date_n_time_label = Label(self.__recordings_details_frame)
        self.__izvestaj_label = Label(self.__recordings_details_frame_container)
        self.__lekar_label = Label(self.__recordings_details_frame)
        self.__tip_label = Label(self.__recordings_details_frame_container)
        self.__snimak_label = Label(self.__recordings_details_frame_container)

        self.__listbox = Listbox(self.__all_patients_frame, activestyle="none")
        self.__search = Entry(self.__all_patients_frame)

        self.__rec_listbox = Listbox(self.__all_recordings_frame, activestyle="none")
        self.__rec_search = Entry(self.__all_recordings_frame)

        self.__main_frame.pack(fill=NONE, expand=TRUE)

        self.__logo = ImageTk.PhotoImage(Image.open("klinika.png"))

        self.__chosenType = StringVar()
        self.__chosenPatient = StringVar()

        self.__allDicoms = []
        self.__snimci = []

        self.podesiMeni(self.__main_frame)
        self.prikaziPocetnu(self.__main_frame)

        self.__main_frame.mainloop()

    def pokreniEditProzor(self):
        try:
            index = self.__listbox.curselection()[0]
        except IndexError:
            return

        pacijent = self.__data[index]
        self.ChangePatient(self.__main_frame, pacijent)

    def prikaziPocetnu(self, master):
        panel = Label(master, image=self.__logo)
        panel.pack()

    def prikaziPacijente(self):
        self.__main_frame.forget()
        self.__recordings_frame.forget()

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

    def recordingsListboxSelect(self, event=None):
        pass

    def recFilterPatientSelected(self, event=None):
        pass

    def recFilterTypeSelected(self, event=None):
        pass

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

    def prikaziSnimak(self):
        try:
            index = self.__rec_listbox.curselection()[0]
        except IndexError:
            return

        dicomWindow = snimanjaDICOM.DICOMSnimci(self.__allDicoms[index], self.__snimci[index], "open")

    def dodajNoviSnimak(self):
        dicomWindow = snimanjaDICOM.DICOMSnimci(None, None, "add")

    def izmeniSnimak(self):
        try:
            index = self.__rec_listbox.curselection()[0]
        except IndexError:
            return

        dicomWindow = snimanjaDICOM.DICOMSnimci(self.__allDicoms[index], self.__snimci[index], "edit")

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Upozorenje", "Da li ste sigurni da želite da napustite aplikaciju?",
                                         icon="warning")
        if odgovor:
            self.destroy()

    def obrisiPacijenta(self):
        try:
            index = self.__listbox.curselection()[0]
        except IndexError:
            return

        pacijent = self.__data[index]
        data.obrisiPacijenta(pacijent)

    def podesiMeni(self, master):
        menu = Menu(self)
        self.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="Pacijenti", menu=subMenu)
        subMenu.add_command(label="Prikaz pacijenata", command=self.prikaziPacijente)
        subMenu.add_command(label="Dodavanje pacijenata", command=lambda: self.NewPatientWindow(master, self.__data))
        subMenu.add_command(label="Izmena pacijenta", command=self.pokreniEditProzor)
        subMenu.add_command(label="Obrisi pacijenta", command=self.obrisiPacijenta)

        snimakMenu = Menu()
        menu.add_cascade(label="Snimanja", menu=snimakMenu)
        snimakMenu.add_command(label="Lista snimanja", command=self.otvoriListuSnimanja)
        snimakMenu.add_command(label="Otvori snimanje", command=self.prikaziSnimak)
        snimakMenu.add_command(label="Dodavanje snimanja", command=self.dodajNoviSnimak)
        snimakMenu.add_command(label="Izmena ili brisanje snimanja", command=self.izmeniSnimak)

        izlazMenu = Menu()
        menu.add_cascade(label="Izlaz", menu=izlazMenu)
        izlazMenu.add_command(label="Izlaz", command=self.komanda_izlaz)

    def otvoriListuSnimanja(self):
        self.__main_frame.forget()
        self.__patient_frame.forget()

        self.__recordings_frame.pack(fill=BOTH, expand=TRUE)
        self.__all_recordings_frame.grid(sticky="nsew", row=0, column=0)
        self.__recordings_details_frame.grid(sticky="nsew", row=0, column=1)

        # kopirano sa SO
        self.__recordings_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.__recordings_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.__recordings_frame.grid_rowconfigure(0, weight=1)

        self.__recordings_details_frame_container.pack(fill=NONE, expand=TRUE)

        comboData = ["Svi pacijenti"]

        for entry in self.__data:
            comboData.append(entry.ime + " " + entry.prezime)

        Label(self.__recordings_details_frame_container, text="Izaberi pacijenta", pady=10).pack()

        recCombobox = ttk.Combobox(self.__recordings_details_frame_container, values=comboData, textvariable=self.__chosenPatient)
        recCombobox.bind("<<ComboboxSelected>>", self.recFilterPatientSelected)
        recCombobox.current(0)
        recCombobox.pack()

        comboTypes = ["Svi tipovi", "Magnetic Resonance(MR)", "Computed Topograph(CT)", "Ultrasound(US)", "Panoramic X-Ray(PX)"]
        Label(self.__recordings_details_frame_container, text="Izaberi tip snimka", pady=10).pack()

        recTypeCombobox = ttk.Combobox(self.__recordings_details_frame_container, values=comboTypes, textvariable=self.__chosenType)
        recCombobox.bind("<<ComboboxSelected>>", self.recFilterTypeSelected)
        recTypeCombobox.current(0)
        recTypeCombobox.pack()

        self.__rec_listbox.bind("<<ListboxSelect>>", self.recordingsListboxSelect)
        self.snimciListboxInsertData()

        self.__rec_listbox.pack(fill=BOTH, expand=TRUE)

    def snimciListboxInsertData(self):
        self.__snimci = os.listdir("DICOM samples")

        self.__rec_listbox.delete(0, END)
        for snimak in self.__snimci:
            read_dicom = pydicom.dcmread("DICOM samples/" + snimak, force=True)
            self.__allDicoms.append(read_dicom)

            ret_string = str(snimak)
            if "StudyDate" in read_dicom:
                ret_string = ret_string + " - " + read_dicom.StudyDate

            if "StudyTime" in read_dicom:
                ret_string = ret_string + " - " + read_dicom.StudyTime

            self.__rec_listbox.insert(END, ret_string)

    class NewPatientWindow:
        def __init__(self, master, allPatients):
            self.window = Toplevel(master)

            self.parent = master
            self.allPatients = allPatients

            self.window.title("Dodaj pacijenta")
            self.window.geometry("240x120")

            Label(self.window, text="LBO: ").grid(row=0, sticky=E)
            Label(self.window, text="Ime: ").grid(row=1, sticky=E)
            Label(self.window, text="Prezime: ").grid(row=2, sticky=E)
            Label(self.window, text="Datum rodjenja: ").grid(row=3, sticky=E)

            self.__lbo_entry = Entry(self.window)
            self.__ime_entry = Entry(self.window)
            self.__prezime_entry = Entry(self.window)
            self.__datum_entry = Entry(self.window)

            btn = Button(self.window, text="Dodaj", command=self.saveNewPatient)
            btn.grid(row=4, columnspan=2)

            self.__lbo_entry.grid(row=0, column=1, sticky=W)
            self.__ime_entry.grid(row=1, column=1, sticky=W)
            self.__prezime_entry.grid(row=2, column=1, sticky=W)
            self.__datum_entry.grid(row=3, column=1, sticky=W)

            self.fillDate()

        def saveNewPatient(self):
            currentLbo = self.__lbo_entry.get()
            currentIme = self.__ime_entry.get()
            currentPrezime = self.__prezime_entry.get()
            currentDatum = self.__datum_entry.get()

            if len(currentLbo) != 11 or currentLbo.isdigit() is False:
                messagebox.showinfo("Greska", "Lose unet LBO (treba da ima 11 karaktera)")
                return
            if len(currentIme) < 3:
                messagebox.showinfo("Greska", "Neispravno uneto ime")
                return
            if len(currentPrezime) < 3:
                messagebox.showinfo("Greska", "Neispravno uneto prezime")
                return
            if currentDatum == "":
                messagebox.showinfo("Greska", "unesi datum")
                return

            for iterator in self.allPatients:
                if iterator.LBO == currentLbo:
                    messagebox.showinfo("Greska", "Korisnik sa ovim LBO vec postoji!")
                    return

            noviPacijent = Pacijent(currentLbo, currentIme, currentPrezime, currentDatum)
            data.sacuvajPacijenta(noviPacijent)
            # newData = data.ucitaj()
            # self.parent.listboxInsertData(newData, self.parent.__listbox)
            self.window.destroy()

        def fillDate(self):
            self.__datum_entry.delete(0, END)
            self.__datum_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    class ChangePatient:
        def __init__(self, master, pacijent):
            self.window = Toplevel(master)

            self.parent = master
            self.patient = pacijent

            self.window.title("Izmeni pacijenta")
            self.window.geometry("240x120")

            Label(self.window, text="LBO: ").grid(row=0, sticky=E)
            Label(self.window, text="Ime: ").grid(row=1, sticky=E)
            Label(self.window, text="Prezime: ").grid(row=2, sticky=E)
            Label(self.window, text="Datum rodjenja: ").grid(row=3, sticky=E)

            self.__lbo_entry = Entry(self.window)
            self.__ime_entry = Entry(self.window)
            self.__prezime_entry = Entry(self.window)
            self.__datum_entry = Entry(self.window)

            btn = Button(self.window, text="Izmeni", command=self.editNewPatient)
            btn.grid(row=4, columnspan=2)

            self.__lbo_entry.grid(row=0, column=1, sticky=W)
            self.__ime_entry.grid(row=1, column=1, sticky=W)
            self.__prezime_entry.grid(row=2, column=1, sticky=W)
            self.__datum_entry.grid(row=3, column=1, sticky=W)

            self.fillPatient()

        def editNewPatient(self):
            currentLbo = self.__lbo_entry.get()
            currentIme = self.__ime_entry.get()
            currentPrezime = self.__prezime_entry.get()
            currentDatum = self.__datum_entry.get()

            if len(currentLbo) != 11 or currentLbo.isdigit() is False:
                messagebox.showinfo("Greska", "Lose unet LBO (treba da ima 11 karaktera)")
                return
            if len(currentIme) < 3:
                messagebox.showinfo("Greska", "Neispravno uneto ime")
                return
            if len(currentPrezime) < 3:
                messagebox.showinfo("Greska", "Neispravno uneto prezime")
                return
            if currentDatum == "":
                messagebox.showinfo("Greska", "unesi datum")
                return
            data.obrisiPacijenta(self.patient)

            noviPacijent = Pacijent(currentLbo, currentIme, currentPrezime, currentDatum)
            data.sacuvajPacijenta(noviPacijent)
            # newData = data.ucitaj()
            # self.parent.listboxInsertData(newData, self.parent.__listbox)
            self.window.destroy()

        def fillPatient(self):
            self.__lbo_entry.delete(0, END)
            self.__lbo_entry.insert(0, self.patient.LBO)
            self.__ime_entry.delete(0, END)
            self.__ime_entry.insert(0, self.patient.ime)
            self.__prezime_entry.delete(0, END)
            self.__prezime_entry.insert(0, self.patient.prezime)
            self.__datum_entry.delete(0, END)
            self.__datum_entry.insert(0, self.patient.datumrodj)

            self.__lbo_entry["state"] = DISABLED


if __name__ == '__main__':
    data = Data()
    patientData = data.ucitaj()

    gui = Gui(patientData)
