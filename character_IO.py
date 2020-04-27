import json

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog


def loadCharacter(self, clear=False):
    try:
        with open(self.pathToJson, 'r') as f:
            self.loadedCharacter = json.loads(f.read())
        self.backupCharacter = self.loadedCharacter
    except FileNotFoundError:
        notFoundWarning = QMessageBox()
        notFoundWarning.setWindowTitle(self.ui.label.text())
        notFoundWarning.setText("Файл не найден")
        notFoundWarning.setIconPixmap(QPixmap(
            "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        notFoundWarning.exec()
    except:
        errorReadingWarning = QMessageBox()
        errorReadingWarning.setWindowTitle(self.ui.label.text())
        errorReadingWarning.setText(
            "Ошибка загрузки, неверная структура файла.")
        errorReadingWarning.setIconPixmap(QPixmap(
            "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        errorReadingWarning.exec()
    else:
        if self.loadedCharacter["default"] == True:
            needClear = self.loadedCharacter["default"]
            loadCharacteristicsAndBonus(self, needClear)
            loadSavingThowsBonus(self, needClear)
            loadSkillsBonus(self, needClear)
            loadCharacterInfo(self, needClear)
            loadCharacterPersonality(self, needClear)
            loadD20BonusBox(self, needClear)
            loadLifeBox(self, needClear)
            self.loadedCharacter["default"] = False
        else:
            loadCharacteristicsAndBonus(self)
            loadSavingThowsBonus(self)
            loadSkillsBonus(self)
            loadCharacterInfo(self)
            loadCharacterPersonality(self)
            loadD20BonusBox(self)
            loadLifeBox(self)
            with open(self.pathToJson, 'w') as f:
                f.write(json.dumps(self.loadedCharacter,
                                   sort_keys=False, indent=2))


def loadCharacteristicsAndBonus(self, clear=False):
    characteristics = self.ui.characteristicBox.findChildren(
        QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            tempBase = self.loadedCharacter[
                "characteristic"][QLineEdit.accessibleName()]
            QLineEdit.setText(str(tempBase) if not clear else None)
            self.loadedCharacter["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int((tempBase - 10) / 2)

    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "bonus"):
            tempBonus = self.loadedCharacter[
                "characteristicBonus"][QLineEdit.accessibleName()]
            QLineEdit.setText(
                (("+" if tempBonus >= 0 else "") + str(tempBonus)) if not clear else None)


def loadSavingThowsBonus(self, clear=False):
    savingThrowsBool = self.ui.savingThrowsBox.findChildren(
        QtWidgets.QRadioButton)
    for QRadioButton in savingThrowsBool:
        QRadioButton.setChecked(self.loadedCharacter["savingThrowsBonus"][
                                QRadioButton.accessibleName()] if not clear else False)

    savingThrows = self.ui.savingThrowsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in savingThrows:
        tempBonus = self.loadedCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()]
        QLineEdit.setText((("+" if tempBonus >= 0 else "") +
                           str(tempBonus)) if not clear else None)


def loadSkillsBonus(self, clear=False):
    skillsBool = self.ui.skillsBox.findChildren(QtWidgets.QRadioButton)
    for QRadioButton in skillsBool:
        QRadioButton.setChecked(self.loadedCharacter["skillsBonus"][
                                QRadioButton.accessibleName()] if not clear else False)

    skills = self.ui.skillsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in skills:
        tempBonus = self.loadedCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()]
        QLineEdit.setText((("+" if tempBonus >= 0 else "") +
                           str(tempBonus)) if not clear else None)


def loadCharacterInfo(self, clear=False):
    charInfos = self.ui.charInfoBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in charInfos:
        QLineEdit.setText(
            str(self.loadedCharacter[QLineEdit.accessibleName()]) if not clear else None)


def loadCharacterPersonality(self, clear=False):
    personalities = self.ui.characterBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in personalities:
        QLineEdit.setText(
            str(self.loadedCharacter[QLineEdit.accessibleName()]) if not clear else None)


def loadD20BonusBox(self, clear=False):
    self.loadedCharacter["passiveWisdom"] = self.loadedCharacter[
        "characteristicBonus"]["wisdomBonus"]
    bonuses = self.ui.d20BonusBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in bonuses:
        tempBonus = self.loadedCharacter[QLineEdit.accessibleName()]
        QLineEdit.setText((("+" if tempBonus >= 0 else "") +
                           str(tempBonus)) if not clear else None)


def loadLifeBox(self, clear=False):
    lifeBoxValues = self.ui.lifeBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in lifeBoxValues:
        tempValues = self.loadedCharacter[QLineEdit.accessibleName()]
        QLineEdit.setText(str(tempValues) if not clear else None)

    successes = self.loadedCharacter["deathSaves"]["successes"]
    self.ui.successes_1.setChecked(
        (True if successes == 1 or successes == 2 or successes == 3 else False) if not clear else False)
    self.ui.successes_2.setChecked(
        (True if successes == 2 or successes == 3 else False) if not clear else False)
    self.ui.successes_3.setChecked(
        (True if successes == 3 else False) if not clear else False)

    failures = self.loadedCharacter["deathSaves"]["failures"]
    self.ui.failures_1.setChecked(
        (True if failures == 1 or failures == 2 or failures == 3 else False) if not clear else False)
    self.ui.failures_2.setChecked(
        (True if failures == 2 or failures == 3 else False) if not clear else False)
    self.ui.failures_3.setChecked(
        (True if failures == 3 else False) if not clear else False)


def saveCharacter(self):
    if self.fileIsNew:
        try:
            self.pathToJson = QFileDialog.getSaveFileName(
                self, "Open Character", "./default_data", "JSON (*.json)")[0]
            saveCharacteristicsAndBonus(self)
            saveSavingThowsBonus(self)
            saveSkillsBonus(self)
            saveCharacterInfo(self)
            saveCharacterPersonality(self)
            saveD20BonusBox(self)
            saveLifeBox(self)
        except FileNotFoundError:
            notFoundWarning = QMessageBox()
            notFoundWarning.setWindowTitle(self.ui.label.text())
            notFoundWarning.setText("Файл не найден")
            notFoundWarning.setIconPixmap(QPixmap(
                "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            notFoundWarning.exec()
        except:
            errorReadingWarning = QMessageBox()
            errorReadingWarning.setWindowTitle(self.ui.label.text())
            errorReadingWarning.setText(
                "Ошибка.")
            errorReadingWarning.setIconPixmap(QPixmap(
                "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            errorReadingWarning.exec()
        else:
            try:
                with open(self.pathToJson, 'w') as f:
                    f.write(json.dumps(self.loadedCharacter,
                                       sort_keys=False, indent=2))
            except:
                errorReadingWarning = QMessageBox()
                errorReadingWarning.setWindowTitle(self.ui.label.text())
                errorReadingWarning.setText(
                    "Ошибка. Путь не выбран.")
                errorReadingWarning.setIconPixmap(QPixmap(
                    "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                errorReadingWarning.exec()
    else:
        try:
            saveCharacteristicsAndBonus(self)
            saveSavingThowsBonus(self)
            saveSkillsBonus(self)
            saveCharacterInfo(self)
            saveCharacterPersonality(self)
            saveD20BonusBox(self)
            saveLifeBox(self)
        except:
            errorReadingWarning = QMessageBox()
            errorReadingWarning.setWindowTitle(self.ui.label.text())
            errorReadingWarning.setText(
                "Ошибка. Путь не выбран.")
            errorReadingWarning.setIconPixmap(QPixmap(
                "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            errorReadingWarning.exec()
        else:
            with open(self.pathToJson, 'w') as f:
                f.write(json.dumps(self.loadedCharacter,
                                   sort_keys=False, indent=2))


def saveCharacteristicsAndBonus(self, clear=False):
    characteristics = self.ui.characteristicBox.findChildren(
        QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            self.loadedCharacter["characteristic"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0
            self.loadedCharacter["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int((self.loadedCharacter["characteristic"][QLineEdit.accessibleName()] - 10) / 2)

    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "bonus"):
            self.loadedCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveSavingThowsBonus(self, clear=False):
    savingThrowsBool = self.ui.savingThrowsBox.findChildren(
        QtWidgets.QRadioButton)
    for QRadioButton in savingThrowsBool:
        self.loadedCharacter["savingThrowsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    savingThrows = self.ui.savingThrowsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in savingThrows:
        self.loadedCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
            QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveSkillsBonus(self, clear=False):
    skillsBool = self.ui.skillsBox.findChildren(QtWidgets.QRadioButton)
    for QRadioButton in skillsBool:
        self.loadedCharacter["skillsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    skills = self.ui.skillsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in skills:
        self.loadedCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()] = int(QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveCharacterInfo(self, clear=False):
    charInfos = self.ui.charInfoBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in charInfos:
        self.loadedCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def saveCharacterPersonality(self, clear=False):
    personalities = self.ui.characterBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in personalities:
        self.loadedCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def saveD20BonusBox(self, clear=False):
    self.loadedCharacter["characteristicBonus"][
        "wisdomBonus"] = self.loadedCharacter["passiveWisdom"]

    bonuses = self.ui.d20BonusBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in bonuses:
        self.loadedCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveLifeBox(self, clear=False):
    lifeBoxValues = self.ui.lifeBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in lifeBoxValues:
        self.loadedCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0

    howManySuccessesChecked = 0
    if self.ui.successes_1.isChecked():
        howManySuccessesChecked = 1
    if self.ui.successes_2.isChecked():
        howManySuccessesChecked = 2
    if self.ui.successes_3.isChecked():
        howManySuccessesChecked = 3
    self.loadedCharacter["deathSaves"]["successes"] = howManySuccessesChecked

    howManyFailuresChecked = 0
    if self.ui.failures_1.isChecked():
        howManyFailuresChecked = 1
    if self.ui.failures_2.isChecked():
        howManyFailuresChecked = 2
    if self.ui.failures_3.isChecked():
        howManyFailuresChecked = 3
    self.loadedCharacter["deathSaves"]["failures"] = howManyFailuresChecked


def backupCharacter(self):
    if self.fileIsNew:
        pass
    else:
        try:
            backupCharacteristicsAndBonus(self)
            backupSavingThowsBonus(self)
            backupSkillsBonus(self)
            backupCharacterInfo(self)
            backupCharacterPersonality(self)
            backupD20BonusBox(self)
            backupLifeBox(self)
        except:
            print("existed file error")
        else:
            with open(self.pathToJson.replace(".json", "_bck.json"), 'w') as f:
                f.write(json.dumps(self.backupCharacter,
                                   sort_keys=False, indent=2))


def backupCharacteristicsAndBonus(self, clear=False):
    characteristics = self.ui.characteristicBox.findChildren(
        QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            self.backupCharacter["characteristic"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0
            self.backupCharacter["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int((self.backupCharacter["characteristic"][QLineEdit.accessibleName()] - 10) / 2)

    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "bonus"):
            self.backupCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupSavingThowsBonus(self, clear=False):
    savingThrowsBool = self.ui.savingThrowsBox.findChildren(
        QtWidgets.QRadioButton)
    for QRadioButton in savingThrowsBool:
        self.backupCharacter["savingThrowsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    savingThrows = self.ui.savingThrowsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in savingThrows:
        self.backupCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
            QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupSkillsBonus(self, clear=False):
    skillsBool = self.ui.skillsBox.findChildren(QtWidgets.QRadioButton)
    for QRadioButton in skillsBool:
        self.backupCharacter["skillsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    skills = self.ui.skillsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in skills:
        self.backupCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()] = int(QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupCharacterInfo(self, clear=False):
    charInfos = self.ui.charInfoBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in charInfos:
        self.backupCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def backupCharacterPersonality(self, clear=False):
    personalities = self.ui.characterBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in personalities:
        self.backupCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def backupD20BonusBox(self, clear=False):
    self.backupCharacter["characteristicBonus"][
        "wisdomBonus"] = self.backupCharacter["passiveWisdom"]

    bonuses = self.ui.d20BonusBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in bonuses:
        self.backupCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupLifeBox(self, clear=False):
    lifeBoxValues = self.ui.lifeBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in lifeBoxValues:
        self.backupCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0

    howManySuccessesChecked = 0
    if self.ui.successes_1.isChecked():
        howManySuccessesChecked = 1
    if self.ui.successes_2.isChecked():
        howManySuccessesChecked = 2
    if self.ui.successes_3.isChecked():
        howManySuccessesChecked = 3
    self.backupCharacter["deathSaves"]["successes"] = howManySuccessesChecked

    howManyFailuresChecked = 0
    if self.ui.failures_1.isChecked():
        howManyFailuresChecked = 1
    if self.ui.failures_2.isChecked():
        howManyFailuresChecked = 2
    if self.ui.failures_3.isChecked():
        howManyFailuresChecked = 3
    self.backupCharacter["deathSaves"]["failures"] = howManyFailuresChecked