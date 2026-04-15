from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox, QFileDialog
from itertools import product
import string

from utils.random_data_generator import export_data, BasePage, show_legal_warning, EXPORT_MAX_COUNT


class IncrementPage(BasePage):
    def __init__(self):
        super().__init__()
        self.data = None  # 初始化self.data

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成自增数据"))

        form_layout = QVBoxLayout()
        self.layout.addLayout(form_layout)

        form_layout.addWidget(QLabel("请输入需要生成的数量:"))
        self.num_entry = QLineEdit()
        form_layout.addWidget(self.num_entry)

        form_layout.addWidget(QLabel("请选择数据类型 (非必填):"))
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems(["数字", "字母"])
        self.data_type_combo.setCurrentIndex(-1)  # 设置为不选中任何值
        form_layout.addWidget(self.data_type_combo)

        form_layout.addWidget(QLabel("请输入标志位 (非必填):"))
        self.flag_entry = QLineEdit()
        form_layout.addWidget(self.flag_entry)

        form_layout.addWidget(QLabel("请输入总位数:"))
        self.total_length_entry = QLineEdit()
        form_layout.addWidget(self.total_length_entry)

        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        generate_button = QPushButton("生成")
        generate_button.clicked.connect(self.generate_data)
        button_layout.addWidget(generate_button)
        generate_button.setIcon(QIcon('./resources/generate_button.png'))  # 设置按钮图标
        generate_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        export_button = QPushButton("导出")
        export_button.clicked.connect(lambda: self.export_data(self.data))
        button_layout.addWidget(export_button)
        export_button.setIcon(QIcon('./resources/export_button.png'))  # 设置按钮图标
        export_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_fields)
        button_layout.addWidget(reset_button)
        reset_button.setIcon(QIcon('./resources/reset_button.png'))  # 设置按钮图标
        reset_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("QTextEdit { font-size: 14pt; }")
        self.layout.addWidget(self.result_text, stretch=1)

        # 调用基类方法添加公司logo
        self.add_logo()

        self.reset_fields()  # 调用重置方法以确保初始状态为空

    def generate_data(self):
        if not show_legal_warning(self):
            return
        try:
            num = int(self.num_entry.text())
            if num > EXPORT_MAX_COUNT:
                QMessageBox.critical(self, "数量超限", f"单次生成数量上限为 {EXPORT_MAX_COUNT} 条")
                return
            data_type = self.data_type_combo.currentText()
            flag = self.flag_entry.text()
            total_length = int(self.total_length_entry.text())

            if data_type == "数字" or not data_type:
                self.data = self.generate_numbers(num, total_length, flag)
                if self.data is None:
                    return  # 如果生成数据失败，则退出
            elif data_type == "字母":
                self.data = self.generate_letters(num, total_length, flag)
                if self.data is None:
                    return  # 如果生成数据失败，则退出

            self.display_data(self.data)
            # QMessageBox.information(self, "生成成功", f"成功生成 {num} 条自增数据")
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成数据时发生错误: {e}")

    def generate_numbers(self, num, total_length, flag):
        data = []
        flag_length = len(flag)
        for i in range(1, num + 1):  # 修改为从1开始生成
            data.append(f"{flag}{str(i).zfill(total_length - flag_length)}")
        return data

    def generate_letters(self, num, total_length, flag):
        alphabet = string.ascii_lowercase
        data = []

        flag_length = len(flag)
        length = total_length - flag_length

        if length < 1:
            QMessageBox.critical(self, "输入错误", "总位数不能小于标志位长度")
            return None

        # 动态定义每个长度的最大组合数
        max_combinations = {}
        total_combinations = 0

        for i in range(1, length + 1):
            if i == 1:
                max_combinations[i] = len(alphabet)
            else:
                max_combinations[i] = max_combinations[i - 1] * len(alphabet)
            total_combinations += max_combinations[i]

        if num > total_combinations:
            QMessageBox.critical(self, "输入错误", f"总数不能超过 {total_combinations} 条")
            return None

        counter = 0
        current_length = 1  # Start with the length of 1

        while counter < num:
            for s in product(alphabet, repeat=current_length):
                combination = ''.join(s)
                # Ensure that the combination length plus flag length does not exceed the total length
                if len(combination) + flag_length > total_length:
                    continue
                # Add leading zeros
                padded_combination = combination.zfill(length)
                data.append(f"{flag}{padded_combination}")
                counter += 1
                if counter >= num:
                    break
            current_length += 1  # Increase the sequence length for the next round of combinations

        return data[:num]  # Ensure the returned data length does not exceed the requested number

    def display_data(self, data):
        self.result_text.clear()
        for item in data:
            self.result_text.append(item)

    def export_data(self, data):
        export_data(self, data)  # 将当前窗口传递给export_data函数
