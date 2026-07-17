from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from Encrypt import get_, Settings
import sys
from UI_Enigasma import Ui_MainWindow


class Enigma_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._set_rotors()
        self._set_reflector()
        self.ui.Plugboard_letters.activated[str].connect(self.selected_letter_in_plugin)
        self.ui.Letters_to_encrypt.activated[str].connect(self.selected_letter_to_encrypt)
        self.ui.Apply.clicked.connect(self.settings)

    def _set_rotors(self):
        rotors = get_("Rotor")
        for rotor in rotors:
            self.ui.First_rotor.addItem(rotor["Number"])
            self.ui.Second_rotor.addItem(rotor["Number"])
            self.ui.Third_rotor.addItem(rotor["Number"])

    def _set_reflector(self):
        reflectors = get_("Reflector")
        for reflector in reflectors:
            self.ui.Reflector.addItem(reflector["Number"])

    def selected_letter_in_plugin(self, text):
        self.ui.Plugboard_settings.insertPlainText(text)

    def selected_letter_to_encrypt(self, text):
        self.ui.Letters.insertPlainText(text)
        en_letter = self._settings.multi_encryption(text)
        self.ui.Encrypted_letters.insertPlainText(en_letter[0])
        self.ui.textBrowser.insertPlainText(en_letter[1])

    def settings(self):
        plugboard_settings = self.ui.Plugboard_settings.toPlainText()
        self.ui.Plugboard_settings.clear()
        reflector = self.ui.Reflector.currentText()
        Third_r = self.ui.Third_rotor.currentText()
        Second_r = self.ui.Second_rotor.currentText()
        First_r = self.ui.First_rotor.currentText()
        rotors_s = ""
        rotors_s += self.ui.Third_rotor_s.currentText()
        rotors_s += self.ui.Second_rotor_s.currentText()
        rotors_s += self.ui.First_rotor_s.currentText()
        rotors_p = ""
        rotors_p += self.ui.Third_rotor_p.currentText()
        rotors_p += self.ui.Second_rotor_p.currentText()
        rotors_p += self.ui.First_rotor_p.currentText()
        self._settings = Settings(plugboard_settings, reflector, Third_r, Second_r, First_r, rotors_s, rotors_p)


def guiMain(args):
    app = QApplication(args)
    window = Enigma_window()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    guiMain(sys.argv)
