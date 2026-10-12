from playwright.sync_api import expect

# 重点：fixture 加 slow_mo，单位毫秒，每一步操作停顿，看清浏览器动作
def test_debug_three_tools(page):
    page.goto("https://www.bing.com")

    search_input = page.locator("#sb_form_q")
    search_input.fill("百度")

    # ---------- 调试三件套 ① pause() 断点暂停，浏览器会弹出调试工具，手动检查页面 ----------
    page.pause()

    search_input.press("Enter")
    page.wait_for_url("**q=**")

    first_result = page.locator("#b_results h2 a").first
    expect(first_result).to_be_visible(timeout=8000)

    with page.expect_popup(timeout=10000) as popup_info:
        first_result.click()
    new_tab = popup_info.value
    new_tab.wait_for_load_state("domcontentloaded")

    # ---------- 调试三件套 ② screenshot 截图，报错自动留存现场 ----------
    new_tab.screenshot(path="./debug_ok.png", full_page=True)

    # assert "runoob.com" in new_tab.url
    assert len(new_tab.title()) > 0

    # 制造一个错误，触发失败截图演示，打开下面注释
    assert "baidu.com" in new_tab.url
