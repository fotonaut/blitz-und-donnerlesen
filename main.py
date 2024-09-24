import sys
#import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QFont


class StopwatchApp(QWidget):
    def __init__(self):
        super().__init__()

        # SQLite-Datenbankverbindung herstellen
        self.conn = sqlite3.connect('woerter.db')
        self.create_database()

        # Hauptlayout
        main_layout = QHBoxLayout()

        # Linke Seite: Tabelle
        self.table = QTableWidget(20, 3)  # 20 Zeilen, 3 Spalten
        font = QFont()
        font.setPointSize(16)  # Setze die Schriftgröße auf 16pt

        # Pulldown-Menü (ComboBox) zum Auswählen des Datums
        self.date_selector = QComboBox(self)
        self.load_dates_into_combobox()
        self.date_selector.currentIndexChanged.connect(self.update_table_with_selected_date)
        
        # Wörter initial anzeigen (für das erste Datum)
        self.update_table_with_selected_date()

        main_layout.addWidget(self.date_selector)
        main_layout.addWidget(self.table)

        # Rechte Seite: Stoppuhr
        right_layout = QVBoxLayout()
        
        self.time_label = QLabel("00:00:00", self)
        self.time_label.setStyleSheet("font-size: 30px;")
        right_layout.addWidget(self.time_label)
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        right_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        right_layout.addWidget(self.stop_button)
        
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)
        right_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(right_layout)

        # Timer-Objekt für die Stoppuhr
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Blitz- und Donnerlesen")
        self.setGeometry(300, 300, 1400, 1200)

    def create_database(self):
        # Erstellt eine Tabelle in der SQLite-Datenbank, falls diese noch nicht existiert
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS woerter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wort TEXT NOT NULL,
                datum TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def load_dates_into_combobox(self):
        # Lade die verfügbaren Datumsangaben aus der Datenbank in die ComboBox
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT datum FROM woerter')
        dates = cursor.fetchall()
        for date in dates:
            self.date_selector.addItem(date[0])

    def update_table_with_selected_date(self):
        # Wörter basierend auf dem ausgewählten Datum laden
        selected_date = self.date_selector.currentText()
        if selected_date:
            words = self.get_words_by_date(selected_date)
            self.display_words_in_table(words)

    def get_words_by_date(self, date):
        # Hole 60 Wörter aus der Datenbank, die dem ausgewählten Datum entsprechen
        cursor = self.conn.cursor()
        cursor.execute('SELECT wort FROM woerter WHERE datum = ? LIMIT 60', (date,))
        words = cursor.fetchall()
        return [word[0] for word in words]

    def display_words_in_table(self, words):
        # Wörter in die Tabelle einfügen
        for i in range(20):
            for j in range(3):
                item = QTableWidgetItem(words[i + j * 20])
                item.setFont(QFont('Sans Serif', 16))  # Schriftgröße setzen
                self.table.setItem(i, j, item)
        # Spaltenbreite anpassen
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)

    def start_timer(self):
        self.timer.start(1000)  # 1000 ms = 1 Sekunde

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.time = QTime(0, 0, 0)  # Zurück auf 00:00:00 setzen
        self.time_label.setText(self.time.toString("hh:mm:ss"))

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.time_label.setText(self.time.toString("hh:mm:ss"))

    def add_test_data(self):
        # Beispielhafte Testdaten hinzufügen (kann entfernt werden, wenn Daten vorhanden sind)
        #cursor = self.conn.cursor()
        example_words = [
            # 60 Wörter für den 09.09.2024...
            ("Buch", "09.09.2024"), ("Enten", "09.09.2024"), ("Möbel", "09.09.2024"), ("Zaun", "09.09.2024"), ("Tal", "09.09.2024"), ("Wolken", "09.09.2024"), ("Gas", "09.09.2024"), ("Garten", "09.09.2024"), ("Birne", "09.09.2024"), ("Hafen", "09.09.2024"), ("heraus", "09.09.2024"), ("Farben", "09.09.2024"), ("Tür", "09.09.2024"), ("hinein", "09.09.2024"), ("Schuhe", "09.09.2024"), ("Winter", "09.09.2024"), ("warten", "09.09.2024"), ("Fach", "09.09.2024"), ("Bilder", "09.09.2024"), ("Silben", "09.09.2024"), ("Tante", "09.09.2024"), ("Album", "09.09.2024"), ("Kalender", "09.09.2024"), ("Telefon", "09.09.2024"), ("Feder", "09.09.2024"), ("Karten", "09.09.2024"), ("Anlage", "09.09.2024"), ("Kabel", "09.09.2024"), ("Arbeiter", "09.09.2024"), ("Raupe", "09.09.2024"), ("Figuren", "09.09.2024"), ("Juwelen", "09.09.2024"), ("Gabel", "09.09.2024"), ("Zuschauer", "09.09.2024"), ("Wochen", "09.09.2024"), ("Aufgaben", "09.09.2024"), ("Ozean", "09.09.2024"), ("leuchten", "09.09.2024"), ("Jaguar", "09.09.2024"), ("Palme", "09.09.2024"), ("Geheimnis", "09.09.2024"), ("Dokumente", "09.09.2024"), ("Gesichter", "09.09.2024"), ("Nashörner", "09.09.2024"), ("Pinguine", "09.09.2024"), ("Roboter", "09.09.2024"), ("Salamander", "09.09.2024"), ("Warteraum", "09.09.2024"), ("Wanderer", "09.09.2024"), ("Gartentor", "09.09.2024"), ("Rauchzeichen", "09.09.2024"), ("Reparatur", "09.09.2024"), ("Rakete", "09.09.2024"), ("Marmelade", "09.09.2024"), ("Pampelmuse", "09.09.2024"), ("Taschentuch", "09.09.2024"), ("Sandalen", "09.09.2024"), ("Silbenbögen", "09.09.2024"), ("Elefanten", "09.09.2024"), ("Melodien", "09.09.2024"), 
            # Weitere 60 Wörter für den 24.09.2024...
            ("Frau", "23.09.2024"), ("Fleisch", "23.09.2024"), ("Schwan", "23.09.2024"), ("Schlauch", "23.09.2024"), ("Zwerge", "23.09.2024"), ("Schnecken", "23.09.2024"), ("Schlaf", "23.09.2024"), ("Schleim", "23.09.2024"), ("Schritte", "23.09.2024"), ("Frosch", "23.09.2024"), ("frisch", "23.09.2024"), ("Zweige", "23.09.2024"), ("Fladen", "23.09.2024"), ("schreiben", "23.09.2024"), ("Flügel", "23.09.2024"), ("Flossen", "23.09.2024"), ("Schrift", "23.09.2024"), ("frei", "23.09.2024"), ("Schweine", "23.09.2024"), ("schmusen", "23.09.2024"), ("Freude", "23.09.2024"), ("Freiheit", "23.09.2024"), ("zwei", "23.09.2024"), ("Flamingo", "23.09.2024"), ("Schwalbe", "23.09.2024"), ("schneiden", "23.09.2024"), ("schminken", "23.09.2024"), ("Früchte", "23.09.2024"), ("Schnüre", "23.09.2024"), ("Schlüssel", "23.09.2024"), ("Frösche", "23.09.2024"), ("Freunde", "23.09.2024"), ("schmatzen", "23.09.2024"), ("schlürfen", "23.09.2024"), ("schlingen", "23.09.2024"), ("Flöhe", "23.09.2024"), ("Schnabel", "23.09.2024"), ("Schlitten", "23.09.2024"), ("Schnuller", "23.09.2024"), ("Schraube", "23.09.2024"), ("Fragezeichen", "23.09.2024"), ("Kugelschreiber", "23.09.2024"), ("Schleiereule", "23.09.2024"), ("Fleischsalate", "23.09.2024"), ("Gezwitscher", "23.09.2024"), ("Schmusekatze", "23.09.2024"), ("Zwillinge", "23.09.2024"), ("Unterschriften", "23.09.2024"), ("Schlüsselloch", "23.09.2024"), ("Schmetterlinge", "23.09.2024"), ("Fledermaus", "23.09.2024"), ("Schmerzen", "23.09.2024"), ("Fischflossen", "23.09.2024"), ("französisch", "23.09.2024"), ("Hundeschnauze", "23.09.2024"), ("Feinschmecker", "23.09.2024"), ("Winterschlaf", "23.09.2024"), ("zwischen", "23.09.2024"), ("Frischlinge", "23.09.2024"), ("Luftschlange", "23.09.2024")
            
        ]
        #cursor.executemany('INSERT INTO woerter (wort, datum) VALUES (?, ?)', example_words)
        #self.conn.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StopwatchApp()
    window.add_test_data()  # Testdaten hinzufügen (einmal ausführen, dann entfernen)
    window.show()
    sys.exit(app.exec_())
