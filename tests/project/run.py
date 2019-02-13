from scrapy.utils.project import get_project_settings
from scrapter.updater import Updater


updater = Updater(get_project_settings())
updater.run()
