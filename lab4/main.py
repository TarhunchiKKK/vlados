from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

import bitstaffing
import hemming
from lab4 import csma_cd

bitsNumberComboBoxItems: list[str] = ['8 бит', '7 бит', '6 бит', '5 бит']


class Ui_MainWindow(object):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.serialPort: QSerialPort = QSerialPort()
        self.serialPort.readyRead.connect(self.onRecieveBytes)

    def setupUi(self, MainWindow):
        # Настройки окна
        MainWindow.setObjectName("SerialPort")
        MainWindow.resize(800, 320)
        MainWindow.setFixedSize(QtCore.QSize(800, 320))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # доступные порты
        self.port = QtWidgets.QComboBox(self.centralwidget)
        self.port.setGeometry(QtCore.QRect(570, 230, 101, 21))
        self.port.setObjectName("port")
        self.fillPortNumberComboBox()

        self.input = QtWidgets.QTextEdit(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(10, 60, 351, 101))
        self.input.setObjectName("input")
        self.input.keyPressEvent = self.onInputTextChanged

        # количество бит в байте
        self.count_of_bits_in_byte = QtWidgets.QComboBox(self.centralwidget)
        self.count_of_bits_in_byte.setGeometry(QtCore.QRect(680, 270, 101, 21))
        self.count_of_bits_in_byte.setObjectName("count_of_bits_in_byte")
        self.fillBitsNumberComboBox()

        self.output = QtWidgets.QTextEdit(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(440, 60, 351, 101))
        self.output.setReadOnly(True)
        self.output.setObjectName("output")

        self.label_input = QtWidgets.QLabel(self.centralwidget)
        self.label_input.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(22)

        self.label_input.setFont(font)
        self.label_input.setObjectName("label_input")

        self.label_output = QtWidgets.QLabel(self.centralwidget)
        self.label_output.setGeometry(QtCore.QRect(440, 10, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_output.setFont(font)
        self.label_output.setObjectName("label_output")

        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(10, 170, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_status.setFont(font)
        self.label_status.setObjectName("label_status")

        self.label_control = QtWidgets.QLabel(self.centralwidget)
        self.label_control.setGeometry(QtCore.QRect(450, 170, 161, 41))

        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_control.setFont(font)
        self.label_control.setObjectName("label_control")
        self.label_count_of_symbols = QtWidgets.QLabel(self.centralwidget)
        self.label_count_of_symbols.setGeometry(QtCore.QRect(10, 220, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_count_of_symbols.setFont(font)
        self.label_count_of_symbols.setObjectName("label_count_of_symbols")

        self.label_baud_rate = QtWidgets.QLabel(self.centralwidget)
        self.label_baud_rate.setGeometry(QtCore.QRect(10, 260, 235, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_baud_rate.setFont(font)
        self.label_baud_rate.setObjectName("label_baud_rate")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(450, 220, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(450, 260, 225, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        self.count_of_received_bytes = QtWidgets.QLineEdit(self.centralwidget)
        self.count_of_received_bytes.setGeometry(QtCore.QRect(270, 230, 111, 24))
        self.count_of_received_bytes.setReadOnly(True)
        self.count_of_received_bytes.setObjectName("count_of_received_bytes")

        self.baud_rate = QtWidgets.QLineEdit(self.centralwidget)
        self.baud_rate.setGeometry(QtCore.QRect(250, 270, 111, 24))
        self.baud_rate.setReadOnly(True)
        self.baud_rate.setObjectName("baud_rate")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.statusBar().setVisible(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.openPort()
        self.port.currentIndexChanged.connect(self.onChangePort)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Последовательный порт"))
        self.label_input.setText(_translate("MainWindow", "Ввод"))
        self.label_output.setText(_translate("MainWindow", "Вывод"))
        self.label_status.setText(_translate("MainWindow", "Статус"))
        self.label_control.setText(_translate("MainWindow", "Контроль"))
        self.label_count_of_symbols.setText(_translate("MainWindow", "Количество переданных байт:"))
        self.label_baud_rate.setText(_translate("MainWindow", "Скорость передачи данных:"))
        self.label_7.setText(_translate("MainWindow", "Номер порта:"))
        self.label_8.setText(_translate("MainWindow", "Количество битов в байте:"))

    def fillPortNumberComboBox(self):
        availablePorts: list[QSerialPortInfo] = QSerialPortInfo.availablePorts()
        currentPort: str = self.port.currentText()
        if availablePorts:
            self.port.blockSignals(True)
            self.port.clear()

            for availablePort in availablePorts:  # [3::1]
                self.port.addItem(availablePort.portName()[3::1])

            currentIndex: int = self.port.findText(currentPort)

            if currentIndex != -1:
                self.port.setCurrentIndex(currentIndex)

            self.port.blockSignals(False)
        else:
            QMessageBox.warning(None, "Ошибка", "Нет доступных COM-портов")
            sys.exit(app.exec_())

    def fillBitsNumberComboBox(self):
        self.count_of_bits_in_byte.clear()
        for item in bitsNumberComboBoxItems:
            self.count_of_bits_in_byte.addItem(item)

    def openPort(self):
        if not self.serialPort.isOpen():
            self.configurePort()
            if not self.tryOpenPort(self.serialPort.portName()):
                availablePorts: list[QSerialPortInfo] = QSerialPortInfo.availablePorts()
                for availablePort in availablePorts:
                    if self.tryOpenPort(availablePort.portName()):
                        self.port.blockSignals(True)
                        self.port.setCurrentText(availablePort.portName()[3::1])
                        self.serialPort.setPortName(availablePort.portName())
                        self.port.blockSignals(False)
                        break
                else:
                    QMessageBox.warning(None, "Ошибка", "Нет доступных COM-портов")
                    sys.exit(app.exec_())
            self.serialPort.open(QtCore.QIODevice.ReadWrite)

    def tryOpenPort(self, portName: str) -> bool:
        port: QSerialPort = QSerialPort()
        port.setPortName(portName)
        if port.open(QtCore.QIODevice.ReadWrite):
            port.close()
            return True
        else:
            return False

    def configurePort(self):
        portName: str = self.port.currentText()
        self.serialPort.setPortName(portName)

        baudRate: int = 9600
        self.serialPort.setBaudRate(baudRate)

        dataBits: int = int(self.count_of_bits_in_byte.currentText()[0])
        self.serialPort.setDataBits(dataBits)

        self.serialPort.setParity(QSerialPort.Parity.NoParity)
        self.serialPort.setStopBits(QSerialPort.StopBits.OneStop)
        self.serialPort.setFlowControl(QSerialPort.FlowControl.NoFlowControl)

    def onInputTextChanged(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self.input, event)
        if event.key() == QtCore.Qt.Key_Return:
            self.onSendBytes()
        # нажат не ENTER
        else:
            # валидация ввода (вводить можно 0 или 1)
            # если введено что-то другое - удалить новый символ и переместить курсор

            # считал введенные данные
            data: str = self.input.toPlainText()
            # положение курсора
            cursor_position: int = self.input.textCursor().position()

            # ты проходишься по всей строке и ищешь запрещенные символы
            # проверять только последний символ ненадежно т.к. ввести могли в середину строки
            for ch in data:
                # вот ты нашел запрещенный символ
                if ch != '0' and ch != '1':
                    # заменяешь его на пустой символ что эквивалентно удалению символа
                    data = data.replace(ch, "")
                    # т.к. символ удален,то позицию курсора нужно на 1 уменьшить
                    cursor_position -= 1
                    self.input.clear()
                    # перезапись ввеенной строки в поле ввода
                    self.input.setPlainText(data)
                    cursor: QTextCursor = self.input.textCursor()
                    cursor.setPosition(cursor_position)
                    self.input.setTextCursor(cursor)
                    break

    def onSendBytes(self):
        text: str = self.input.toPlainText().replace("\n", "")


        self.input.clear()
        self.count_of_received_bytes.clear()
        self.baud_rate.setText(str(self.serialPort.baudRate()))
        # ожидание, пока не закончится вся асинхронка
        QtWidgets.QApplication.processEvents()


        # получаешь список кадров (введенные данные ты делишь на кадры длинной 18)
        cadres: list[str] = bitstaffing.split_input_data_on_cadres(text)
        # вот эту строку ты будешь записывать в порт
        data_to_send: str = ''
        # проход по списку кдров
        for cadr in cadres:
            # флаг и dest_address условию константные
            flag: str = '00010010'
            dest_address: str = '0000'
            # source_address == номер твоего порта в бинарном виде
            source_address: str = bitstaffing.get_source_address(self.serialPort.portName())

            # это поле data в структуре кадра
            data: str = cadr
            fcs: str = hemming.code(data)
            # искажаем дату (смотри тх и реализацию метода)
            data = hemming.distort_data(data)

            # делаешь битстаффинг
            staffed_cadr: str = bitstaffing.bit_staffing(dest_address + source_address + data)
            # отправляешь данные вместе с выводом плюса=ов-минусов
            data_to_send += csma_cd.send_data(flag + staffed_cadr, self.get_append_status())


        # дальше уже твой код
        sendedBytesCount: int = len(data_to_send)
        self.serialPort.write(data_to_send.encode())
        self.input.clear()
        self.count_of_received_bytes.setText(str(sendedBytesCount))
        self.baud_rate.setText(str(self.serialPort.baudRate()))

    def onRecieveBytes(self):
        text = self.serialPort.readAll().data().decode()
        if len(text) == 0:
            QMessageBox.warning(None, "Ошибка", "Нельзя прочесть данные из порта")
            sys.exit(app.exec_())
        else:
            # тут ты разбиваешь пришедшую из порта строку на кадры
            cadres: list[str] = bitstaffing.split_recieved_data_on_cadres(text)
            # эту строку ты будешь выводить в окно вывода
            data_to_output: str = ''
            # эту строку ты будешь выводить в окно статуса
            highlighted_data: str = ''

            for cadr in cadres:
                # выделение битов, полученных при дебитстаффинге (читай тз и реализацию этого метода)
                highlighted_cadr: str = bitstaffing.get_highlighted_data(cadr) + '\n'

                # делаешь дебитстаффинг и из полученной строки извлекаешь только поле дата (соответствует с 8 по 26 символы)
                destaffed_cadr: str = bitstaffing.de_bit_staffing(cadr)
                # извлекаешь fcs из строки
                recieved_fcs: str = destaffed_cadr[-2::1]
                # извлекаешь поле data из строки
                destaffed_cadr = destaffed_cadr[8:26:1]
                # пересчитываешь fcs на приемнике
                calculated_fcs: str = hemming.code(destaffed_cadr)

                # если два fcs не совпали - исправить ошибку в сообщении
                if recieved_fcs != calculated_fcs:
                    destaffed_cadr = hemming.fix_data(destaffed_cadr, recieved_fcs)

                data_to_output += destaffed_cadr
                highlighted_data += highlighted_cadr

            # вывод статуса (!!!!!!!тебе нужно его добавить!!!!!!!!)
            self.status.setText(highlighted_data)
            # вывод в поле для вывода
            self.output.setText(data_to_output)
            self.baud_rate.setText(str(self.serialPort.baudRate()))

    def onChangePort(self, index):
        if self.serialPort.isOpen():
            self.serialPort.close()
        self.fillBitsNumberComboBox()
        self.fillPortNumberComboBox()
        self.openPort()

    # функция вывода плюсов-минусов
    # тебе надо добавить окно plus_minus
    def get_append_status(self):
        text_edit: QtWidgets.QTextEdit = self.plus_minus
        def closure(symbol: str):
            status: str = text_edit.toPlainText()
            status += symbol
            text_edit.setText(status)
        return closure

    def __str__(self):
        self.port.setFlowControl(QSerialPort.FlowControl.SoftwareControl)
        self.port.setFlowControl(QSerialPort.FlowControl.HardwareControl)
        self.port.setFlowControl(QSerialPort.FlowControl.NoFlowControl)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
