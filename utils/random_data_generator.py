from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, \
    QMessageBox, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog, QSpacerItem, QSizePolicy, QCheckBox
from faker import Faker
import re
import random
from utils.data import provinces

fake = Faker('zh_CN')

class RandomDataGenerator:
    def generate_phone_number(self):
        return fake.phone_number()

    def generate_email(self):
        return fake.email()

    def generate_address(self):
        address = fake.address()
        # 去除邮政编码
        address = re.sub(r'\d{6}', '', address)
        # 去除多余的换行符和空格
        address = ' '.join(address.split())
        return address

    def generate_male_name(self):
        return fake.name_male()

    def generate_female_name(self):
        return fake.name_female()

    def generate_random_name(self):
        return fake.name()

    def get_random_district_code(self, provinces):
        province = random.choice(list(provinces.keys()))
        cities = [city for city in provinces[province].keys() if city != "province_code"]
        if not cities:
            return provinces[province]["province_code"]  # 返回省级代码
        city = random.choice(cities)
        districts = [district for district in provinces[province][city].keys() if district != "city_code"]
        if not districts:
            return provinces[province][city]["city_code"]  # 返回市级代码
        district = random.choice(districts)
        return provinces[province][city][district]

# def export_data(data):
#     try:
#         file_path, _ = QFileDialog.getSaveFileName(None, "保存文件", "", "Text files (*.txt);;All files (*)")
#         if file_path:
#             with open(file_path, 'w') as f:
#                 for item in data:
#                     f.write(f"{item}\n")
#             QMessageBox.information(None, "导出成功", f"数据成功导出到 {file_path}")
#     except Exception as e:
#         QMessageBox.critical(None, "错误", f"导出数据时发生错误: {e}")

_has_warned = False


def show_legal_warning(parent):
    """显示法律警告弹窗，全局仅首次生成时弹出。"""
    global _has_warned
    if _has_warned:
        return True
    reply = QMessageBox.warning(
        parent, "法律警告",
        "1. 本工具生成的所有数据均为虚拟测试数据，不代表任何真实个人或机构。\n"
        "2. 严禁用于伪造证件、冒充身份、批量注册虚假账户、诈骗等任何非法活动。\n"
        "3. 继续使用即表示您同意遵守法律法规并承担全部责任。\n\n"
        "是否继续？",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        _has_warned = True
        return True
    else:
        return False


EXPORT_HEADER = "# 虚拟测试数据，严禁用于非法用途"
EXPORT_MAX_COUNT = 1000


def export_data(parent, data):
    if not data:
        QMessageBox.critical(parent, "错误", "没有数据可导出，请先生成数据")
        return
    try:
        file_path, _ = QFileDialog.getSaveFileName(parent, "保存文件", "", "Text files (*.txt);;All files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(EXPORT_HEADER + "\n")
                for item in data:
                    f.write(f"{item}\n")
            QMessageBox.information(parent, "导出成功", f"数据成功导出到 {file_path}")
    except Exception as e:
        QMessageBox.critical(parent, "错误", f"导出数据时发生错误: {e}")


class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon('resources/background.png'))  # 设置窗口图标
        self.create_widgets()

    def create_widgets(self):
        pass

    def reset_fields(self):
        # 重置所有 QLineEdit 输入框
        for widget in self.findChildren(QLineEdit):
            widget.clear()

        # 重置所有 QComboBox 下拉框
        for widget in self.findChildren(QComboBox):
            widget.setCurrentIndex(-1)

        # 清除所有 QTextEdit 文本显示框
        for widget in self.findChildren(QTextEdit):
            widget.clear()

        # 重置所有 QTreeWidget，如果有的话
        for widget in self.findChildren(QTreeWidget):
            widget.clear()

        # 重置所有 QCheckBox，默认全部选中
        for widget in self.findChildren(QCheckBox):
            widget.setChecked(True)

        # 针对特定页面的额外重置逻辑，比如重新填充地区树或设置 district_code
        if hasattr(self, 'populate_district_tree'):
            self.populate_district_tree(provinces)

        if hasattr(self, 'district_code'):
            self.district_code = None

    def add_logo(self):
        # 创建水平布局和占位符，使logo固定在右下角
        logo_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        logo_layout.addItem(spacer)

        logo_label = QLabel()
        pixmap = QPixmap('resources/company_logo.png')
        logo_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 调整大小
        logo_layout.addWidget(logo_label)

        self.layout.addLayout(logo_layout)
