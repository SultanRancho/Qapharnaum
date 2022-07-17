from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt, QMimeData)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import pickle
import os
from functools import partial
import time
import keyboard
from PyQt5.QtCore import *
import threading

global note_liste

note_liste = []

# Load save data
if os.path.exists("save.sv"):
    with open("save.sv", "rb") as fic:
        try:
            note_liste = pickle.load(fic)
        except:
            with open("save.sv", "wb") as fic2:
                fic2.write(pickle.dumps(note_liste))
            pass

app = QApplication(sys.argv)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Get usable screen area
        screensize = QDesktopWidget().availableGeometry()
        # Configure the windows
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # Hide windows top
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)

        # Set style of windows
        MainWindow.window().setStyleSheet(u"background-color:black;\nborder-style:solid;\nborder-width: 2px;\nborder-color: green;")

        # Choose windows size
        x = int(screensize.width()/3 * 2)
        y = screensize.y()
        width = screensize.width() - x
        height = screensize.height()

        # Assign geometry
        MainWindow.setGeometry(x, y, width + 5, height)

        # Create widget area
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Create scroll area
        self.scrollArea = QScrollArea(self.centralwidget)
        # Configure scroll area
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(10, int(height/2), width-20, int(height / 2)-10)
        self.scrollArea.setStyleSheet(u"border-width: 1px;")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Create widget scroll area
        self.scrollAreaWidgetContents = QWidget()
        # Configure widget scroll area
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setAlignment(Qt.AlignTop)

        # Add to scroll Area
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        def close():
            global running
            running = False
            MainWindow.close()

        # Create "close" button
        self.pushButton = QPushButton(self.centralwidget)
        # Configure "close" button
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"background-color:black;\ncolor: green;\nborder-color: green;\nborder-style: solid;\nborder-width: 2px;")
        self.pushButton.clicked.connect(close)

        def hide():
            sh_exist = True
            if not os.path.exists("key.k"):
                with open("key.k", "w") as key:
                    shortcut = QInputDialog.getText(self.pushButton_4, "Shortcut", "Enter the shortcut to use to wake up the application :", text="Ctrl+alt+n", flags=Qt.FramelessWindowHint)
                    if shortcut[1]:
                        key.write(shortcut[0])
                    else:
                        sh_exist = False

            if sh_exist:
                MainWindow.setVisible(False)

                if os.path.exists("key.k"):
                    with open("key.k", "r") as key:
                        keyboard.wait(key.read())
                        MainWindow.setVisible(True)
                        resize()

        def resize():
            screensize = QDesktopWidget().availableGeometry()

            global height, width, x, y

            # Choose windows size
            x = int(screensize.width() / 3 * 2)
            y = screensize.y()
            width = screensize.width() - x
            height = screensize.height()

            # Assign geometry
            MainWindow.setGeometry(x, y, width + 5, height)

            self.pushButton.setGeometry(QRect(10, 10, int(width / 3) - 20, int(height / 30)))

            self.pushButton_4.setGeometry(QRect(int(width / 3) * 2, 10, int(width / 3) - 20, int(height / 30)))

            self.label_2.adjustSize()
            self.label_2.move(int(width / 2 - self.label_2.width() / 2), self.pushButton.height() + 20)

            self.textEdit.setGeometry(
                QRect(10, self.label_2.y() + self.label_2.height() + 10, width - 20, int(height / 60 * 15)))

            self.pushButton_2.setGeometry(
                QRect(10, self.textEdit.y() + self.textEdit.height() + 10, int(width / 3), int(height / 30)))

            self.checkbox.adjustSize()
            self.checkbox.setGeometry(
                QRect(width - 10 - self.checkbox.width(), self.textEdit.y() + self.textEdit.height() + 10,
                      self.checkbox.width(), self.checkbox.height()))

            self.modify_button.setGeometry(QRect(self.pushButton_2.x() + self.pushButton_2.width() + 10,
                                                 self.textEdit.y() + self.textEdit.height() + 10, int(width / 3),
                                                 int(height / 30)))

            self.scrollArea.setGeometry(10, int(height / 2), width - 20, int(height / 2) - 10)

            index = 0
            for i in note_liste:
                if not i[2]:
                    self.verticalLayout.itemAt(index).layout().itemAt(1).widget().setText(wrap("<html>"+i[0]+"</html>"))
                index += 1

        # Create "hide" button
        self.pushButton_4 = QPushButton(self.centralwidget)
        # Configure "hide" button
        self.pushButton_4.setObjectName(u"pushButton")
        self.pushButton_4.setStyleSheet(
            u"background-color:black;\ncolor: green;\nborder-color: green;\nborder-style: solid;\nborder-width: 2px;")
        self.pushButton_4.clicked.connect(hide)

        # Create "Notes" Label
        self.label_2 = QLabel(self.centralwidget)
        # Configure "Notes" Label
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 8pt \"MS Shell Dlg 2\";\nfont-size: 50px;\ncolor: green;\nanchor: center;\nborder:none;")

        # Create Text Entry
        self.textEdit = QPlainTextEdit(self.centralwidget)
        # Configure Text Entry
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"color: green; font-size: 15px;")

        def add():
            with open("save.sv", "wb") as fic:
                date = str(time.localtime().tm_mday)+"/"+str(time.localtime().tm_mon)+"/"+str(time.localtime().tm_year)+" "+str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)
                note_liste.insert(0, [self.textEdit.toPlainText(), date, self.checkbox.checkState()])
                fic.write(pickle.dumps(note_liste))
                refresh()
                rem_modify()

        # Create "Add" Button
        self.pushButton_2 = QPushButton(self.centralwidget)
        # Configure "Add" Button
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"color:green;")
        self.pushButton_2.clicked.connect(add)

        self.checkbox = QCheckBox(self.centralwidget)
        self.checkbox.setText("Display as HTML")
        self.checkbox.setStyleSheet("color: green; border: none")

        # Delete a note
        def delete(pos):
            note_liste.pop(pos)
            with open("save.sv", "wb") as fic:
                fic.write(pickle.dumps(note_liste))
                refresh()
                rem_modify()

        # Activ modify
        def modify(pos):
            rem_modify()
            global height, width, x, y
            self.checkbox.setCheckState(note_liste[pos][2])
            self.textEdit.setPlainText(note_liste[pos][0])
            self.modify_button.clicked.connect(lambda: set_modif(pos))
            self.modify_button.setGeometry(QRect(self.pushButton_2.x() + self.pushButton_2.width() + 10,
                                                 self.textEdit.y() + self.textEdit.height() + 10, int(width / 3),
                                                 int(height / 30)))
            MainWindow.layout().addWidget(self.modify_button)

        # Set modification
        def set_modif(pos):
            with open("save.sv", "wb") as fic:
                note_liste[pos][0] = self.textEdit.toPlainText()
                note_liste[pos][2] = self.checkbox.checkState()
                fic.write(pickle.dumps(note_liste))
                refresh()
                rem_modify()

        # Copy note
        def copy(pos):
            class AnotherWindow(QWidget):
                def __init__(self):
                    super().__init__()
                    # Configure windows
                    self.setWindowTitle(QCoreApplication.translate("Copy", u"Copy", None))

                    # Set windows size
                    copy_width = int(screensize.width() / 3)
                    copy_height = int(screensize.height() / 5 * 3)
                    copy_x = int(screensize.width() / 3)
                    copy_y = int(screensize.height() / 5)

                    self.setGeometry(copy_x, copy_y, copy_width, copy_height)

                    # Init layout
                    copy_layout = QVBoxLayout()

                    # Init text
                    if note_liste[pos][2] == 0:
                        copy_text = QPlainTextEdit()
                        copy_text.setPlainText(note_liste[pos][0])
                    else:
                        copy_text = QTextEdit()
                        copy_text.setText(note_liste[pos][0])

                    # Configure text
                    copy_text.setGeometry(0, 0, 400, 400)
                    copy_text.setEnabled(True)
                    copy_text.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
                    copy_text.setStyleSheet("border-style:solid; border-width: 1px; border-color: green;")

                    # Init copy button
                    copy_button = QPushButton()

                    # Configure copy button
                    copy_button.setText("Copy all")
                    copy_button.setStyleSheet("background-color: black; color: green; border-style:solid; border-width: 1px; border-color: green;")

                    cb = QApplication.clipboard()
                    cb.clear(mode=cb.Clipboard)

                    # Save actual state of the note
                    text = note_liste[pos][0]

                    # Copy as html
                    def mime_copy():
                        mimedata = QMimeData()
                        mimedata.setHtml(text)
                        cb.setMimeData(mimedata, mode=cb.Clipboard)

                    if note_liste[pos][2] == 0:
                        copy_button.clicked.connect(lambda: cb.setText(note_liste[pos][0], mode=cb.Clipboard))
                    else:
                        copy_button.clicked.connect(mime_copy)

                    # Configure display
                    self.setStyleSheet("background-color: black; color: green; font-size: 15px;")

                    copy_layout.addWidget(copy_text)
                    copy_layout.addWidget(copy_button)

                    self.setLayout(copy_layout)

            self.nw = AnotherWindow()
            self.nw.show()

        def move(pos):
            class AnotherWindow(QWidget):
                def __init__(self):
                    super().__init__()
                    # Configure windows
                    self.setWindowTitle(QCoreApplication.translate("Move", u"Move", None))

                    global actual_pos
                    actual_pos = pos

                    def go_up():
                        global actual_pos
                        if not actual_pos == 0:
                            add1 = note_liste[actual_pos]
                            add2 = note_liste[actual_pos-1]
                            note_liste.pop(actual_pos-1)
                            note_liste.pop(actual_pos-1)
                            note_liste.insert(actual_pos-1, add2)
                            note_liste.insert(actual_pos-1, add1)
                            actual_pos -= 1
                            refresh()
                            with open("save.sv", "wb") as fic:
                                fic.write(pickle.dumps(note_liste))

                    def go_down():
                        global actual_pos
                        if not actual_pos == len(note_liste)-1:
                            add1 = note_liste[actual_pos]
                            add2 = note_liste[actual_pos+1]
                            note_liste.pop(actual_pos)
                            note_liste.pop(actual_pos)
                            note_liste.insert(actual_pos, add1)
                            note_liste.insert(actual_pos, add2)
                            actual_pos += 1
                            refresh()
                            with open("save.sv", "wb") as fic:
                                fic.write(pickle.dumps(note_liste))

                    button_layout = QVBoxLayout()

                    self.setStyleSheet("border-style: solid; border-color: green; border-width: 2px; color: green; background-color: black;")

                    up_button = QPushButton()
                    up_button.setText("Go up")
                    up_button.setStyleSheet("border-style: solid; border-color: green; border-width: 2px; color: green; background-color: black; width: 90px; height: 20px;")
                    up_button.clicked.connect(go_up)
                    button_layout.addWidget(up_button)

                    move_button = QPushButton()
                    move_button.setText("Move")
                    move_button.setStyleSheet(
                        "border-style: solid; border-color: green; border-width: 2px; color: green; background-color: black; width: 90px; height: 20px;")

                    def go_move():
                        global actual_pos
                        new_pos = QInputDialog.getInt(move_button, "Move", "Enter the new places of this note:", actual_pos+1, 1, len(note_liste), 1)

                        n_pos = new_pos[0] - 1

                        if new_pos[1]:
                            if n_pos > actual_pos:
                                note_liste.insert(n_pos+1, note_liste[actual_pos])
                            elif n_pos < actual_pos:
                                note_liste.insert(n_pos, note_liste[actual_pos])

                            if n_pos > actual_pos:
                                note_liste.pop(actual_pos)
                            else:
                                note_liste.pop(actual_pos+1)

                            if n_pos == len(note_liste):
                                actual_pos = len(note_liste)-1
                            else:
                                actual_pos = n_pos

                            refresh()

                            with open("save.sv", "wb") as fic:
                                fic.write(pickle.dumps(note_liste))

                    move_button.clicked.connect(go_move)
                    button_layout.addWidget(move_button)

                    down_button = QPushButton()
                    down_button.setText("Go down")
                    down_button.setStyleSheet("border-style: solid; border-color: green; border-width: 2px; color: green; background-color: black; width: 90px; height: 20px;")
                    down_button.clicked.connect(go_down)
                    button_layout.addWidget(down_button)

                    self.setLayout(button_layout)

                    self.adjustSize()

            self.nw = AnotherWindow()
            self.nw.show()

        # Hide modification button
        def rem_modify():
            try:
                self.modify_button.deleteLater()
            except:
                pass

            # Reinit modify button
            self.modify_button = QPushButton()
            self.modify_button.setStyleSheet("color: green")
            self.modify_button.setText("Modify")
            self.modify_button.setGeometry(QRect(self.pushButton_2.x() + self.pushButton_2.width() + 10,
                                                 self.textEdit.y() + self.textEdit.height() + 10, int(width / 3),
                                                 int(height / 30)))

            # Clear text editor content
            self.textEdit.setPlainText("")

        self.modify_button = QPushButton()
        self.modify_button.setStyleSheet("color: green")
        self.modify_button.setText("Modify")

        def wrap(texte):
            # Init variables
            line = ""
            return_content = ""
            texte = texte[6: len(texte)-7]

            for i in texte:
                # Size line
                actual_text_size = QFontMetrics(QFont("Helvetica", 15)).width(line)

                scr_width = QDesktopWidget().availableGeometry().width() / 3 - 20

                i = i.replace("<", "&lt;")
                i = i.replace(">", "&gt;")

                if actual_text_size > scr_width:
                    return_content = return_content + line + "<br>"
                    line = ""
                    line = line + i
                elif i == "\n":
                    return_content = return_content + line + "<br>"
                    line = ""
                else:
                    line = line + i

            return_content = return_content + line

            return "<html>"+return_content+"</html>"

        # Refresh the note display
        def refresh():
            # Empty the notes liste
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(0).layout().itemAt(0).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(1).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(2).layout().itemAt(0).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(2).layout().itemAt(1).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(2).layout().itemAt(2).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(2).layout().itemAt(3).widget().deleteLater()
                self.verticalLayout.itemAt(0).layout().itemAt(2).layout().deleteLater()
                self.verticalLayout.removeItem(self.verticalLayout.itemAt(0))
            # Add the new notes
            for i in note_liste:
                # Create text entry label
                label_add = QLabel()
                label_date = QLabel(i[1])

                if i[2]:
                    label_add.setText(i[0])
                else:
                    label_add.setText(wrap("<html>"+i[0]+"</html>"))

                # Configure text label
                label_add.setStyleSheet("border: none; color: green; font-size: 15px; margin-top: 5px; font-family: Helvetica")
                label_add.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
                label_add.setTextInteractionFlags((Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse))
                label_add.setOpenExternalLinks(True)

                # Configure date label
                if note_liste.index(i) != 0:
                    label_date.setStyleSheet("border: none; color: green; font-size: 10px; margin-top: 30px;")
                else:
                    label_date.setStyleSheet("border: none; color: green; font-size: 10px;")
                label_date.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
                label_date.setTextInteractionFlags(Qt.TextSelectableByMouse)

                # Create "Delete" Button
                pushbutton_del = QPushButton()
                # Configure "Delete" Button
                pushbutton_del.setText("Delete")
                pushbutton_del.adjustSize()
                pushbutton_del.setStyleSheet("color: green; margin-top: 10px; padding: 2px; width: "+str(pushbutton_del.width() + pushbutton_del.width() / 10))

                # Create "Modify" Button
                pushbutton_mod = QPushButton()
                # Configure "Modify" Button
                pushbutton_mod.setText("Modify")
                pushbutton_mod.adjustSize()
                pushbutton_mod.setStyleSheet("color: green; margin-top: 10px; padding: 2px; width: "+str(pushbutton_mod.width() + pushbutton_mod.width() / 10))

                # Create "Copy" Button
                pushbutton_cop = QPushButton()
                # Configure "Copy" Button
                pushbutton_cop.setText("Copy")
                pushbutton_cop.adjustSize()
                pushbutton_cop.setStyleSheet("color: green; margin-top: 10px; padding: 2px; width: " + str(pushbutton_cop.width() + pushbutton_cop.width() / 10))

                # Create "Move" Button
                pushbutton_mov = QPushButton()
                # Configure "Move" Button
                pushbutton_mov.setText("Move")
                pushbutton_mov.adjustSize()
                pushbutton_mov.setStyleSheet("color: green; margin-top: 10px; padding: 2px; width: " + str(pushbutton_mov.width() + pushbutton_mov.width() / 10))

                # Create layout-s
                box = QVBoxLayout()
                button_box = QHBoxLayout()
                button_box.setAlignment(Qt.AlignLeft)

                # Adapte la taille des label
                label_add.adjustSize()
                label_date.adjustSize()
                pushbutton_mod.adjustSize()
                pushbutton_del.adjustSize()
                pushbutton_cop.adjustSize()
                pushbutton_mov.adjustSize()

                box.addWidget(label_date, alignment=Qt.AlignTop)
                box.addWidget(label_add, alignment=Qt.AlignTop)

                # Get the box position
                self.verticalLayout.addLayout(box)

                # set button function
                pushbutton_del.clicked.connect(partial(delete, self.verticalLayout.indexOf(box)))
                pushbutton_mod.clicked.connect(partial(modify, self.verticalLayout.indexOf(box)))
                pushbutton_cop.clicked.connect(partial(copy, self.verticalLayout.indexOf(box)))
                pushbutton_mov.clicked.connect(partial(move, self.verticalLayout.indexOf(box)))

                # Replace the box
                button_box.addWidget(pushbutton_mod, alignment=Qt.AlignTop)
                button_box.addWidget(pushbutton_del, alignment=Qt.AlignTop)
                button_box.addWidget(pushbutton_cop, alignment=Qt.AlignTop)
                button_box.addWidget(pushbutton_mov, alignment=Qt.AlignTop)

                box.addLayout(button_box)
                self.verticalLayout.removeItem(box)
                self.verticalLayout.addLayout(box)

        refresh()

        def adapt_screen():
            global running
            running = True
            prec = QDesktopWidget().availableGeometry()
            while running:
                if prec != QDesktopWidget().availableGeometry():
                    resize()
                prec = QDesktopWidget().availableGeometry()
                time.sleep(3)

        th1 = threading.Thread(target=adapt_screen)
        th1.start()

        # Configure windows composition
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        # Adjust Widget size
        self.pushButton.setGeometry(QRect(10, 10, int(width/3) - 20, int(height / 30)))

        self.pushButton_4.setGeometry(QRect(int(width/3)*2, 10, int(width/3) - 20, int(height / 30)))

        self.label_2.adjustSize()
        self.label_2.move(int(width / 2 - self.label_2.width() / 2), self.pushButton.height() + 20)

        self.textEdit.setGeometry(QRect(10, self.label_2.y() + self.label_2.height()+10, width - 20, int(height / 60 * 15)))

        self.pushButton_2.setGeometry(QRect(10, self.textEdit.y()+self.textEdit.height()+10, int(width / 3), int(height / 30)))

        self.checkbox.adjustSize()
        self.checkbox.setGeometry(QRect(width - 10 - self.checkbox.width(), self.textEdit.y()+self.textEdit.height()+10, self.checkbox.width(), self.checkbox.height()))

        self.modify_button.setGeometry(QRect(self.pushButton_2.x() + self.pushButton_2.width() + 10,
                                             self.textEdit.y() + self.textEdit.height() + 10, int(width / 3),
                                             int(height / 30)))

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        MainWindow.setProperty("WindowFlag", "")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Notes", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Add", None))


win = QMainWindow()
Ui_MainWindow().setupUi(win)
win.show()
app.exec_()