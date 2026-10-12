from playwright.sync_api import expect

def test_step5_wait(page):
    page.goto("https://www.bing.com")

    search_input = page.locator("#sb_form_q")
    search_input.fill("playwright 教程")
    search_input.press("Enter")

    page.wait_for_url("**q=**")

    first_item = page.locator("#b_results h2 a").first
    expect(first_item).to_be_visible()

    with page.expect_popup(timeout=10000) as popup_info:
        first_item.click()
    new_page = popup_info.value
    
    # 改成 domcontentloaded，DOM解析完成即可，不等广告全部加载
    new_page.wait_for_load_state("domcontentloaded")

    # 断言：确认已经跳转到菜鸟教程域名
    assert "runoob.com" in new_page.url
    assert len(new_page.title()) > 0
    print(f"新页面URL：{new_page.url}")
    print(f"新页面标题：{new_page.title()}")
