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