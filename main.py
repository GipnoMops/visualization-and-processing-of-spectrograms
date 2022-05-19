from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QWidget, QVBoxLayout, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy import integrate
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import interp1d
from interface import Ui_MainWindow
import numpy as np
import sys


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.way = str()
        self.ext = list()
        self.minim = list()
        self.fun = interp1d
        self.med_x = list()
        self.y_vel = list()
        self.n_for_med = 50
        self.num_of_points = 10000

        self.ui.charts.setCurrentWidget(self.ui.orig_gra)

        self.ui.orig_gra_btn.clicked.connect(self.showOG)
        self.ui.standards_btn.clicked.connect(self.showAP1)
        self.ui.auto_peaks_btn_2.clicked.connect(self.showAP2)
        self.ui.rules_btn.clicked.connect(self.showRP)
        self.ui.result_btn.clicked.connect(self.showR)

        self.ui.n_for_med_btn.clicked.connect(self.change_num_med)
        self.ui.num_of_points_btn.clicked.connect(self.change_num_of_points)

        self.ui.open_file_btn.clicked.connect(self.open_file)
        self.ui.add_point_btn.clicked.connect(self.add_point)
        self.ui.del_point_btn.clicked.connect(self.del_point)

        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.toolbar1 = NavigationToolbar(self.canvas1, self.ui.widget_6)
        self.ui.orig_canvaas.addWidget(self.toolbar1)
        self.ui.orig_canvaas.addWidget(self.canvas1)

        self.figure3 = plt.figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.toolbar3 = NavigationToolbar(self.canvas3, self.ui.widget_6)
        self.ui.auto_canvas2.addWidget(self.toolbar3)
        self.ui.auto_canvas2.addWidget(self.canvas3)

        self.ui.tableWidget.setColumnWidth(0, 130)
        self.ui.tableWidget.setColumnWidth(1, 250)
        self.ui.tableWidget.setColumnWidth(2, 250)
        self.integ_inten = list()
        self.max_inten = list()

        self.ui.tableWidget_2.setColumnWidth(0, 250)
        self.ui.tableWidget_2.setColumnWidth(1, 150)
        self.ui.tableWidget_2.setColumnWidth(2, 250)
        self.ui.tableWidget_2.setColumnWidth(3, 300)


    def change_num_med(self):
        res, okPressed = QInputDialog.getInt(self.ui.widget, "Изменить параметр апроксимации", "Percentage:",
                                             self.n_for_med, 2, 1000, 1)
        self.n_for_med = res
        if okPressed:
            self.drow_plots()

    def change_num_of_points(self):
        res, okPressed = QInputDialog.getInt(self.ui.widget, "Изменить гладкость графика", "Percentage:",
                                             self.num_of_points, 100, 10000000, 10)
        self.num_of_points = res
        if okPressed:
            self.drow_plots()

    def load_data(self):
        self.ui.tableWidget.setRowCount(len(self.integ_inten))
        for i in range(len(self.integ_inten)):
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.integ_inten[i])))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.max_inten[i])))

    def load_data_2(self):
        self.ui.tableWidget_2.setRowCount(12)
        nul = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "&"]
        first = ["v(OH)", "v(OH)", "v_as(CH_2) or v_s(CH_3) or v_??(СР_2) or b(CH_3)", "v(CO_2)", "b_(H-O-H)",
                 "v_as(TO_4)", "v_as(YO_4)", "v_as(TO_4)", "v_s(TO_4)", "v_s(SiOSi)+b(OSiO), v(AL-OH)", "b(TO_4)", "???"]
        second = ["3600-3700", "3200-3600", "2855", "2300", "1630-1635", "1225-1230",
                  "1108-1110", "960-970", "800", "550", "450", "???-???"]
        third = ["Кислотные ОН-группы мостиковых гидроксилов  Al-OH-O или Si-OH-Al (центры Бренстеда)",
                 "ОН-группы каркасных Si-OH группировок, либо молекулы H2O",
                 "Остатки органического темплата (TPAOH) в полостях каркаса TS (асимметричные –CH2, "
                 "симметричные –CH3 и растягивающие  –CH2 колебания; деформационные колебания –CH3)",
                 "Сорбированные молекулы CO2 в порах с наибольшими размерами на поверхности",
                 "Деформационные колебания H–O–H",
                 "Асимметричные валентные колебания внутри TS",
                 "Асимметричные валентные колебания внутри тетраэдров ТO4",
                 "Титан в каркасе TS",
                 "Симметричные валентные колебания внутри тетраэдров ТO4",
                 "Указывает на принадлежность цеолита к семейству ZSM",
                 "Деформационные колебания связей  Т–O", "не определено"]
        for i in range(12):
            self.ui.tableWidget_2.setItem(i, 0, QTableWidgetItem(str(nul[i])))
            self.ui.tableWidget_2.setItem(i, 1, QTableWidgetItem(str(first[i])))
            self.ui.tableWidget_2.setItem(i, 2, QTableWidgetItem(str(second[i])))
            self.ui.tableWidget_2.setItem(i, 3, QTableWidgetItem(str(third[i])))

    def open_file(self):
        res, okPressed = QFileDialog.getOpenFileName(self.ui.widget_6, 'Open file', '/User', 'Data File (*.dat *.asc *.txt)')
        if res != '' and okPressed:
            self.way = res
            self.drow_plots()

    def add_point(self):
        res, okPressed = QInputDialog.getDouble(self.ui.widget, "Добавить точку", "Координата х точки:", 10.05, 0.00, 5000.00, 2)
        if okPressed:
            self.change_extr(res, 1)

    def del_point(self):
        res, okPressed = QInputDialog.getInt(self.ui.widget, "Удалить точку", "Номер точки:", 28, 0, 1000, 1)
        if okPressed:
            self.change_extr(res, 2)


    def drow_plots(self):
        self.ext.clear()
        self.minim.clear()
        self.figure1.clear()
        self.integ_inten.clear()
        self.max_inten.clear()
        ax1 = self.figure1.add_subplot(111)

        inFile = open(self.way)
        x_coord = list()
        y_coord = list()
        for line in inFile:
            line = list(map(str, line.split()))
            x, y = float(line[0]), float(line[1])
            x_coord.append(x)
            y_coord.append(y)
        ax1.plot(x_coord, y_coord, color='b')
        ax1.grid()
        self.canvas1.draw()
