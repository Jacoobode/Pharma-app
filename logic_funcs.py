from PyQt5 import QtWidgets
from db_connect import DrugDataBase
from design import Ui_MainWindow
from PyQt5 import QtCore

class LogicFuncs(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.dr = DrugDataBase()
        self.ui.comboBox.addItem("")

        for key in self.dr.CATEGORY_KEYWORDS.keys():
            self.ui.comboBox.addItem(key)
        self.ui.comboBox.addItem("Other")

        self.ui.pushButton.clicked.connect(self.combined_search)

        self.ui.listWidget.itemClicked.connect(self.insert_description)
        self.ui.listWidget.itemClicked.connect(self.insert_extra_info)
        self.ui.pushButton_2.clicked.connect(self.add_medicine_from_form)
        self.ui.pushButton_3.clicked.connect(self.delete)

    def combined_search(self):
        query = self.ui.lineEdit.text().strip()

        combo_value = self.ui.comboBox.currentText()

        if query:
            results_by_name = self.dr.search_drugs_by_name(query)
            if results_by_name:
                names = [d['name'] for d in results_by_name if 'name' in d and d['name']]
                self.ui.listWidget.clear()
                self.ui.listWidget.addItems(names)
                return
            else:
                results_by_symptom = self.dr.search_by_symptoms(query)
                if results_by_symptom:
                    names = [d['name'] for d in results_by_symptom if 'name' in d and d['name']]
                    self.ui.listWidget.clear()
                    self.ui.listWidget.addItems(names)
                    return
                else:
                    QtWidgets.QMessageBox.information(self, "No Results", f'Nothing found for "{query}"')
                    return

        if combo_value == '':
            all_names = self.dr.all_medicines()
            names = [d['name'] for d in all_names if 'name' in d and d['name']]
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(names)

        elif combo_value in self.dr.CATEGORY_KEYWORDS.keys():
            drugs_by_category = self.dr.get_drugs_by_category(combo_value)
            names = [d['name'] for d in drugs_by_category if 'name' in d and d['name']]
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(names)

        elif combo_value == 'Other':
            all_drugs = self.dr.all_medicines()
            meds = []
            for drug in all_drugs:
                description = drug.get('description', '') or ''
                if not description.strip():
                    continue
                category = self.dr.detect_category(description)
                if category == 'Other' and drug.get('name'):
                    meds.append(drug)
            names = [med['name'] for med in meds]
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(names)

    def insert_description(self, item):
        self.ui.textEdit_3.clear()
        selected_name = item.text()

        all_meds = self.dr.all_medicines()
        for med in all_meds:
            if med.get('name') == selected_name:
                description = med.get('description', "No description")
                if description is None or not description.strip():
                    description = "No description"
                self.ui.textEdit_3.insertPlainText(description)
                break

    def insert_extra_info(self, item):
        self.ui.textEdit_4.clear()
        selected_name = item.text()

        all_meds = self.dr.all_medicines()
        for med in all_meds:
            if med.get('name') == selected_name:
                description = med.get('description', '') or ''
                category = self.dr.detect_category(description)

                info_text = f"Category: {category}\n\n"

                extra_fields = {
                    "Synthesis Reference": med.get('synthesis-reference', "No information"),
                    "State": med.get('state',"No information"),
                    "Group": med.get('group',"No information"),
                    "Indication": med.get('indication',"No information"),
                    "Pharmacodynamics": med.get('pharmacodynamics',"No information"),
                    "Mechanism of Action": med.get('mechanism-of-action',"No information"),
                    "Toxicity": med.get('toxicity',"No information"),
                    "Metabolism": med.get('metabolism',"No information"),
                    "Absorption": med.get('absorption',"No information"),
                }

                for title, value in extra_fields.items():
                    if value and value.strip():
                        info_text += f"{title}:\n{value.strip()}\n\n"

                self.ui.textEdit_4.setPlainText(info_text)
                break

    def clear_input_fields(self):
        self.ui.lineEdit_2.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit.clear()
        self.ui.textEdit_7.clear()
        self.ui.textEdit_8.clear()
        self.ui.textEdit_9.clear()
        self.ui.textEdit_10.clear()
        self.ui.textEdit_11.clear()
        self.ui.textEdit_12.clear()
        self.ui.textEdit_13.clear()
        self.ui.textEdit_14.clear()
        self.ui.textEdit_15.clear()
        self.ui.textEdit_16.clear()

    def add_medicine_from_form(self):

        name = self.ui.lineEdit_2.text().strip()


        if not name:
            QtWidgets.QMessageBox.warning(self, "Error", "Enter the name of the medicine")
            return

        type = self.ui.textEdit_2.toPlainText().strip()
        created = self.ui.textEdit.toPlainText().strip()
        updated = self.ui.textEdit_7.toPlainText().strip()
        description = self.ui.textEdit_8.toPlainText().strip()
        state = self.ui.textEdit_9.toPlainText().strip()
        indication = self.ui.textEdit_10.toPlainText().strip()
        pharmacodynamics = self.ui.textEdit_11.toPlainText().strip()
        toxicity = self.ui.textEdit_12.toPlainText().strip()
        absorption = self.ui.textEdit_13.toPlainText().strip()
        volume = self.ui.textEdit_14.toPlainText().strip()
        food_interaction = self.ui.textEdit_15.toPlainText().strip()
        mechanism_of_action = self.ui.textEdit_16.toPlainText().strip()


        try:
            self.dr.add_medicine(type, created, updated,name,description,state,indication,pharmacodynamics,
                         toxicity,absorption,volume,food_interaction,mechanism_of_action)
            self.dr.conn.commit()
            QtWidgets.QMessageBox.information(self, "Successfully", "Medicine added successfully!")
            self.clear_input_fields()
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.critical(self, "Error", f"Add failure: {e}")

    def start(self):
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_C:
            self.clear_input_fields()
            self.ui.listWidget.clear()
            self.ui.comboBox.clear()
            self.ui.lineEdit.clear()
            self.ui.textEdit_3.clear()
            self.ui.textEdit_4.clear()
        elif event.key() == QtCore.Qt.Key_Return:
            self.combined_search()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def delete(self):
        if self.ui.lineEdit_2.text():
            name = self.ui.lineEdit_2.text().strip()
            self.dr.delete_medicine(name)
            QtWidgets.QMessageBox.information(self, "Successfully", "Medicine deleted successfully!")
            self.clear_input_fields()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Enter the name of the medicine")






