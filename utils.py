import subprocess
import os

def bash_command(bash_command:str):
    return str(subprocess.check_output(bash_command, shell=True))

def suppr(window):
    bash_command("xdotool key --window %d Delete"%window)

def echap(window):
    bash_command("xdotool key --window %d Escape"%window)

def click(x:int, y:int, window=None):
    bash_command("xdotool mousemove --window %d %d %d"%(window,
                                                        x, y))
    bash_command("xdotool click --window %d %d"%(window, 1))

def type_in_win(string, window=None):
    bash_command("xdotool type --delay 100 --window %d %s"%(window, string))

def get_window_by_name(name:str):
    output = bash_command("xdotool search --name '%s'" % name)
    return [int(x) for x in output[2:-3].split('\\n')]

def focus(window:str):
    bash_command("xdotool windowfocus %d"%(window))

def get_window_size(window:str):
    bash_command("xdotool search --name '%s'" % name)

#	wid_hex=`printf '%#12x\n' $1`
#	color=`xwd -silent -id $wid_hex | convert xwd:- -crop 1x1+$2+$3 text:`
#	echo $color |cut -d "(" -f 2 |cut -d ")" -f 1
def get_pixel_color(window:str):
    pass

def screen_capture(width, height, x, y, out, window):
    screen = "xwd -silent -id %s -out out.xwd"%window
    convert = "convert -crop \"%dx%d+%d+%d\" out.xwd %s "%(width,
            height, x, y, out)
    bash_command(screen)
    bash_command(convert)

def read_on_screenshot(window:str, filename:str):
    pass

if __name__ == "__main__":
    out = get_window_by_name("Dofus 2")[0]
    #move to 0 0
    click(230, 152, window=out)
    type_in_win("test", window=out)
    screen_capture(window=out,filename="out.png")
