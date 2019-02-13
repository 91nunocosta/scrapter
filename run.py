from scrapter.updater import Updater
from scrapy.utils.project import get_project_settings

def execute():
    updater = Updater(get_project_settings())
    updater.run()

if __name__ == "__main__":
    execute()