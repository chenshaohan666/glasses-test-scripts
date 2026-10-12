from playwright.sync_api import expect

def test_chanjing_login_success(page):
    """场景：蝉镜网站-密码登录正向用例"""
    page.goto("https://www.chanjing.cc/home")

    # 打开登录弹窗
    page.get_by_role("button", name="登录/注册").click()
    page.locator(".icon-box").click()
    page.get_by_text("密码登录").click()

    # 输入账号密码
    page.get_by_role("textbox", name="请输入手机号").fill("18225376190")
    page.get_by_role("textbox", name="请输入密码").fill("123456")

    page.locator(".el-checkbox__inner").first.click()
    page.get_by_role("button", name="登录", exact=True).click()
    page.get_by_role("button", name="同意", exact=True).click()

    # 校验1：登录之后登录注册按钮消失
    expect(page.get_by_role("button", name="登录/注册")).not_to_be_visible(timeout=8000)

    # 校验2：侧边栏【我的】出现，确认登录态
    my_tab = page.get_by_role("link", name="我的")
    expect(my_tab).to_be_visible(timeout=8000)

    # ---------------- hover悬浮头像，弹出悬浮下拉菜单 ----------------
    # 筛选正确的头像组件，过滤多余的.c-user元素
    avatar = page.locator(".c-user").filter(has_text="个人中心").first
    expect(avatar).to_be_visible(timeout=8000)

    # ✅模拟鼠标悬浮 hover，不是click！hover之后悬浮面板才渲染
    avatar.hover()

    # 悬浮之后，退出登录元素变为可见
    logout_btn = page.get_by_text("退出登录")
    expect(logout_btn).to_be_visible(timeout=5000)

    # 点击退出登录
    logout_btn.click()

    # 断言退出成功：登录/注册按钮重新出现
    expect(page.get_by_role("button", name="登录/注册")).to_be_visible(timeout=8000)
