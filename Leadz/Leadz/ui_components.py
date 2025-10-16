# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QFrame, QTextEdit, QSizePolicy)
from PySide6.QtGui import QFont, QPalette, QPixmap, QPainter, QIcon, QColor, QPen

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("title_bar")
        self.setFixedHeight(32)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setScaledContents(True)
        if parent.windowIcon():
             self.icon_label.setPixmap(parent.windowIcon().pixmap(16, 16))
        layout.addWidget(self.icon_label)

        self.title_label = QLabel(parent.windowTitle())
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_label.setStyleSheet("padding-left: 5px;")
        layout.addWidget(self.title_label)

        button_size = QSize(28, 28)
        icon_size = QSize(12, 12)

        self.minimize_button = QPushButton()
        self.minimize_button.setObjectName("title_bar_button")
        self.minimize_button.setFixedSize(button_size)
        self.minimize_button.setIconSize(icon_size)
        self.minimize_button.clicked.connect(parent.showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton()
        self.maximize_button.setObjectName("title_bar_button")
        self.maximize_button.setFixedSize(button_size)
        self.maximize_button.setIconSize(icon_size)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QPushButton()
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(button_size)
        self.close_button.setIconSize(icon_size)
        self.close_button.clicked.connect(parent.close)
        layout.addWidget(self.close_button)

        self.start_move_pos = None

    def _create_button_icon(self, shape, color):
        pixmap = QPixmap(12, 12)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(color), 1.5)
        painter.setPen(pen)

        if shape == 'minimize':
            painter.drawLine(1, 6, 11, 6)
        elif shape == 'maximize':
            painter.drawRect(1, 1, 10, 10)
        elif shape == 'restore':
            painter.drawRect(3, 1, 8, 8)
            painter.fillRect(1, 3, 8, 8, self.palette().color(QPalette.Window))
            painter.drawRect(1, 3, 8, 8)
        elif shape == 'close':
            painter.drawLine(2, 2, 10, 10)
            painter.drawLine(2, 10, 10, 2)

        painter.end()
        return QIcon(pixmap)

    def update_button_icons(self, theme):
        icon_color = theme['window_text']
        
        self.minimize_icon = self._create_button_icon('minimize', icon_color)
        self.maximize_icon = self._create_button_icon('maximize', icon_color)
        self.restore_icon = self._create_button_icon('restore', icon_color)
        self.close_icon = self._create_button_icon('close', icon_color)
        self.close_icon_hover = self._create_button_icon('close', '#FFFFFF')
        
        self.minimize_button.setIcon(self.minimize_icon)
        self.close_button.setIcon(self.close_icon)
        self.update_maximize_icon()


    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()

    def update_maximize_icon(self):
        if self.parent_window.isMaximized():
            self.maximize_button.setIcon(self.restore_icon)
        else:
            self.maximize_button.setIcon(self.maximize_icon)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_move_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.start_move_pos is not None:
            if self.parent_window.isMaximized():
                return
            delta = event.globalPosition().toPoint() - self.start_move_pos
            self.parent_window.move(self.parent_window.pos() + delta)
            self.start_move_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.start_move_pos = None
        
    def mouseDoubleClickEvent(self, event):
        self.toggle_maximize()

class JobCard(QFrame):
    def __init__(self, job_data, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.job_data = job_data
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # --- Title ---
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setWeight(QFont.Bold)
        self.title_label = QLabel(self.job_data.get("jobTitle", "No Title"))
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)
        
        # --- Company & Location ---
        company_font = QFont()
        company_font.setPointSize(9)
        company_location = "{} - {}".format(self.job_data.get('company', 'N/A'), self.job_data.get('location', 'N/A'))
        self.company_label = QLabel(company_location)
        self.company_label.setFont(company_font)
        layout.addWidget(self.company_label)

        # --- Details Line (Type, Experience, Salary) ---
        details_parts = []
        
        def process_detail(detail_value):
            if isinstance(detail_value, list):
                return ", ".join(map(str, detail_value))
            return str(detail_value)

        job_type_raw = self.job_data.get("job_type", "N/A")
        if job_type_raw and job_type_raw != "N/A":
            details_parts.append(process_detail(job_type_raw))
        
        experience_raw = self.job_data.get("experience", "N/A")
        if experience_raw and experience_raw != "N/A":
            details_parts.append(process_detail(experience_raw))
            
        salary_raw = self.job_data.get("salary", "N/A")
        if salary_raw and salary_raw != "N/A":
            details_parts.append(f"Salary: {process_detail(salary_raw)}")

        if details_parts:
            details_font = QFont()
            details_font.setPointSize(9)
            details_font.setItalic(True)
            self.details_label = QLabel(" | ".join(details_parts))
            self.details_label.setFont(details_font)
            self.details_label.setWordWrap(True)
            layout.addWidget(self.details_label)

        # --- Skills ---
        skills = self.job_data.get("skills", [])
        if skills:
            skills_text = ", ".join(skills) if isinstance(skills, list) else str(skills)
            skills_font = QFont()
            skills_font.setPointSize(9)
            self.skills_label = QLabel(f"<b>Skills:</b> {skills_text}")
            self.skills_label.setFont(skills_font)
            self.skills_label.setWordWrap(True)
            layout.addWidget(self.skills_label)
        
        # --- Summary ---
        summary_text = self.job_data.get("summary", "No summary available.")
        self.summary_edit = QTextEdit(summary_text)
        self.summary_edit.setReadOnly(True)
        self.summary_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.summary_edit.setFrameShape(QFrame.NoFrame)
        self.summary_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_edit.document().setDocumentMargin(0)
        self.summary_edit.setFixedHeight(self.summary_edit.document().size().height())
        layout.addWidget(self.summary_edit, 1)

        # --- Bottom Link ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 5, 0, 0)
        bottom_layout.addStretch()

        url = self.job_data.get("url", "#")
        self.link_label = QLabel('<a href="{}">View Full Listing</a>'.format(url))
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setAlignment(Qt.AlignRight)
        bottom_layout.addWidget(self.link_label)
        
        layout.addLayout(bottom_layout)
        
        self._apply_theme()

    def _apply_theme(self):
        theme = self.theme_manager.get_current_theme()
        
        self.setStyleSheet("""
            QFrame {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """.format(bg=theme['job_bubble_bg'], border=theme['job_bubble_border']))

        self.title_label.setStyleSheet("color: {text}; background-color: transparent; border: none;".format(text=theme['text']))
        self.company_label.setStyleSheet("color: {secondary}; background-color: transparent; border: none;".format(secondary=theme['text_secondary']))
        
        if hasattr(self, 'details_label'):
             self.details_label.setStyleSheet("color: {highlight}; font-style: italic; background-color: transparent; border: none;".format(highlight=theme['highlight']))
        
        if hasattr(self, 'skills_label'):
             self.skills_label.setStyleSheet("color: {secondary}; background-color: transparent; border: none;".format(secondary=theme['text_secondary']))

        self.summary_edit.setStyleSheet("""
            QTextEdit {{
                color: {text};
                background-color: transparent;
                border: none;
                font-size: 9pt;
            }}
        """.format(text=theme['text_secondary']))

        self.link_label.setStyleSheet("color: {link}; background-color: transparent; border: none;".format(link=theme['link']))

    def refresh_theme(self):
        self._apply_theme()