import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://cn.bing.com/")
    page.get_by_role("searchbox", name="输入搜索词").click()
    page.get_by_role("searchbox", name="输入搜索词").fill("playwright教程")
    page.get_by_label("搜索网页").get_by_role("img").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Playwright 教程 | 菜鸟教程").click()
    page1 = page1_info.value
