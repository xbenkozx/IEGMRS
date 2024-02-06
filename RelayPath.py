
from prettytable import PrettyTable
from LocalDatabase import LocalDatabase

class RelayPath:
    PATH_SS_THRESHOLD = 3

    score_table             = ""
    primary_relay_table     = ""
    alternate_replay_table  = ""
    non_contact_table       = ""

    preferred_primary_callsign = ''
    exclude_node_callsigns = []

    def __init__(self):
        self.ldb = LocalDatabase()
    
    def generateRelayPaths(self):
        cs_data_list = self.ldb.fetchCallsigns()

        #Get all callsigns that are currently in the Signals table. These are the contactable stations. Excludes stations with a signal below the SS Threshold
        rx_cs_list = self.getContactableCallsignList(cs_data_list)

        #Based on the contactable callsign list, create a score based on the signal score summed from all stations that RX that specific station.
        score_list = self.createScoreList(cs_data_list, rx_cs_list)

        #Output SS threshold
        # output = f"PATH SS THRESHOLD: {RelayPath.PATH_SS_THRESHOLD}\n\n"

        #Output Relay Signal Score table
        table = PrettyTable()
        table.field_names = ['Callsign', 'Score', 'RX Count']
        for r in score_list:
            table.add_row([r['callsign'], r['score'], r['count']])
        self.score_table = str(table)

        #Output Primary Relay Path table
        relay_list, non_contact_list = self.createRelayList(cs_data_list, rx_cs_list, score_list)
        self.primary_relay_table = self.createRelayTable(relay_list)

        #Output Isolated Callsigns table. These are callsigns that have entries for TX but no log for RX signals
        table = PrettyTable()
        table.field_names = ['Isolated Callsigns']
        for r in sorted(non_contact_list):
            table.add_row([r])
        self.non_contact_table = str(table)

    def createRelayList(self, cs_data_list, rx_cs_list, score_list):
        non_contact_list = []
        relay_list = []
        
        #Assign Primary Contact
        primary_callsign = None

        #Assign Primary if a preferred callsign is set
        if self.preferred_primary_callsign != '':
            for s in score_list:
                if s['callsign'] == self.preferred_primary_callsign:
                    primary_callsign = self.getCallsignDataFromCallsign(cs_data_list, s['callsign'])
                    s['node_status'] = 1
                    relay_list.append(s)
                    break
        
        #If not preferred primary or preferred primary is not listed, assign primary based on highest SS score.
        if primary_callsign == None:
            for s in score_list:
                if s['callsign'] not in self.exclude_node_callsigns:
                    primary_callsign = self.getCallsignDataFromCallsign(cs_data_list, s['callsign'])
                    s['node_status'] = 1
                    relay_list.append(s)
                    break
        
        #Return empty list if primary callsign is not assigned.
        if primary_callsign == None:
            return [], []

        # Create simple RX callsign list. This is a stripped down list from the RX callsigns list listing only the callsigns and no other data.
        primary_callsign.rx_cs = []
        for rx in primary_callsign.rx_list:
            if int(rx.ss) >= RelayPath.PATH_SS_THRESHOLD:
                primary_callsign.rx_cs.append(rx.rx)
        primary_callsign.rx_cs.append(primary_callsign.callsign)

        
        #List callsigns that are contactable but not in the RX list of the primary contact
        missing_cs = []
        for cs in rx_cs_list:
            if cs not in primary_callsign.rx_cs:
                missing_cs.append(cs)

        #Loop through the score list
        for s in self.createScoreList(cs_data_list, missing_cs):
            #if the score list callsign is in the primary contact RX list and is not in the exluded callsigns.
            if s['callsign'] in primary_callsign.rx_cs and s['callsign'] not in self.exclude_node_callsigns:
                s['node_status'] = 2
                appendtolist = False

                #Loop through callsign RX list and check to see if any RX callsigns match in the missing callsigns list.
                for cs in s['cs_list']:
                    if cs in missing_cs:
                        appendtolist = True     
                        missing_cs.remove(cs)   #Remove contactable callsigns from missing callsigns list.

                if appendtolist:
                    relay_list.append(s)

        non_contact_list += missing_cs      #Append any remaining missing callsigns to the non-contact list.
        return relay_list, non_contact_list
    
    def getCallsignDataFromCallsign(self, cs_data_list, callsign):
        for cs_data in cs_data_list:
            if cs_data.callsign == callsign:
                return cs_data

    def getContactableCallsignList(self, cs_data_list):
        rx_cs_list = []
        for e in cs_data_list:
            for rx in e.rx_list:
                if int(rx.ss) >= RelayPath.PATH_SS_THRESHOLD:
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
                if int(rx.ss) >= RelayPath.PATH_SS_THRESHOLD and rx.rx in rx_cs_list:
                    score += int(rx.ss)
                    count += 1
                    cs_list.append(rx.rx)

            cs_list = sorted(cs_list)
            if score > 0:
                score_list.append({'callsign': e.callsign, 'score': score, 'count': count, 'cs_list': cs_list})

        score_list = sorted(score_list, key=lambda score_list: score_list['score'])
        score_list.reverse()
        return score_list
    
    def createRelayTable(self, relay_list):
        table = PrettyTable()
        table.field_names = ['Node', 'Callsign', 'RX Callsigns']
        for score in relay_list:
            cs_list = ""
            for cs in score['cs_list']:
                cs_list += cs + '\n'
            # cs_list = cs_list.strip()
            table.add_row([score['node_status'], score['callsign'], cs_list])
        return str(table)