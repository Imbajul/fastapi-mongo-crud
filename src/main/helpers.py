import os
import models

app_conf = models.AppSettings()

def setup_data_dir():
    os.makedirs(app_conf.data_dir, exist_ok=True)