USER_AGENT = "twiscrap"


BOT_NAME = "twiscrap"
LOG_LEVEL = "INFO"

SPIDER_MODULES = ["twiscrap.spiders"]
NEWSPIDER_MODULE = "twiscrap.spiders"

CLOSESPIDER_ITEMCOUNT = 100
DOWNLOAD_DELAY = 1.0


# settings for selenium
from shutil import which

SELENIUM_DRIVER_NAME = "firefox"
SELENIUM_BROWSER_EXECUTABLE_PATH = which("firefox")
SELENIUM_DRIVER_EXECUTABLE_PATH = which("geckodriver")
SELENIUM_DRIVER_ARGUMENTS = ["-headless"]
DOWNLOADER_MIDDLEWARES = {"scrapy_selenium.SeleniumMiddleware": 800}
