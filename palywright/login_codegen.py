import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.chanjing.cc/home")
    page.get_by_role("button", name="登录/注册").click()
    page.locator(".icon-box").click()
    page.get_by_text("密码登录").click()
    page.get_by_role("textbox", name="请输入手机号").click()
    page.get_by_role("textbox", name="请输入手机号").fill("18225376190")
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill("123456")
    page.locator(".el-checkbox__inner").first.click()
    page.get_by_role("button", name="登录", exact=True).click()
    page.get_by_role("button", name="同意", exact=True).click()
    page.locator("div").filter(has_text="退出登录").nth(4).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
