# Git常用操作命令

---

## 一、第一次使用

### 1. 克隆远程仓库（第一次下载代码）
```cmd
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
```

### 2. 配置用户名和邮箱（只需要做一次）
```cmd
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

---

## 二、日常操作（最常用）

### 1. 查看当前状态
```cmd
git status
```
> 看哪些文件改了，哪些还没提交。

### 2. 提交代码（改完代码后）
```cmd
# 添加所有修改的文件
git add .

# 提交到本地仓库
git commit -m "改了什么功能"

# 推送到GitHub
git push
```

> 三步：`add` → `commit` → `push`

---

## 三、拉取代码

### 拉取最新代码（别人改了代码后）
```cmd
git pull
```

> 把GitHub上的最新代码拉到本地。

---

## 四、查看历史

### 查看提交记录
```cmd
git log --oneline
```

> 简洁的提交历史。

### 查看具体某个文件改了什么
```cmd
git diff 文件名
```

---

## 五、撤销操作

### 撤销还没add的修改
```cmd
git checkout 文件名
```

### 撤销已经add但还没commit的
```cmd
git reset HEAD 文件名
```

---

## 六、分支操作（可选）

### 新建分支
```cmd
git checkout -b 分支名
```

### 切换分支
```cmd
git checkout 分支名
```

### 推送分支到GitHub
```cmd
git push -u origin 分支名
```

---

## 七、常见问题

### 1. push报错，说远程有新内容
```cmd
git pull origin main --rebase
git push
```

### 2. 想放弃本地修改，用远程的
```cmd
git fetch origin
git reset --hard origin/main
```

### 3. 不想上传某些文件
在项目根目录创建 `.gitignore` 文件，写上：
```
__pycache__/
*.pyc
测试报告_*/
screenshots/
```

---

## 日常工作流（记住这三个就行）

```cmd
# 早上上班，先拉最新代码
git pull

# 改完代码，提交
git add .
git commit -m "改了什么"
git push
```

就这三步，够日常用了。
