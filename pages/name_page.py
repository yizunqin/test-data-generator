# coding=utf-8
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox
from utils.random_data_generator import RandomDataGenerator, BasePage, export_data, show_legal_warning, EXPORT_MAX_COUNT

class NamePage(BasePage):
    def __init__(self):
        self.data_generator = RandomDataGenerator()
        super().__init__()
        self.data = None  # 初始化self.data

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成随机姓名"))

        # form_layout = QVBoxLayout()
        # self.layout.addLayout(form_layout)
        #
        # form_layout.addWidget(QLabel("请输入需要生成的数量:"))
        # self.num_entry = QLineEdit()
        # form_layout.addWidget(self.num_entry)

        form_layout = QVBoxLayout()
        self.layout.addLayout(form_layout)
        form_layout.addWidget(QLabel("请输入需要生成的数量:"))

        self.num_entry = QLineEdit()

        # 使用 placeholder 来设置默认显示文本
        self.num_entry.setPlaceholderText("10")  # 显示默认值为10

        # 如果你想要在用户进入输入框时清除 placeholder，也可以实现
        self.num_entry.installEventFilter(self)  # 安装事件过滤器，用于监控焦点事件

        form_layout.addWidget(self.num_entry)

        form_layout.addWidget(QLabel("请选择性别(男/女，非必填):"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])
        form_layout.addWidget(self.gender_combo)

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

    def generate_data(self):
        if not show_legal_warning(self):
            return
        try:
            num_text = self.num_entry.text().strip()  # 获取输入框的内容并去掉空白
            num = int(num_text) if num_text else 10  # 如果输入框为空，默认生成10个
            gender = self.gender_combo.currentText()
            if num <= 0:
                QMessageBox.critical(self, "输入错误", "请输入正整数")
                return
            if num > EXPORT_MAX_COUNT:
                QMessageBox.critical(self, "数量超限", f"单次生成数量上限为 {EXPORT_MAX_COUNT} 条")
                return

            if gender == "男":
                self.data = [self.data_generator.generate_male_name() for _ in range(num)]
            elif gender == "女":
                self.data = [self.data_generator.generate_female_name() for _ in range(num)]
            else:
                self.data = [self.data_generator.generate_random_name() for _ in range(num)]

            self.display_data()
            # QMessageBox.information(self, "生成成功", f"成功生成 {num} 条随机姓名")
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成数据时发生错误: {e}")

    def display_data(self):
        try:
            self.result_text.clear()
            for item in self.data:
                self.result_text.append(item)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示数据时发生错误: {e}")

    def export_data(self, data):
        export_data(self, data)  # 将当前窗口传递给export_data函数
