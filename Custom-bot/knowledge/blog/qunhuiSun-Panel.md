# 群晖7.2 导航页Sun-Panel部署

> 标题：群晖7.2 导航页Sun-Panel部署
> 分类：面板与工具
> 标签：群晖
> 原文：https://www.xinz.fun/archives/qunhuiSun-Panel

> **导读**：这篇是「群晖7.2 导航页Sun-Panel部署」的实操教程。下文按「Sun-Panel简介」「**特点**[****](https://doc.sun-panel.top/zh_cn/introduce/project.html#%E7%89%B9%E7%82%B9)」「拉取镜像」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. Sun-Panel简介
2. **特点**[****](https://doc.sun-panel.top/zh_cn/introduce/project.html#%E7%89%B9%E7%82%B9)
3. 拉取镜像
4. docker部署
5. 基本使用教程
6. 侧边栏导航JS部署
7. 侧边导航栏JS代码

## Sun-Panel简介

**简单、易用、美观**

**一个NAS、服务器导航面板、简易docker管理器、Homepage、浏览器首页**

## **特点**[****](https://doc.sun-panel.top/zh_cn/introduce/project.html#%E7%89%B9%E7%82%B9)

- 🍉 界面简洁，功能强大，资源占用少
- 🍊 上手简单，可视化操作，可0代码使用
- 🍠 一键切换内、外网模式链接
- 🍵 支持docker部署（支持Arm系统）
- 🎪 支持多账号隔离使用
- 🎏 支持查看系统状态
- 🫙 支持自定义js、css
- 🍻 简单使用可以无需连接外部数据库
- 🍾 丰富图标风格自由搭配，支持[**iconify图标库**](https://icon-sets.iconify.design/)
- 🚁 支持网页内置小窗口打开（部分三方网站屏蔽此功能）
- 🐳 简单的docker管理器，支持查看容器状态、控制容器的开启和关闭

**Sun-Panel是一个优秀的导航页，尝试了各种导航页部署后，最终选用了Sun-Panel，集易上手、方便快捷、作者大大**[**@红烧猎人**](https://doc.sun-panel.top/zh_cn/)**更新神速，需求更新的快快的，最近又更新了docker和侧边栏这些非常实用的功能，不过在群晖环境下，直接使用官方套件版的话，docker的管理功能不好实现，本次直接使用docker的方式部署。**

## 拉取镜像

首先连接群晖SSH，这里使用Xshell，输入sudo -i，接着输入密码进入root模式（输密码不显示字符，直接回车就好）：

```bash
sudo -i
```

```bash
username@Coco:/$ sudo -i
Password: 
root@XXX:~#
```

显示上面的代码就可以了，接着拉取镜像（#2024年8月22日最新测试版）:

```bash
docker pull hslr/sun-panel:1.5.2-beta24-08-22
```

现在镜像不太好拉，我等不及了，用香港服务器pull下来放网盘了，有需要的可以点这里[sun-panel:1.5.2-beta24-08-22](https://cocohe.lanzouv.com/ickMm286busb)，密码d20b。

下载好的镜像上传至群晖即可

*~~命令可以pull下拉的话跳过这一部分即可~~*

## docker部署
### 路径创建

镜像下载好后，别急着部署，使用官方命令会报目录不存在，所以我们先去群晖文件管理器中找到`docker`文件夹，新建一个`sunpanel`文件夹，接着在`sunpanel`文件夹中新建一个`conf`文件夹，

### 一键部署

使用SSH 命令一键部署即可，记得需要root权限

`#注意这里与官方命令不一样的是前面的本机路径，请根据自己的实际情况选择docker文件夹所在的volume #docker管理功能实现需要挂载docker守护进程 #镜像与上面pull的版本保持一致`

```bash
docker run -d --restart=always -p 3002:3002 \
-v /volume1/docker/sunpanel/conf:/app/conf \
-v /var/run/docker.sock:/var/run/docker.sock \
--name sun-panel \
hslr/sun-panel:1.5.2-beta24-08-22
```

`#附上群友提供的群晖挂载路径可供参考选择：`

```
-v /volume1/docker/sun-panel/conf:/app/conf 
-v /volume1/docker/sun-panel/conf/database:/app/database 
-v /volume1/docker/sun-panel/conf/uploads:/app/uploads 
-v /volume1/docker/sun-panel/conf/custom:/app/custom
-v /volume1/docker/sun-panel/web:/app/web 
-v /var/run/docker.sock:/var/run/docker.sock
```

显示如下界面表示已经部署成功了，访问`127.0.0.2:3002`(127.0.0.2替换为群晖的ip地址)即可享用Sun-Panel了。

```bash
root@XXX:~# docker run -d --restart=always -p 3002:3002 \
> -v /volume1/docker/sunpanel/conf:/app/conf \
> -v /var/run/docker.sock:/var/run/docker.sock \
> --name sun-panel \
> hslr/sun-panel:1.5.2-beta24-08-22
641570e4558559ef705307d58c6c949b54bba29a47a03503040cbb2c7334157d
root@XXX:~#
```

## 基本使用教程
### **默认账号密码**[****](https://doc.sun-panel.top/zh_cn/usage/quick_deploy.html#%E9%BB%98%E8%AE%A4%E8%B4%A6%E5%8F%B7%E5%AF%86%E7%A0%81)

账号：[**admin@sun.cc**](mailto:admin@sun.cc)

密码：**12345678**

![配图](/upload/QQ_1726986588276.png)

登录后可以看到docker已经挂载成功了，说明安装很完美！

具体更多的功能相信大家点点鼠标就明白了哈哈。

## 侧边栏导航JS部署

这是上个版本大佬新推出的功能，对于站点内容巨多的我来说太需要这个功能了，快速定位各个菜单，而且还适配了手机端，其实挂载这个很简单，不过需要支持一下大佬，毕竟为爱发电不是长久之计，现在优惠100年（终身）会员88币，需要PRO功能的同学可以支持一下。[@支持PRO版](https://pro.sun-panel.top/)

侧边栏导航JS部署其实很简单，大佬提供了完整的JS代码（后附），粘贴到设置栏的JS对应位置即可。

![配图](/upload/QQ_1726986632339.png)

安装好的效果，有环保行业的同学也可以看看我的[Sunpanel导航页](http://ray.cocoheo.cn:3002/)效果：

![配图](/upload/QQ_1726986436948.png)![配图](/upload/QQ_1726986456856.png)

## 侧边导航栏JS代码

```
(function () {
  // =========== Config Start ===========
  // ------------------------------------
  // 距离滚动偏移量
  const scrollOffset = 80

  // 显示风格( auto:自动(默认) | mobile:左上角显示触发按钮-移动端风格 | sidebar:常态显示侧栏)
  const displayStyle = 'auto'

  // 移动端宽度定义
  const mobileWidth = 800

  const SunPanelTOCDomIdName = 'sun-panel-toc-dom'

  // 左上角按钮 SVG 图标
  const svgTocMobileBtn = '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 24 24"><path fill="currentColor" d="M17.5 4.5c-1.95 0-4.05.4-5.5 1.5c-1.45-1.1-3.55-1.5-5.5-1.5c-1.45 0-2.99.22-4.28.79C1.49 5.62 1 6.33 1 7.14v11.28c0 1.3 1.22 2.26 2.48 1.94c.98-.25 2.02-.36 3.02-.36c1.56 0 3.22.26 4.56.92c.6.3 1.28.3 1.87 0c1.34-.67 3-.92 4.56-.92c1 0 2.04.11 3.02.36c1.26.33 2.48-.63 2.48-1.94V7.14c0-.81-.49-1.52-1.22-1.85c-1.28-.57-2.82-.79-4.27-.79M21 17.23c0 .63-.58 1.09-1.2.98c-.75-.14-1.53-.2-2.3-.2c-1.7 0-4.15.65-5.5 1.5V8c1.35-.85 3.8-1.5 5.5-1.5c.92 0 1.83.09 2.7.28c.46.1.8.51.8.98z"/><path fill="currentColor" d="M13.98 11.01c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.54-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.71-.83.66c-1.62-.19-3.39-.04-4.73.39c-.08.01-.16.03-.23.03m0 2.66c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.53-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.71-.83.66c-1.62-.19-3.39-.04-4.73.39a1 1 0 0 1-.23.03m0 2.66c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.53-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.7-.83.66c-1.62-.19-3.39-.04-4.73.39a1 1 0 0 1-.23.03"/></svg>'

  // ------------------------------------
  // =========== Config End ===========

  // 滚动容器的类名
  const scrollContainerElementClassName = '.scroll-container'

  // 一些函数
  const isMobile = () => {
    if (displayStyle === 'mobile') {
      return true
    }
    else if (displayStyle === 'pc') {
      return false
    }
    const width = window.innerWidth
    return width < mobileWidth
  }

  function createDom() {
    // 检测是否已经存在TOC DOM，存在则删除
    (function () {
      const element = document.getElementById(SunPanelTOCDomIdName)
      if (element) {
        element.remove()
      }
    })()

    const SunPanelTOCDom = document.createElement('div')
    SunPanelTOCDom.id = SunPanelTOCDomIdName
    document.body.appendChild(SunPanelTOCDom)

    // ========= Add style start =========
    const style = document.createElement('style')
    const SunPanelTOCDomStyleId = `#${SunPanelTOCDomIdName}`
    style.textContent = `
    ${SunPanelTOCDomStyleId} #toc-mobile-btn {
        top: 20px !important;
        left: 20px !important;
        position: fixed;
        width: 46px;
        height: 46px;
        background-color: #2a2a2a6b;
        color: white;
        border-radius: 0.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }

    ${SunPanelTOCDomStyleId} .hidden {
        display: none !important;
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar {
        width: 40px;
        padding: 10px;
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: width 0.3s ease, background-color 0.3s ease;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
        background-color: none;
    }

    ${SunPanelTOCDomStyleId} .toc-mobile-btn-svg-container{
      width:21px;
      height:21px;
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion {
        width: 200px !important;
        display: flex;
        background-color: rgb(42 42 42 / 90%);
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar .toc-sidebar-box {
        width: 500px;
    }

    ${SunPanelTOCDomStyleId} .title-bar-box {
        display: flex;
        align-items: center;
        position: relative;
        cursor: pointer;
    }

    ${SunPanelTOCDomStyleId} .title-bar-slip {
        width: 20px;
        height: 6px;
        background-color: white;
        border-radius: 4px;
        margin: 15px 0;
        transition: height 0.3s ease, width 0.3s ease;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
    }

    ${SunPanelTOCDomStyleId} .title-bar-title {
        opacity: 0;
        white-space: nowrap;
        transition: opacity 0.3s ease, transform 0.3s ease, margin-left 0.3s ease;
        font-size: 14px;
        color: white;
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-title {
        opacity: 1;
        margin-left: 10px;
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-slip {
        box-shadow: none;
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-slip {
        width: 40px;
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-title {
        font-size: 20px;
    }

      `
    // 添加样式到文档头部
    SunPanelTOCDom.appendChild(style)

    // ========= Add style end =========

    // 添加移动端菜单按钮
    const tocMobileBtn = document.createElement('div')
    tocMobileBtn.id = 'toc-mobile-btn'
    tocMobileBtn.classList.add('backdrop-blur-[2px]')
    SunPanelTOCDom.appendChild(tocMobileBtn)

    const tocMobileBtnSvgcContainer = document.createElement('div')
    tocMobileBtnSvgcContainer.innerHTML = svgTocMobileBtn
    tocMobileBtnSvgcContainer.classList.add('toc-mobile-btn-svg-container')
    tocMobileBtn.appendChild(tocMobileBtnSvgcContainer)

    // 创建侧边栏容器
    const sidebar = document.createElement('div')
    sidebar.id = 'toc-sidebar'

    const sidebarBox = document.createElement('div')
    sidebarBox.className = 'toc-sidebar-box'

    // 查询出所有类名包含 item-group-index- 的元素
    const items = document.querySelectorAll('[class*="item-group-index-"]')

    // 遍历并打印每个元素的完整类名
    items.forEach((item) => {
      item.classList.forEach((className) => {
        if (className.startsWith('item-group-index-')) {
          const titleBarBox = document.createElement('div')
          titleBarBox.className = 'title-bar-box'
          // titleBarBox.href = `#${item.id}`
          titleBarBox.dataset.groupClassName = className

          // 目录条
          const titleBarSlip = document.createElement('div')
          titleBarSlip.className = 'title-bar-slip'

          // 创建一个链接
          const titleBarTitle = document.createElement('div')
          titleBarTitle.className = 'title-bar-title'

          // 获取子元素中 class="group-title" 的内容
          const titleElement = item.querySelector('.group-title')
          const titleText = titleElement ? titleElement.textContent : item.id
          titleBarTitle.textContent = titleText

          titleBarBox.appendChild(titleBarSlip)
          titleBarBox.appendChild(titleBarTitle)

          sidebarBox.appendChild(titleBarBox)
        }
      })
    })

    sidebar.appendChild(sidebarBox)

    // 将侧边栏添加到页面中
    SunPanelTOCDom.appendChild(sidebar)

    function mobileHideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion')
      sidebar.classList.add('hidden')
    }

    function hideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion')
    }

    function showSidebar() {
      sidebar.classList.add('toc-sidebar-expansion')
      sidebar.classList.remove('hidden')
    }

    // ----------------
    // 监听宽度变化开始
    // ----------------
    function debounce(func, wait) {
      let timeout
      return function (...args) {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
          func.apply(this, args)
        }, wait)
      }
    }

    function handleResize() {
      if (isMobile()) {
        tocMobileBtn.classList.remove('hidden')
        sidebar.classList.add('hidden')
      }
      else {
        tocMobileBtn.classList.add('hidden')
        sidebar.classList.remove('hidden')
      }
    }

    // 使用防抖函数包装你的处理函数
    const debouncedHandleResize = debounce(handleResize, 200)

    // 添加事件监听器
    window.addEventListener('resize', debouncedHandleResize)

    // 首次触发
    handleResize()

    // ----------------
    // 监听宽度变化结束
    // ----------------

    // 监听移动端按钮点击
    tocMobileBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('toc-sidebar-expansion')) {
        // 隐藏
        mobileHideSidebar()
      }
      else {
        // 显示
        showSidebar()
      }
    })

    // 监听TOC栏失去hover
    sidebar.addEventListener('mouseleave', () => {
      if (isMobile()) {
        // 隐藏
        mobileHideSidebar()
      }
      else {
        hideSidebar()
      }
    })

    // 监听TOC栏获得hover
    sidebar.addEventListener('mouseenter', () => {
      showSidebar()
    })

    // 监听TOC点击事件
    document.querySelectorAll('.title-bar-box').forEach((box) => {
      box.addEventListener('click', function (event) {
      // 检查触发事件的元素是否有 'data-groupClassName' 属性
        if (this.dataset.groupClassName) {
        // 获取 'data-groupClass' 属性的值
          const groupClassName = this.dataset.groupClassName
          // 使用属性值作为选择器查询对应的元素
          const targetElement = document.querySelector(`.${groupClassName}`)
          if (targetElement) {
          // 获取目标元素的 'top' 坐标
            const targetTop = targetElement.offsetTop
            const scrollContainerElement = document.querySelector(scrollContainerElementClassName)
            if (scrollContainerElement) {
              scrollContainerElement.scrollTo({
                top: targetTop - scrollOffset,
                behavior: 'smooth', // 平滑滚动
              })
            }
          }
        }
      })
    })
  }

  // 判断是否已经存在分组，不存在将定时监听
  const items = document.querySelectorAll('[class*="item-group-index-"]')
  if (items.length > 0) {
    createDom()
    return
  }

  const interval = setInterval(() => {
    const items = document.querySelectorAll('[class*="item-group-index-"]')
    if (items.length > 0) {
      createDom()
      clearInterval(interval)
    }
  }, 1000)
})()
```

### css注释

这段代码是一个 JavaScript 自执行函数，用于在网页上创建一个目录（Table of Contents, TOC）面板，允许用户通过点击目录项平滑滚动到相应的页面部分。下面是对代码的详细解释，并增加了每段的注释。

```
(function () {
  // =========== Config Start ===========
  // ------------------------------------
  // 距离滚动偏移量
  const scrollOffset = 80; // 滚动时页面顶部的偏移量

  // 显示风格( auto:自动(默认) | mobile:左上角显示触发按钮-移动端风格 | sidebar:常态显示侧栏)
  const displayStyle = 'auto'; // 控制目录的显示方式

  // 移动端宽度定义
  const mobileWidth = 800; // 定义移动设备的宽度阈值

  const SunPanelTOCDomIdName = 'sun-panel-toc-dom'; // TOC DOM 元素的 ID

  // 左上角按钮 SVG 图标
  const svgTocMobileBtn = '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 24 24"><path fill="currentColor" d="..."/></svg>'; // SVG 图标的定义

  // ------------------------------------
  // =========== Config End ===========

  // 滚动容器的类名
  const scrollContainerElementClassName = '.scroll-container'; // 滚动容器的选择器

  // 一些函数
  const isMobile = () => {
    // 判断当前设备是否为移动设备
    if (displayStyle === 'mobile') {
      return true; // 如果显示风格为移动，则返回 true
    } else if (displayStyle === 'pc') {
      return false; // 如果显示风格为 PC，则返回 false
    }
    const width = window.innerWidth; // 获取当前窗口的宽度
    return width < mobileWidth; // 如果宽度小于定义的移动宽度，则返回 true
  };

  function createDom() {
    // 创建 TOC DOM 元素
    (function () {
      const element = document.getElementById(SunPanelTOCDomIdName);
      if (element) {
        element.remove(); // 如果 TOC 元素已经存在，则删除它
      }
    })();

    const SunPanelTOCDom = document.createElement('div'); // 创建 TOC 容器
    SunPanelTOCDom.id = SunPanelTOCDomIdName; // 设置 ID
    document.body.appendChild(SunPanelTOCDom); // 将 TOC 容器添加到文档中

    // ========= Add style start =========
    const style = document.createElement('style'); // 创建样式元素
    const SunPanelTOCDomStyleId = `#${SunPanelTOCDomIdName}`; // TOC 容器的样式 ID
    style.textContent = `
    ${SunPanelTOCDomStyleId} #toc-mobile-btn {
        top: 20px !important; // 移动端按钮的顶部位置
        left: 20px !important; // 移动端按钮的左侧位置
        position: fixed; // 固定定位
        width: 46px; // 按钮宽度
        height: 46px; // 按钮高度
        background-color: #2a2a2a6b; // 按钮背景颜色
        color: white; // 按钮文字颜色
        border-radius: 0.5rem; // 按钮圆角
        display: flex; // 使用 Flexbox 布局
        justify-content: center; // 居中对齐
        align-items: center; // 垂直居中
        cursor: pointer; // 鼠标悬停时显示为手型
    }

    ${SunPanelTOCDomStyleId} .hidden {
        display: none !important; // 隐藏类的样式
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar {
        width: 40px; // 侧边栏的初始宽度
        padding: 10px; // 内边距
        position: fixed; // 固定定位
        top: 0; // 顶部对齐
        left: 0; // 左侧对齐
        height: 100%; // 高度为 100%
        overflow: hidden; // 隐藏溢出内容
        display: flex; // 使用 Flexbox 布局
        flex-direction: column; // 垂直排列
        justify-content: center; // 垂直居中
        transition: width 0.3s ease, background-color 0.3s ease; // 动画过渡效果
        border-top-right-radius: 20px; // 右上角圆角
        border-bottom-right-radius: 20px; // 右下角圆角
        background-color: none; // 背景颜色
    }

    ${SunPanelTOCDomStyleId} .toc-mobile-btn-svg-container {
      width: 21px; // SVG 容器宽度
      height: 21px; // SVG 容器高度
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion {
        width: 200px !important; // 展开时侧边栏宽度
        display: flex; // 使用 Flexbox 布局
        background-color: rgb(42 42 42 / 90%); // 背景颜色
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2); // 阴影效果
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar .toc-sidebar-box {
        width: 500px; // 侧边栏内容宽度
    }

    ${SunPanelTOCDomStyleId} .title-bar-box {
        display: flex; // 使用 Flexbox 布局
        align-items: center; // 垂直居中
        position: relative; // 相对定位
        cursor: pointer; // 鼠标悬停时显示为手型
    }

    ${SunPanelTOCDomStyleId} .title-bar-slip {
        width: 20px; // 滑块宽度
        height: 6px; // 滑块高度
        background-color: white; // 滑块颜色
        border-radius: 4px; // 滑块圆角
        margin: 15px 0; // 上下外边距
        transition: height 0.3s ease, width 0.3s ease; // 动画过渡效果
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5); // 滑块阴影效果
    }

    ${SunPanelTOCDomStyleId} .title-bar-title {
        opacity: 0; // 初始透明度
        white-space: nowrap; // 不换行
        transition: opacity 0.3s ease, transform 0.3s ease, margin-left 0.3s ease; // 动画过渡效果
        font-size: 14px; // 字体大小
        color: white; // 字体颜色
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-title {
        opacity: 1; // 展开时透明度
        margin-left: 10px; // 左侧外边距
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-slip {
        box-shadow: none; // 展开时去掉阴影
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-slip {
        width: 40px; // 鼠标悬停时滑块宽度
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-title {
        font-size: 20px; // 鼠标悬停时标题字体大小
    }
    `;
    // 添加样式到文档头部
    SunPanelTOCDom.appendChild(style); // 将样式添加到 TOC DOM 中

    // ========= Add style end =========

    // 添加移动端菜单按钮
    const tocMobileBtn = document.createElement('div'); // 创建移动端按钮
    tocMobileBtn.id = 'toc-mobile-btn'; // 设置 ID
    tocMobileBtn.classList.add('backdrop-blur-[2px]'); // 添加样式类
    SunPanelTOCDom.appendChild(tocMobileBtn); // 将按钮添加到 TOC DOM 中

    const tocMobileBtnSvgcContainer = document.createElement('div'); // 创建 SVG 容器
    tocMobileBtnSvgcContainer.innerHTML = svgTocMobileBtn; // 将 SVG 图标添加到容器
    tocMobileBtnSvgcContainer.classList.add('toc-mobile-btn-svg-container'); // ��加样式类
    tocMobileBtn.appendChild(tocMobileBtnSvgcContainer); // 将 SVG 容器添加到按钮

    // 创建侧边栏容器
    const sidebar = document.createElement('div'); // 创建侧边栏
    sidebar.id = 'toc-sidebar'; // 设置 ID

    const sidebarBox = document.createElement('div'); // 创建侧边栏内容容器
    sidebarBox.className = 'toc-sidebar-box'; // 设置类名

    // 查询出所有类名包含 item-group-index- 的元素
    const items = document.querySelectorAll('[class*="item-group-index-"]'); // 获取所有相关的目录项

    // 遍历并打印每个元素的完整类名
    items.forEach((item) => {
      item.classList.forEach((className) => {
        if (className.startsWith('item-group-index-')) { // 只处理以 'item-group-index-' 开头的类名
          const titleBarBox = document.createElement('div'); // 创建标题条
          titleBarBox.className = 'title-bar-box'; // 设置类名
          // titleBarBox.href = `#${item.id}`; // 可以用来设置链接到对应项（如果需要）

          titleBarBox.dataset.groupClassName = className; // 将类名存储在 data 属性中

          // 目录条
          const titleBarSlip = document.createElement('div'); // 创建滑块
          titleBarSlip.className = 'title-bar-slip'; // 设置类名

          // 创建一个链接
          const titleBarTitle = document.createElement('div'); // 创建标题
          titleBarTitle.className = 'title-bar-title'; // 设置类名

          // 获取子元素中 class="group-title" 的内容
          const titleElement = item.querySelector('.group-title'); // 查询标题元素
          const titleText = titleElement ? titleElement.textContent : item.id; // 获取文本内容，若不存在则使用 ID
          titleBarTitle.textContent = titleText; // 设置标题文本

          titleBarBox.appendChild(titleBarSlip); // 将滑块添加到标题条
          titleBarBox.appendChild(titleBarTitle); // 将标题添加到标题条

          sidebarBox.appendChild(titleBarBox); // 将标题条添加到侧边栏内容
        }
      });
    });

    sidebar.appendChild(sidebarBox); // 将侧边栏内容添加到侧边栏

    // 将侧边栏添加到页面中
    SunPanelTOCDom.appendChild(sidebar); // 将侧边栏添加到 TOC DOM 中

    // 移动端隐藏侧边栏的函数
    function mobileHideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion'); // 移除展开类
      sidebar.classList.add('hidden'); // 添加隐藏类
    }

    // 隐藏侧边栏的函数
    function hideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion'); // 移除展开类
    }

    // 显示侧边栏的函数
    function showSidebar() {
      sidebar.classList.add('toc-sidebar-expansion'); // 添加展开类
      sidebar.classList.remove('hidden'); // 移除隐藏类
    }

    // ----------------
    // 监听宽度变化开始
    // ----------------
    function debounce(func, wait) {
      let timeout; // 定义定时器
      return function (...args) {
        clearTimeout(timeout); // 清除上一个定时器
        timeout = setTimeout(() => {
          func.apply(this, args); // 在指定时间后执行函数
        }, wait);
      };
    }

    function handleResize() {
      // 处理窗口大小变化
      if (isMobile()) {
        tocMobileBtn.classList.remove('hidden'); // 如果是移动设备，显示按钮
        sidebar.classList.add('hidden'); // 隐藏侧边栏
      } else {
        tocMobileBtn.classList.add('hidden'); // 如果是 PC，隐藏按钮
        sidebar.classList.remove('hidden'); // 显示侧边栏
      }
    }

    // 使用防抖函数包装你的处理函数
    const debouncedHandleResize = debounce(handleResize, 200); // 设置防抖处理函数

    // 添加事件监听器
    window.addEventListener('resize', debouncedHandleResize); // 监听窗口大小变化

    // 首次触发
    handleResize(); // 初始处理窗口大小

    // ----------------
    // 监听宽度变化结束
    // ----------------

    // 监听移动端按钮点击
    tocMobileBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('toc-sidebar-expansion')) {
        // 如果侧边栏已展开，则隐藏
        mobileHideSidebar();
      } else {
        // 否则显示
        showSidebar();
      }
    });

    // 监听TOC栏失去hover
    sidebar.addEventListener('mouseleave', () => {
      if (isMobile()) {
        // 隐藏
        mobileHideSidebar();
      } else {
        hideSidebar(); // 否则隐藏侧边栏
      }
    });

    // 监听TOC栏获得hover
    sidebar.addEventListener('mouseenter', () => {
      showSidebar(); // 显示侧边栏
    });

    // 监听TOC点击事件
    document.querySelectorAll('.title-bar-box').forEach((box) => {
      box.addEventListener('click', function (event) {
        // 检查触发事件的元素是否有 'data-groupClassName' 属性
        if (this.dataset.groupClassName) {
          // 获取 'data-groupClass' 属性的值
          const groupClassName = this.dataset.groupClassName;
          // 使用属性值作为选择器查询对应的元素
          const targetElement = document.querySelector(`.${groupClassName}`);
          if (targetElement) {
            // 获取目标元素的 'top' 坐标
            const targetTop = targetElement.offsetTop;
            const scrollContainerElement = document.querySelector(scrollContainerElementClassName);
            if (scrollContainerElement) {
              scrollContainerElement.scrollTo({
                top: targetTop - scrollOffset, // 滚动到目标位置，减去偏移量
                behavior: 'smooth', // 平滑滚动
              });
            }
          }
        }
      });
    });
  }

  // 判断是否已经存在分组，不存在将定时监听
  const items = document.querySelectorAll('[class*="item-group-index-"]'); // 查询所有目录项
  if (items.length > 0) {
    createDom(); // 如果存在，则创建 TOC
    return; // 退出函数
  }

  const interval = setInterval(() => {
    const items = document.querySelectorAll('[class*="item-group-index-"]'); // 每隔一秒检查一次
    if (items.length > 0) {
      createDom(); // 如果发现目录项，则创建 TOC
      clearInterval(interval); // 清除定时器
    }
  }, 1000); // 每隔 1000 毫秒检查一次
})();
```

### 总结

这段代码的主要功能是创建一个动态的目录面板，允许用户通过点击目录项平滑滚动到页面的相应部分。代码中使用了自执行函数、DOM 操作、事件监听和防抖等技术，确保在不同设备和窗口大小下都能正常工作。每段代码都添加了注释，帮助理解其功能和作用。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
