from PIL import Image as imagepil
from PIL import ImageTk

import pydicom_PIL
from pydicom_PIL import show_PIL
import pydicom

import numpy

from datetime import datetime

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox


class DICOMSnimci(Toplevel):


    def postavi_datumrodj_frame_a(self, stanje):
        self.__datumrodj_entry["state"] = stanje

    def postavi_datumsnimka_frame_a(self, stanje):
        self.__datumsnimka_entry["state"] = stanje

    def postavi_ime_lekara_frame_a(self, stanje):
        self.__ime_lekara_entry["state"] = stanje

    def izvestaj_frame_a(self, stanje):
        self.__izvestaj_entry["state"] = stanje

    def komanda_pacijent_postoji(self):
        stanje = NORMAL if self.__pacijent_postoji.get() else DISABLED
        self.__pacijent_entry["state"] = stanje

    def komanda_tip_postoji(self):
        stanje = "readonly" if self.__tip_postoji.get() else DISABLED
        self.__tip_combobox["state"] = stanje

    def komanda_datumrodj_postoji(self):
        stanje = NORMAL if self.__datumrodj_postoji.get() else DISABLED
        self.postavi_datumrodj_frame_a(stanje)

    def komanda_datumsnimka_postoji(self):
        stanje = NORMAL if self.__datumsnimka_postoji.get() else DISABLED
        self.postavi_datumsnimka_frame_a(stanje)

    def komanda_ime_lekara_postoji(self):
        stanje = NORMAL if self.__ime_lekara_postoji.get() else DISABLED
        self.postavi_ime_lekara_frame_a(stanje)

    def komanda_izvestaj_postoji(self):
        stanje = NORMAL if self.__izvestaj_postoji.get() else DISABLED
        self.izvestaj_frame_a(stanje)

    def azuriraj_stanja(self):
        self.komanda_pacijent_postoji()
        self.komanda_tip_postoji()
        self.komanda_datumrodj_postoji()
        self.komanda_datumsnimka_postoji()
        self.komanda_ime_lekara_postoji()
        self.komanda_izvestaj_postoji()

    def komanda_otvori_i_edituj(self):
        try:
            self["cursor"] = "wait"
            self.update()

            self.__dataset = self.__read_dicom  # otvaranje DICOM datoteke; force parametar obezbeđuje čitanje nepotpunih datoteka
            print(self.__dataset)

            # omogućavanje interfejsa za izmenu i čuvanje
            self.__pacijent_postoji_checkbutton["state"] = NORMAL
            self.__tip_postoji_checkbutton["state"] = NORMAL
            self.__datumrodj_postoji_checkbutton["state"] = NORMAL
            self.__datumsnimka_postoji_checkbutton["state"] = NORMAL
            self.__ime_lekara_postoji_checkbutton["state"] = NORMAL
            self.__izvestaj_postoji_checkbutton["state"] = NORMAL

            self.__ocisti_button["state"] = NORMAL
            self.__sacuvaj_button["state"] = NORMAL
            self.__datoteka_meni.entryconfig(0, state=NORMAL)
            self.__datoteka_meni.entryconfig(1, state=NORMAL)

            try:
                if self.__dataset["PatientName"]:
                    self.__pacijent.set(self.__dataset.PatientName)
                    self.__pacijent_postoji.set(True)
                else:
                    self.__pacijent_postoji.set(False)
            except:
                print("No patient name field")

            try:
                if self.__dataset["Modality"]:
                    for vrednost, tekst in [("CT", "Computed Tomography"), ("US", "Ultrasound]"),
                                            ("MR", "Magnetic Resonance"), ("PX", "Panoramic X-Ray")]:
                        if vrednost == self.__dataset.Modality:
                            self.__tip.set(tekst)
                            break
                    self.__tip_postoji.set(True)
                else:
                    self.__tip_postoji.set(False)
            except:
                print("No modality field")


            try:
                if self.__dataset["ReferringPhysicianName"]:
                    self.__ime_lekara.set(self.__dataset.ReferringPhysicianName)  # vrednost podatka
                    self.__ime_lekara_postoji.set(True)
                else:
                    self.__ime_lekara_postoji.set(False)
            except:
                print("No referring physician field")

            try:
                if self.__dataset["PatientBirthDate"]:
                    self.__datumrodj.set(self.__dataset.PatientBirthDate)
                    self.__datumrodj_postoji.set(True)
                else:
                    self.__datumrodj_postoji.set(False)
            except:
                print("No patient birth date field")

            try:
                if self.__dataset["StudyDate"]:
                    self.__datumsnimka.set(self.__dataset.StudyDate)
                    self.__datumsnimka_postoji.set(True)
                else:
                    self.__datumsnimka_postoji.set(False)
            except:
                print("No study date field")

            try:
                if self.__dataset["StudyDescription"]:
                    self.__izvestaj.set(self.__dataset.StudyDescription)
                    self.__izvestaj_postoji.set(True)
                else:
                    self.__izvestaj_postoji.set(False)
            except:
                print("No study description field")

            self.azuriraj_stanja()  # omogućavanje polja za izmenu na osnovu pročitanih podataka
        except Exception as ex:  # desila se greška
            print()
            print(ex)

        try:
            pil_slika = pydicom_PIL.get_PIL_image(
                self.__dataset)  # pokušaj dekompresije i čitanja slike iz dataset objekta
            sirina = pil_slika.width
            visina = pil_slika.height
            print("originalne dimenzije:", sirina, ",", visina)

            maks_dimenzija = 900
            if sirina > maks_dimenzija or visina > maks_dimenzija:
                if sirina > visina:  # smanjiti sliku po većoj od 2 dimenzije
                    odnos = maks_dimenzija / sirina
                    sirina = maks_dimenzija
                    visina = int(odnos * visina)  # manja dimenzija se smanjuje proporcionalno
                else:
                    odnos = maks_dimenzija / visina
                    sirina = int(odnos * sirina)  # manja dimenzija se smanjuje proporcionalno
                    visina = maks_dimenzija
            print("nove dimenzije:", sirina, ",", visina)
            pil_slika = pil_slika.resize((sirina, visina),
                                         imagepil.LANCZOS)  # LANCZOS metoda je najbolja za smanjivanje slike

            slika = ImageTk.PhotoImage(pil_slika)  # PIL slika se mora prevesti u TkInter sliku (ImageTk)
            self.__slika_label["image"] = slika
            self.__slika_label.image = slika
        except Exception as ex:  # desila se greška; reset-ovanje slike na podrazumevanu
            # PIL slika se mora prevesti u TkInter sliku (ImageTk)
            # slika = ImageTk.PhotoImage(Image.new('L', (200, 200))) # crna slika dimenzija 200x200 piksela
            slika = ImageTk.PhotoImage(imagepil.open("DICOM-Logo.jpg"))  # bilo koja druga podrazumevana slika
            self.__slika_label["image"] = slika  # labeli se dodeljuje slika
            self.__slika_label.image = slika  # referenca na TkInter sliku se mora sačuvati, inače nece biti prikazana!

            print()
            print(ex)

        self["cursor"] = ""

    def komanda_dodaj(self):
        self.__pacijent_postoji_checkbutton["state"] = NORMAL
        self.__tip_postoji_checkbutton["state"] = NORMAL
        self.__datumrodj_postoji_checkbutton["state"] = NORMAL
        self.__datumsnimka_postoji_checkbutton["state"] = NORMAL
        self.__ime_lekara_postoji_checkbutton["state"] = NORMAL
        self.__izvestaj_postoji_checkbutton["state"] = NORMAL

        self.__ocisti_button["state"] = NORMAL
        self.__sacuvaj_button["state"] = NORMAL
        self.__datoteka_meni.entryconfig(0, state=DISABLED)
        self.__datoteka_meni.entryconfig(1, state=NORMAL)

        slika = ImageTk.PhotoImage(imagepil.open("DICOM-Logo.jpg"))  # bilo koja druga podrazumevana slika
        self.__slika_label["image"] = slika  # labeli se dodeljuje slika
        self.__slika_label.image = slika  # referenca na TkInter sliku se mora sačuvati, inače nece biti prikazana!

    def komanda_otvori(self):
        try:
            self["cursor"] = "wait"
            self.update()

            self.__dataset = self.__read_dicom
            print(self.__dataset)

            self.__ocisti_button["state"] = DISABLED
            self.__sacuvaj_button["state"] = DISABLED
            self.__datoteka_meni.entryconfig(0, state=DISABLED)
            self.__datoteka_meni.entryconfig(1, state=DISABLED)

            try:
                if self.__dataset["PatientName"]:
                    self.__pacijent.set(self.__dataset.PatientName)
                    self.__pacijent_postoji.set(True)
                else:
                    self.__pacijent_postoji.set(False)
            except:
                print("No patient name field")

            try:
                if self.__dataset["Modality"]:
                    for vrednost, tekst in [("CT", "Computed Tomography"), ("US", "Ultrasound]"),
                                            ("MR", "Magnetic Resonance"), ("PX", "Panoramic X-Ray")]:
                        if vrednost == self.__dataset.Modality:
                            self.__tip.set(tekst)
                            break
                    self.__tip_postoji.set(True)
                else:
                    self.__tip_postoji.set(False)
            except:
                print("No modality field")


            try:
                if self.__dataset["ReferringPhysicianName"]:
                    self.__ime_lekara.set(self.__dataset.ReferringPhysicianName)  # vrednost podatka
                    self.__ime_lekara_postoji.set(True)
                else:
                    self.__ime_lekara_postoji.set(False)
            except:
                print("No referring physician field")

            try:
                if self.__dataset["PatientBirthDate"]:
                    self.__datumrodj.set(self.__dataset.PatientBirthDate)
                    self.__datumrodj_postoji.set(True)
                else:
                    self.__datumrodj_postoji.set(False)
            except:
                print("No patient birth date field")

            try:
                if self.__dataset["StudyDate"]:
                    self.__datumsnimka.set(self.__dataset.StudyDate)
                    self.__datumsnimka_postoji.set(True)
                else:
                    self.__datumsnimka_postoji.set(False)
            except:
                print("No study date field")

            try:
                if self.__dataset["StudyDescription"]:
                    self.__izvestaj.set(self.__dataset.StudyDescription)
                    self.__izvestaj_postoji.set(True)
                else:
                    self.__izvestaj_postoji.set(False)
            except:
                print("No study description field")

        except Exception as ex:  # desila se greška
            print()
            print(ex)

        try:
            pil_slika = pydicom_PIL.get_PIL_image(
                self.__dataset)  # pokušaj dekompresije i čitanja slike iz dataset objekta
            sirina = pil_slika.width
            visina = pil_slika.height
            print("originalne dimenzije:", sirina, ",", visina)

            maks_dimenzija = 900
            if sirina > maks_dimenzija or visina > maks_dimenzija:
                if sirina > visina:  # smanjiti sliku po većoj od 2 dimenzije
                    odnos = maks_dimenzija / sirina
                    sirina = maks_dimenzija
                    visina = int(odnos * visina)  # manja dimenzija se smanjuje proporcionalno
                else:
                    odnos = maks_dimenzija / visina
                    sirina = int(odnos * sirina)  # manja dimenzija se smanjuje proporcionalno
                    visina = maks_dimenzija
            print("nove dimenzije:", sirina, ",", visina)
            pil_slika = pil_slika.resize((sirina, visina),
                                         imagepil.LANCZOS)  # LANCZOS metoda je najbolja za smanjivanje slike

            slika = ImageTk.PhotoImage(pil_slika)  # PIL slika se mora prevesti u TkInter sliku (ImageTk)
            self.__slika_label["image"] = slika
            self.__slika_label.image = slika
        except Exception as ex:  # desila se greška; reset-ovanje slike na podrazumevanu
            # PIL slika se mora prevesti u TkInter sliku (ImageTk)
            # slika = ImageTk.PhotoImage(Image.new('L', (200, 200))) # crna slika dimenzija 200x200 piksela
            slika = ImageTk.PhotoImage(imagepil.open("DICOM-Logo.jpg"))  # bilo koja druga podrazumevana slika
            self.__slika_label["image"] = slika  # labeli se dodeljuje slika
            self.__slika_label.image = slika  # referenca na TkInter sliku se mora sačuvati, inače nece biti prikazana!

            print()
            print(ex)

        self["cursor"] = ""

    def komanda_ocisti(self):
        self.__pacijent.set("")
        self.__tip.set("US")
        self.__datumrodj.set("")
        self.__datumsnimka.set("")
        self.__ime_lekara.set("")
        self.__izvestaj.set("")

    def komanda_sacuvaj(self):
        self["cursor"] = "wait"
        self.update()

        naziv_fajla = ""

        if self.__pacijent_postoji.get():  # podatak zadržan?
            self.__dataset.PatientName = self.__pacijent.get()  # vrednost podatka
            naziv_fajla = naziv_fajla + self.__pacijent.get() + "-"
        elif "PatientName" in self.__dataset:
            del self.__dataset.PatientName  # brisanje podatka iz dataset-a

        if self.__tip_postoji.get():
            for vrednost, tekst in [("CT", "Computed Tomography"), ("US", "Ultrasound]"), ("MR", "Magnetic Resonance"),
                                    ("PX", "Panoramic X-Ray")]:
                if tekst == self.__tip.get():
                    self.__dataset.Modality = vrednost
                    break
            naziv_fajla = naziv_fajla + self.__tip.get() + "-"
        elif "Modality" in self.__dataset:
            del self.__dataset.Modality

        if self.__datumrodj_postoji.get():
            self.__dataset.PatientBirthDate = datetime.strptime(str(self.__datumrodj.get()), "%Y%m%d")
        elif "PatientBirthDate" in self.__dataset:
            del self.__dataset.PatientBirthDate

        if self.__datumsnimka_postoji.get():
            self.__dataset.StudyDate = self.__datumsnimka.get()
        elif "StudyDate" in self.__dataset:
            del self.__dataset.StudyDate

        if self.__ime_lekara_postoji.get():
            self.__dataset.ReferringPhysicianName = self.__ime_lekara.get()
        elif "Referring Physician Name" in self.__dataset:
            del self.__dataset.ReferringPhysicianName

        if self.__izvestaj_postoji.get():
            self.__dataset.StudyDescription = self.__izvestaj.get()
        elif "Study Description" in self.__dataset:
            del self.__dataset.StudyDescription

        try:
            if self.__command == "add":
                naziv_fajla = naziv_fajla + datetime.now().strftime("%d%m%Y")
                self.__dataset.save_as(
                    self.__staza_do_datoteke + naziv_fajla + ".dcm")  # čuvanje dataset-a; ako ne postoji, biće kreiran
            else:
                self.__dataset.save_as(self.__staza_do_datoteke)
        except Exception as ex:
            print()
            print(ex)
            messagebox.showerror("DICOM", "Greška pri čuvanju datoteke!")

        self["cursor"] = ""

    def komanda_sacuvaj_kao(self):
        # otvaranje dijalog prozora za odabir datoteke
        staza_do_datoteke = filedialog.asksaveasfilename(
            initialdir="./DICOM samples",
            title="Čuvanje",
            filetypes=[("DICOM files", "*.dcm")],
            defaultextension=".dcm")
        if staza_do_datoteke == "":
            return

        self.__staza_do_datoteke = staza_do_datoteke
        self.komanda_sacuvaj()

    def komanda_izlaz(self):
        self.destroy()

    def __init__(self, readDicom, fileName, command) -> object:
        super().__init__()

        self.__read_dicom = readDicom
        self.__command = command
        self.__staza_do_datoteke = "DICOM samples/" + fileName

        self.__dataset = pydicom.Dataset()
        self.__dataset.is_little_endian = True
        self.__dataset.is_implicit_VR = True

        self.__pacijent_postoji = BooleanVar(self, False)
        self.__pacijent = StringVar(self)

        self.__tip_postoji = BooleanVar(self, False)
        self.__tip = StringVar(self, "US")

        self.__datumrodj_postoji = BooleanVar(self, False)
        self.__datumrodj = IntVar(self)

        self.__datumsnimka_postoji = BooleanVar(self, False)
        self.__datumsnimka = IntVar(self)

        self.__ime_lekara_postoji = BooleanVar(self, False)
        self.__ime_lekara = StringVar(self)

        self.__izvestaj_postoji = BooleanVar(self, False)
        self.__izvestaj = StringVar(self)

        # pravljenje GUI-a
        # /////////////////////3///////////////////////////////////////////////////////////////////
        newImage = imagepil.new('L', (200, 200))
        slika = ImageTk.PhotoImage(newImage)
        self.__slika_label = Label(self, image=slika)
        self.__slika_label.image = slika
        self.__slika_label.pack(side=LEFT, expand=1)

        unos_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        unos_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__datumrodj_frame = Frame(unos_frame)
        self.__datumsnimka_frame = Frame(unos_frame)
        self.__ime_lekara_frame = Frame(unos_frame)
        self.__izvestaj_frame = Frame(unos_frame)

        self.__pacijent_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__pacijent_postoji,
                                                          command=self.komanda_pacijent_postoji, state=DISABLED)
        self.__tip_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__tip_postoji,
                                                     command=self.komanda_tip_postoji, state=DISABLED)
        self.__datumrodj_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__datumrodj_postoji,
                                                           command=self.komanda_datumrodj_postoji, state=DISABLED)
        self.__datumsnimka_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__datumsnimka_postoji,
                                                             command=self.komanda_datumsnimka_postoji, state=DISABLED)
        self.__izvestaj_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__izvestaj_postoji,
                                                          command=self.komanda_izvestaj_postoji, state=DISABLED)
        self.__ime_lekara_postoji_checkbutton = Checkbutton(unos_frame, variable=self.__ime_lekara_postoji,
                                                            command=self.komanda_ime_lekara_postoji, state=DISABLED)

        self.__ocisti_button = Button(unos_frame, text="Očisti", width=10, command=self.komanda_ocisti, state=DISABLED)
        self.__sacuvaj_button = Button(unos_frame, text="Sačuvaj", width=10, command=self.komanda_sacuvaj,
                                       state=DISABLED)

        self.__pacijent_entry = Entry(unos_frame, textvariable=self.__pacijent, state=DISABLED)
        self.__tip_combobox = Combobox(unos_frame, values=("US", "MR", "CT", "PX"), textvariable=self.__tip,
                                       state=DISABLED)
        self.__datumsnimka_entry = Entry(unos_frame, textvariable=self.__datumsnimka, state=DISABLED)
        self.__datumrodj_entry = Entry(unos_frame, textvariable=self.__datumrodj, state=DISABLED)
        self.__ime_lekara_entry = Entry(unos_frame, textvariable=self.__ime_lekara, state=DISABLED)
        self.__izvestaj_entry = Entry(unos_frame, textvariable=self.__izvestaj, state=DISABLED)


        red = 1
        self.__pacijent_postoji_checkbutton.grid(row=red)
        red += 1
        self.__tip_postoji_checkbutton.grid(row=red)
        red += 1
        self.__datumrodj_postoji_checkbutton.grid(row=red)
        red += 1
        self.__datumsnimka_postoji_checkbutton.grid(row=red)
        red += 1
        self.__ime_lekara_postoji_checkbutton.grid(row=red)
        red += 1
        self.__izvestaj_postoji_checkbutton.grid(row=red)

        red = 1
        kolona = 1
        Label(unos_frame, text="Pacijent:").grid(row=red, column=kolona, sticky=E)
        red += 1
        Label(unos_frame, text="Tip:").grid(row=red, column=kolona, sticky=E)
        red += 1
        Label(unos_frame, text="Datum rodjenja:").grid(row=red, column=kolona, sticky=E)
        red += 1
        Label(unos_frame, text="Datum snimka:").grid(row=red, column=kolona, sticky=E)
        red += 1
        Label(unos_frame, text="Ime lekara").grid(row=red, column=kolona, sticky=E)
        red += 1
        Label(unos_frame, text="Izvestaj").grid(row=red, column=kolona, sticky=E)

        red = 0
        kolona = 2
        self.__ocisti_button.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__pacijent_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__tip_combobox.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datumrodj_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__datumsnimka_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__ime_lekara_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__izvestaj_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        self.__sacuvaj_button.grid(row=red, column=kolona, sticky=W)

        meni_bar = Menu(self)

        self.__datoteka_meni = Menu(meni_bar, tearoff=0)
        self.__datoteka_meni.add_command(label="Sačuvaj", command=self.komanda_sacuvaj, state=DISABLED)
        self.__datoteka_meni.add_command(label="Sačuvaj kao...", command=self.komanda_sacuvaj_kao, state=DISABLED)
        self.__datoteka_meni.add_separator()
        self.__datoteka_meni.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=self.__datoteka_meni)

        pomoc_meni = Menu(meni_bar, tearoff=0)
        meni_bar.add_cascade(label="Pomoć", menu=pomoc_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)
        self.title("DICOM")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        # programski izazvani događaji
        self.focus_force()

        if self.__command == "open":
            self.komanda_otvori()
        elif self.__command == "edit":
            self.komanda_otvori_i_edituj()
        elif self.__command == "add":
            self.komanda_dodaj()
