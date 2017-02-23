# coding=utf-8
""" Code For Selenium Webdrivers """
import platform


WINDOWS32_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-win32/geckodriver"
WINDOWS64_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-win64/geckodriver"
LINUX32_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-linux32/geckodriver"
LINUX64_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-linux64/geckodriver"


def get_geckodriver_path():
    """ Get correct driver path for the type of system the server is running on.

    Note: Assumes Windows or Linux

    :return: gecko driver path
    """
    system_name = platform.system()
    is_64_bit = platform.machine().endswith('64')
    if system_name == "Windows":
        return WINDOWS64_GECKODRIVER_PATH if is_64_bit else WINDOWS32_GECKODRIVER_PATH
    return LINUX64_GECKODRIVER_PATH if is_64_bit else LINUX32_GECKODRIVER_PATH
