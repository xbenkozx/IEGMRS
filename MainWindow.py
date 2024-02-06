#Import global classes
import requests, json
from prettytable import PrettyTable

#Import PySide classes
from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem

#Import local classes
from ui.ui_mainwindow import Ui_MainWindow
from LocalDatabase import LocalDatabase
from RelayPath import RelayPath

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        #Setup Qt UI
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Add click actions to top menu
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSync.triggered.connect(self.downloadData)
        self.ui.actionAbout.triggered.connect(self.showAbout)

        #When callsign text box text is changed
        self.ui.callsignEdit.textChanged.connect(self.loadData)

        #When TX/RX selector is changed
        self.ui.txRxSelect.currentIndexChanged.connect(self.loadData)

        #Set table resize mode. This makes the table use the entire width of its parent
        self.ui.signalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Load db into variable
        self.ldb = LocalDatabase()

        #Search local database and display data. This starts as anb empty callsign, returning all entries.
        self.loadData()

        #Generate relay path tables
        self.generateRelayPaths()

    def downloadData(self):
        #Download all current data from the server and store it locally into database
        try:
            x = requests.get("https://erc.iegmrs.com/data/callsign/dump")   #Fetch all current data into json string
            self.ldb.syncCallsignData(json.loads(x.text))                   #Load string into array and push to database

            x = requests.get("https://erc.iegmrs.com/data/signal/dump")     #Fetch all current data into json string
            self.ldb.syncSignalData(json.loads(x.text))                     #Load string into array and push to database

        except requests.ConnectionError:
            #Fails when there is no internet connection.
            pass

        self.loadData()
        self.generateRelayPaths()

    def loadData(self):
        #Get callsign text
        callsign = self.ui.callsignEdit.text()

        #Get RX/TX dropdown and compare if it is selected 'RX' or 'TX'
        if self.ui.txRxSelect.currentText() == 'RX':
            #Fetch all callsigns that {callsign} heard 
            cs_data_list = self.ldb.fetchRxSignal(callsign)
        else:
            #Fetch all callsigns that heard {callsign}
            cs_data_list = self.ldb.fetchTxSignal(callsign)

        #Create table model and set table headers
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['RX', 'TX', 'SS', 'DATE', 'LAT/LNG'])

        #Loop through returned entries and insert into table
        for e in cs_data_list:
            row = []
            row.append(QStandardItem(e.rx))
            row.append(QStandardItem(e.tx))
            row.append(QStandardItem(e.ss))
            row.append(QStandardItem(e.date))
            row.append(QStandardItem(e.lat + ', ' + e.lng))
            model.appendRow(row)

        #Set model to table to display the results.
        self.ui.signalTableView.setModel(model)

    def generateRelayPaths(self):
        rp = RelayPath()
        rp.generateRelayPaths()

        #Output SS threshold
        output = f"PATH SS THRESHOLD: {rp.PATH_SS_THRESHOLD}\n\n"

        #Output Relay Signal Score table
        output += "RELAY SIGNAL SCORE\n"
        output += rp.score_table

        #Output Primary Relay Path table
        output += "\n\nRELAY PATH\n"
        output += rp.primary_relay_table
        output += '\n\n'

        #Output Isolated Callsigns table. These are callsigns that have entries for TX but no log for RX signals
        output += rp.non_contact_table

        self.ui.relayPathTextView.setPlainText(output)

    def showAbout(self):
        dlg = QMessageBox()
        dlg.setWindowTitle('About')
        dlg.setText('v0.1b')
        dlg.show()


    