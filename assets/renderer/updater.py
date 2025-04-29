import flet as ft


class Updater:
    def __init__(self):
        self.sector = {}
        self.sectorlist = []

    def create_sector(self,sector_name:str):
        self.sectorlist.append(sector_name)
        self.sector[sector_name] = []

    def add_to_sector(self,sector_name,update):
        self.sector[sector_name].append(update)

    def update_sector(self,sector = None):
        if sector != None:
            for item in self.sector[sector]:
                try:
                    item.update()
                except Exception as error:

                    print("err skip",error)

        else:
            #update all
            for sector_name in self.sectorlist:
                for item in self.sector[sector_name]:
                    try:
                        item.update()

                    except Exception as error:
                        self.sector[sector_name].remove(item)
                        print("err skip", error)


updater = Updater()
updater.create_sector("debug")