from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QFont
import sys

import qasync, asyncio
from Praximedes import Praximedes

class VoiceAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.praximedes = Praximedes(confirmation_message="")
        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle("Praximedes GUI")
        self.setGeometry(200, 200, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Label
        self.status_label = QLabel("Status: Idle", self)
        layout.addWidget(self.status_label)

        # Output area
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Command feedback will appear here...")
        layout.addWidget(self.output_text)

        # Listening Button
        self.listen_button = QPushButton("Start Listening")
        self.listen_button.setIcon(QIcon("mic_icon.png"))  # Replace with your icon
        self.listen_button.clicked.connect(self.start_listening)
        layout.addWidget(self.listen_button)

        # LED Controls
        self.led_on_button = QPushButton("Turn On LED")
        self.led_on_button.clicked.connect(self.turn_on_led)
        layout.addWidget(self.led_on_button)

        self.led_off_button = QPushButton("Turn Off LED")
        self.led_off_button.clicked.connect(self.turn_off_led)
        layout.addWidget(self.led_off_button)

        # Set layout and show
        self.setLayout(layout)

    def start_listening(self):
        # Replace this with your voice processing logic
        self.status_label.setText("Status: Listening...")
        self.output_text.append("Listening mode activated. Say 'Hey Praximedes'.")

    @qasync.asyncSlot()
    async def turn_on_led(self):
        # Style of labels
        self.status_label.setStyleSheet("color: green")

        # Process of running function
        self.output_text.append("Turning on LED...")
        await self.praximedes.LED_turnOn()
        self.status_label.setText("Status: LED On")

    @qasync.asyncSlot()
    async def turn_off_led(self):
        # Style of labels
        self.status_label.setStyleSheet("color: red")

        # Process of running function
        self.output_text.append("Turning off LED...")
        await self.praximedes.LED_turnOff()
        self.status_label.setText("Status: LED Off")


if __name__ == "__main__":
    #Setting up a loop for asynchronous activity
    app = QApplication(sys.argv)
    app.setFont(QFont("Helvetica", 12))
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    #Setting up GUI
    gui = VoiceAssistantGUI()
    gui.show()

    #Run async functions
    with loop:
      loop.run_forever()