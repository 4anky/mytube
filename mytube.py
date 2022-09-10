__version__ = "0.1.0"

from PyQt6.QtWidgets import QApplication
from gui import MyTubeWindow


app = QApplication([])
window = MyTubeWindow(version=__version__)
window.show()
app.exec()