#*******************************************************

        si = len(y_coord)//self.n_for_med
        y = np.array(y_coord[0 : self.n_for_med * si])
        y.shape = si, self.n_for_med

        y_c = list()
        med = np.median(y, axis=1)
        for i in med:
            for j in range(self.n_for_med):
                y_c.append(i)
#*******************************************************

        self.figure3.clear()
        ax3 = self.figure3.add_subplot(111)
        x = np.array(x_coord[0 : self.n_for_med * si])
        x.shape = si, self.n_for_med
        self.med_x = np.median(x, axis=1)
        self.fun = interp1d(self.med_x, med, 'cubic')

        t = np.linspace(min(self.med_x), max(self.med_x), self.num_of_points)

        self.y_vel = self.fun(t)
        peaks = argrelextrema(self.y_vel, np.greater)[0].tolist()
        minim = argrelextrema(self.y_vel, np.less)[0].tolist()

        for i in peaks:
            self.ext.append(t[i])
        for i in minim:
            self.minim.append(t[i])

        ax3.plot(t, self.fun(t))
        ax3.plot(self.ext, self.fun(self.ext), color='r')
        for i in range(len(self.ext)):
            ax3.text(self.ext[i], self.fun(self.ext)[i] + 0.02, str(i + 1), ha='center')
        for i in range(len(self.minim)):
            if 3700 > self.minim[i] > 3600:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("A"), ha='center')
            elif 3600 > self.minim[i] > 3200:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("B"), ha='center')
            elif 2856 > self.minim[i] > 2854:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("C"), ha='center')
            elif 2301 > self.minim[i] > 2299:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("D"), ha='center')
            elif 1635 > self.minim[i] > 1630:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("E"), ha='center')
            elif 1230 > self.minim[i] > 1225:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("F"), ha='center')
            elif 1110 > self.minim[i] > 1108:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("G"), ha='center')
            elif 970 > self.minim[i] > 960:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("H"), ha='center')
            elif 801 > self.minim[i] > 799:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("I"), ha='center')
            elif 551 > self.minim[i] > 549:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("J"), ha='center')
            elif 451 > self.minim[i] > 449:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("K"), ha='center')
            else:
                ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str("&"), ha='center')
        ax3.grid()
        self.canvas3.draw()
