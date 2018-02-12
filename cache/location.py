class Location:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS location_cache (ssid TEXT, trilong INT, trilat INT, addr TEXT)')

    def store(self, ssid, long, lat, address):
        self.cursor.execute("REPLACE INTO location_cache VALUES (?, ?, ?, ?)", (ssid, long, lat, address))
        self.db.commit()

    def get(self, ssid):
        q = self.cursor.execute("SELECT ssid, trilong, trilat, addr, 1 AS cache FROM location_cache WHERE ssid = ?", (ssid,))

        return q.fetchall()

    def flush(self):
        self.cursor.execute("DELETE FROM location_cache")
        self.db.commit()
