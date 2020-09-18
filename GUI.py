import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import mysql
import mysql.connector
import Video
import plate_detection as pd
import w2sms
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

class window(QtWidgets.QWidget):
    
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(600,100,600,600)
        self.title = "E-challan"
        self.setWindowTitle(self.title)
        self.init_ui()
        
    def init_ui(self):
        self.vbox = QtWidgets.QVBoxLayout()
        self.k = 0
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(20)
        
        img1 = QtWidgets.QLabel(self)
        pixmap2 = QPixmap('rtoimg.jpg')
        pixmap42 = pixmap2.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        img1.setPixmap(pixmap42)
        
        self.title = QtWidgets.QLabel("Traffic Violation Echallan Payment",self)
        self.title.setFont(font)
        self.title.move(100,70)
        
        font1 = QtGui.QFont()
        font1.setBold(True)
        font1.setPointSize(10)
        
        self.groupbox = QtWidgets.QGroupBox()
        self.vbox.addStretch(1)
        
        self.createTable()
        self.tableWidget.cellClicked.connect(self.Submit)
        
        self.hboxt = QtWidgets.QHBoxLayout()
        self.hboxt.addStretch()
        self.hboxt.addWidget(img1)
        self.hboxt.addWidget(self.title)
        self.hboxt.addStretch()
        
        self.vbox.addLayout(self.hboxt)
        self.vbox.addWidget(self.tableWidget)
        self.vbox.addWidget(self.groupbox)
        self.vbox.addStretch(1)
        
        self.setLayout(self.vbox)
        self.show()
        
        
    def createTable(self):
        database = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='echallan')
        cur = database.cursor()
        cur.execute("SELECT * FROM vehicle_violated")
        rows = cur.fetchall()
        self.c1 = []
        self.n1= []
        self.v = []
        self.o1 = []
        self.f1 = []
        
        for i in range(len(rows)):
            self.c1.append(str(rows[i][0]))
            self.n1.append(str(rows[i][1]))
            self.v.append(str(rows[i][2]))
            self.o1.append(str(rows[i][3]))
            self.f1.append(str(rows[i][4]))
        
        self.tableWidget = QTableWidget(len(rows), 6)
        self.col_header = ['Challan No', 'Name', 'Vehicle No', 'Offence commited', 'Fine', 'Details']
        self.tableWidget.setHorizontalHeaderLabels(self.col_header)
        self.tableWidget.setEditTriggers( QTableWidget.NoEditTriggers )
        
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        
        for i in range(len(rows)):
            self.tableWidget.setItem(i,0,QTableWidgetItem(self.c1[i]))
            self.tableWidget.setItem(i,1,QTableWidgetItem(self.n1[i]))
            self.tableWidget.setItem(i,2,QTableWidgetItem(self.v[i]))
            self.tableWidget.setItem(i,3,QTableWidgetItem(self.o1[i]))
            self.tableWidget.setItem(i,4,QTableWidgetItem(self.f1[i]))
            self.tableWidget.setItem(i,5,QTableWidgetItem('Details'))
    
            
    def createGroupLayout(self):
        self.grid = QtWidgets.QGridLayout()
        
        self.challan_no = QtWidgets.QLabel("Challan Number - ",self)
        self.cno = QtWidgets.QLabel(self)
        
        
        self.name = QtWidgets.QLabel("Owner Name - ",self)
        self.na = QtWidgets.QLabel(self)
        
        self.vehicle_no = QtWidgets.QLabel("Vehicle Number - ",self)
        self.vn = QtWidgets.QLabel(self)
        
        self.offence = QtWidgets.QLabel("Offence Commited - ",self)
        self.oc = QtWidgets.QLabel(self)
        
        self.vehicle_model = QtWidgets.QLabel("Vehicle Model - ",self)
        self.vm = QtWidgets.QLabel(self)
        
        self.phone_no = QtWidgets.QLabel("Phone Number - ",self)
        self.pn = QtWidgets.QLabel(self)
        
        self.fine = QtWidgets.QLabel("Total Fine - ",self)
        self.f = QtWidgets.QLabel(self)
        
        self.lb1 = QtWidgets.QLabel("Evidence - ",self)
    
        self.img= QtWidgets.QLabel(self)
        
        approve = QtWidgets.QPushButton('Approve',self)
        approve.clicked.connect(self.Approve)
        
        deny = QtWidgets.QPushButton('Deny',self)
        deny.clicked.connect(self.Deny)
        
        #self.grid.setSpacing(0)
        self.grid.addWidget(self.challan_no, 1, 0)
        self.grid.addWidget(self.cno, 1, 1)
        self.grid.addWidget(self.name, 2, 0)
        self.grid.addWidget(self.na, 2, 1)
        self.grid.addWidget(self.vehicle_no, 3, 0)
        self.grid.addWidget(self.vn, 3, 1)
        self.grid.addWidget(self.offence, 4, 0)
        self.grid.addWidget(self.oc, 4, 1)
        self.grid.addWidget(self.vehicle_model, 5, 0)
        self.grid.addWidget(self.vm, 5, 1)
        self.grid.addWidget(self.phone_no, 6, 0)
        self.grid.addWidget(self.pn, 6, 1)
        self.grid.addWidget(self.fine, 7, 0)
        self.grid.addWidget(self.f, 7, 1)
        self.grid.addWidget(self.lb1, 8, 0)
        self.grid.addWidget(self.img, 8, 1)
        self.grid.addWidget(approve, 9, 0)
        self.grid.addWidget(deny, 9, 1)
        
        self.groupbox.setLayout(self.grid)
           
    def Submit(self, row, column):
        if self.k == 0:
            self.createGroupLayout()
            self.k=1
        self.curr_row = row
        number = self.v[row]

        database = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='echallan')
        cur = database.cursor()
        cur.execute("SELECT * FROM vehicle_data where Vehicle_no = (%s)",(number,))
        row = cur.fetchone()
        
        self.c = []
        self.n = []
        self.v1 = []
        self.o = []
        self.fi = []
        self.p = []
        self.vmo = []
        
        self.c.append(str(row[0]))
        self.n.append(str(row[1]))
        self.v1.append(str(row[2]))
        self.o.append(str(row[3]))
        self.p.append(str(row[4]))
        self.vmo.append(str(row[5]))
        self.fi.append(str(row[6]))
        
        self.cno.setText(self.c[-1])
        self.cno.adjustSize()
        
        self.na.setText(self.n[-1])
        self.na.adjustSize()
        
        self.vn.setText(self.v1[-1])
        self.vn.adjustSize()
        
        self.oc.setText(self.o[-1])
        self.oc.adjustSize()    
        
        self.vm.setText(self.vmo[-1])
        self.vm.adjustSize()
        
        self.pn.setText(self.p[-1])
        self.pn.adjustSize()
        
        self.f.setText(self.fi[-1])
        self.f.adjustSize()
        
        pixmap = QPixmap('./data/frame368.jpg')
        pixmap4 = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap4)
        
    
        
    def Approve(self):
        number = self.v1[-1]
        database = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='echallan')
        cur = database.cursor()
        cur.execute("SELECT * FROM vehicle_data where Vehicle_no = (%s)",(number,))
        row = cur.fetchone()
        
        cn = str(row[0])
        fine = int(row[6])
        fine = str(fine + 200)
        
        cur. execute("UPDATE vehicle_data SET fee = (%s) WHERE Challan_no = (%s)",(fine, cn, ))
        
        database.commit()
        message = ' Challan Number: '+self.c[-1]+'\n Name: '+self.n[-1]+'\n Vehicle number: '+self.v[-1]
        message += '\n Offence commited: '+self.o[-1]+'\n fine: '+fine
        print(message)
        
        w2sms.send( self.p[-1], message )
        
        self.tableWidget.removeRow(self.curr_row)
        
        self.cno.setText(" ")
        self.cno.adjustSize()
        
        self.na.setText(" ")
        self.na.adjustSize()
        
        self.vn.setText(" ")
        self.vn.adjustSize()
        
        self.oc.setText(" ")
        self.oc.adjustSize()    
        
        self.vm.setText(" ")
        self.vm.adjustSize()
        
        self.pn.setText(" ")
        self.pn.adjustSize()
        
        self.f.setText(" ")
        self.f.adjustSize()
        
        pixmap = QPixmap(' ')
        pixmap4 = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap4)
        
        print(self.c1)
        
        for i in range(0, len(self.v)):
            if number == self.v[i]:
                rown = i
                
        del self.c1[rown]
        del self.n1[rown]
        del self.v[rown]
        del self.o1[rown]
        del self.f1[rown]
        
        
    def Deny(self):
        number = self.v1[-1]
        self.tableWidget.removeRow(self.curr_row)
        
        self.cno.setText(" ")
        self.cno.adjustSize()
        
        self.na.setText(" ")
        self.na.adjustSize()
        
        self.vn.setText(" ")
        self.vn.adjustSize()
        
        self.oc.setText(" ")
        self.oc.adjustSize()    
        
        self.vm.setText(" ")
        self.vm.adjustSize()
        
        self.pn.setText(" ")
        self.pn.adjustSize()
        
        self.f.setText(" ")
        self.f.adjustSize()
        
        pixmap = QPixmap(' ')
        pixmap4 = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.img.setPixmap(pixmap4)
        
        self.tableWidget.cellClicked.connect(self.Submit)
        
        for i in range(0, len(self.v)):
            if number == self.v[i]:
                rown = i
                
        del self.c1[rown]
        del self.n1[rown]
        del self.v[rown]
        del self.o1[rown]
        del self.f1[rown]
        

def setdatabase():
    database = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='echallan')
    for i in range(len(vnumber)):
        cur = database.cursor()
        cur.execute("SELECT * FROM vehicle_data where Vehicle_no = (%s)",(vnumber[i],))
        row = cur.fetchone()
        
        c = str(row[0])
        n = str(row[1])
        v = str(row[2])
        o = str(row[3])
        fi = str(row[6])
        
        sql = "INSERT INTO vehicle_violated (Challan_no, Name, Vehicle_no, Offence_commited, fine) VALUES (%s, %s, %s, %s, %s)"
        val = (c, n, v, o, fi)
        cur.execute(sql, val)
        database.commit()
        
def deletedatabase():
    database = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='echallan')
    cur = database.cursor()
    cur.execute("DELETE FROM vehicle_violated")
    database.commit()

Video.GenerateFrames()
vnumber = pd.GetNumber()
vnumber[0] = vnumber[0].replace(" ","")
deletedatabase()
setdatabase()
app = QtWidgets.QApplication(sys.argv)
w = window()
sys.exit(app.exec_())
     
