from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys
import requests
import os
import urllib.request

class song():
    def __init__(self,name,artist,album):
        self.name = name
        self.artist = artist
        self.album = album
    def __str__(self):
        return "{} by {} | Album: {}".format(self.name,self.artist,self.album)

class App_Musiclist(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.connectdb()
        self.countbtn = 0
    def connectdb(self):
        try:
            os.remove("musiclist.db")
        except FileNotFoundError:
            pass
        self.connection = sqlite3.connect("musiclist.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE musiclist (song_name TEXT,song_artist TEXT,song_album TEXT)")
        self.connection.commit()
    def setupUi(self):
        #CREATING WIDGETS
        self.save_list_txt = QtWidgets.QPushButton("Save List to TXT")
        self.delete_list = QtWidgets.QPushButton("Delete Current List")
        self.add_song = QtWidgets.QPushButton("Add Song")
        self.add_song.setObjectName('add_song_btn')
        self.add_song_field = QtWidgets.QLineEdit()
    
        #STYLE
        self.save_list_txt.setStyleSheet("color: rgb(162, 16, 26);")
        self.delete_list.setStyleSheet("color: rgb(162, 16, 26);")
        self.add_song.setStyleSheet("color: rgb(162, 16, 26);")
        
        #SETTING LAYOUT
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.add_song)
        h_box.addWidget(self.add_song_field)
        h_box.addWidget(self.delete_list)
        h_box.addWidget(self.save_list_txt)
        self.v_box_2 = QtWidgets.QVBoxLayout()
        self.v_box = QtWidgets.QVBoxLayout()
        self.v_box.addLayout(h_box)
        self.v_box.addLayout(self.v_box_2)
        self.v_box.addStretch()
        
        #EVENTS
        self.add_song.clicked.connect(self.event_add_song)
        self.delete_list.clicked.connect(self.event_delete_list)
        self.save_list_txt.clicked.connect(self.event_save_list_to_txt)
        
        
        #WINDOW PROPERTIES
        self.setLayout(self.v_box)
        #self.setGeometry(700,100,750,500)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("music.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.setWindowTitle("Music List")

        
    def get_song_from_lastfm(self,song_name):
        try:
            # GETTING TRACK & ARTIST
            track_url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track={}&api_key=31873cc90c27539710b2e41cf3a7ef24&format=json".format(
                song_name)
            track_val = requests.get(track_url).json()
            
            # GETTING ALBUM FROM TRACK
            album_url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=31873cc90c27539710b2e41cf3a7ef24&artist={}&track={}&format=json".format(track_val["results"]["trackmatches"]["track"][0]["artist"],track_val["results"]["trackmatches"]["track"][0]["name"])
            album_val = requests.get(album_url).json()
            
            song_info = [album_val["track"]["name"], album_val["track"]["artist"]["name"],album_val["track"]["album"]["title"]]
            
            return song_info
        except:
            return False
      
    def event_add_song(self):
        from_who = self.sender().objectName()
        if from_who == 'add_song_btn':
            get_input = self.add_song_field.text()
            song_info = self.get_song_from_lastfm(get_input)
        elif from_who == 'file_add_song':
            text, okPressed = QtWidgets.QInputDialog.getText(self, "Add Song","Song Name: ", QtWidgets.QLineEdit.Normal, "")
            song_info = self.get_song_from_lastfm(text)

        if song_info == False:
            pass
        else:
            track = song(song_info[0],song_info[1],song_info[2])
            self.cursor.execute("INSERT INTO musiclist Values(?,?,?)",(song_info[0],song_info[1],song_info[2]))
            self.connection.commit()
            self.add_label = QtWidgets.QLabel(str(track))
            self.add_label.setObjectName(song_info[0])
            #Create Widgets & Layout
            self.new_h_box = QtWidgets.QHBoxLayout()
            self.new_h_box.setObjectName("delhbox|{}".format(self.countbtn))
            new_del_btn = QtWidgets.QPushButton("X")
            new_del_btn.setObjectName("delbtn|{}".format(self.countbtn))
            new_img = QtWidgets.QLabel()
            #Getting img and create img
            #getting url
            track_url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=31873cc90c27539710b2e41cf3a7ef24&artist={}&track={}&format=json".format(song_info[1],song_info[0])
            track_val = requests.get(track_url).json()
            url = track_val['track']['album']['image'][1]['#text'] 
            if url == '':
                new_img.setPixmap(QtGui.QPixmap('music.ico').scaled(64, 64, QtCore.Qt.KeepAspectRatio))
            else:
                data = urllib.request.urlopen(url).read()
                image = QtGui.QImage()
                image.loadFromData(data)
                new_img.setPixmap(QtGui.QPixmap(image))

            #Add items to layout & setting to v_box_2
            self.new_h_box.addWidget(new_img)
            self.new_h_box.addWidget(self.add_label)
            self.new_h_box.addStretch()
            self.new_h_box.addWidget(new_del_btn)
            self.v_box_2.addLayout(self.new_h_box)
            self.countbtn += 1
            new_del_btn.clicked.connect(self.del_selected_item)
        self.add_song_field.clear()
        
    def del_selected_item(self):
        btn = self.sender().objectName()
        number = btn.split("|")[1]
        layout = self.findChild(QtCore.QObject, "delhbox|{}".format(number))
        song_name = layout.itemAt(1).widget().objectName()
        self.cursor.execute("DELETE FROM musiclist WHERE song_name = ?",(song_name,))
        self.connection.commit()
        self.clearLayout(layout)
        
    def event_save_list_to_txt(self):
        self.cursor.execute("SELECT * FROM musiclist")
        current_songs = self.cursor.fetchall()
        if len(current_songs) == 0:
            msg_box = QtWidgets.QMessageBox.warning(self, 'Empty List!', "Empty List!", QtWidgets.QMessageBox.Ok)
        else:
            save_to_where = QtWidgets.QFileDialog.getSaveFileName(self, "Save Your List to ?", os.getenv("HOME"),"Text Files (*.txt)")
            try:
                with open(save_to_where[0],"w",encoding = "utf-8") as file:
                    for i in current_songs:
                        add_this = song(i[0],i[1],i[2])
                        file.write(str(add_this) + '\n')
                msg_box = QtWidgets.QMessageBox.warning(self, 'List Saved !', "List Saved !", QtWidgets.QMessageBox.Ok)
            except FileNotFoundError:
                pass

    def event_delete_list(self):
        self.clearLayout(self.v_box_2)
        self.countbtn = 0
        self.cursor.execute("DELETE FROM musiclist")

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())



            
# app = QtWidgets.QApplication(sys.argv)
# ui = App_Musiclist()
# sys.exit(app.exec_())

