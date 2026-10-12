def test_step2_more_ways(page):
    page.goto("https://www.bing.com")

    # 4 种抓法（③ 修正：.first 是属性，不加括号）
    print("① ID 抓法    #sb_form_q             →", page.locator("#sb_form_q").count())
    print("② 层级抓法   #sb_form input         →", page.locator("#sb_form input").count())   # 3 = 抓宽了，正常
    print("③ 位置抓法   input 第1个             →", page.locator("input").first.count())       # .first 不加括号
    print("④ 模糊抓法   [id*='sb_form']         →", page.locator('[id*="sb_form"]').count())   # 可能 1 也可能 2

    # ⑤ 加一条：层级 + ID 双重锁定，一定是 1
    print("⑤ 双重锁定   #sb_form input#sb_form_q →", page.locator("#sb_form input#sb_form_q").count())

    # 填字验证
    page.locator("#sb_form_q").fill("多抓法验证")
    print("填进去的字：", page.locator("#sb_form_q").input_value())

    page.wait_for_timeout(1500)