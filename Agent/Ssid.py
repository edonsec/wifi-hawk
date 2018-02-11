class Ssid:
    def __init__(self, db):
        self.db = db

    def get_clients(self, client=None):
        c = self.db.cursor()
        d = self.db.cursor()

        if client:
            search_criteria = 'and client = ?'
            search_params = (client,)
        else:
            search_criteria = ''
            search_params = ()

        for client in c.execute(
                'SELECT client, COUNT(*) amt from ssid_log WHERE proximity = 0 ' + search_criteria + 'GROUP BY client '
                                                                                                     'ORDER BY amt',
                search_params):
            ssid_list = []
            for ssid in d.execute('SELECT ssid FROM ssid_log WHERE client = ? AND proximity = 0', (client['client'],)):
                ssid_list.append(ssid['ssid'])

            yield {
                "client": client["client"],
                "ssid": ssid_list
            }
