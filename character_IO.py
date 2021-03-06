import json
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from jsonschema import validate, ValidationError


def displayWarningMessage(self, text, detailed=None):
    WarningMessage = QMessageBox()
    WarningMessage.setWindowTitle(self.ui.label.text())
    WarningMessage.setText(text)
    WarningMessage.setIconPixmap(QPixmap(
        "images/messages/warning").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    WarningMessage.setDetailedText(str(detailed))
    WarningMessage.exec()


def loadCharacter(self):
    try:
        with open(self.pathToJson, 'r', encoding="utf-8") as f:
            self.loadedCharacter = json.loads(f.read())
        self.backupCharacter = self.loadedCharacter
        validate(self.loadedCharacter, self.charSchema)
    except FileNotFoundError as e:
        displayWarningMessage(self, "[LOAD] Файл не найден.", e)
    except ValidationError as e:
        displayWarningMessage(self, "[LOAD] Файл не соответствует шаблону.", e)
    except Exception as e:
        displayWarningMessage(self, "[LOAD] Ошибка загрузки, выбран неверный файл или он повреждён.", e)
    else:
        needClear = self.loadedCharacter["default"]
        loadCharacteristicsAndBonus(self, needClear)
        loadSavingThowsBonus(self, needClear)
        loadSkillsBonus(self, needClear)
        loadCharacterInfo(self, needClear)
        loadCharacterPersonality(self, needClear)
        loadD20BonusBox(self, needClear)
        loadLifeBox(self, needClear)
        loadEquipmentBox(self, needClear)
        loadMoneyBox(self, needClear)
        self.loadedCharacter["default"] = False


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

    temper = self.ui.temperBox.findChildren(QtWidgets.QTextEdit)
    for QTextEdit in temper:
        QTextEdit.setText(
            str(self.loadedCharacter["personality"]["appearance"][QTextEdit.accessibleName()]) if not clear else None)

    temp = ""
    for features in self.loadedCharacter["personality"]["features"]:
        temp += str(features) + ", "
    temp = temp[:-2] if (temp[-2] == "," and temp[-1] == " ") else temp
    self.ui.featuresAndTraitsEdit.setText(temp if not clear else None)


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


def loadEquipmentBox(self, clear=False):
    temp = ""
    for equipment in self.loadedCharacter["equipment"]:
        temp += str(equipment) + ", "
    temp = temp[:-2] if (temp[-2] == "," and temp[-1] == " ") else temp
    self.ui.equipment.setText(temp) if not clear else self.ui.equipment.clear()


def loadMoneyBox(self, clear=False):
    moneyBoxValues = self.ui.moneyBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in moneyBoxValues:
        QLineEdit.setText(str(self.loadedCharacter["money"][
                                  QLineEdit.accessibleName()]) if not clear else None)


def saveCharacter(self):
    if self.fileIsNew:
        try:
            self.pathToJson = QFileDialog.getSaveFileName(
                self, "Open Character", "./saves", "JSON (*.json)")[0]
        except FileNotFoundError as e:
            displayWarningMessage(self, "[SAVE] Путь не выбран.", e)
            self.fileIsNew = True
        except Exception as e:
            displayWarningMessage(self, "[SAVE] Ещё какая-то ошибка.", e)
            self.fileIsNew = True
    saveCharacteristicsAndBonus(self)
    saveSavingThowsBonus(self)
    saveSkillsBonus(self)
    saveCharacterInfo(self)
    saveCharacterPersonality(self)
    saveD20BonusBox(self)
    saveLifeBox(self)
    saveEquipmentBox(self)
    saveMoneyBox(self)
    try:
        with open(self.pathToJson, 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.loadedCharacter,
                               sort_keys=False, indent=2))
    except FileNotFoundError as e:
        displayWarningMessage(self, "[SAVE] Путь не выбран.", e)
    except Exception as e:
        displayWarningMessage(self, "[SAVE] Ещё какая-то ошибка.", e)
    else:
        self.fileIsNew = False


