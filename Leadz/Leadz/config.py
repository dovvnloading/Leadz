# -*- coding: utf-8 -*-

LLM_MODEL = 'qwen3:8b'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2' 
SEARCH_RESULTS_COUNT = 25
TOP_N_PAGES_TO_ANALYZE = 8
SIMILARITY_THRESHOLD = 0.40

THEMES = {
    'light': {
        'name': 'Light',
        'window_bg': '#FFFFFF',
        'window_text': '#1a1a1a',
        'base': '#F5F5F5',
        'text': '#1a1a1a',
        'text_secondary': '#555555',
        'button_bg': '#E8E8E8',
        'button_text': '#1a1a1a',
        'job_bubble_bg': '#F9F9F9',
        'job_bubble_border': '#E0E0E0',
        'link': '#0066CC',
        'highlight': '#0066CC',
        'highlight_hover': '#0052a3',
        'highlight_pressed': '#003d7a',
        'input_bg': '#FFFFFF',
        'input_border': '#D0D0D0',
        'title_bar_bg': '#F0F0F0',
        'title_bar_border': '#D0D0D0',
    },
    'dark': {
        'name': 'Dark',
        'window_bg': '#1e1e1e',
        'window_text': '#E0E0E0',
        'base': '#252525',
        'text': '#E0E0E0',
        'text_secondary': '#AAAAAA',
        'button_bg': '#353535',
        'button_text': '#E0E0E0',
        'job_bubble_bg': '#2a2a2a',
        'job_bubble_border': '#3a3a3a',
        'link': '#4DA6FF',
        'highlight': '#0066CC',
        'highlight_hover': '#1177DD',
        'highlight_pressed': '#2288EE',
        'input_bg': '#2a2a2a',
        'input_border': '#404040',
        'title_bar_bg': '#2c2c2c',
        'title_bar_border': '#404040',
    }
}