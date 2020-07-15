import sys
from PIL import Image
from PySide2 import QtCore, QtWidgets, QtGui

class MainWindow( QtWidgets.QWidget ):
    def __init__( self ):
        QtWidgets.QWidget.__init__( self )
        self.setAcceptDrops( True )

        self.labelQueue = QtWidgets.QLabel( "Queue" )
        self.labelQueue.setAlignment( QtCore.Qt.AlignCenter )
        self.labelActions = QtWidgets.QLabel( "Actions" )
        self.labelActions.setAlignment( QtCore.Qt.AlignCenter )

        self.queue = QtCore.QStringListModel( [ "hello", "world" ] )
        self.listboxQueue = QtWidgets.QListView()
        self.listboxQueue.setFixedHeight( 200 )
        self.listboxQueue.setModel( self.queue )

        self.actions = QtCore.QStringListModel( [ "hello", "world" ] )
        self.listboxActions = QtWidgets.QListView()
        self.listboxActions.setModel( self.actions )

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget( self.labelQueue, 0, 0 )
        self.layout.addWidget( self.listboxQueue, 1, 0 )
        self.layout.addWidget( self.labelActions, 2, 0 )
        self.layout.addWidget( self.listboxActions, 3, 0 )
        self.setLayout( self.layout )

    def dragEnterEvent( self, e ):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent( self, e ):
        for url in e.mimeData().urls():
            file_name = url.toLocalFile()
            print( "Dropped file: " + file_name )
            self.queue.setStringList( self.queue.stringList() + [ file_name ] )

if __name__ == '__main__':
    app = QtWidgets.QApplication( sys.argv )
    window = MainWindow()
    window.setFixedSize( 250, 400 )
    window.setWindowTitle( "Resizer 2.0" )
    window.show()
    sys.exit( app.exec_() )