def saveCharacteristicsAndBonus(self):
    characteristics = self.ui.characteristicBox.findChildren(
        QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            self.loadedCharacter["characteristic"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0
            self.loadedCharacter["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int(
                (self.loadedCharacter["characteristic"][QLineEdit.accessibleName()] - 10) / 2)

    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "bonus"):
            self.loadedCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveSavingThowsBonus(self):
    savingThrowsBool = self.ui.savingThrowsBox.findChildren(
        QtWidgets.QRadioButton)
    for QRadioButton in savingThrowsBool:
        self.loadedCharacter["savingThrowsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    savingThrows = self.ui.savingThrowsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in savingThrows:
        self.loadedCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
            QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveSkillsBonus(self):
    skillsBool = self.ui.skillsBox.findChildren(QtWidgets.QRadioButton)
    for QRadioButton in skillsBool:
        self.loadedCharacter["skillsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    skills = self.ui.skillsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in skills:
        self.loadedCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()] = int(QLineEdit.text().replace("+", "")) if (
                QLineEdit.text().replace("+", "") != "") else 0


def saveCharacterInfo(self):
    charInfos = self.ui.charInfoBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in charInfos:
        if QLineEdit.accessibleDescription() == "int":
            self.loadedCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text()) if (QLineEdit.text() != "") else 0
        else:
            self.loadedCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def saveCharacterPersonality(self):
    personalities = self.ui.characterBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in personalities:
        self.loadedCharacter[QLineEdit.accessibleName()] = QLineEdit.text()

    temper = self.ui.temperBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in temper:
        self.loadedCharacter[QLineEdit.accessibleName()] = QLineEdit.text()

    features = self.ui.featuresAndTraitsEdit.toPlainText().split(", ")
    if features[-1] == "":
        del features[-1]
    self.loadedCharacter["personality"]["features"] = features


def saveD20BonusBox(self):
    self.loadedCharacter["characteristicBonus"][
        "wisdomBonus"] = self.loadedCharacter["passiveWisdom"]

    bonuses = self.ui.d20BonusBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in bonuses:
        self.loadedCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def saveLifeBox(self):
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


def saveEquipmentBox(self):
    equipment = self.ui.equipment.toPlainText().split(", ")
    equipment = equipment[:-2] if (equipment[-2] == "," and equipment[-1] == " ") else equipment
    self.loadedCharacter["equipment"] = equipment


def saveMoneyBox(self):
    moneyBoxValues = self.ui.moneyBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in moneyBoxValues:
        self.loadedCharacter["money"][QLineEdit.accessibleName()] = int(QLineEdit.text()) if (
                QLineEdit.text() != "") else 0


def backupCharacter(self):
    if not self.fileIsNew:
        backupCharacteristicsAndBonus(self)
        backupSavingThowsBonus(self)
        backupSkillsBonus(self)
        backupCharacterInfo(self)
        backupCharacterPersonality(self)
        backupD20BonusBox(self)
        backupLifeBox(self)
        backupEquipmentBox(self)
        backupMoneyBox(self)
        with open(self.pathToJson.replace(".json", "_bck.json"), 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.backupCharacter,
                               sort_keys=False, indent=2))


