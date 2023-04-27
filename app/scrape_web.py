from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path
from util import get_name_md5
from functools import reduce, partial
import re

root_dir = Path("./web")
if not root_dir.is_dir():
    root_dir.mkdir(exist_ok=True, parents=True)


def entry(url: str):
    md5_name = get_name_md5(url)
    work_dir = root_dir / md5_name
    work_dir.mkdir(exist_ok=True, parents=True)
    source = scrape_html_from_web(url=url, work_dir=work_dir)
    cleansing_data = html_cleansing(source=source, work_dir=work_dir)
    with open((work_dir / "cleansing.html"), "w") as f:
        f.write(cleansing_data)


def scrape_html_from_web(url: str, work_dir: Path):
    source = None
    cache_path = work_dir / "index.html"
    if cache_path.is_file():
        with open(cache_path, "r", newline="") as site_cache:
            source = site_cache.read()
    else:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(options=options)
        # driver.implicitly_wait(30)
        driver.get(url)
        sleep(5)
        source = driver.page_source
        # driver.save_screenshot("./screenshot.png")
        driver.quit()
        with open(cache_path, "w") as site_cache:
            site_cache.write(source)
    return source


def html_cleansing(source: str, work_dir: str):
    soup = BeautifulSoup(source, "html.parser")
    container = soup.find("div", {"type": "book"})
    title_tag = container.find("h1", {"class": "text-3xl text-ash-800 font-bold"})
    introduction_tag = container.find(
        "p",
        {
            "class": "px-5 py-4 rounded-lg bg-ash-50 text-base text-ash-800 mb-8 whitespace-pre-wrap leading-relaxed"
        },
    )
    ql_editor_tag = container.find("div", {"class": "ql-editor"})

    for tag in ql_editor_tag.find_all(["p", re.compile("h\d+")]):
        text = tag.get_text()
        tag.replace_with(text)

    for tag in soup.find_all(["script", "link", "style", "noscript", "iframe"]):
        tag.extract()

    output_html = soup.prettify()

    with open(work_dir / "cleansing.html", "w") as f:
        f.write(output_html)

    soup = BeautifulSoup(output_html, "html.parser")
    ql_editor_tag = soup.find("div", {"class": "ql-editor"})
    composed_sub = reduce(
        lambda f, g: lambda x: f(g(x)),
        [
            partial(re.compile("\n+").sub, "\n"),
            partial(re.compile("[ \t]+").sub, ""),
        ],
    )
    title = title_tag.get_text().strip()
    introduction = introduction_tag.get_text().strip()
    content = composed_sub(ql_editor_tag.get_text()).strip()
    file_content = f"""標題:
{title}

前言:
{introduction}

正文:
{content}
"""
    with open(work_dir / "file.txt", "w") as file:
        file.write(file_content)

    return output_html


if __name__ == "__main__":
    entry(url="https://www.digiknow.com.tw/knowledge/6425296595c7c")
    # entry(url="https://www.digiknow.com.tw/knowledge/6440f4c7d342e")
