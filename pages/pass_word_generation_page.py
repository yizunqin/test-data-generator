# password_generator_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon
from utils.random_data_generator import RandomDataGenerator, export_data, show_legal_warning, EXPORT_MAX_COUNT
from utils.random_data_generator import BasePage
import random

class PasswordGeneratorPage(BasePage):  # 继承 BasePage，获得 reset_fields 等功能
    def __init__(self):
        self.data = None  # 初始化self.data
        super().__init__()

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成随机密码"))

        # 输入密码长度
        self.layout.addWidget(QLabel("请输入密码长度:"))
        self.password_length_entry = QLineEdit()
        self.password_length_entry.setPlaceholderText("8")  # 默认密码长度为8
        self.layout.addWidget(self.password_length_entry)

        # 输入生成的密码数量
        self.layout.addWidget(QLabel("请输入需要生成的密码数量:"))
        self.password_num_entry = QLineEdit()
        self.password_num_entry.setPlaceholderText("5")  # 默认生成5个密码
        self.layout.addWidget(self.password_num_entry)

        # 复选框：选择是否包含大写字母、小写字母、数字和特殊字符
        self.uppercase_checkbox = QCheckBox("包含大写字母")
        self.uppercase_checkbox.setChecked(True)  # 默认选中
        self.layout.addWidget(self.uppercase_checkbox)

        self.lowercase_checkbox = QCheckBox("包含小写字母")
        self.lowercase_checkbox.setChecked(True)  # 默认选中
        self.layout.addWidget(self.lowercase_checkbox)

        self.digit_checkbox = QCheckBox("包含数字")
        self.digit_checkbox.setChecked(True)  # 默认选中
        self.layout.addWidget(self.digit_checkbox)

        self.special_checkbox = QCheckBox("包含特殊字符")
        self.special_checkbox.setChecked(True)  # 默认选中
        self.layout.addWidget(self.special_checkbox)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        # 生成按钮
        generate_button = QPushButton("生成")
        generate_button.clicked.connect(self.generate_passwords)
        button_layout.addWidget(generate_button)
        generate_button.setIcon(QIcon('./resources/generate_button.png'))  # 设置按钮图标
        generate_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 导出按钮
        export_button = QPushButton("导出")
        export_button.clicked.connect(lambda: self.export_data(self.data))
        button_layout.addWidget(export_button)
        export_button.setIcon(QIcon('./resources/export_button.png'))  # 设置按钮图标
        export_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 重置按钮
        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_fields)
        button_layout.addWidget(reset_button)
        reset_button.setIcon(QIcon('./resources/reset_button.png'))  # 设置按钮图标
        reset_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 用于显示生成的密码
        self.password_result_text = QTextEdit()
        self.password_result_text.setReadOnly(True)
        self.password_result_text.setStyleSheet("QTextEdit { font-size: 14pt; }")
        self.layout.addWidget(self.password_result_text, stretch=1)

        # 调用基类方法添加公司logo
        self.add_logo()

    def generate_passwords(self):
        if not show_legal_warning(self):
            return
        try:
            # 获取用户输入的密码长度和生成数量
            length = int(self.password_length_entry.text()) if self.password_length_entry.text() else 8
            num_passwords = int(self.password_num_entry.text()) if self.password_num_entry.text() else 5
            if num_passwords > EXPORT_MAX_COUNT:
                QMessageBox.critical(self, "数量超限", f"单次生成数量上限为 {EXPORT_MAX_COUNT} 条")
                return

            # 获取复选框状态，判断用户选择的字符类型
            include_uppercase = self.uppercase_checkbox.isChecked()
            include_lowercase = self.lowercase_checkbox.isChecked()
            include_digits = self.digit_checkbox.isChecked()
            include_special = self.special_checkbox.isChecked()

            # 至少需要选择一个字符类型
            if not (include_uppercase or include_lowercase or include_digits or include_special):
                QMessageBox.critical(self, "选择错误", "请至少选择一种字符类型")
                return

            # 可选字符池
            char_pool = ''
            if include_uppercase:
                char_pool += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if include_lowercase:
                char_pool += 'abcdefghijklmnopqrstuvwxyz'
            if include_digits:
                char_pool += '0123456789'
            if include_special:
                char_pool += '!@#$%^&*()-_=+[]{}|;:,.<>?'

            # 生成密码
            self.data = []
            for _ in range(num_passwords):
                password = ''.join(random.choice(char_pool) for _ in range(length))
                self.data.append(password)

            # 显示生成的密码
            self.display_data()

        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")

    def display_data(self):
        try:
            self.password_result_text.clear()
            for pwd in self.data:
                self.password_result_text.append(pwd)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示数据时发生错误: {e}")

    def export_data(self, data):
        export_data(self, data)  # 调用 utils.random_data_generator 中的 export_data 函数
