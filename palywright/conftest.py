import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "viewport": {"width": 1920, "height": 1080},
        "extra_http_headers": {
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
    }


@pytest.fixture(scope="function")
def page(page):
    # 清除webdriver标记
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
    """)
    yield page

    # 用例失败自动截图
    if hasattr(page.test_case, "failed") and page.test_case.failed:
        page.screenshot(path="bing_fail.png", full_page=True)
