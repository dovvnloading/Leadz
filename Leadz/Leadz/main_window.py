# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                               QScrollArea, QFrame, QSystemTrayIcon,
                               QMenu, QComboBox)
from PySide6.QtGui import QFont, QIcon, QAction, QPixmap, QImage

from config import THEMES
from theme_manager import ThemeManager
from search_worker import JobSearchWorker
from ui_components import CustomTitleBar, JobCard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.theme_manager = ThemeManager()
        self.setWindowTitle("Leadz")
        self.setGeometry(100, 100, 900, 750)
        
        icon = self.create_app_icon()
        self.setWindowIcon(icon)
        
        self.setup_tray_icon(icon)
        self.setup_ui()
        self.apply_theme()
        
        self.worker = None

    def create_app_icon(self):
        return QIcon("C:/Users/Admin/source/repos/Leadz/assets/Leadz.ico")

    def setup_tray_icon(self, icon):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Leadz")
        
        tray_menu = QMenu(self)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide_window)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1) # Border for resizing
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        content_frame = QFrame()
        main_layout.addWidget(content_frame)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        header = QFrame()
        header.setMaximumHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 15, 25, 15)
        header_layout.setSpacing(20)
        
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Bold)
        self.title_label = QLabel("Leadz")
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        theme_label = QLabel("Theme:")
        header_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.setCurrentText(self.theme_manager.theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        self.theme_combo.setMinimumWidth(120)
        header_layout.addWidget(self.theme_combo)
        
        content_layout.addWidget(header)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(separator)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setLineWidth(0)
        
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(25, 20, 25, 20)
        self.results_layout.setSpacing(15)
        self.results_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.results_container)
        content_layout.addWidget(self.scroll_area, 1)
        
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFrameShape(QFrame.NoFrame)
        footer.setMaximumHeight(150)
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(25, 15, 25, 20)
        footer_layout.setSpacing(12)
        
        self.status_label = QLabel("Ready to search. Enter a job title or description.")
        status_font = QFont()
        status_font.setPointSize(9)
        self.status_label.setFont(status_font)
        footer_layout.addWidget(self.status_label)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("e.g., Senior Python Developer, Remote, New York")
        self.query_input.returnPressed.connect(self.start_search)
        self.query_input.setMinimumHeight(42)
        search_layout.addWidget(self.query_input)
        
        self.search_button = QPushButton()
        self.search_button.setObjectName("search_button")
        self.search_button.clicked.connect(self.start_search)
        self.search_button.setFixedSize(42, 42)
        self.search_button.setIconSize(QSize(24, 24))
        search_layout.addWidget(self.search_button)
        
        footer_layout.addLayout(search_layout)
        content_layout.addWidget(footer)

    def apply_theme(self):
        theme = self.theme_manager.get_current_theme()
        palette = self.theme_manager.get_palette()
        self.setPalette(palette)
        
        self.title_bar.update_button_icons(theme)
        
        highlight_hover_alpha = theme['highlight_hover'] + '40'
        highlight_pressed_alpha = theme['highlight_pressed'] + '60'
        
        stylesheet = """
            #title_bar {{
                background-color: {title_bar_bg};
                border-bottom: 1px solid {title_bar_border};
            }}
            #title_bar QLabel {{
                color: {text};
                background-color: transparent;
                border: none;
            }}
            #title_bar_button {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }}
            #title_bar_button:hover {{
                background-color: {button_bg};
            }}
            #close_button {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }}
            #close_button:hover {{
                background-color: #E81123;
            }}
            QMainWindow {{ 
                background-color: {bg}; 
                border: 1px solid {title_bar_border}; 
            }}
            QWidget {{ background-color: {bg}; color: {text}; }}
            QFrame#footer {{
                border-top: 1px solid {border};
            }}
            QLineEdit {{ 
                background-color: {input_bg}; 
                color: {text}; 
                border: 1px solid {border};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 10pt;
            }}
            QLineEdit:focus {{
                border: 1px solid {highlight};
            }}
            QPushButton#search_button {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }}
            QPushButton#search_button:hover {{
                background-color: {highlight_hover_alpha};
            }}
            QPushButton#search_button:pressed {{
                background-color: {highlight_pressed_alpha};
            }}
            QPushButton#search_button:disabled {{
                background-color: {button_bg};
            }}
            QScrollArea {{ background-color: {base}; border: none; }}
            QScrollBar:vertical {{
                border: none;
                background: {base};
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {border};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QComboBox {{
                background-color: {button_bg};
                color: {button_text};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 9pt;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: url(down_arrow.png); 
            }}
            QComboBox QAbstractItemView {{
                background-color: {button_bg};
                border: 1px solid {border};
                selection-background-color: {highlight};
                color: {button_text};
            }}
            QLabel {{ color: {text}; }}
            QFrame {{ background-color: {bg}; border: none; }}
            QFrame[frameShape="4"] {{
                border-top: 1px solid {border};
            }}
        """.format(
            bg=theme['window_bg'], 
            base=theme['base'],
            text=theme['window_text'], 
            input_bg=theme['input_bg'], 
            border=theme['input_border'],
            highlight=theme['highlight'], 
            highlight_hover_alpha=highlight_hover_alpha,
            highlight_pressed_alpha=highlight_pressed_alpha,
            button_bg=theme['button_bg'],
            button_text=theme['button_text'],
            title_bar_bg=theme['title_bar_bg'],
            title_bar_border=theme['title_bar_border']
        )
        self.setStyleSheet(stylesheet)
        
        # Manually set the close button hover icon, as stylesheets can't swap icons
        if hasattr(self.title_bar, 'close_icon_hover'):
            # This is a trick to change icon on hover. We can't do it purely in QSS for custom properties.
            # A more robust way involves custom widgets and event handling, but this is a common workaround.
            # The style sheet will change the BG, and if needed we could use event filters to swap icons.
            # For now, the BG color change is the primary feedback.
            pass

        icon_path = "C:/Users/Admin/source/repos/Leadz/assets/sned.png"
        try:
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                image = pixmap.toImage()
                if theme['name'] == 'Dark':
                    image.invertPixels(QImage.InvertRgb)
                
                self.search_button.setIcon(QIcon(QPixmap.fromImage(image)))
        except Exception as e:
            print(f"Error loading button icon: {e}")

        for i in range(self.results_layout.count()):
            widget = self.results_layout.itemAt(i).widget()
            if isinstance(widget, JobCard):
                widget.refresh_theme()

    def change_theme(self, theme_name):
        self.theme_manager.save_theme(theme_name)
        self.apply_theme()

    def start_search(self):
        query = self.query_input.text().strip()
        if not query or (self.worker and self.worker.isRunning()):
            return
        self.clear_results()
        self.search_button.setEnabled(False)
        self.status_label.setText("Searching...")
        self.worker = JobSearchWorker(query)
        self.worker.status_update.connect(self.update_status)
        self.worker.job_found.connect(self.add_job_card)
        self.worker.finished.connect(self.search_finished)
        self.worker.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def add_job_card(self, job_data):
        card = JobCard(job_data, self.theme_manager)
        self.results_layout.addWidget(card)

    def search_finished(self):
        self.search_button.setEnabled(True)
        if self.results_layout.count() == 0:
            self.status_label.setText("Search complete. No relevant jobs found.")

    def clear_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def hide_window(self):
        self.hide()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == 105: # WindowStateChange
            self.title_bar.update_maximize_icon()
        elif event.type() == 2: # This is QEvent.Hide, but let's be safe
            if self.isMinimized():
                self.hide()
                event.ignore()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()