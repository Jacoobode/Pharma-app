from PyQt5.QtWidgets import QApplication
from logic_funcs import LogicFuncs

app = QApplication([])
window = LogicFuncs()
window.start()
app.exec_()