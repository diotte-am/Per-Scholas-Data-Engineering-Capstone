class load():
    def __init__(self, data):
        # connect to the database, save connection as object
        self.data = data

    def load_data(self):
        print(len(self.data), "lines loaded.")