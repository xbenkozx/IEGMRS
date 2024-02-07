class Callsign:
    id          = 0
    callsign    = ""
    name        = ""
    lat         = ""
    lng         = ""

    def __init__(self, data=None):
        self.id         = 0
        self.callsign   = ""
        self.name       = ""
        self.lat        = ""
        self.lng        = ""

        if data != None:
            self.id         = data['id']
            self.callsign   = data['callsign']
            self.name       = data['name']
            self.lat        = data['lat']
            self.lng        = data['lng']

    def makeCrossList(self, min_ss):
        self.rx_cs = []
        for rx in self.rx_list:
            if int(rx.ss) >= min_ss:
                self.rx_cs.append(rx.rx)

        # Create simple TX callsign list. This is a stripped down list from the RX callsigns list listing only the callsigns and no other data.
        self.tx_cs = []
        for tx in self.tx_list:
            if int(tx.ss) >= min_ss:
                self.tx_cs.append(tx.tx)

        self.rx_tx_cs = []
        for tx in self.tx_cs:
            if tx in self.rx_cs:
                self.rx_tx_cs.append(tx)