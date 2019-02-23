__author__ = 'Ahmet Tolga Erdönmez'
__version__ = '1.0'
from PyQt5 import QtWidgets,QtGui
import sys
import musiclist_v2

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setWindowIcon(QtGui.QIcon('music.ico'))
        self.setWindowTitle('Music List')
        
        
    def setupUI(self):
        mainMenu = self.menuBar() 
        file_menu = mainMenu.addMenu('File')
        #File
        file_save = QtWidgets.QAction('Save TXT', self)
        file_save.setShortcut('Ctrl+S')
        
        file_add_song = QtWidgets.QAction('Add Song', self)
        file_add_song.setObjectName('file_add_song')
        file_add_song.setShortcut('Ctrl+A')
        
        file_delete_list = QtWidgets.QAction('Delete List', self)
        file_delete_list.setShortcut('Ctrl+D')

        file_quit = QtWidgets.QAction('Close', self)
        file_quit.setShortcut('Ctrl+Q')

        file_menu.addAction(file_save)
        file_menu.addAction(file_add_song)
        file_menu.addAction(file_delete_list)
        file_menu.addAction(file_quit)

        app_musiclist = musiclist_v2.App_Musiclist()
        self.setCentralWidget(app_musiclist)
        
        #Menu Events
        file_save.triggered.connect(app_musiclist.event_save_list_to_txt)
        file_add_song.triggered.connect(app_musiclist.event_add_song)
        file_delete_list.triggered.connect(app_musiclist.event_delete_list)
        file_quit.triggered.connect(self.close)
            
        
        

        self.setGeometry(750,100,500,500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("music.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show()
        
        
app = QtWidgets.QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
window = MainWindow()
sys.exit(app.exec_())
