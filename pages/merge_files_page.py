import os
import chardet
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, \
    QHBoxLayout, QSizePolicy
from utils.random_data_generator import BasePage, show_legal_warning

class MergeFilesPage(BasePage):
    def __init__(self):
        super().__init__()

        # 初始化文件路径列表和分隔符
        self.files_list = []  # 用于存储上传的文件路径
        # self.create_widgets()

    def create_widgets(self):
        self.layout.addWidget(QLabel("合并多个文本文件"))

        # 上传文件按钮
        upload_button = QPushButton("选择文件")
        upload_button.clicked.connect(self.upload_files)
        upload_button.setIcon(QIcon('./resources/upload.png'))  # 设置按钮图标
        # upload_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左
        self.layout.addWidget(upload_button)

        # 已上传文件数量和列表显示
        self.uploaded_files_label = QLabel("已上传文件数量: 0")
        self.layout.addWidget(self.uploaded_files_label)

        # 设置 QTextEdit 的高度策略
        self.uploaded_files_text = QTextEdit()
        self.uploaded_files_text.setReadOnly(True)

        # 设置为固定高度，并允许水平扩展
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.uploaded_files_text.setSizePolicy(size_policy)

        # 设置一个适当的高度，例如 80 像素
        self.uploaded_files_text.setFixedHeight(80)
        self.layout.addWidget(self.uploaded_files_text)

        # 分隔符输入框
        self.layout.addWidget(QLabel("请输入分隔符（空格、逗号等）:"))
        self.separator_entry = QLineEdit()
        self.separator_entry.setPlaceholderText("请输入分隔符，例如空格")
        self.layout.addWidget(self.separator_entry)

        # 按钮布局：合并和重置
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        # 合并按钮
        merge_button = QPushButton("合并")
        merge_button.clicked.connect(self.merge_files)
        button_layout.addWidget(merge_button)
        merge_button.setIcon(QIcon('./resources/generate_button.png'))  # 设置按钮图标
        merge_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 重置按钮
        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_fields)
        button_layout.addWidget(reset_button)
        reset_button.setIcon(QIcon('./resources/reset_button.png'))  # 设置按钮图标
        reset_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 显示合并结果的文本框
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("QTextEdit { font-size: 10pt; }")
        self.layout.addWidget(self.result_text)

        # 添加公司 logo
        self.add_logo()

    def upload_files(self):
        # 打开文件对话框，允许用户选择多个文件
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "Text Files (*.txt);;All Files (*)")
        if files:
            self.files_list.extend(files)  # 将选择的文件路径添加到文件列表中
            self.update_uploaded_files_display()

    def update_uploaded_files_display(self):
        """更新已上传文件的数量和文件路径列表"""
        file_count = len(self.files_list)
        self.uploaded_files_label.setText(f"已上传文件数量: {file_count}")
        self.uploaded_files_text.clear()
        self.uploaded_files_text.append("\n".join(self.files_list))  # 显示文件路径列表

    def detect_encoding(self, file_path):
        """自动检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # 读取文件前10KB
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                if encoding:
                    self.result_text.append(f"文件 {file_path} 检测到的编码: {encoding}")
                    return encoding
                else:
                    raise ValueError("无法检测到编码")
        except Exception as e:
            self.result_text.append(f"检测编码失败，尝试常见编码: {e}")
            return None

    def try_open_file(self, file_path):
        """根据自动检测的编码或回退机制打开文件"""
        try:
            # 检测文件编码
            encoding = self.detect_encoding(file_path)
            if encoding:
                # 使用检测到的编码打开文件
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    lines = f.readlines()
                    self.result_text.append(f"使用 {encoding} 编码成功打开文件 {file_path}")
                    return lines
            else:
                raise ValueError("无法检测文件编码")
        except Exception as e:
            self.result_text.append(f"自动检测失败，尝试使用GBK、ISO-8859-1或UTF-8打开: {e}")
            # 回退到 GBK、ISO-8859-1 或 UTF-8 打开
            encodings = ['gbk', 'iso-8859-1', 'utf-8']
            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc, errors='replace') as f:
                        lines = f.readlines()
                        self.result_text.append(f"使用{enc}编码成功打开文件 {file_path}")
                        return lines
                except Exception as e:
                    self.result_text.append(f"使用{enc}编码打开文件失败: {e}")
            raise ValueError("无法打开文件")

    def merge_files(self):
        if not show_legal_warning(self):
            return
        # 检查是否有文件上传
        if not self.files_list:
            QMessageBox.critical(self, "错误", "请选择至少一个文件进行合并")
            return

        # 获取分隔符，默认为空格
        separator = self.separator_entry.text().strip()
        if not separator:
            separator = " "  # 如果用户没有输入分隔符，使用空格作为默认分隔符

        # 新文件名
        output_file_path, _ = QFileDialog.getSaveFileName(self, "保存合并文件", "", "Text Files (*.txt);;All Files (*)")
        if not output_file_path:
            return

        try:
            # 打开所有上传的文件并进行合并
            combined_lines = []  # 用于存储合并后的所有行
            for file_path in self.files_list:
                lines = self.try_open_file(file_path)
                combined_lines.append(lines)  # 将每个文件的行添加到列表中

            # 逐行合并所有文件
            with open(output_file_path, 'w', encoding='utf-8', errors='replace') as output_file:
                for row in zip(*combined_lines):  # 使用zip逐行合并多个文件
                    row = [line.strip() for line in row]  # 去除每行末尾的换行符
                    output_file.write(separator.join(row) + '\n')

            # 显示成功消息
            self.result_text.append(f"文件已成功合并并保存到: {output_file_path}")
            QMessageBox.information(self, "合并成功", f"文件已成功合并并保存到 {output_file_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"合并文件时发生错误: {e}")

    def reset_fields(self):
        # 重置输入框和选择文件
        self.files_list.clear()  # 清空已上传文件列表
        self.uploaded_files_label.setText("已上传文件数量: 0")
        self.uploaded_files_text.clear()
        self.separator_entry.clear()
        self.result_text.clear()
