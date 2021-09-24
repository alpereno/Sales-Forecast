# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 06:35:33 2020

@author: alper
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn import preprocessing

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.rData()  #verileri okuma
        self.lblEncoder()     #verileri ayrıştırma
        self.fitdata()   #verileri eğitme
        self.ui()  #kullanıcı arayüzünü oluşturma ve butona basıldığında sonuçları bastırma
              
        
        
    def ui(self):#kullanıcı arayüz sistemi
        self.setGeometry(650,350,600,400)
        self.Wplatform = QComboBox()
        self.Wplatform.addItems(list(self.leplatform.classes_))
        self.Wgenre = QComboBox()
        self.Wgenre.addItems(list(self.legenre.classes_))
        self.Wpublisher = QComboBox()
        self.Wpublisher.addItems(list(self.lepublisher.classes_))
        self.buttonara = QPushButton("Göster")
        self.buttonara.clicked.connect(self.btnpredict)
        self.lblNa = QLabel("NA")
        self.lblEu = QLabel("EU")
        self.lblOther = QLabel("OTHER")
        self.lblGlobal = QLabel("GLOBAL")
        hbox = QHBoxLayout()
        hbox.addWidget(self.lblNa)
        hbox.addWidget(self.lblEu)
        hbox.addWidget(self.lblOther)
        hbox.addWidget(self.lblGlobal)
        
        plat_label=QLabel("Platform")
        genre_label=QLabel("Genre")
        pub_label=QLabel("Publisher")
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(plat_label)
        vbox.addWidget(self.Wplatform)
        vbox.addWidget(genre_label)
        vbox.addWidget(self.Wgenre)
        vbox.addWidget(pub_label)
        vbox.addWidget(self.Wpublisher)
        vbox.addWidget(self.buttonara)
        
        
        
        self.setLayout(vbox)
    
        self.show()
        
    def convertor():
        dic_platform={}
        for x in platform:
            dic_platform[x]="a"
            
    def rData(self):#verileri okuyup gerekli kolonlara ayırır
        self.veriler = pd.read_csv('vgsales4.csv')
        self.platform = self.veriler.iloc[:,0:1].values
        self.genre = self.veriler.iloc[:,1:2].values
        self.publisher = self.veriler.iloc[:,2:3].values
        self.NaSales = self.veriler.iloc[:,3:4].values
        self.EuSales = self.veriler.iloc[:,4:5].values
        self.OtherSales = self.veriler.iloc[:,5:6].values
        self.GlobalSales = self.veriler.iloc[:,6:7].values
        
    def lblEncoder(self):#program encoder kullanarak kategorik verileri ayrıştırır
        from sklearn import preprocessing
        self.leplatform = preprocessing.LabelEncoder()
        self.legenre = preprocessing.LabelEncoder()
        self.lepublisher = preprocessing.LabelEncoder()
        
        self.platform[:,0] = self.leplatform.fit_transform(self.platform[:,0])#Wii = 7 SNES=6 NES=3 vermiş program
        self.genre[:,0] = self.legenre.fit_transform(self.genre[:,0])#Sports = 8 platform türü = 2 Misc = 1 vermiş
        self.publisher[:,0] = self.lepublisher.fit_transform(self.publisher[:,0])#nintendo = 1 microsoft = 0  #sony = 2 take-two=3 vermiş

        print(list(self.leplatform.classes_))
        
    
    def btnpredict(self):#butona basıldığında tahmin işlemi yapılır gerekli labellere yazılır
        NAsonuc = self.regNa.predict([[self.Wplatform.currentIndex(),self.Wgenre.currentIndex(), self.Wpublisher.currentIndex()]])
        EUsonuc = self.regEu.predict([[self.Wplatform.currentIndex(),self.Wgenre.currentIndex(), self.Wpublisher.currentIndex()]])
        OTHERsonuc = self.regOther.predict([[self.Wplatform.currentIndex(),self.Wgenre.currentIndex(), self.Wpublisher.currentIndex()]])
        GLOBALsonuc = self.regGlobal.predict([[self.Wplatform.currentIndex(),self.Wgenre.currentIndex(), self.Wpublisher.currentIndex()]])
        
        
        self.lblNa.setText("NA: " + str(NAsonuc[0])[0:4])
        self.lblEu.setText("EU: " + str(EUsonuc[0])[0:4])
        self.lblOther.setText("OTHER: " + str(OTHERsonuc[0])[0:4])
        self.lblGlobal.setText("GLOBAL: " + str(GLOBALsonuc[0])[0:4])
        
        
    def fitdata(self):#gerekli tahminler için programı eğitir
        self.regNa = linear_model.Ridge()
        s=pd.concat([pd.DataFrame(self.platform,columns=["Platform"]),pd.DataFrame(self.genre,columns=["Genre"]),pd.DataFrame(self.publisher,columns=["Publisher"]),pd.DataFrame(self.NaSales,columns=["NA_Sales"])], axis=1)
        self.regNa.fit(s[["Platform","Genre","Publisher"]],self.veriler.NA_Sales)#programı eğittim önceki verilerle
        self.regEu = linear_model.Ridge()
        self.regEu.fit(s[["Platform","Genre","Publisher"]],self.veriler.EU_Sales)#programı eğittim önceki verilerle
        self.regGlobal = linear_model.Ridge()
        self.regGlobal.fit(s[["Platform","Genre","Publisher"]],self.veriler.Global_Sales)
        self.regOther = linear_model.Ridge()
        self.regOther.fit(s[["Platform","Genre","Publisher"]],self.veriler.Other_Sales)             
        
        
        
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    app.exec()
    
        
        
