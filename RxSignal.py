class RxSignal:
    id      = 0
    tx      = ""
    rx      = ""
    ss      = ""
    date    = ""
    lat     = ""
    lng     = ""

    def __init__(self, data=None):
        self.id     = 0
        self.tx     = ""
        self.rx     = ""
        self.ss     = ""
        self.date   = ""

        if data != None:
            self.id      = data['id']
            self.tx      = data['tx']
            self.rx      = data['rx']
            self.ss      = data['ss']
            self.date    = data['date']

            if 'lat' in data.keys():
                self.lat = data['lat']
                self.lng = data['lng']