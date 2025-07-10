# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 837)
        MainWindow.setWindowIcon(QIcon("icon.png"))

        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #fdf9f4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10pt;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }

            QPushButton {
                background-color: #1e4f3f;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #286e5b;
            }

            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 6px;
                background: white;
            }

            QTabBar::tab {
                background: #eee;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 6px;
                margin: 2px;
            }

            QTabBar::tab:selected {
                background: #1e4f3f;
                color: white;
            }

            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 750, 341, 40))
        self.pushButton_2.setObjectName("pushButton_2")

        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setGeometry(QtCore.QRect(20, 480, 701, 261))
        self.tabWidget_2.setObjectName("tabWidget_2")

        tabs = [
            ("Type", "textEdit_2"),
            ("Created", "textEdit"),
            ("Updated", "textEdit_7"),
            ("Description", "textEdit_8"),
            ("State", "textEdit_9"),
            ("Indication", "textEdit_10"),
            ("Pharmacodynamics", "textEdit_11"),
            ("Toxicity", "textEdit_12"),
            ("Absorption", "textEdit_13"),
            ("Volume of distribution", "textEdit_14"),
            ("Food interactions", "textEdit_15"),
            ("Mechanism of action", "textEdit_16"),
        ]
        for label, obj_name in tabs:
            tab = QtWidgets.QWidget()
            edit = QtWidgets.QTextEdit(tab)
            edit.setGeometry(QtCore.QRect(0, 0, 701, 241))
            edit.setObjectName(obj_name)
            setattr(self, obj_name, edit)
            self.tabWidget_2.addTab(tab, label)

        # ზედა TabWidget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(200, 110, 441, 311))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.textEdit_3 = QtWidgets.QTextEdit(self.tab)
        self.textEdit_3.setGeometry(QtCore.QRect(0, -10, 441, 301))
        self.textEdit_3.setObjectName("textEdit_3")
        self.tabWidget.addTab(self.tab, "Description")

        self.tab_2 = QtWidgets.QWidget()
        self.textEdit_4 = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_4.setGeometry(QtCore.QRect(-10, -10, 451, 301))
        self.textEdit_4.setObjectName("textEdit_4")
        self.tabWidget.addTab(self.tab_2, "Other recommendations")

        # ComboBox
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(180, 50, 170, 31))
        self.comboBox.setObjectName("comboBox")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(355, 40, 171, 41))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 430, 171, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")

        # ListWidget
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 161, 381))
        self.listWidget.setObjectName("listWidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(550, 40, 120, 40))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(380, 750, 341, 40))
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 430, 200, 31))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 776, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Medicine Manager"))
        self.pushButton_2.setText(_translate("MainWindow", "➕ Add Medicine"))
        self.pushButton.setText(_translate("MainWindow", "🔍 Search"))
        self.pushButton_3.setText(_translate("MainWindow", "🗑️ Delete"))
        self.label.setText(_translate("MainWindow", "Name of medicine to add or delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
