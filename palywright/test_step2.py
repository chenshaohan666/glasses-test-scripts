def test_step2_locate(page):
    page.goto("https://www.bing.com")

    # 2. 用 ID 抓住必应搜索框
    box = page.locator("#sb_form_q")

    # 3. 验证：找到了几个？可见吗？
    print("找到几个搜索框：", box.count())     # 输出 1 = 抓到了
    print("搜索框可见吗：", box.is_visible())  # 输出 True

    # 4. 填字，证明抓对了
    box.fill("验证定位成功")
    print("填进去的字：", box.input_value())

    page.wait_for_timeout(1500)