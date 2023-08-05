# -*- coding: utf-8 -*-

"""
PyInstaller's hook.
"""


import donb_custom_widget
from pathlib import Path
data_folder = Path(donb_custom_widget.__file__).parent / "data"

ui_files_path = data_folder / "ui_files"
datas = [(str(ui_files_path), "data/ui_files")]
