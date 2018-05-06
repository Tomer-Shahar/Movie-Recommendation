

import sys
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog


class recommenderGui:

  def __init__(self, controller):
    self.controller = controller
    self.loginWindow = None
    self.mainWindow = None
    self.existingUserLoginWindow = None
    self.existingUserWindow = None
    self.visitorWindow = None

  #  the main function that opens the main window at the beginning
  def showMainWindow(self):
    app = QtWidgets.QApplication(sys.argv)
    self.mainWindow = QtWidgets.QMainWindow()
    self.mainWindow.ui = uic.loadUi('GUI/main_window.ui', self.mainWindow)
    self.mainWindow.existing_user_button.clicked.connect(self.openExisitingUserLoginWindow)
    self.mainWindow.visitorButton.clicked.connect(self.openVisitorWindow)
    self.mainWindow.show()
    sys.exit(app.exec_())

  def openVisitorWindow(self):
    self.visitorWindow = QtWidgets.QDialog()
    self.visitorWindow = uic.loadUi('GUI/visitor_window', self.visitorWindow)

  def openExisitingUserLoginWindow(self):
    self.existingUserLoginWindow = QtWidgets.QMainWindow()
    self.existingUserLoginWindow = uic.loadUi('GUI/login_window_2.ui', self.existingUserWindow)
    self.existingUserLoginWindow.login_button_box.accepted.connect(self.openExistingUserWindow)
    self.existingUserLoginWindow.show()
    self.mainWindow.close()
   # print(self.loginWindow.input_id.text())

  def openExistingUserWindow(self):
    self.existingUserWindow.main_menu_button.clicked.connect(showMainWindow)
    user_id = self.existingUserLoginWindow.input_id.text()
    num_of_movie = self.existingUserLoginWindow.comboBox.currentText()
    recommendations = self.controller.get_personal_recommendations(user_id, num_of_movie)
    self.existingUserWindow = QtWidgets.QMainWindow()
    self.existingUserWindow = uic.loadUi('GUI/existing_user_window_2.ui', self.existingUserWindow)
    i = 0
    for movie_name in recommendations:
      self.existingUserWindow.recommendationsTable.insertRow(i)
      year = movie_name[-5:-1]
      name = movie_name[0:-7]
      self.existingUserWindow.recommendationsTable.setItem(i,0,QTableWidgetItem(name))
      self.existingUserWindow.recommendationsTable.setItem(i,1,QTableWidgetItem(year))
      i = i+1
    self.existingUserWindow.show()
    self.existingUserLoginWindow.close()

  def showMainWindow(self):

  def closeRecWindow(self, event):
    print("close")
    event.accept()
""""""

class Dialogs(QDialog):
  def closeEvent(self, event):
    self.close()











class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = uic.loadUi('login_window.ui', self)


class ExistingUserWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ExistingUserWindow, self).__init__()
        self.ui = uic.loadUi('existing_user_window.ui', self)


class VisitorWindow(QtWidgets.QDialog):
    def __init__(self):
        super(VisitorWindow, self).__init__()
        self.ui = uic.loadUi('visitor_window.ui', self)

def openExisitingUserWindow(self):
    print("hey")
    existingUserWindow = ExistingUserWindow()
    existingUserWindow.show()
    print(self.loginWindow.input_id.text())



def openExisitingUserWindow():
    loginWindow = LoginWindow()
    loginWindow.show()


 ## try:
 #   coinN = int(input("Enter next coin: "))

 #   if coinN == "" and totalcoin == rand:
 #     print("Congratulations. Your calculations were a success.")
 #   if coinN == "" and totalcoin < rand:
 #     print("I'm sorry. You only entered", totalcoin, "cents.")

 # except ValueError: #   print("Invalid Input")
 # else:
 #   totalcoin = totalcoin + coin
    print("Connecting button")
    loginWindow.buttonBox.Ok.clicked.connect(openExisitingUserWindow)

   # if loginWindow.input_id.text() != "":
    #    loginWindow.buttonBox.Ok.clicked.connect(openExisitingUserWindow(loginWindow.input_id.text()))

   # if loginWindow.input_id.text() is not None:
   #     user_id_as_string = loginWindow.input_id.text()
   #     print(user_id_as_string)

