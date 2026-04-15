from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QTextEdit, QScrollArea, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from utils.random_data_generator import BasePage


class WelcomePage(BasePage):
    def create_widgets(self):
        self.layout.addWidget(QLabel("欢迎使用数据生成器工具！"))

        button_layout = QVBoxLayout()

        self.functionality_button = QPushButton("实现功能")
        self.functionality_button.setIcon(QIcon('resources/functionality_icon.png'))  # 添加图标
        self.functionality_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")
        self.functionality_button.clicked.connect(lambda: self.display_content("功能"))
        button_layout.addWidget(self.functionality_button)

        self.rules_button = QPushButton("生成规则")
        self.rules_button.setIcon(QIcon('resources/rules_icon.png'))  # 添加图标
        self.rules_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")
        self.rules_button.clicked.connect(lambda: self.display_content("规则"))
        button_layout.addWidget(self.rules_button)

        self.notes_button = QPushButton("注意事项")
        self.notes_button.setIcon(QIcon('resources/notes_icon.png'))  # 添加图标
        self.notes_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")
        self.notes_button.clicked.connect(lambda: self.display_content("注意事项"))
        button_layout.addWidget(self.notes_button)

        # 新增版本说明按钮
        self.version_button = QPushButton("版本说明")
        self.version_button.setIcon(QIcon('resources/version_icon.png'))  # 添加图标
        self.version_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")
        self.version_button.clicked.connect(lambda: self.display_content("版本说明"))
        button_layout.addWidget(self.version_button)

        # 新增版本说明按钮
        self.version_button = QPushButton("法律责任归属")
        self.version_button.setIcon(QIcon('resources/attribution_of_legal_responsibility.png'))  # 添加图标
        self.version_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")
        self.version_button.clicked.connect(lambda: self.display_content("归属"))
        button_layout.addWidget(self.version_button)

        self.layout.addLayout(button_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        self.add_logo()

        # 默认展示第一个按钮下的内容
        self.display_content("归属")

    def display_content(self, content_type):
        for i in reversed(range(self.content_layout.count())):
            widget_to_remove = self.content_layout.itemAt(i).widget()
            self.content_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        if content_type == "功能":
            content = (
                "该工具完成以下功能：\n\n"
                "1. 生成随机身份证号\n"
                "2. 生成统一社会信用代码\n"
                "3. 生成随机数据（电子邮件、地址）\n"
                "4. 生成随机电话号码\n"
                "5. 生成随机姓名\n"
                "6. 生成自增数据\n"
            )
        elif content_type == "规则":
            content = (
                "生成数据的条件填写及规则说明：\n\n"
                "1. 输入生成数量：请输入正整数，表示需要生成的数据条数。\n"
                "2. 区划选择：通过树状结构选择区划，非必填。\n"
                "3. 生日：格式为 YYYY.MM.DD，非必填。\n"
                "4. 性别：填写男或女，非必填。\n"
                "5. 数据类型选择：选择生成的数据类型（电子邮件、地址）。\n"
                "6. 姓名生成选择性别后，生成的数据也只会更贴近男或女，会出现男性包含女性姓名的情况，或女性包含男性姓名的情况。\n"
                "7. 自增数据生成条件标志位非必填，不填写的条件下，默认为0\n"
                "8. 自增数据生成条件数据类型非必填，不填写的条件下，默认为数字\n"
            )
        elif content_type == "注意事项":
            content = (
                "注意事项：\n\n"
                "1. 确保输入的生成数量为正整数。\n"
                "2. 区划选择非必填，但若选择则需选择有效区划。\n"
                "3. 生日格式必须为 YYYYMMDD，若不填则随机生成。\n"
                "4. 性别填写必须为男或女，若不填则随机生成。\n"
                "5. 数据类型选择必须为电子邮件或地址之一。\n"
                "6. 自增数据总位数条件为必填项。\n"
                "7. 自增数据数据类型选择字母时：总位数与生成条数有逻辑关系，\n"
                "   总位数为1时生成条数不能超过26，为2时不能超过26*26+26，\n"
                "   以此类推；标志位占据总位数1位，例如标志位输入1个字符，\n"
                "   总位数为2，则不能超过26条，以此类推。"
            )
        elif content_type == "版本说明":
            content = (
                "版本说明：\n\n"
                "版本 1.0.1:\n"
                "1. 增加了生成自增数据功能。\n"
                "2. 优化了用户界面布局。\n"
                "3. 修复了已知bug。\n\n"
                "版本 1.0.0:\n"
                "1. 初始版本，提供基础的随机数据生成功能。\n"
            )

        elif content_type == "归属":
            content = (
                "开发者声明:\n\n"
                "1. 本工具的开发者及贡献者不对您使用本工具的行为承担任何法律责任。\n"
                "2. 您是本工具的唯一使用者，对使用本工具产生的一切后果负全部责任。\n\n"
                "使用者责任:\n\n"
                "若您将本工具或其生成的数据用于违法活动，\n"
                "您将自行承担相应的民事、行政或刑事责任，开发者有权向司法机关举报。\n\n"
                "平台责任:\n\n"
                "本工具托管于第三方代码托管平台（如 GitHub），\n"
                "平台不对本工具的内容及使用后果负责。\n"
            )

        content_label = QLabel(content)
        content_label.setWordWrap(True)
        self.content_layout.addWidget(content_label)
