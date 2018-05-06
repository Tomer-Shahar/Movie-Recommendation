

import sys
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QMessageBox
from qtpy import QtCore


class recommenderGui:

  def __init__(self, controller):
    self.controller = controller
    self.mainWindow = None
    self.existingUserLoginWindow = None
    self.existingUserWindow = None
    self.visitorWindow = None
    self.newUserID = None

  #  the main function that opens the main window at the beginning
  def showMainWindow(self):
    app = QtWidgets.QApplication(sys.argv)
    self.mainWindow = QtWidgets.QMainWindow()
    self.mainWindow.setWindowIcon(QtGui.QIcon("GUI/film-reel.png") )
    self.mainWindow.ui = uic.loadUi('GUI/main_window.ui', self.mainWindow)
    self.mainWindow.existing_user_button.clicked.connect(self.openExisitingUserLoginWindow)
    self.mainWindow.visitorButton.clicked.connect(self.openVisitorWindow)
    self.mainWindow.show()
    sys.exit(app.exec_())

  def openVisitorWindow(self):
    self.visitorWindow = QtWidgets.QDialog()
    self.visitorWindow.setWindowIcon(QtGui.QIcon("GUI/film-reel.png") )
    self.visitorWindow = uic.loadUi('GUI/visitor_window.ui', self.visitorWindow)
    popularMovies = self.controller.get_top_movies_global(20)
    i = 0
    for movie_name in popularMovies:
      self.visitorWindow.popularTable.insertRow(i)
      year = movie_name[0][-5:-1]
      name = movie_name[0][0:-7]
      self.visitorWindow.popularTable.setItem(i,0,QTableWidgetItem(name))
      self.visitorWindow.popularTable.item(i,0).setFlags(QtCore.Qt.ItemIsEnabled)
      self.visitorWindow.popularTable.setItem(i,1,QTableWidgetItem(year))
      self.visitorWindow.popularTable.item(i,1).setFlags(QtCore.Qt.ItemIsEnabled)
      self.visitorWindow.popularTable.setItem(i,2,QTableWidgetItem(str(movie_name[1])))
      self.visitorWindow.popularTable.item(i,2).setFlags(QtCore.Qt.ItemIsEnabled)
      self.visitorWindow.popularTable.setItem(i,3,QTableWidgetItem(""))
      i = i+1
    self.visitorWindow.submit_button.clicked.connect(self.submit)
    header = self.visitorWindow.popularTable.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    self.visitorWindow.show()
    self.mainWindow.close()

  def submit(self):
    user_ratings = []
    success = False
    popularMovies = self.controller.get_top_movies_global(20)
    for i in range(0,20):
      rank_score = self.visitorWindow.popularTable.item(i,3).text()
       # if not rank_score.isdigit():
       # message_box = QMessageBox()
       # message_box.about(self.visitorWindow, "Wrong input", "Please ensure you've entered a number between 0 and 5.")
       # message_box.close()
       # self.visitorWindow.show()
       # break

      movie_to_rank = popularMovies[i][0]
      try:
        rank_number = float(rank_score)
        if rank_number < 0 or rank_number > 5:
          message_box = QMessageBox()
          message_box.about(self.visitorWindow, "Wrong input", "Please ensure you've entered a number between 0 and 5.")
          message_box.close()
          self.visitorWindow.show()
          break
        ranked_movie = (movie_to_rank, rank_number)
        user_ratings.append(ranked_movie)
        if i==19:
          success = True
      except ValueError:
        message_box = QMessageBox()
        message_box.about(self.visitorWindow, "Wrong input", "Please ensure you've entered a number between 0 and 5.")
        message_box.close()
        self.visitorWindow.show()
    if success:
      new_user_id = self.controller.add_user(user_ratings)
      self.newUserID = QtWidgets.QDialog()
      self.newUserID = uic.loadUi('GUI/new_user_id.ui', self.newUserID)
      self.newUserID.user_id_text.setText(str(new_user_id))
      self.newUserID.new_user_id_box.accepted.connect(self.returnToLoginWindow)
      self.newUserID.show()



  def openExisitingUserLoginWindow(self):
    self.existingUserLoginWindow = QtWidgets.QDialog()
    self.existingUserLoginWindow.setWindowIcon(QtGui.QIcon("GUI/film-reel.png") )
    self.existingUserLoginWindow = uic.loadUi('GUI/login_window.ui', self.existingUserLoginWindow)
    self.existingUserLoginWindow.login_button_box.accepted.connect(self.openExistingUserWindow)
    self.existingUserLoginWindow.input_id.setValidator(QIntValidator())
    self.existingUserLoginWindow.show()

  def openExistingUserWindow(self):

    user_id = self.existingUserLoginWindow.input_id.text()
    if user_id != '':
      if self.controller.user_exists(int(user_id)):
        num_of_movie = self.existingUserLoginWindow.comboBox.currentText()
        recommendations = self.controller.get_personal_recommendations(user_id, num_of_movie)
        self.existingUserWindow = QtWidgets.QDialog()
        self.existingUserWindow.setWindowIcon(QtGui.QIcon("GUI/film-reel.png") )
        self.existingUserWindow = uic.loadUi('GUI/existing_user_window.ui', self.existingUserWindow)
        i = 0
        for movie_name in recommendations:
          self.existingUserWindow.recommendationsTable.insertRow(i)
          year = movie_name[-5:-1]
          name = movie_name[0:-7]
          self.existingUserWindow.recommendationsTable.setItem(i,0,QTableWidgetItem(name))
          self.existingUserWindow.recommendationsTable.item(i,0).setFlags(QtCore.Qt.ItemIsEnabled)
          self.existingUserWindow.recommendationsTable.setItem(i,1,QTableWidgetItem(year))
          self.existingUserWindow.recommendationsTable.item(i,1).setFlags(QtCore.Qt.ItemIsEnabled)
          i = i+1
        self.existingUserLoginWindow.close()
        header = self.existingUserWindow.recommendationsTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.existingUserWindow.show()
        self.existingUserWindow.main_menu_button.clicked.connect(self.returnToMainWindow)
        self.existingUserWindow.login_button.clicked.connect(self.showLoginWindow)
      else:
        message_box = QMessageBox()
        message_box.about(self.visitorWindow, "Id not found", "Please enter a valid Id.")
        message_box.close()
        self.existingUserLoginWindow.show()
    else:
      message_box = QMessageBox()
      message_box.about(self.visitorWindow, "Missing id", "Be sure you enter your id.")
      message_box.close()
      self.existingUserLoginWindow.show()

  def returnToMainWindow(self):
    self.existingUserWindow.close()
    self.mainWindow.show()

  def showLoginWindow(self):
    self.existingUserWindow.close()
    self.existingUserLoginWindow.show()

  def returnToLoginWindow(self):
    self.visitorWindow.close()
    self.existingUserLoginWindow.show()

  def closeRecWindow(self, event):
    print("close")
    event.accept()




#class Dialogs(QDialog):
#  def closeEvent(self, event):
#    self.close()
