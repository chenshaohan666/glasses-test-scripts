# 用例1：fill 填字 + press 按回车 → 完成一次搜索（重点）
def test_step3_fill_and_press(page):
    page.goto("https://www.bing.com")

    # fill：往搜索框输入关键词
    page.locator("#sb_form_q").fill("playwright 教程")
    page.wait_for_timeout(500)

    # press：按回车触发搜索（不用找搜索按钮，最稳）
    page.locator("#sb_form_q").press("Enter")
    page.wait_for_timeout(1500)

    # 看看发生了什么
    print("搜索后URL：", page.url)
    print("搜索后标题：", page.title())


# 用例2：点击第一条结果，并接住它打开的新标签页
def test_step3_click(page):
    # 1. 搜索
    page.goto("https://www.bing.com")
    page.locator("#sb_form_q").fill("playwright 教程")
    page.locator("#sb_form_q").press("Enter")
    page.wait_for_timeout(1500)

    # 2. 抓到第一条结果，先看看点的是哪条
    first_result = page.locator("#b_results h2 a").first
    print("我要点击的是：", first_result.inner_text())

    # 3. 关键：点击的同时，用 expect_popup 接住可能弹出的新标签页
    with page.expect_popup() as popup_info:
        first_result.click()
    new_page = popup_info.value        # 新标签页 = 另一个 page 对象
    new_page.wait_for_load_state()     # 等它加载完

    # 4. 这次看新标签页跳哪去了
    print("新标签页URL：", new_page.url)
    print("新标签页标题：", new_page.title())