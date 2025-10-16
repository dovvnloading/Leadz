# -*- coding: utf-8 -*-
import json
from pathlib import Path

from PySide6.QtGui import QPalette, QColor

from config import THEMES

class ThemeManager:
    def __init__(self):
        self.config_dir = Path.home() / '.job_llama'
        try:
            self.config_dir.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create config dir: {e}")
        self.settings_file = self.config_dir / 'settings.json'
        self.theme = self._load_theme()

    def _load_theme(self):
        if not self.settings_file.exists():
            return 'dark'
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('theme', 'dark')
        except Exception as e:
            print(f"Settings file error: {e}")
            try:
                self.settings_file.unlink()
            except:
                pass
            return 'dark'

    def save_theme(self, theme_name):
        self.theme = theme_name
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump({'theme': theme_name}, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get_current_theme(self):
        return THEMES.get(self.theme, THEMES['dark'])

    def get_palette(self):
        theme = self.get_current_theme()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(theme['window_bg']))
        palette.setColor(QPalette.WindowText, QColor(theme['window_text']))
        palette.setColor(QPalette.Base, QColor(theme['input_bg']))
        palette.setColor(QPalette.AlternateBase, QColor(theme['base']))
        palette.setColor(QPalette.ToolTipBase, QColor(theme['window_bg']))
        palette.setColor(QPalette.ToolTipText, QColor(theme['window_text']))
        palette.setColor(QPalette.Text, QColor(theme['text']))
        palette.setColor(QPalette.Button, QColor(theme['button_bg']))
        palette.setColor(QPalette.ButtonText, QColor(theme['button_text']))
        palette.setColor(QPalette.BrightText, QColor(theme['window_text']))
        palette.setColor(QPalette.Link, QColor(theme['link']))
        palette.setColor(QPalette.Highlight, QColor(theme['highlight']))
        palette.setColor(QPalette.HighlightedText, QColor(theme['window_bg']))
        return palette