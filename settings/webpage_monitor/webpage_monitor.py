"""
Module defining the a class and a wrapper function to check for changes in a webpage.
"""

import os
import re
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver

from .. import color_theme
from .webpage_monitor_settings import URLS_TO_MONITOR, WEBDRIVER_LOG_PATH

BASE_DIR = Path(__file__).resolve().parent
HOME_DIR = Path(os.path.expanduser("~"))


COLORS = color_theme.init_theme()
OK = COLORS["dim"][0]
WARN = COLORS["warning"]
DNGR = COLORS["danger"]
CRIT = COLORS["critical"]


class Scraper:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")

        service = webdriver.FirefoxService(log_path=WEBDRIVER_LOG_PATH)

        self.driver = webdriver.Firefox(options=options, service=service)
        self.driver.maximize_window()

        self.url_scheme_subdomain_re = re.compile(r"https?://(www\.)?")

        self.changed_pages = set()
        self.nonresponding_pages = set()
        self.missing_comparison_pages = set()

    def _scrape(self, url: str):
        self.driver.get(url)
        source = BeautifulSoup(self.driver.page_source)

        return source

    def _get_latest_state(self, url: str, domain_path: str):
        latest_state = ""

        try:
            latest_state = str(self._scrape(url))
        except:
            self.nonresponding_pages.add(domain_path)

        return latest_state

    def _get_comparison_state(self, url: str, domain_path: str):
        comparison_state = ""

        if os.path.exists(self._get_comparison_state_file_path(domain_path)):
            with open(self._get_comparison_state_file_path(domain_path), "r") as f:
                comparison_state = f.read()
        else:
            self._write_comparison_state_file(url, domain_path)

        return comparison_state

    def _write_comparison_state_file(self, url: str, domain_path: str):
        latest_state = self._get_latest_state(url, domain_path)
        if latest_state:
            with open(self._get_comparison_state_file_path(domain_path), "w") as f:
                f.write(latest_state)
        self.missing_comparison_pages.add(domain_path)

    def _get_comparison_state_file_path(self, domain_path: str):
        return BASE_DIR / f"comparison_{domain_path}.html"

    def _strip_url_scheme_and_subdomain(self, url: str):
        return (
            self.url_scheme_subdomain_re.sub("", url).rstrip("/").replace("/", "\u2044")
        )

    def compare_sources(self, urls: list[str]):
        for url in urls:
            domain_and_path = self._strip_url_scheme_and_subdomain(url)

            comparison_state = self._get_comparison_state(url, domain_and_path)
            latest_state = self._get_latest_state(url, domain_and_path)

            if latest_state and comparison_state and latest_state != comparison_state:
                self.changed_pages.add(domain_and_path)

        self.driver.quit()

    def report_results(self):
        string_builder = []
        closing_tag = "</span>"
        if self.changed_pages:
            icon = "!"
            style = f"<span foreground='{CRIT}' font='JetBrainsMono Nerd Font bold'>"
            string_builder.append(
                f"{style}{icon}{len(self.changed_pages)}{closing_tag}"
            )
        if self.missing_comparison_pages:
            icon = "?"
            style = f"<span foreground='{DNGR}'>"
            string_builder.append(
                f"{style}{icon}{len(self.missing_comparison_pages)}{closing_tag}"
            )
        if self.nonresponding_pages:
            icon = "-"
            style = f"<span foreground='{WARN}'>"
            string_builder.append(
                f"{style}{icon}{len(self.nonresponding_pages)}{closing_tag}"
            )

        critical_results = "".join(string_builder)
        if critical_results:
            final_result = critical_results
        else:
            style = f"<span foreground='{OK}'>"
            final_result = f"{style}No changes{closing_tag}"

        return final_result


def check_once():
    """
    Wrapper function to init a Scraper instance that checkes all URLs in the global
    URLS_TO_MONITOR list variable.
    """
    scraper = Scraper()
    scraper.compare_sources(URLS_TO_MONITOR)
    return scraper.report_results()
