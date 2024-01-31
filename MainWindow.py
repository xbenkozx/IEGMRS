import requests, json
from prettytable import PrettyTable

from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ui.ui_mainwindow import Ui_MainWindow
from LocalDatabase import LocalDatabase

PATH_SS_THRESHOLD = 3

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSync.triggered.connect(self.downloadData)
        self.ui.actionAbout.triggered.connect(self.showAbout)

        self.ui.callsignEdit.textChanged.connect(self.loadData)
        self.ui.txRxSelect.currentIndexChanged.connect(self.loadData)

        self.ui.signalTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ldb = LocalDatabase()

        self.loadData()
        self.generateRelayPaths()

    def downloadData(self):
        try:
            x = requests.get("https://erc.iegmrs.com/data/callsign/dump")
            self.ldb.syncCallsignData(json.loads(x.text))

            x = requests.get("https://erc.iegmrs.com/data/signal/dump")
            self.ldb.syncSignalData(json.loads(x.text))

        except requests.ConnectionError:
            pass #Offline

        self.loadData()
        self.generateRelayPaths()

    def loadData(self):
        callsign = self.ui.callsignEdit.text()
        if self.ui.txRxSelect.currentText() == 'RX':
            cs_data_list = self.ldb.fetchRxSignal(callsign)
        else:
            cs_data_list = self.ldb.fetchTxSignal(callsign)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['RX', 'TX', 'SS', 'DATE', 'LAT/LNG'])

        for e in cs_data_list:
            row = []
            row.append(QStandardItem(e.rx))
            row.append(QStandardItem(e.tx))
            row.append(QStandardItem(e.ss))
            row.append(QStandardItem(e.date))
            row.append(QStandardItem(e.lat + ', ' + e.lng))
            model.appendRow(row)

        self.ui.signalTableView.setModel(model)

    def generateRelayPaths(self):
        cs_data_list = self.ldb.fetchCallsigns()

        rx_cs_list = self.getContactableCallsignList(cs_data_list)
        score_list = self.createScoreList(cs_data_list, rx_cs_list)

        output = f"PATH SS THRESHOLD: {PATH_SS_THRESHOLD}\n\n"

        output += "RELAY SIGNAL SCORE\n"
        table = PrettyTable()
        table.field_names = ['Callsign', 'Score', 'RX Count']
        for r in score_list:
            table.add_row(r[:3])
        output += str(table)

        output += "\n\nPRIMARY RELAY PATH\n"
        relay_list, non_contact_list = self.createRelayList(cs_data_list, 0)
        output += self.createRelayTable(relay_list)

        output += "\n\nALTERNATE RELAY PATH\n"
        relay_list, non_contact_list = self.createRelayList(cs_data_list, 1)
        output += self.createRelayTable(relay_list)

        output += '\n\n'

        table = PrettyTable()
        table.field_names = ['Isolated Callsigns']
        for r in sorted(non_contact_list):
            table.add_row([r])
        output += str(table)

        self.ui.relayPathTextView.setPlainText(output)

    def showAbout(self):
        dlg = QMessageBox()
        dlg.setWindowTitle('About')
        dlg.setText('v0.1b')
        dlg.show()


    def createRelayList(self, cs_data_list, cs_score_idx):
        non_contact_list = []
        relay_list = []

        rx_cs_list = self.getContactableCallsignList(cs_data_list)
        score_list = self.createScoreList(cs_data_list, rx_cs_list)

        #Assign Primary List Primary Contact
        score_list[cs_score_idx].append('PRIMARY')
        relay_list.append(score_list[cs_score_idx])
        

        #Get primary data from score list
        primary_callsign = self.getCallsignDataFromCallsign(cs_data_list, score_list[cs_score_idx][0])
        

        # Create simple RX list
        primary_callsign.rx_cs = []
        for rx in primary_callsign.rx_list:
            if int(rx.ss) >= PATH_SS_THRESHOLD:
                primary_callsign.rx_cs.append(rx.rx)
        primary_callsign.rx_cs.append(primary_callsign.callsign)

        
        #List missing CS
        missing_cs = []
        for cs in rx_cs_list:
            if cs not in primary_callsign.rx_cs:
                missing_cs.append(cs)

        for s in self.createScoreList(cs_data_list, missing_cs):
            if s[0] in primary_callsign.rx_cs:
                s.append('SECONDARY')
                appendtolist = False
                for cs in s[3]:
                    if cs in missing_cs:
                        appendtolist = True
                        missing_cs.remove(cs)

                if appendtolist:
                    relay_list.append(s)

        non_contact_list += missing_cs
        return relay_list, non_contact_list
    
    def getCallsignDataFromCallsign(self, cs_data_list, callsign):
        for cs_data in cs_data_list:
            if cs_data.callsign == callsign:
                return cs_data

    def getContactableCallsignList(self, cs_data_list):
        rx_cs_list = []
        for e in cs_data_list:
            for rx in e.rx_list:
                if int(rx.ss) >= PATH_SS_THRESHOLD:
                    if rx.rx not in rx_cs_list:
                        rx_cs_list.append(rx.rx)

        return rx_cs_list

    def createScoreList(self, cs_data_list, rx_cs_list):
        score_list = []
        for e in cs_data_list:
            score = 0
            count = 0
            cs_list = []
            for rx in e.rx_list:
                if int(rx.ss) >= PATH_SS_THRESHOLD and rx.rx in rx_cs_list:
                    score += int(rx.ss)
                    count += 1
                    cs_list.append(rx.rx)

            cs_list = sorted(cs_list)
            if score > 0:
                score_list.append([e.callsign, score, count, cs_list])

        score_list = sorted(score_list, key=lambda score_list: score_list[1])
        score_list.reverse()
        return score_list
    
    def createRelayTable(self, relay_list):
        table = PrettyTable()
        table.field_names = ['Order', 'Callsign', 'Score', 'RX Count', 'RX Callsigns']
        for score in relay_list:
            cs_list = ""
            for cs in score[3]:
                cs_list += cs + '\n'
            # cs_list = cs_list.strip()
            table.add_row([score[4], score[0], score[1], score[2], cs_list])
        return str(table)