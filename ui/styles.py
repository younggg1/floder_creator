def get_win11_style():
    """返回类 Win11 风格的 QSS 样式表"""
    return """
    /* 全局字体设置 */
    * {
        font-family: "Segoe UI Variable Text", "Microsoft YaHei", sans-serif;
        font-size: 14px;
        outline: none;
    }

    /* 主窗口背景 */
    QMainWindow, QDialog {
        background-color: #f3f3f3;
    }

    /* 输入框样式 */
    QLineEdit, QPlainTextEdit, QTextEdit {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #0067c0;
    }
    QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus {
        border-bottom: 2px solid #0067c0;
        background-color: #ffffff;
    }

    /* 按钮基础样式 */
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 4px;
        padding: 6px 16px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #f9f9f9;
        border-color: #c0c0c0;
    }
    QPushButton:pressed {
        background-color: #f0f0f0;
    }

    /* 强调/主要按钮样式 */
    QPushButton#PrimaryButton {
        background-color: #0067c0;
        color: white;
        border: none;
        font-weight: 500;
    }
    QPushButton#PrimaryButton:hover {
        background-color: #1975c5;
    }
    QPushButton#PrimaryButton:pressed {
        background-color: #005fb8;
    }

    /* 复选框样式 */
    QCheckBox {
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 1px solid #dcdcdc;
        border-radius: 3px;
        background: white;
    }
    QCheckBox::indicator:checked {
        background-color: #0067c0;
        border-color: #0067c0;
        image: url(check.png); /* 这里如果需要可以生成一个，暂时用颜色替代 */
    }

    /* 组合框样式 */
    QGroupBox {
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        font-weight: bold;
        background-color: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 20px;
        padding: 0 5px;
        color: #454545;
    }

    /* 滚动条预览样式 */
    QScrollBar:vertical {
        border: none;
        background: #f3f3f3;
        width: 8px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #cdcdcd;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #bababa;
    }

    /* 标签样式 */
    QLabel {
        color: #1a1a1a;
    }

    /* 日志区域样式 */
    QPlainTextEdit#LogArea {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 13px;
        color: #333333;
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
    }
    """
