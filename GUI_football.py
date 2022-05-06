from random import randint
from tkinter import Frame, Listbox, ttk
import tkinter
from tkinter.constants import CENTER, HORIZONTAL, TRUE, VERTICAL
from tkinter.font import Font
from tkinter import Button, E, LabelFrame, messagebox, Label, Menu, W, Tk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from numpy.typing import _128Bit
import pandas as pd
import predictor as predict
window = Tk()

raw_data = pd.read_csv('C:\\Users\\Huy Quoc\\PyCode\\betting\\final_dataset2.csv')
columns_req = ['HomeTeam','AwayTeam','FTR','MW']
playing_statistics = raw_data[columns_req]

def prediction():
    MG = COMBO0.get()
    VD = int(COMBO1.get())
    Match = COMBO2.get()
    if int(MG[0])==0:
        MG_num = int(MG[1])
    else:
        MG_num = int(MG[:2])
    index = MG_num*380+(VD-1)*10
    Teams = Match.split(sep=' vs ')
    HomeTeam = Teams[0]
    AwayTeam = Teams[1]
    for i in range(index,index+10):
        if raw_data['HomeTeam'][i]==HomeTeam and raw_data['AwayTeam'][i]==AwayTeam:
            index = i
            break
    X_all = raw_data[['HTP', 'ATP', 'HM1', 'HM2', 'HM3', 'AM1', 'AM2', 'AM3', 'HTGD', 'ATGD', 'DiffFormPts', 'DiffLP']]
    X_all.HM1 = X_all.HM1.astype('str')
    X_all.HM2 = X_all.HM2.astype('str')
    X_all.HM3 = X_all.HM3.astype('str')
    X_all.AM1 = X_all.AM1.astype('str')
    X_all.AM2 = X_all.AM2.astype('str')
    X_all.AM3 = X_all.AM3.astype('str')
    X_all = predict.preprocess_features(X_all)
    X_all = X_all.drop(['HM1_M', 'HM2_M', 'HM3_M', 'AM1_M', 'AM2_M', 'AM3_M'], axis = 1)
    x = X_all.take([index])
    Y = predict.predict(x)
    htw=Y[0,2]*100
    atw=Y[0,1]*100
    tie=Y[0,0]*100
    messagebox.showinfo('Dự đoán kết quả','Tỉ lệ thắng của đội nhà: {:.2f}%'.format(htw)+'\n\nTỉ lệ thắng của đội khách: {:.2f}%'.format(atw)+'\n\n''Tỉ lệ hòa: {:.2f}%'.format(tie))

def view_pl_stats():
    MG = COMBO0.get()
    VD = int(COMBO1.get())
    Match = COMBO2.get()
    if int(MG[0])==0:
        MG_num = int(MG[1])
    else:
        MG_num = int(MG[:2])
    index = MG_num*380+(VD-1)*10-1
    Teams = Match.split(sep=' vs ')
    HomeTeam = Teams[0]
    AwayTeam = Teams[1]
    Doidau = []
    PhongDoNha = list()
    PhongDoNhaNha = list()
    PhongDoKhach = list()
    PhongDoKhachKhach = list()
    count_doidau = 0
    count_nha = 0
    count_nhanha = 0
    count_khach = 0
    count_khachkhach = 0
    check = True
    while check and index>0:
        if playing_statistics['HomeTeam'][index]==HomeTeam and playing_statistics['AwayTeam'][index]==AwayTeam or playing_statistics['HomeTeam'][index]==AwayTeam and playing_statistics['AwayTeam'][index]==HomeTeam:
            if count_doidau<5:
                Doidau.append((raw_data['HomeTeam'][index]+" vs "+raw_data['AwayTeam'][index],raw_data['Date'][index],str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])))
                count_doidau+=1

        if playing_statistics['HomeTeam'][index]==HomeTeam:
            if count_nha<5:
                PhongDoNha.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_nha+=1
            if count_nhanha<5:
                PhongDoNhaNha.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_nhanha+=1

        if playing_statistics['AwayTeam'][index]==AwayTeam:
            if count_khach<5:
                PhongDoKhach.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_khach+=1
            if count_khachkhach<5:
                PhongDoKhachKhach.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_khachkhach+=1

        if playing_statistics['AwayTeam'][index]==HomeTeam:
            if count_nha<5:
                PhongDoNha.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_nha+=1

        if playing_statistics['HomeTeam'][index]==AwayTeam:
            if count_khach<5:
                PhongDoKhach.append(raw_data['HomeTeam'][index]+" "+str(raw_data['FTHG'][index])+" - "+str(raw_data['FTAG'][index])+" "+raw_data['AwayTeam'][index])
                count_khach+=1

        if count_doidau == count_nha == count_nhanha == count_khach == count_khachkhach ==5:
            check = False
        index-=1

    trv.delete(*trv.get_children())
    for Doidau_ in Doidau:
        trv.insert('', tkinter.END, values=Doidau_)

    lbx0.delete(0,tkinter.END)
    lbx1.delete(0,tkinter.END)
    lbx2.delete(0,tkinter.END)
    lbx3.delete(0,tkinter.END)
    for i in range(len(PhongDoNha)):
        lbx0.insert('end',PhongDoNha[i])
    for i in range(len(PhongDoNhaNha)):
        lbx1.insert('end',PhongDoNhaNha[i])
    for i in range(len(PhongDoKhach)):
        lbx2.insert('end',PhongDoKhach[i])
    for i in range(len(PhongDoKhachKhach)):
        lbx3.insert('end',PhongDoKhachKhach[i])
        
    