"""      
#verileri okuma
veriler = pd.read_csv('vgsales4.csv')

#verileri kategorilerine ayırma
platform = veriler.iloc[:,0:1].values
genre = veriler.iloc[:,1:2].values
publisher = veriler.iloc[:,2:3].values
NaSales = veriler.iloc[:,3:4].values
EuSales = veriler.iloc[:,4:5].values
OtherSales = veriler.iloc[:,5:6].values
GlobalSales = veriler.iloc[:,6:7].values



#data = [platform,genre,publisher]
#parameter = pd.DataFrame(data, columns=['platform', 'genre', 'publisher'])
#parameter = pd.DataFrame(data = parameter, index = range(30), columns = [platform, genre, publisher])
#parameter[:,0] = le.fit_transform(parameter[:,0])



#linear regression     genre-NaSales için
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn import preprocessing


s=pd.concat([pd.DataFrame(platform,columns=["Platform"]),pd.DataFrame(genre,columns=["Genre"]),pd.DataFrame(publisher,columns=["Publisher"]),pd.DataFrame(NaSales,columns=["NA_Sales"])], axis=1)
print(s)


reg = linear_model.Ridge()
reg.fit(s[["Platform","Genre","Publisher"]],veriler.NA_Sales)#programı eğittim önceki verilerle

sonuc = reg.predict([[1,0,0]]) #tahmin yapıyor
print(sonuc)


 grafik çizdirme
x = s[["Platform","Genre","Publisher"]]
plt.scatter(s[["Platform","Genre","Publisher"]], s[['NA_Sales']], color = 'red')
plt.plot(s[["Platform","Genre","Publisher"]],reg.predict(s[["Platform","Genre","Publisher"]]), color = 'blue')
plt.show()

"""




"""
#polinomal regresyon
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 4)
genre_poly =poly_reg.fit_transform(s.iloc[:,0:3])
print(genre_poly)

nasales = np.array(s['NA_Sales'])

lin_reg2 = LinearRegression()
lin_reg2.fit(genre_poly, nasales)
sonuc = lin_reg2.predict(poly_reg.fit_transform(np.array([[16,10,15]])))
print(sonuc)


plt.scatter(genre, nasales, color = 'red')
plt.plot(genre_poly, lin_reg2.predict(poly_reg.fit_transform(np.array([[16,10,15]]))), color = 'blue')
plt.show()



"""