def backupCharacteristicsAndBonus(self):
    characteristics = self.ui.characteristicBox.findChildren(
        QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            self.backupCharacter["characteristic"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0
            self.backupCharacter["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int(
                (self.backupCharacter["characteristic"][QLineEdit.accessibleName()] - 10) / 2)

    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "bonus"):
            self.backupCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupSavingThowsBonus(self):
    savingThrowsBool = self.ui.savingThrowsBox.findChildren(
        QtWidgets.QRadioButton)
    for QRadioButton in savingThrowsBool:
        self.backupCharacter["savingThrowsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    savingThrows = self.ui.savingThrowsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in savingThrows:
        self.backupCharacter["characteristicBonus"][QLineEdit.accessibleName()] = int(
            QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupSkillsBonus(self):
    skillsBool = self.ui.skillsBox.findChildren(QtWidgets.QRadioButton)
    for QRadioButton in skillsBool:
        self.backupCharacter["skillsBonus"][
            QRadioButton.accessibleName()] = QRadioButton.isChecked()

    skills = self.ui.skillsBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in skills:
        self.backupCharacter[
            "characteristicBonus"][QLineEdit.accessibleName()] = int(QLineEdit.text().replace("+", "")) if (
                QLineEdit.text().replace("+", "") != "") else 0


def backupCharacterInfo(self):
    charInfos = self.ui.charInfoBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in charInfos:
        if QLineEdit.accessibleDescription() == "int":
            self.backupCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text()) if (QLineEdit.text() != "") else 0
        else:
            self.backupCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def backupCharacterPersonality(self):
    personalities = self.ui.characterBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in personalities:
        self.backupCharacter[QLineEdit.accessibleName()] = QLineEdit.text()


def backupD20BonusBox(self):
    self.backupCharacter["characteristicBonus"][
        "wisdomBonus"] = self.backupCharacter["passiveWisdom"]

    bonuses = self.ui.d20BonusBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in bonuses:
        self.backupCharacter[QLineEdit.accessibleName()] = int(QLineEdit.text().replace(
            "+", "")) if (QLineEdit.text().replace("+", "") != "") else 0


def backupLifeBox(self):
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


def backupEquipmentBox(self):
    equipment = self.ui.equipment.toPlainText().split(", ")
    equipment = equipment[:-2] if (equipment[-2] == "," and equipment[-1] == " ") else equipment
    self.backupCharacter["equipment"] = equipment


def backupMoneyBox(self):
    moneyBoxValues = self.ui.moneyBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in moneyBoxValues:
        self.backupCharacter["money"][QLineEdit.accessibleName()] = int(QLineEdit.text()) if (
                QLineEdit.text() != "") else 0


def saveGenerated(self):
    self.newCharacterGen["default"] = False
    self.newCharacterGen["playerName"] = self.ui.playerName.text()
    self.newCharacterGen["charName"] = self.ui.charName.text()

    characteristics = self.ui.characteristicBox.findChildren(QtWidgets.QLineEdit)
    for QLineEdit in characteristics:
        if (QLineEdit.accessibleDescription() == "base"):
            self.newCharacterGen["characteristic"][QLineEdit.accessibleName()] = int(
                QLineEdit.text().replace("+", "")) if (QLineEdit.text().replace("+", "") != "") else 0
            self.newCharacterGen["characteristicBonus"][
                QLineEdit.accessibleName() + "Bonus"] = int(
                (self.newCharacterGen["characteristic"][QLineEdit.accessibleName()] - 10) / 2)

    self.newCharacterGen["personality"]["appearance"][
        "personalityTraits"] = self.ui.personalityEdit.toPlainText()
    self.newCharacterGen["personality"]["appearance"]["ideals"] = self.ui.idealsEdit.toPlainText()
    self.newCharacterGen["personality"]["appearance"]["bonds"] = self.ui.bondsEdit.toPlainText()
    self.newCharacterGen["personality"]["appearance"]["flaws"] = self.ui.flawsEdit.toPlainText()

    self.newCharacterGen["class"] = self.selectedClass
    self.newCharacterGen["hitDiceCoeffiecient"] = self.loadedClasses[
        self.selectedClass]["init"]["hitDiceCoeffiecient"]
    self.newCharacterGen["savingThrowsBonus"] = self.loadedClasses[
        self.selectedClass]["init"]["savingThrowsBonus"]
    for i in range(self.loadedClasses[self.selectedClass]["init"]["money"]):
        self.newCharacterGen["money"]["gold"] += random.randint(1, 4)
    self.newCharacterGen["money"]["gold"] *= 10 if self.selectedClass != "Monk" else 1
    self.newCharacterGen["proficiencyBonus"] = self.loadedClasses[self.selectedClass][
        "table"][self.newCharacterGen["level"] - 1]["proficiencyBonus"]
    self.newCharacterGen["personality"]["features"] = self.loadedClasses[
        self.selectedClass]["table"][self.newCharacterGen["level"] - 1]["features"]
    self.newCharacterGen["equipment"] = self.loadedClasses[self.selectedClass]["init"]["equipment"]
    for additionalEquipment in self.classEquipmentChecked:
        for eq in additionalEquipment:
            self.newCharacterGen["equipment"].append(eq.text())
    for skillTrue in self.classSkillsChecked:
        skillTrue.setText(skillTrue.text().replace("animal handling", "animalHandling"))
        skillTrue.setText(skillTrue.text().replace("sleight of hand", "sleightOfHand"))
        if skillTrue.text() in self.newCharacterGen["skillsBonus"]:
            self.newCharacterGen["skillsBonus"][skillTrue.text()] = True

    self.newCharacterGen["race"] = self.selectedRace
    self.newCharacterGen["speed"] = self.loadedRaces[self.selectedRace]["speed"]
    for skills in self.loadedRaces[self.selectedRace]["skills"]:
        self.newCharacterGen["personality"]["features"].append(skills)

    if "subraces" in self.loadedRaces[self.selectedRace]:
        if self.ui.raceSubCombo.currentText() in self.loadedRaces[self.selectedRace]["subraces"]:
            if "bonuses" in self.loadedRaces[self.selectedRace]["subraces"][self.ui.raceSubCombo.currentText()]:
                for sub in self.loadedRaces[self.selectedRace]["subraces"][self.ui.raceSubCombo.currentText()][
                    "bonuses"]:
                    if sub == "characteristic":
                        for characteristic in self.loadedRaces[self.selectedRace]["subraces"][
                            self.ui.raceSubCombo.currentText()]["bonuses"][sub]:
                            self.newCharacterGen[sub][characteristic] += self.loadedRaces[self.selectedRace][
                                "subraces"][self.ui.raceSubCombo.currentText()]["bonuses"][sub][characteristic]
                    elif sub == "skills":
                        self.newCharacterGen["personality"]["features"] += \
                            self.loadedRaces[self.selectedRace]["subraces"][
                                self.ui.raceSubCombo.currentText()]["bonuses"][sub]
                    else:
                        self.newCharacterGen[sub] += self.loadedRaces[self.selectedRace]["subraces"][
                            self.ui.raceSubCombo.currentText()]["bonuses"][sub]

    self.newCharacterGen["background"] = self.selectedBackground

    self.newCharacterGen["specialization"] = self.ui.backgroundSpecChoose.currentText()

    self.newCharacterGen["alignment"] = self.selectedAlignment
