# AList魔改示例教程

> 标题：AList魔改示例教程
> 分类：AList网盘
> 标签：docker、alist、alist美化
> 原文：https://www.xinz.fun/archives/AListmogai

> **导读**：这篇是「AList魔改示例教程」的实操教程。下文按「[**前言**](https://anwen-anyi.github.io/index/03-code.html#%E5%89%8D%E8%A8%80)」「[**1. 先修改 Loading 试试水**](https://anwen-anyi.github.io/index/03-code.html#_1-%E5%85%88%E4%BF%AE%E6%94%B9-loading-%E8%AF%95%E8%AF%95%E6%B0%B4)」「[**2. 修改并且取消在加密码情况下的出现的登录按钮**](https://anwen-anyi.github.io/index/03-code.html#_2-%E4%BF%AE%E6%94%B9%E5%B9%B6%E4%B8%94%E5%8F%96%E6%B6%88%E5%9C%A8%E5%8A%A0%E5%AF%86%E7%A0%81%E6%83%85%E5%86%B5%E4%B8%8B%E7%9A%84%E5%87%BA%E7%8E%B0%E7%9A%84%E7%99%BB%E5%BD%95%E6%8C%89%E9%92%AE)」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾AList网盘的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. [**前言**](https://anwen-anyi.github.io/index/03-code.html#%E5%89%8D%E8%A8%80)
2. [**1. 先修改 Loading 试试水**](https://anwen-anyi.github.io/index/03-code.html#_1-%E5%85%88%E4%BF%AE%E6%94%B9-loading-%E8%AF%95%E8%AF%95%E6%B0%B4)
3. [**2. 修改并且取消在加密码情况下的出现的登录按钮**](https://anwen-anyi.github.io/index/03-code.html#_2-%E4%BF%AE%E6%94%B9%E5%B9%B6%E4%B8%94%E5%8F%96%E6%B6%88%E5%9C%A8%E5%8A%A0%E5%AF%86%E7%A0%81%E6%83%85%E5%86%B5%E4%B8%8B%E7%9A%84%E5%87%BA%E7%8E%B0%E7%9A%84%E7%99%BB%E5%BD%95%E6%8C%89%E9%92%AE)
4. [**3.修改了不登录的后台显示**](https://anwen-anyi.github.io/index/03-code.html#_3-%E4%BF%AE%E6%94%B9%E4%BA%86%E4%B8%8D%E7%99%BB%E5%BD%95%E7%9A%84%E5%90%8E%E5%8F%B0%E6%98%BE%E7%A4%BA)
5. [**4. 取消游客访问和语言选择的按钮默认为简体中文**](https://anwen-anyi.github.io/index/03-code.html#_4-%E5%8F%96%E6%B6%88%E6%B8%B8%E5%AE%A2%E8%AE%BF%E9%97%AE%E5%92%8C%E8%AF%AD%E8%A8%80%E9%80%89%E6%8B%A9%E7%9A%84%E6%8C%89%E9%92%AE%E9%BB%98%E8%AE%A4%E4%B8%BA%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
6. [**5.删除"本地设置"里面的语言切换按钮，已经默认为中文**](https://anwen-anyi.github.io/index/03-code.html#_5-%E5%88%A0%E9%99%A4-%E6%9C%AC%E5%9C%B0%E8%AE%BE%E7%BD%AE-%E9%87%8C%E9%9D%A2%E7%9A%84%E8%AF%AD%E8%A8%80%E5%88%87%E6%8D%A2%E6%8C%89%E9%92%AE-%E5%B7%B2%E7%BB%8F%E9%BB%98%E8%AE%A4%E4%B8%BA%E4%B8%AD%E6%96%87)
7. [**6. 将本地设置里面的夜间/白天 切换模式和刷新按钮(刷新需要登录)移动到主页**](https://anwen-anyi.github.io/index/03-code.html#_6-%E5%B0%86%E6%9C%AC%E5%9C%B0%E8%AE%BE%E7%BD%AE%E9%87%8C%E9%9D%A2%E7%9A%84%E5%A4%9C%E9%97%B4-%E7%99%BD%E5%A4%A9-%E5%88%87%E6%8D%A2%E6%A8%A1%E5%BC%8F%E5%92%8C%E5%88%B7%E6%96%B0%E6%8C%89%E9%92%AE-%E5%88%B7%E6%96%B0%E9%9C%80%E8%A6%81%E7%99%BB%E5%BD%95-%E7%A7%BB%E5%8A%A8%E5%88%B0%E4%B8%BB%E9%A1%B5)
8. [**7.将登录页面的 "登录到" 隐藏，后期适配自己的使用**](https://anwen-anyi.github.io/index/03-code.html#_7-%E5%B0%86%E7%99%BB%E5%BD%95%E9%A1%B5%E9%9D%A2%E7%9A%84-%E7%99%BB%E5%BD%95%E5%88%B0-%E9%9A%90%E8%97%8F-%E5%90%8E%E6%9C%9F%E9%80%82%E9%85%8D%E8%87%AA%E5%B7%B1%E7%9A%84%E4%BD%BF%E7%94%A8)
9. [**8.ipa界面添加下载和复制链接按钮,同时添加巨魔安装按钮**](https://anwen-anyi.github.io/index/03-code.html#_8-ipa%E7%95%8C%E9%9D%A2%E6%B7%BB%E5%8A%A0%E4%B8%8B%E8%BD%BD%E5%92%8C%E5%A4%8D%E5%88%B6%E9%93%BE%E6%8E%A5%E6%8C%89%E9%92%AE-%E5%90%8C%E6%97%B6%E6%B7%BB%E5%8A%A0%E5%B7%A8%E9%AD%94%E5%AE%89%E8%A3%85%E6%8C%89%E9%92%AE)
10. [**9. 去掉底部内容（有原因的）**](https://anwen-anyi.github.io/index/03-code.html#_9-%E5%8E%BB%E6%8E%89%E5%BA%95%E9%83%A8%E5%86%85%E5%AE%B9-%E6%9C%89%E5%8E%9F%E5%9B%A0%E7%9A%84)
11. [**10. 添加一个infuse播放器(3.9.2版本移植到官方内了)**](https://anwen-anyi.github.io/index/03-code.html#_10-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AAinfuse%E6%92%AD%E6%94%BE%E5%99%A8-3-9-2%E7%89%88%E6%9C%AC%E7%A7%BB%E6%A4%8D%E5%88%B0%E5%AE%98%E6%96%B9%E5%86%85%E4%BA%86)
12. [**11. 修改一下搜索，变的更加匹配 ✅**](https://anwen-anyi.github.io/index/03-code.html#_11-%E4%BF%AE%E6%94%B9%E4%B8%80%E4%B8%8B%E6%90%9C%E7%B4%A2-%E5%8F%98%E7%9A%84%E6%9B%B4%E5%8A%A0%E5%8C%B9%E9%85%8D-%E2%9C%85)
13. 以及其余 5 个小节

## [**前言**](https://anwen-anyi.github.io/index/03-code.html#%E5%89%8D%E8%A8%80)

虽然默认的也挺好的，但是吧就是想折腾折腾，就魔改了一下前端嘿嘿

以下代码是我自己魔改了前端的一些地方，虽然可能位置和行数不太对，大概浮动的地方不会差很大的.

如果需要修改的话自己clone前端代码哦，可以[**在线调试**](https://anwen-anyi.github.io/index/build/kaifa.html)，具体怎么调试也很简单

## [**1. 先修改 Loading 试试水**](https://anwen-anyi.github.io/index/03-code.html#_1-%E5%85%88%E4%BF%AE%E6%94%B9-loading-%E8%AF%95%E8%AF%95%E6%B0%B4)

源码文件位置：**alist-web\src\components\FullLoading.tsx**

查看**hope**文档链接：[**https://hope-ui.com/docs/feedback/spinneropen**](https://hope-ui.com/docs/feedback/spinneropen) [**in new window**](https://hope-ui.com/docs/feedback/spinner)

点击查看示例代码

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE)

![配图](https://anwen-anyi.github.io/img/code/1.png)

## [**2. 修改并且取消在加密码情况下的出现的登录按钮**](https://anwen-anyi.github.io/index/03-code.html#_2-%E4%BF%AE%E6%94%B9%E5%B9%B6%E4%B8%94%E5%8F%96%E6%B6%88%E5%9C%A8%E5%8A%A0%E5%AF%86%E7%A0%81%E6%83%85%E5%86%B5%E4%B8%8B%E7%9A%84%E5%87%BA%E7%8E%B0%E7%9A%84%E7%99%BB%E5%BD%95%E6%8C%89%E9%92%AE)

修改取消原因:修改了登录界面和后台入口的地址防止泄露，[**如何修改登录地址和后台地址**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E5%8F%B0%E5%9C%B0%E5%9D%80%E5%92%8C%E7%99%BB%E5%BD%95%E5%9C%B0%E5%9D%80)

源码文件位置：**alist-web\src\pages\home\Password.tsx**

```json
{/* 上面是原来的 下面是我自己改的，大概位置在48行，找不到可以用浏览器搜索 */}
          {/* <Text>{t("global.have_account")}</Text> */}
          {/* <Text
            color="$info9"
            as={LinkWithBase}
            href={`/@login?redirect=${encodeURIComponent(location.pathname)}`}
          >
            {t("global.go_login")}
          </Text> */}

          <Text>{t("不公开去要密码或离开")}</Text>
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-1)

![配图](https://anwen-anyi.github.io/img/code/2.png)

## [**3.修改了不登录的后台显示**](https://anwen-anyi.github.io/index/03-code.html#_3-%E4%BF%AE%E6%94%B9%E4%BA%86%E4%B8%8D%E7%99%BB%E5%BD%95%E7%9A%84%E5%90%8E%E5%8F%B0%E6%98%BE%E7%A4%BA)

源码文件位置：**alist-web\src\pages\manage\users\Profile.tsx**

点击查看示例代码

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-2)

![配图](https://anwen-anyi.github.io/img/code/3.png)

## [**4. 取消游客访问和语言选择的按钮默认为简体中文**](https://anwen-anyi.github.io/index/03-code.html#_4-%E5%8F%96%E6%B6%88%E6%B8%B8%E5%AE%A2%E8%AE%BF%E9%97%AE%E5%92%8C%E8%AF%AD%E8%A8%80%E9%80%89%E6%8B%A9%E7%9A%84%E6%8C%89%E9%92%AE%E9%BB%98%E8%AE%A4%E4%B8%BA%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

#### [**如何改成默认为简体中文：**](https://anwen-anyi.github.io/index/03-code.html#%E5%A6%82%E4%BD%95%E6%94%B9%E6%88%90%E9%BB%98%E8%AE%A4%E4%B8%BA%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

- 首先先拉取中文语言包，丢进去初始化一下，具体怎么初始化点击这里查看教程 ==> [**win版**](https://anwen-anyi.github.io/index/build/win.html#_1-4-%E6%89%8B%E5%8A%A8%E4%B8%8B%E8%BD%BD%E8%AF%AD%E8%A8%80%E5%8C%85%E5%9C%B0%E5%9D%80)，[**Linux版**](https://anwen-anyi.github.io/index/build/linux.html#_1-4-%E4%B8%8B%E8%BD%BD%E8%AF%AD%E8%A8%80%E6%96%87%E4%BB%B6%E5%B9%B6%E4%B8%94%E5%88%9D%E5%A7%8B%E5%8C%96)
- 然后英语(en)的直接删除了即可，语言文件夹里面只剩下了 lang/zh\_cn 这个中文的 这样就会默认使用中文的

删除英文语言文件后的错误

源码文件位置：**alist-web\src\pages\login\index.tsx**

```json
        {/* 177行，取消游客访问 */}
        {/* <Button
          w="$full"
          colorScheme="accent"
          onClick={() => {
            changeToken()
            to(
              decodeURIComponent(searchParams.redirect || base_path || "/"),
              true
            )
          }}
        >
          {t("login.use_guest")}
        </Button> */}

          {/* 198行，Ctrl+F查下面的源码关键字修改，取消语言选择 */}
          {/* <SwitchLanguageWhite /> */}
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-3)

![配图](https://anwen-anyi.github.io/img/code/4.png)

## [**5.删除"本地设置"里面的语言切换按钮，已经默认为中文**](https://anwen-anyi.github.io/index/03-code.html#_5-%E5%88%A0%E9%99%A4-%E6%9C%AC%E5%9C%B0%E8%AE%BE%E7%BD%AE-%E9%87%8C%E9%9D%A2%E7%9A%84%E8%AF%AD%E8%A8%80%E5%88%87%E6%8D%A2%E6%8C%89%E9%92%AE-%E5%B7%B2%E7%BB%8F%E9%BB%98%E8%AE%A4%E4%B8%BA%E4%B8%AD%E6%96%87)

如何默认中文，看上面我的[**查看操作**](https://anwen-anyi.github.io/index/03-code.html#_4-%E5%8F%96%E6%B6%88%E6%B8%B8%E5%AE%A2%E8%AE%BF%E9%97%AE%E5%92%8C%E8%AF%AD%E8%A8%80%E9%80%89%E6%8B%A9%E7%9A%84%E6%8C%89%E9%92%AE%E9%BB%98%E8%AE%A4%E4%B8%BA%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)，只留下中文的话如果你浏览器语言是英文的浏览器会报错 👉 [**解决办法**](https://anwen-anyi.github.io/index/03-code.html#_4-%E5%8F%96%E6%B6%88%E6%B8%B8%E5%AE%A2%E8%AE%BF%E9%97%AE%E5%92%8C%E8%AF%AD%E8%A8%80%E9%80%89%E6%8B%A9%E7%9A%84%E6%8C%89%E9%92%AE%E9%BB%98%E8%AE%A4%E4%B8%BA%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

源码文件位置：**alist-web\src\pages\home\toolbar\LocalSettings.tsx**

```json
              {/* 第65行隐藏即可 */}
              {/* <SwitchLanguageWhite /> */}
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-4)

![配图](https://anwen-anyi.github.io/img/code/5.png)

## [**6. 将本地设置里面的夜间/白天 切换模式和刷新按钮(刷新需要登录)移动到主页**](https://anwen-anyi.github.io/index/03-code.html#_6-%E5%B0%86%E6%9C%AC%E5%9C%B0%E8%AE%BE%E7%BD%AE%E9%87%8C%E9%9D%A2%E7%9A%84%E5%A4%9C%E9%97%B4-%E7%99%BD%E5%A4%A9-%E5%88%87%E6%8D%A2%E6%A8%A1%E5%BC%8F%E5%92%8C%E5%88%B7%E6%96%B0%E6%8C%89%E9%92%AE-%E5%88%B7%E6%96%B0%E9%9C%80%E8%A6%81%E7%99%BB%E5%BD%95-%E7%A7%BB%E5%8A%A8%E5%88%B0%E4%B8%BB%E9%A1%B5)

文件位置：**alist-web\src\pages\home\toolbar\Right.tsx**

夜间模式使用的代码位置：**alist-web\src\components\SwitchColorMode.tsx**

点击查看示例代码

### [**不会加,可以参考这里的完整代码**](https://anwen-anyi.github.io/index/03-code.html#%E4%B8%8D%E4%BC%9A%E5%8A%A0-%E5%8F%AF%E4%BB%A5%E5%8F%82%E8%80%83%E8%BF%99%E9%87%8C%E7%9A%84%E5%AE%8C%E6%95%B4%E4%BB%A3%E7%A0%81)

点击查看完整代码示例

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-5)

![配图](https://anwen-anyi.github.io/img/code/6.png)

## [**7.将登录页面的 "登录到" 隐藏，后期适配自己的使用**](https://anwen-anyi.github.io/index/03-code.html#_7-%E5%B0%86%E7%99%BB%E5%BD%95%E9%A1%B5%E9%9D%A2%E7%9A%84-%E7%99%BB%E5%BD%95%E5%88%B0-%E9%9A%90%E8%97%8F-%E5%90%8E%E6%9C%9F%E9%80%82%E9%85%8D%E8%87%AA%E5%B7%B1%E7%9A%84%E4%BD%BF%E7%94%A8)

源码文件位置：**alist-web\src\pages\login\index.tsx**

```
  const title = createMemo(() => {
    // 33行左右取消后台显示的 登录到 字样
    // ${t("login.login_to")} 汉化包里面的登录到字样 "login_to": "登录到",
    // ${getSetting("site_title")} 网站标题
    // return `${t("login.login_to")}`
    // return `${t("login.login_to")} ${getSetting("site_title")}`
    return `${getSetting("site_title")}`
  })
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-6)

![配图](https://anwen-anyi.github.io/img/code/7.png)

## [**8.ipa界面添加下载和复制链接按钮,同时添加巨魔安装按钮**](https://anwen-anyi.github.io/index/03-code.html#_8-ipa%E7%95%8C%E9%9D%A2%E6%B7%BB%E5%8A%A0%E4%B8%8B%E8%BD%BD%E5%92%8C%E5%A4%8D%E5%88%B6%E9%93%BE%E6%8E%A5%E6%8C%89%E9%92%AE-%E5%90%8C%E6%97%B6%E6%B7%BB%E5%8A%A0%E5%B7%A8%E9%AD%94%E5%AE%89%E8%A3%85%E6%8C%89%E9%92%AE)

源码文件位置：**alist-web\src\pages\home\previews\ipa.tsx**

两个按钮来自 **alist-web\src\pages\home\previews\download.tsx**

巨魔安装相关的已经合并，大于 v3.13.1 以上的版本会实装(不包含 v3.13.1

点击查看示例代码

#### [**目前仅支持 .ipa文件 若想支持 .tipa文件需要添加**](https://anwen-anyi.github.io/index/03-code.html#%E7%9B%AE%E5%89%8D%E4%BB%85%E6%94%AF%E6%8C%81-ipa%E6%96%87%E4%BB%B6-%E8%8B%A5%E6%83%B3%E6%94%AF%E6%8C%81-tipa%E6%96%87%E4%BB%B6%E9%9C%80%E8%A6%81%E6%B7%BB%E5%8A%A0)

源码路径：**alist-web\src\pages\home\previews\index.ts**

需要将 tipa文件也添加进去

```json
	{
    name: "Ipa",
    exts: ["ipa","tipa"],
    component: lazy(() => import("./ipa")),
  },
```

.tipa 文件添加图标样式

源码路径：**alist-web\src\utils\icon.ts**

添加一下后缀文件名在里面即可

```
  "dmg,ipa,plist,tipa": BsApple,
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-7)

![配图](https://anwen-anyi.github.io/img/code/8.png)

## [**9. 去掉底部内容（有原因的）**](https://anwen-anyi.github.io/index/03-code.html#_9-%E5%8E%BB%E6%8E%89%E5%BA%95%E9%83%A8%E5%86%85%E5%AE%B9-%E6%9C%89%E5%8E%9F%E5%9B%A0%E7%9A%84)

这里去掉还是有原因的，因为我们修改了后台地址和登录地址

但是呢不知道出于什么原因，我们修改了后台管理地址，但是输入 **URL/@manage** 还是能进入默认界面，虽然进入了默认界面，提示路径不对，也不知道账号密码，但是通过CSS自定义的内容全部失效了，底部的登录（管理）入口出现了，暴露了我们修改后的 登录（管理）地址

特此直接从根将这个能暴露我们后台登录地址的信息除掉

**但是要自己在底部自定义一个底部信息哦 保留一下版权信息**

源码文件位置：**alist-web\src\pages\home\Footer.tsx**

```json
	{/*
      <HStack spacing="$1">
        <Anchor href="https://github.com/Xhofe/alist" external>
          {t("home.footer.powered_by")}
        </Anchor>
        <span>|</span>
        <AnchorWithBase
          as={Link}
          href={UserMethods.is_guest(user()) ? "/@login" : "/@manage"}
        >
          {t(
            UserMethods.is_guest(user()) ? "login.login" : "home.footer.manage"
          )}
        </AnchorWithBase>
      </HStack>
	*/}
```

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-8)

![配图](https://anwen-anyi.github.io/img/code/9.png)

## [**10. 添加一个infuse播放器(3.9.2版本移植到官方内了)**](https://anwen-anyi.github.io/index/03-code.html#_10-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AAinfuse%E6%92%AD%E6%94%BE%E5%99%A8-3-9-2%E7%89%88%E6%9C%AC%E7%A7%BB%E6%A4%8D%E5%88%B0%E5%AE%98%E6%96%B9%E5%86%85%E4%BA%86)

在底部添加一个新的播放器，“infuse”IOS上面用的人挺多的 支持的格式好像也挺多.

infuse官网：[**Firecore - Video Player for iOS, Apple TV, and Macopen in new window**](https://firecore.com/)

(新)源码文件位置：**alist-web/src/pages/home/previews/**[**video\_box.tsxopen in new window**](https://github.com/alist-org/alist-web/blob/main/src/pages/home/previews/video_box.tsx#L17-L21)

(旧)源码文件位置：**alist-web\src\pages\home\previews\video.tsx**

```
const players: { icon: string; name: string; scheme: string }[] = [
  { icon: "iina", name: "IINA", scheme: "iina://weblink?url=$durl" },
  { icon: "potplayer", name: "PotPlayer", scheme: "potplayer://$durl" },
    {
    icon: "infuse",
    name: "Infuse",
    scheme: "infuse://x-callback-url/play?url=$durl",
  },
  { icon: "vlc", name: "VLC", scheme: "vlc://$durl" },
  { icon: "nplayer", name: "nPlayer", scheme: "nplayer-$durl" },
  {
    icon: "mxplayer",
    name: "MX Player",
    scheme:
      "intent:$durl#Intent;package=com.mxtech.videoplayer.ad;S.title=$name;end",
  },
  {
    icon: "mxplayer-pro",
    name: "MX Player Pro",
    scheme:
      "intent:$durl#Intent;package=com.mxtech.videoplayer.pro;S.title=$name;end",
  },
]
```

加好后我们给他一个图标，图标的文件夹位置是：**alist-web\public\images**

可以下载右侧的这个图片或者自己弄一个，格式是 **.webp** 格式的哦~ [**点击蓝色这里查看图片保存open in new window**](https://down.onmicrosoft.cn/oss/u20221115822a1936_1669345226327_12955142_file.webp)

保存下来后记得命名成 **infuse.webp**

**如何自己做一个webp格式的图片，我用的PS做的，然后加一个插件:** [**https://blog.csdn.net/kangweijian/article/details/125197799open**](https://blog.csdn.net/kangweijian/article/details/125197799open) [**in new window**](https://blog.csdn.net/kangweijian/article/details/125197799)

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-9)

![配图](https://anwen-anyi.github.io/img/code/10.png)

## [**11. 修改一下搜索，变的更加匹配 ✅**](https://anwen-anyi.github.io/index/03-code.html#_11-%E4%BF%AE%E6%94%B9%E4%B8%80%E4%B8%8B%E6%90%9C%E7%B4%A2-%E5%8F%98%E7%9A%84%E6%9B%B4%E5%8A%A0%E5%8C%B9%E9%85%8D-%E2%9C%85)

- **开启搜索框需要先在**`AList`将索引打开启用才可以显示搜索框,否则看不到，[**点击查看如何使用open in new window**](https://alist.nn.ci/zh/guide/advanced/search.html#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)

搜索有两个版本一个是最新的一个是v3.6.0及之前的

使用的图标库地址：[**https://solid-icons.vercel.app/search/searchopen**](https://solid-icons.vercel.app/search/searchopen) [**in new window**](https://solid-icons.vercel.app/search/search)

此版本用于最新版搜索源码修改

仅限于V3.6.0版本搜索

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-10)

![配图](https://anwen-anyi.github.io/img/code/11.png)

![配图](https://anwen-anyi.github.io/img/code/11-2.gif)

## [**12.修改文件图标**](https://anwen-anyi.github.io/index/03-code.html#_12-%E4%BF%AE%E6%94%B9%E6%96%87%E4%BB%B6%E5%9B%BE%E6%A0%87)

源码文件位置：**alist-web\src\utils\icon.ts**

图标库：[**https://solid-icons.vercel.app/open**](https://solid-icons.vercel.app/open) [**in new window**](https://solid-icons.vercel.app/)

点击查看示例代码

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-11)

![配图](https://anwen-anyi.github.io/img/code/12.png)

## [**13.给后台登录的按钮添加颜色（可使用主颜色）**](https://anwen-anyi.github.io/index/03-code.html#_13-%E7%BB%99%E5%90%8E%E5%8F%B0%E7%99%BB%E5%BD%95%E7%9A%84%E6%8C%89%E9%92%AE%E6%B7%BB%E5%8A%A0%E9%A2%9C%E8%89%B2-%E5%8F%AF%E4%BD%BF%E7%94%A8%E4%B8%BB%E9%A2%9C%E8%89%B2)

**源码文件位置1-左侧语言选项按钮**：**alist-web\src\components\SwitchLanguage.tsx**

- 按钮位置分布：前端本地设置，登录页面，AList后台左侧边栏

**源码文件位置2-中间切换夜间/白色按钮**：**alist-web\src\components\SwitchColorMode.tsx**

- 按钮位置分布：前端本地设置，登录页面，AList后台左侧边栏

**源码文件位置3-右侧单点登录按钮**：**alist-web\src\pages\login\SSOLogin.tsx**

- 按钮位置分布：登录页面

**源码文件位置4-右侧WebAuthn登录按钮**：**alist-web\src\pages\login\index.tsx**

- 按钮位置分布：登录页面

- 使用主颜色：指的是在AList后台设置的颜色，路径 -->`AList后台` --> 设置 --> 样式 --> `主颜色`
- 用固定颜色：指的是直接在源码中写死

| 方法\优缺点 | 优点 | 缺点 |
| --- | --- | --- |
| 固定 | 可以设置不同颜色 | 更换只能重新编译 |
| 主颜色 | 可以随时换颜色 | 和前端显示的图标颜色统一可能不适合登录页面背景 |

---

#### [**使用主颜色**](https://anwen-anyi.github.io/index/03-code.html#%E4%BD%BF%E7%94%A8%E4%B8%BB%E9%A2%9C%E8%89%B2)

**语言选项模式切换单点登录WebAuthn**

```
import { getMainColor } from "~/store"

......
......

export const SwitchLanguageWhite = () => (
  <SwitchLanguage as={IoLanguageOutline} color={getMainColor()} boxSize="$8" />
)
```

#### [**用固定颜色**](https://anwen-anyi.github.io/index/03-code.html#%E7%94%A8%E5%9B%BA%E5%AE%9A%E9%A2%9C%E8%89%B2)

**语言选项模式切换单点登录WebAuthn**

```
export const SwitchLanguageWhite = () => (
  <SwitchLanguage as={IoLanguageOutline} color={"$accent10"} boxSize="$8" />
)
```

**修改后的对比预览图：**

翻译忘记截图了，我这里预览图不显示翻译是因为我之前已经删掉了，

**使用主颜色用固定颜色**

![配图](https://anwen-anyi.github.io/img/code/13-huodong.png)

虽然只改了这几个，不过像后台左侧边栏和前端设置里面的应该是同理方法

## [**14.修改默认为某"视图"方式**](https://anwen-anyi.github.io/index/03-code.html#_14-%E4%BF%AE%E6%94%B9%E9%BB%98%E8%AE%A4%E4%B8%BA%E6%9F%90-%E8%A7%86%E5%9B%BE-%E6%96%B9%E5%BC%8F)

首页默认视图为 "列表 list" 格式，有的小伙伴想着默认为 "网格格式" 怎么办呢? 改源码呗....

源码文件位置：**alist-web\src\store\obj.ts**

```
export type LayoutType = "list" | "grid" | "image"
const [layout, setLayout] = createStorageSignal<LayoutType>("layout", "list")
```

大概在177行左右，可能有变化会浮动代码行数，代码是不会变的

默认这里是 **"list"** ，如果你要默认为 "网格视图" 自己改成 **"grid"** 即可，"image" 是图片视图估计没人默认用

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-12)

就像这样的上面是网格视图 下面的是列表视图，默认是列表视图的哦~如果你要改图标可以看[**图标如何修改**](https://anwen-anyi.github.io/index/03-code.html#_12-%E4%BF%AE%E6%94%B9%E6%96%87%E4%BB%B6%E5%9B%BE%E6%A0%87)

![配图](https://anwen-anyi.github.io/img/code/14.png)

## [**15.修改PWA内容**](https://anwen-anyi.github.io/index/03-code.html#_15-%E4%BF%AE%E6%94%B9pwa%E5%86%85%E5%AE%B9)

现在支持将网页通过`PWA`添加到桌面了,但是添加的图标不是很好看的样子,

具体如预览中最后的那个图标,没处理好背景颜色黑乎乎的~我们自己修改一下

源码1修改的好像是IOS的，源码2是修改的安卓的~

源码文件位置1：**alist-web\index.html**

把原本的第三行(高亮显示的)改成自己的链接，或者使用和我同款的

```
    <link
      rel="apple-touch-icon"
      href="https://jsd.nn.ci/gh/alist-org/logo@main/logo.png"
    />
```

> 和我同款图标链接：[**https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpegopen**](https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpegopen) [**in new window**](https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpeg)

源码文件位置2：**alist-web\public\static\manifest.json**

老规矩，一样是修改第八行(高亮位置)改成自己的链接，或者使用和我同款的

```json
{
  "display": "standalone",
  "scope": "/",
  "start_url": "/",
  "name": "AList",
  "icons": [
    {
      "src": "https://jsd.nn.ci/gh/alist-org/logo@main/logo.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

> 和我同款图标链接：[**https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpegopen**](https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpegopen) [**in new window**](https://pic.rmb.bdstatic.com/bjh/aff9c9c8817d943d6857a73188958d45.jpeg)

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-13)

上面的是IOS，下面的是安卓

下图第三个是修改 `后` 的图标，第四个是修改 `前` 的图标

![配图](https://anwen-anyi.github.io/img/code/15-1.png)

下图第一个是修改 `后` 的图标，第二个是修改 `前` 的图标，安卓的倒是没黑乎乎

![配图](https://anwen-anyi.github.io/img/code/15-2.jpg)

## [**$ 修改后台地址和登录地址**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E5%8F%B0%E5%9C%B0%E5%9D%80%E5%92%8C%E7%99%BB%E5%BD%95%E5%9C%B0%E5%9D%80)

就没代码了，自己批量替换即可~

**@login** 是登录地址，**@manage** 是后台地址

#### [**修改后的对比预览图：**](https://anwen-anyi.github.io/index/03-code.html#%E4%BF%AE%E6%94%B9%E5%90%8E%E7%9A%84%E5%AF%B9%E6%AF%94%E9%A2%84%E8%A7%88%E5%9B%BE-14)

![配图](https://anwen-anyi.github.io/img/code/x.png)![配图](https://anwen-anyi.github.io/img/code/xx.png)

[**在 GitHub 上编辑此页open in new window**](https://github.com/anwen-anyi/anwen-anyi.github.io/edit/main/src/index/03-code.md)

**上次编辑于:** 2024/4/9 20:16:07

**贡献者:** AnWen-anyi

[**上一页**](https://anwen-anyi.github.io/index/02-addcloud.html)

[AList添加存储教程](https://anwen-anyi.github.io/index/02-addcloud.html)

[**下一页**](https://anwen-anyi.github.io/index/05-head.html)

[**美化自定义头部**](https://anwen-anyi.github.io/index/05-head.html)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
