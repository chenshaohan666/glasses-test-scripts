from playwright.sync_api import expect

# 用例1：正常版 —— 断言全通过
def test_step4_assert_pass(page):
    page.goto("https://www.bing.com")
    page.locator("#sb_form_q").fill("playwright 教程")
    page.locator("#sb_form_q").press("Enter")
    page.wait_for_timeout(1500)

    # ① 断言：URL 里出现 q=，说明真的执行了搜索
    assert "q=" in page.url

    # ② 断言：标题里包含关键词
    assert "playwright" in page.title().lower()

    # ③ 断言：第一条搜索结果可见（expect 会自动等待出现）
    expect(page.locator("#b_results h2 a").first).to_be_visible()

    print("✅ 全部断言通过，pytest 自动判定成功")


# 用例2：故意失败版 —— 看 pytest 怎么"抓你"
def test_step4_assert_fail(page):
    page.goto("https://www.bing.com")

    # 故意写一个不可能成立的条件
    assert "我故意写错的词" in page.title()