import tkinter
from tkinter import filedialog as fd
import PyPDF2
import tkinter.messagebox

okno = tkinter.Tk()
okno.title("Metraż")

szary = "gray15"
jszary = "grey80"

frame = tkinter.Frame(okno, bg=szary)
frame.pack()

# przeliczniki
x = 25.4 / 72
y = 1000000

# zmienne do ilości A4/A3
a4, a3 = 0, 0

# min i max metraż dla A4/A3
a41 = 0.0623
a42 = a41 + 0.003

a31 = 0.123
a32 = a31 + 0.003

# zmienna dla metrażu
full_metraz = 0


# wybieranie PDFa
def wybierz():
    global npliku

    filetypes = (
        ('Pliki PDF', '*.pdf'),
        ('Wszystkie pliki', '*.*')
    )

    npliku = fd.askopenfilename(
        title='Wybierz plik PDF',
        initialdir='Desktop',
        filetypes=filetypes)


# wybór pliku
fplik = tkinter.LabelFrame(frame, padx=20, pady=20, borderwidth=0, highlightthickness=0, bg=szary)
fplik.grid(row=0, column=0)

wyb = tkinter.Button(fplik, text="Wybierz plik PDF", command=wybierz, width=25, height=2, fg="white", bg="royalblue3",
                     font=("Arial", 10), borderwidth=0, highlightthickness=0)
wyb.grid(row=0, column=0)

# wybór cen
fprice = tkinter.LabelFrame(frame, width=30, padx=20, pady=10, borderwidth=0, highlightthickness=0, bg=szary)
fprice.grid(row=1, column=0)

# cena za m2
cenam2_zm = tkinter.StringVar()
lcenam2 = tkinter.Label(fprice, text="Cena za m²  ", bg=szary, fg=jszary)
lcenam2.grid(row=0, column=0)
cenam2 = tkinter.Entry(fprice, borderwidth=0, highlightthickness=0, bg=jszary)
cenam2.grid(row=0, column=1)

# cena za A4
lcena4 = tkinter.Label(fprice, text="Cena za A4  ", bg=szary, fg=jszary)
lcena4.grid(row=1, column=0)
cena4 = tkinter.Entry(fprice, borderwidth=0, highlightthickness=0, bg=jszary)
cena4.grid(row=1, column=1)

# cena za A3
lcena3 = tkinter.Label(fprice, text="Cena za A3  ", bg=szary, fg=jszary)
lcena3.grid(row=2, column=0)
cena3 = tkinter.Entry(fprice, borderwidth=0, highlightthickness=0, bg=jszary)
cena3.grid(row=2, column=1)


# test
def oblicz():
    global full_metraz, a4, a3
    pdf = PyPDF2.PdfFileReader(npliku)
    lstron = pdf.numPages

    for zm in range(lstron):

        p = pdf.getPage(zm)

        p.mediaBox.getWidth()
        p.mediaBox.getHeight()

        w = float(p.mediaBox.getWidth()) * x
        h = float(p.mediaBox.getHeight()) * x

        roz = float((w * h) / float(1000000))

        if a41 < roz < a42:
                a4 += 1
        elif a31 < roz < a32:
                a3 += 1
        else:
                full_metraz += roz

    cm2 = cenam2.get()
    ca4 = cena4.get()
    ca3 = cena3.get()

    print("A4 x ", a4)
    print("A3 x ", a3)
    print("{:.3f}".format(full_metraz), "m2")

    koszt = (float(cm2) * full_metraz) + (float(ca4) * a4) + (float(ca3) * a3)

    print("Cena za wydruk to " + str("{:.2f}".format(koszt)) + "zł")

    wynik = "Cena: "+str("{:.2f}".format(koszt))+"zł "+"\n""\n"+str(lstron)+" str.""\n"+str(a4)+" x A4""\n"+str(a3)+" x A3""\n"+"{:.3f}".format(full_metraz)+" m² "

    tkinter.messagebox.showinfo("Wycena", wynik)

    a4, a3, full_metraz = 0, 0, 0


fok = tkinter.LabelFrame(frame, borderwidth=0, highlightthickness=0, pady=20, bg=szary)
fok.grid(row=3, column=0)

ok = tkinter.Button(fok, text="Oblicz", command=oblicz, width=25, height=2, fg="white", bg="royalblue3",
                    font=("Arial", 10), borderwidth=0, highlightthickness=0)
ok.grid(row=0, column=0)

cc = tkinter.Label(frame,
                   text="Program na licencji GNU GPL (Otwarte oprogramowanie) \nSpółdzielnia Szmira 2022  "
                        "github.com/uwucyjan/metraz",
                   font=("Arial", 7), pady=5, fg="grey40", bg=szary)
cc.grid(row=4, column=0)

okno.mainloop()
