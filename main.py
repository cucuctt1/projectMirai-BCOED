import flet as ft
from assets.block import base_block as BB
from  assets.viewer import block_display as BD
import threading
from assets.renderer.updater import *
import time


def updatecycle(updater,sleeptime = 1/1000):

    while True:
        updater.update_sector()
        time.sleep(sleeptime)
updatethread = threading.Thread(target=updatecycle,args=(updater,),daemon=True)

def main(page:ft.Page):
    block_dis = BD.block_display(1000, 1000)
    block = BB.Base(215,200,10,10,block_dis)


    block_dis.installize(page, updater, "debug")
    updater.add_to_sector("debug", page)

    #page.debug = True

    page.theme_mode = "light"
    page.update()
    updatethread.start()
    pass


if __name__ == "__main__":
    ft.app(target=main)
    #application_status = False