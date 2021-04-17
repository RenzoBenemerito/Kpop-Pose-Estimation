from PyQt5.QtWidgets import QApplication

from views import StartWindow

app = QApplication([])
start_window = StartWindow()
start_window.resize(480, 720)
start_window.show()
app.exit(app.exec_())