#GUI window
window.title('Match Predictor')
window.geometry()

IMAGEX = Image.open('C:\\Users\\Huy Quoc\\PyCode\\betting\\background')
background_image=ImageTk.PhotoImage(IMAGEX)
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Title
lbl = Label(window, text="THÔNG TIN TRẬN ĐẤU VÀ DỰ ĐOÁN KẾT QUẢ", font=("Arial Bold", 12))
lbl.grid()

#To create button
FRAME0 = LabelFrame(window)
FRAME0.grid(padx=8, pady=8)
LAB0 = Label(FRAME0, text='Chọn mùa giải')
LAB0.grid()
LAB1 = Label(FRAME0, text='Chọn vòng đấu')
LAB1.grid(row=0, column=1)
LAB2 = Label(FRAME0, text='Chọn trận đấu')
LAB2.grid(row=0, column=2)

# combo boxes.

#List creation from dict
count = 1
MG_LIST = list()
for i in range(21):
    if i<9:
        MG = "0"+str(i)+"-0"+str(i+1)
    elif i==9:
        MG = "0"+str(i)+"-"+str(i+1)
    else:
        MG = str(i)+"-"+str(i+1)
    MG_LIST.append(MG)

VD_LIST = list()
while(count < 39):
    VD_LIST.append(count)
    count += 1

TD_LIST = list()
def showMG(event):
    COMBO1.delete(0,"end")
    COMBO2.delete(0,"end")

def showVD(event):
    VD = event.widget.get()
    MG = COMBO0.get()
    TD_LIST.clear()
    COMBO2.delete(0,"end")

    for i in range(0,playing_statistics.shape[0]):
        
        x=i//380
        if x<9:
            x = "0"+str(x)+"-0"+str(x+1)
        elif i==9:
            x = "0"+str(x)+"-"+str(x+1)
        else:
            x = str(x)+"-"+str(x+1)

        if x == MG and playing_statistics['MW'][i] == int(VD):
            TD_LIST.append(playing_statistics['HomeTeam'][i]+" vs "+playing_statistics['AwayTeam'][i])

    COMBO2['values'] = (TD_LIST)

COMBO0 = Combobox(FRAME0)
COMBO0['values'] = (MG_LIST)
COMBO0.current(20)
COMBO0.grid(padx=5, pady=5)
COMBO0.bind("<<ComboboxSelected>>",showMG)

COMBO1 = Combobox(FRAME0)
COMBO1['values'] = (VD_LIST)
COMBO1.grid(padx=5, pady=5, row=1, column=1)
COMBO1.bind("<<ComboboxSelected>>",showVD)

COMBO2 = Combobox(FRAME0, width=50)
COMBO2.grid(padx=5, pady=5, row=1, column=2)

# Stats button.
STATS_BTN = Button(FRAME0, bg='darkcyan', text='Thông tin trận đấu'
                   ,command=view_pl_stats)
STATS_BTN.grid(sticky=W+E, padx=5, pady=5, row=2,columnspan=2)

# Predict button.
BTN = Button(FRAME0, bg='lightgreen', text='Dự đoán kết quả',
             command=prediction)
BTN.grid(sticky=W+E, padx=5, pady=5, row=2, column=2)   

#TreeView
FRAME1 = LabelFrame(window, text="THÀNH TÍCH ĐỐI ĐẦU", font=("Arial", 8))
FRAME1.grid(padx=8, pady=8)
trv = ttk.Treeview(FRAME1, columns=(1,2,3), show='headings', height=6)

trv.heading(1, text="Trận đấu")
trv.heading(2, text="Ngày diễn ra")
trv.heading(3, text="Kết quả chung cuộc")

#Scrollbars
vsb= ttk.Scrollbar(FRAME1, orient=VERTICAL,command=trv.yview)  
trv.configure(yscroll=vsb.set)
hsb = ttk.Scrollbar(FRAME1, orient=HORIZONTAL, command=trv.xview)
trv.configure(xscroll=hsb.set)

trv.grid(row=0, column=0)
vsb.grid(row=0, column=1)
hsb.grid(row=1, column=0)

#ListBox
FRAME2 = LabelFrame(window)
FRAME2.grid(padx=8, pady=8)
lb2 = Label(FRAME2, text="PHONG ĐỘ ĐỘI NHÀ", font=("Arial Bold", 10))
lb2.grid(columnspan=2, row=0)
lb3 = Label(FRAME2, text="PHONG ĐỘ ĐỘI KHÁCH", font=("Arial Bold", 10))
lb3.grid(column=2, columnspan=2, row=0)

lb4 = Label(FRAME2, text="5 trận gần nhất", font=("Arial Bold", 10))
lb4.grid(column=0, row=1)
lb5 = Label(FRAME2, text="Phong độ sân nhà", font=("Arial Bold", 10))
lb5.grid(column=1, row=1)
lb6 = Label(FRAME2, text="5 trận gần nhất", font=("Arial Bold", 10))
lb6.grid(column=2, row=1)
lb7 = Label(FRAME2, text="Phong độ sân khách", font=("Arial Bold", 10))
lb7.grid(column=3, row=1)

lbx0 = Listbox(FRAME2, width=40)
lbx1 = Listbox(FRAME2, width=40)
lbx2 = Listbox(FRAME2, width=40)
lbx3 = Listbox(FRAME2, width=40)
lbx0.grid(column=0, row=2)
lbx1.grid(column=1, row=2)
lbx2.grid(column=2, row=2)
lbx3.grid(column=3, row=2)

window.mainloop()