import datetime
import sys
import time

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtWidgets import *
from voice_assistant import speak


def get_the_time_as_a_string(seconds):
    str_time = ''
    utc_time = datetime.datetime.utcfromtimestamp(seconds)
    hours, minutes, seconds = utc_time.hour, utc_time.minute, utc_time.second
    if hours:
        str_time += f'{hours} часов '
    if minutes:
        str_time += f'{minutes} минут '
    if seconds:
        str_time += f'{seconds} секунд'
    return str_time


class Timer(QWidget):
    def __init__(self):
        super(Timer, self).__init__()
        self.setWindowIcon(QIcon('icon.ico'))
        self.past_tense = 0
        self.working_time = 45 * 60
        self.time_relax = 15 * 60
        self.title = QLabel(self)
        self.time = QLabel(self)
        self.time_edit = QTimeEdit(self)
        self.timer = QTimer(self)
        self.start_and_stop_button = QPushButton('Start', self)
        self.v_layout = QVBoxLayout()

        self.customize_font()
        self.add_widgets()
        self.add_functions()

    def customize_font(self):
        font = QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.title.setFont(font)
        self.time.setFont(font)
        self.time_edit.setFont(font)
        self.start_and_stop_button.setFont(font)

    def add_widgets(self):
        self.v_layout.addWidget(self.title)
        self.v_layout.addWidget(self.time)
        self.v_layout.addWidget(self.time_edit)
        self.v_layout.addWidget(self.start_and_stop_button)
        self.setLayout(self.v_layout)

    def add_functions(self):
        self.title.setText('Установите таймер')
        self.time.hide()
        self.time.setAlignment(Qt.AlignCenter)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.start_and_stop_button.clicked.connect(self.start_or_stop_the_timer)
        self.timer.timeout.connect(self.update_timer)

    def start_or_stop_the_timer(self):
        if not self.timer.isActive():
            self.start_the_timer()
        else:
            self.stop_the_timer()

    def start_the_timer(self):
        self.start_and_stop_button.setText('Stop')
        self.timer.start(1000)
        self.hide_or_show_time_edit(show=0)

    def hide_or_show_time_edit(self, show):
        if show:
            self.time.hide()
            self.time_edit.show()
        else:
            self.time.show()
            self.time_edit.hide()

    def stop_the_timer(self):
        self.start_and_stop_button.setText('Start')
        self.timer.stop()

    def update_timer(self):
        if self.timer_is_over():
            self.hide_or_show_time_edit(show=1)
            self.stop_the_timer()
            return
        q_time = self.time_edit.time()
        q_time_minus_second = q_time.addSecs(-1)
        self.time_edit.setTime(q_time_minus_second)

        str_q_time_minus_second = q_time_minus_second.toString('HH:mm:ss')
        self.time.setText(str_q_time_minus_second)

        self.stop_timer_for_break()

    def timer_is_over(self):
        return self.time_edit.time() == QTime(0, 0, 0)

    def stop_timer_for_break(self):
        self.past_tense += 1
        if self.is_time_to_rest():
            str_time = get_the_time_as_a_string(self.time_relax)
            speak(f'Перерыв {str_time}')
            time.sleep(self.time_relax)
            speak('Перерыв закончился')

    def is_time_to_rest(self):
        return self.past_tense % self.working_time == 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = Timer()
    timer.show()
    sys.exit(app.exec_())
