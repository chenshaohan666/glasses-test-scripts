def test_step1_just_open(page):
    page.goto("https://www.bing.com")
    print("浏览器已经打开了，当前页面标题是：", page.title())