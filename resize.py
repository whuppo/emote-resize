import os, subprocess
from tkinter import *
from tkinter import messagebox
from TkinterDnD2 import *
from PIL import Image
import zipfile

current_version = 1.2

class ListObject:
    def __init__( self, name, fullpath, filt, mode ):
        self.name = name
        self.fullpath = fullpath
        self.location = os.path.dirname( fullpath )
        self.filt = filt
        self.mode = mode

    def __str__( self ):
        modes = [
            "processing",
            "completed",
            "INVALID"
        ]
        return self.name + " (" + self.filt + ")" + " \u2013 " + modes[ self.mode ]

root = TkinterDnD.Tk()
root.withdraw()
root.title( "Resizer " + str( current_version ) )
root.grid_rowconfigure( 1, weight=1, minsize=250 )
root.grid_columnconfigure( 0, weight=1, minsize=300 )
root.resizable( False, False )

title = StringVar()
Label( root, textvariable=title ).grid(
    row=0, column=0, padx=10, pady=5
)
title.set( "Drag and drop files here:" )

listbox = Listbox( root, name='dnd_resize',
    selectmode='single', width=1, height=1 )
listbox.config( activestyle="none" )
listbox.grid(
    row=1, column=0, padx=5, pady=5, sticky='NEWS'
)

listbox.dirs = []

zipbox = IntVar()
Checkbutton( root, text="Package as ZIP", variable=zipbox).grid(
    row=2, column=0, padx=8, pady=0, sticky=W
)

filters = (
    "Nearest Neighbor",
    "Box",
    "Bilinear",
    "Hamming",
    "Bicubic",
    "Lanczos"
)
img_filters = (
    Image.NEAREST,
    Image.BOX,
    Image.BILINEAR,
    Image.HAMMING,
    Image.BICUBIC,
    Image.LANCZOS
)
filtersvar = StringVar()
filtersvar.set( filters[3] )

filterlabel = StringVar()
Label( root, textvariable=filterlabel ).grid(
    row=3, column=0, padx=8, pady=0, sticky=W
)
filterlabel.set( "Filter" )
OptionMenu( root, filtersvar, *filters ).grid(
    row=3, column=0, padx=40, pady=0, sticky=W
)

def drop_enter( event ):
    event.widget.focus_force()
    return event.action

def suffix( location ):
    suffix = 0
    ext = os.path.splitext( location )
    while os.path.exists( location ):
        suffix += 1
        if suffix == 1:
            location = ext[0] + " (" + str( suffix ) + ")" + ext[1]
        else:
            location = ext[0][:-3 - len( str( suffix ) ) ] + " (" + str( suffix ) + ")" + ext[1]
    return location

def drop( event ):
    if event.data:
        if event.widget == listbox:
            files = listbox.tk.splitlist( event.data )
            if zipbox.get():
                zipf = zipfile.ZipFile( os.path.dirname( files[0] ) + '\\' + os.path.splitext( os.path.basename( files[0] ) )[0] + '-batch.zip', 'w' )
            title.set( "Processing..." )
            for f in files:
                file = ListObject( os.path.basename( f ), os.path.realpath( f ), filtersvar.get(), 0 )
                if os.path.exists( f ) and os.path.isfile( f ) and os.path.splitext( f )[1] == ".png":
                    listbox.insert( END, file )
                    
                    im = Image.open( f )
                    width, height = im.size
                    location = suffix( file.location + "\\" + os.path.splitext( file.name )[0] + str( int( height/2 ) ) + ".png" )
                    im.copy().resize( ( int( width/2 ), int( height/2 ) ), img_filters[filters.index( filtersvar.get() )] ).save( location )
                    location = suffix( file.location + "\\" + os.path.splitext( file.name )[0] + str( int( height/4 ) ) + ".png" )
                    im.copy().resize( ( int( width/4 ), int( height/4 ) ), img_filters[filters.index( filtersvar.get() )] ).save( location )
                    
                    file.mode = 1
                    listbox.delete( END )
                    listbox.insert( END, file )
                    listbox.dirs.append( file.fullpath )
                else:
                    file.mode = 2
                    listbox.insert( END, file )
                if zipbox.get():
                    for i in range( 1, 4 ):
                        if i == 1:
                            path = file.location + "\\" + os.path.splitext( file.name )[0] + ".png"
                        else:
                            if i == 3: i = 4
                            path = file.location + "\\" + os.path.splitext( file.name )[0] + str( int( height/i ) ) + ".png"
                        zipf.write( path, os.path.basename( path ), zipfile.ZIP_DEFLATED )
            title.set( "Drag and drop files here:" )
            if zipbox.get():
                listbox.insert( END, os.path.splitext( os.path.basename( files[0] ) )[0] + '-batch.zip' )
                listbox.dirs.append( file.location + "\\" + os.path.splitext( os.path.basename( files[0] ) )[0] + '-batch.zip' )
                zipf.close()

def open_dir( event ):
    to_open = listbox.dirs[ listbox.curselection()[0] ]
    if os.path.isfile( to_open ):
        subprocess.Popen( "explorer /select,\"" + to_open + "\"")
    else:
        messagebox.showerror( "Error", "Cannot open directory, file doesn't exist!" )

listbox.bind( "<Double-Button-1>", open_dir )
listbox.drop_target_register( DND_FILES )
listbox.dnd_bind('<<DropEnter>>', drop_enter)
listbox.dnd_bind('<<Drop>>', drop)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root.update_idletasks()
root.deiconify()
icon = PhotoImage( file=resource_path( 'resize.png' ) )
root.iconphoto( True, icon )
root.mainloop()