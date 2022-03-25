from config import setting

import urllib

def get_db():
    db_password = urllib.parse.quote_plus(setting.database_password)
   
    URL = f'postgresql://{setting.database_username}:{db_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

    return URL