#*******************************************************

        self.integ()
        self.peak_height()
        self.load_data()
        self.load_data_2()
        inFile.close()


    def change_extr(self, n, k):
        self.integ_inten.clear()
        self.max_inten.clear()
        self.figure3.clear()
        ax3 = self.figure3.add_subplot(111)

        t = np.linspace(min(self.med_x), max(self.med_x), self.num_of_points)
        ax3.plot(t, self.fun(t))

        if k == 1:
            for j in range(len(self.ext)):
                if j == 0 and n < self.ext[j]:
                    self.ext.insert(j, n)
                    break
                elif j != (len(self.ext) - 1) and self.ext[j] < n < self.ext[j + 1]:
                    self.ext.insert(j + 1, n)
                    break
                elif j == len(self.ext) - 1:
                    self.ext.append(n)
        if k == 2:
            self.ext.pop(n - 1)

        ax3.plot(self.ext, self.fun(self.ext), color='r')
        for i in range(len(self.ext)):
            ax3.text(self.ext[i], self.fun(self.ext)[i] + 0.02, str(i + 1), ha='center')

        for i in range(len(self.minim)):
            ax3.text(self.minim[i], self.fun(self.minim)[i] - 0.02, str(i + 1), ha='center')

        ax3.grid()
        self.canvas3.draw()

        self.integ()
        self.peak_height()
        self.load_data()

    def integ(self):
        for i in range(len(self.ext) - 1):
            x1 = self.ext[i]
            x2 = self.ext[i + 1]
            y1 = self.fun(x1)
            y2 = self.fun(x2)
            a = integrate.quad(self.fun, self.ext[i], self.ext[i+1])[0]
            y = lambda x: (((y2 - y1) * x) + (x2 * y1 - x1 * y2)) / (x2 - x1)
            b = integrate.quad(y, self.ext[i], self.ext[i+1])[0]
            self.integ_inten.append(b - a)

    def peak_height(self):
        for i in range(len(self.ext) - 1):
            t = np.linspace(self.ext[i], self.ext[i + 1], 200) ###
            x1 = self.ext[i]
            x2 = self.ext[i + 1]
            y1 = self.fun(x1)
            y2 = self.fun(x2)
            y = lambda x: (((y2 - y1) * x) + (x2 * y1 - x1 * y2)) / (x2 - x1)
            Max = 0
            for j in range(len(t) - 1):
                if y(t[j]) - self.fun(t[j]) > Max:
                    Max = y(t[j]) - self.fun(t[j])
            self.max_inten.append(Max)


    def show(self):
        self.main_win.show()

    def showOG(self):
        self.ui.charts.setCurrentWidget(self.ui.orig_gra)

    def showAP1(self):
        self.ui.charts.setCurrentWidget(self.ui.auto_peaks_1)

    def showAP2(self):
        self.ui.charts.setCurrentWidget(self.ui.auto_peaks_2)

    def showRP(self):
        self.ui.charts.setCurrentWidget(self.ui.rules_page)

    def showR(self):
        self.ui.charts.setCurrentWidget(self.ui.result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())