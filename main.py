from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image

from models import FakeData

class Gui(Tk):

    def __init__(self, data):
        super().__init__()

        self.__lbo = ""
        self.__ime = ""
        self.__prezime = ""
        self.__datumrodj = ""

        self.__data = data

        self.geometry("640x480")

        main_frame = Frame(self, relief=GROOVE, padx=10, pady=10)
        main_frame.pack(fill=NONE, expand=TRUE)

        self.__logo = ImageTk.PhotoImage(Image.open("klinika.png"))

        self.podesiMeni(main_frame)
        self.prikaziPocetnu(main_frame)

        main_frame.mainloop()

    def prikaziPocetnu(self, master):
        panel = Label(master, image=self.__logo)
        panel.pack()

    def prikaziPacijente(self, master: Frame):
        master.forget()

        patient_frame = Frame(self, height=480, width=640)
        patient_frame.pack(fill=BOTH, expand=TRUE)

        all_patients_frame = Frame(patient_frame, borderwidth=2, relief="ridge")
        patient_details_frame = Frame(patient_frame, borderwidth=2)

        all_patients_frame.grid(sticky="nsew", row=0, column=0)
        patient_details_frame.grid(sticky="nsew", row=0, column=1)

        # kopirano sa SO
        patient_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        patient_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        patient_frame.grid_rowconfigure(0, weight=1)

        patient_details_frame_container = Frame(patient_details_frame, borderwidth=10)
        patient_details_frame_container.pack(fill=NONE, expand=TRUE)

        Label(patient_details_frame_container, text="LBO: ").grid(row=0, sticky=E)
        Label(patient_details_frame_container, text="Ime: ").grid(row=1, sticky=E)
        Label(patient_details_frame_container, text="Prezime: ").grid(row=2, sticky=E)
        Label(patient_details_frame_container, text="Datum rodjenja: ").grid(row=3, sticky=E)

        self.__lbo_label = Label(patient_details_frame_container).grid(row=0, sticky=E)
        self.__ime_label = Label(patient_details_frame_container).grid(row=1, sticky=E)
        self.__prezime_label = Label(patient_details_frame_container).grid(row=2, sticky=E)
        self.__datum_label = Label(patient_details_frame_container).grid(row=3, sticky=E)

        self.__listbox = Listbox(all_patients_frame, activestyle="none")
        self.__listbox.bind("<<ListboxSelect>>", self.listboxSelect)
        self.listboxInsertData(self.__data)

        self.__listbox.pack(fill=BOTH, expand=TRUE)


    def listboxSelect(self, event=None):
        if not self.__listbox.curselection():
            self.ocistiLabele()
            return

        indeks = self.__listbox.curselection()[0]
        pacijent = self.__data[indeks]
        self.popuniLabele(pacijent)

    def listboxInsertData(self, pacijenti):
        self.__listbox.delete(0, END)
        for pacijent in pacijenti:
            self.__listbox.insert(END, pacijent.ime + " " + pacijent.prezime)

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
        subMenu.add_command(label="Prikaz pacijenata", command=lambda: self.prikaziPacijente(master))
        subMenu.add_command(label="Dodavanje pacijenata")
        subMenu.add_command(label="Izmena pacijenata")

        snimakMenu = Menu()
        menu.add_cascade(label="Snimanja", menu=snimakMenu)
        snimakMenu.add_command(label="Lista snimanja")
        snimakMenu.add_command(label="Dodavanje snimanja")
        snimakMenu.add_command(label="Izmena ili brisanje snimanja")

        izlazMenu = Menu()
        menu.add_cascade(label="Izlaz", menu=izlazMenu)
        izlazMenu.add_command(label="Izlaz", command=self.komanda_izlaz)


if __name__ == '__main__':
    fakeData = FakeData()
    patientData = fakeData.getPacijenti

    gui = Gui(patientData)