"""
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    windtableow = MyWindow()
   # window.__getattribute__(recommendationsTable).insertRow(3)
    window.existing_user_button.clicked.connect(openExisitingUserWindow)
    #window = LoginWindow()
    table = QtWidgets.QTableWidget()
    .setRowCount(4)
    table.setColumnCount(2)
    #layout = QtWidgets.QVBoxLayout()
    #layout.addWidget(table)
    #window.setLayout(layout)
    h_box = QtWidgets.QHBoxLayout()
    h_box.addStretch()
    h_box.addWidget(table)
    h_box.addStretch()
    v_box = QtWidgets.QVBoxLayout()
    v_box.addWidget(table)
    v_box.addLayout(h_box)
    window.setLayout(v_box)
    window.show()

    sys.exit(app.exec_())
"""



##from Controller.Control import Controller
##from Model.Recommender import Parse
#class View:
#    def _init_(self, controller):
#        self.controller = controller
#        uic.loadUi('user_gui.ui', self)
#        self.show()
#
#    def mainWindow(self):
#
#        app = QtWidgets.QApplication(sys.argv)
#        #window = Window()
#        window = QtWidgets.QWidget()  # main window
#        window.setWindowTitle('TENS Movie Recommender')
#        window.setGeometry(600,300,600,600)
#        header = QtWidgets.QLabel(window)
#        header.setText('Welcome to TENS Movie Recommendation System!')
#        header.setGeometry(0,0,400,50)
#        header.font()
#        header.move(20,20)
#        ExistingUserButton = QtWidgets.QPushButton('Existing user')
#        ExistingUserButton.setGeometry(100, 100,30,100)
#        VisitorButton = QtWidgets.QPushButton('Just a visitor')
#        VisitorButton.setGeometry(50,50,100,100)
# #       VisitorButton.clicked.connect(func)
#        ExistingUserButton.clicked.connect(openLoginWindow)
#        v_box = QtWidgets.QVBoxLayout()
#        v_box.addWidget(ExistingUserButton)
#        v_box.addWidget(VisitorButton)
#        window.setLayout(v_box)
#  #      window.show()
#        sys.exit(app.exec_())
#
##def window():
##    app = QtWidgets.QApplication(sys.argv)
##    w = QtWidgets.QWidget()
##    w.setWindowTitle('TENS Movie Recommender')
##
##    l1 = QtWidgets.QLabel(w)
##    l2 = QtWidgets.QLabel(w)
##    l1.setText('Hello World')
##    l2.setPixmap(QtGui.QPixmap('globe.png'))
##    w.setGeometry(600, 250, 600, 600)
##    l1.move(100, 20)
##    l2.move(120, 90)
##    b = QtWidgets.QPushButton('Push Me')
##    l = QtWidgets.QLabel('Look at me')
##    h_box = QtWidgets.QHBoxLayout()
##    h_box.addStretch()
##    h_box.addWidget(l)
##    h_box.addStretch()
##    v_box = QtWidgets.QVBoxLayout()
##    v_box.addWidget(b)
##    v_box.addLayout(h_box)
##    w.setLayout(v_box)
##
##
##    w.show()
##    sys.exit(app.exec_())
##
##window()
##
##
#class Login(QtWidgets.QDialog):
#    def __init__(self, parent=None):
#        super(Login, self).__init__(parent)
#        self.controller = Controller()
#        self.ID = QtWidgets.QLineEdit(self)
#        self.buttonLogin = QtWidgets.QPushButton('Login', self)
#        self.buttonLogin.clicked.connect(self.handleLogin)
#        layout = QtWidgets.QVBoxLayout(self)
#        layout.addWidget(self.ID)
#        layout.addWidget(self.buttonLogin)
#
#    def handleLogin(self):
#        users = self.controller.getAllUsers()
#        id = int(self.ID.text())
#        if(id in users): #Existing user
#            print("hel")
#        else:
#            QtWidgets.QMessageBox.warning(
#            self, 'Error', 'User id does not exist in the system.')
#
#
#
#def openLoginWindow():
#    login = Login()
#    if login.exec_() == QtWidgets.QDialog.Accepted:
#        openLoggedInWindow
#
#
#def openLoggedInWindow():
#    loginWindow = QtWidgets.QWidget()
#    loginWindow.show()
#
##class Window(QtWidgets.QMainWindow):
##    def __init__(self, parent=None):
##        super(Window, self).__init__(parent)
##        # self.ui = Ui_MainWindow()
##        # self.ui.setupUi(self)
##
##def func():
##  print("helloooo")
##
##if __name__ == '__main__':
##
##
##
##
#
