from utils import * 
import time

def screen_price(out="out.png"):
    screen_capture(width=470, height=160, x=430, y=152,
                   window=win,out=out)

def search_resource(resource:str):
    click(230, 152, window=win)
    type_in_win(resource, window=win)
    time.sleep(1)
    click(650, 160, window=win)
    time.sleep(1)


if __name__ == "__main__":
    win = get_window_by_name("Dofus 2")[0]
    focus(win)
    #move to 0 0
    search_resource("Ailes\ de\ Moskito\n")
    screen_price()

