# Docker容器Sun-Panel部署

> 标题：Docker容器Sun-Panel部署
> 分类：面板与工具
> 标签：docker
> 原文：https://www.xinz.fun/archives/Sun-Panel

> **导读**：这篇是「Docker容器Sun-Panel部署」的实操教程。下文按「dockere命令」「拉取不下来尝试换源：」「自定义页脚需要填写」的顺序展开，命令、配置和路径均可直接参考，但请把域名、端口、密钥和目录替换成自己的值。
>
> 适合正在折腾面板与工具的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. dockere命令
2. 拉取不下来尝试换源：
3. 自定义页脚需要填写
4. 侧边栏js 设置完需等待加载 {时间暂不明确}

## dockere命令

docker pull hslr/sun-panel:latest

或者 docker pull hslr/sun-panel:beta

beta版本加版本号

```bash
docker run -d --restart=always -p 3002:3002 \
-v /opt/1panel/apps/sun-panel/conf:/app/conf \
-v /var/run/docker.sock:/var/run/docker.sock \
--name sun-panel \
hslr/sun-panel:1.5.2-beta24-08-23
```

稳定最新版本

```bash
docker run -d --restart=always -p 3002:3002 \
-v /opt/1panel/apps/sun-panel/conf:/app/conf \
-v /var/run/docker.sock:/var/run/docker.sock \
--name sun-panel \
hslr/sun-panel:latest
```

beta最新版本

```bash
docker run -d --restart=always -p 3002:3002 \
-v /opt/1panel/apps/sun-panel/conf:/app/conf \
-v /var/run/docker.sock:/var/run/docker.sock \
--name sun-panel \
hslr/sun-panel:beta
```

## 拉取不下来尝试换源：

```
https://appscross.com/blog/how-to-use-dockerhub-in-china-for-a-specific-period.html
```

## 自定义页脚需要填写

![配图](/upload/image-fcnd.png)

```
<script src="/custom/toc.js"></script>
```

## 侧边栏js 设置完需等待加载 {时间暂不明确}

![配图](/upload/QQ_1726986632339-ztuy.png)请打开折叠的代码或者直接点击复制按钮

### 默认版本

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

### 带播放器版本

播放器自己去注册然后添加

播放器注册地址: [点击前往](https://myhkw.cn)

```
(function () {
  // =========== Config Start ===========
  const scrollOffset = 80;
  const displayStyle = 'auto';
  const mobileWidth = 800;
  const SunPanelTOCDomIdName = 'sun-panel-toc-dom';
  const svgTocMobileBtn = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M17.5 4.5c-1.95 0-4.05.4-5.5 1.5c-1.45-1.1-3.55-1.5-5.5-1.5c-1.45 0-2.99.22-4.28.79C1.49 5.62 1 6.33 1 7.14v11.28c0 1.3 1.22 2.26 2.48 1.94c.98-.25 2.02-.36 3.02-.36c1.56 0 3.22.26 4.56.92c.6.3 1.28.3 1.87 0c1.34-.67 3-.92 4.56-.92c1 0 2.04.11 3.02.36c1.26.33 2.48-.63 2.48-1.94V7.14c0-.81-.49-1.52-1.22-1.85c-1.28-.57-2.82-.79-4.27-.79M21 17.23c0 .63-.58 1.09-1.2.98c-.75-.14-1.53-.2-2.3-.2c-1.7 0-4.15.65-5.5 1.5V8c1.35-.85 3.8-1.5 5.5-1.5c.92 0 1.83.09 2.7.28c.46.1.8.51.8.98z"/><path fill="currentColor" d="M13.98 11.01c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.54-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.71-.83.66c-1.62-.19-3.39-.04-4.73.39c-.08.01-.16.03-.23.03m0 2.66c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.53-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.71-.83.66c-1.62-.19-3.39-.04-4.73.39a1 1 0 0 1-.23.03m0 2.66c-.32 0-.61-.2-.71-.52c-.13-.39.09-.82.48-.94c1.53-.5 3.53-.66 5.36-.45c.41.05.71.42.66.83s-.42.7-.83.66c-1.62-.19-3.39-.04-4.73.39a1 1 0 0 1-.23.03"/></svg>';
  const scrollContainerElementClassName = '.scroll-container';

  const isMobile = () => {
    if (displayStyle === 'mobile') {
      return true;
    } else if (displayStyle === 'pc') {
      return false;
    }
    const width = window.innerWidth;
    return width < mobileWidth;
  }

  function createDom() {
    (function () {
      const element = document.getElementById(SunPanelTOCDomIdName);
      if (element) {
        element.remove();
      }
    })();

    const SunPanelTOCDom = document.createElement('div');
    SunPanelTOCDom.id = SunPanelTOCDomIdName;
    document.body.appendChild(SunPanelTOCDom);

    const style = document.createElement('style');
    const SunPanelTOCDomStyleId = `#${SunPanelTOCDomIdName}`;
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

    ${SunPanelTOCDomStyleId} .toc-mobile-btn-svg-container {
      width: 21px;
      height: 21px;
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
    `;
    SunPanelTOCDom.appendChild(style);

    const tocMobileBtn = document.createElement('div');
    tocMobileBtn.id = 'toc-mobile-btn';
    tocMobileBtn.classList.add('backdrop-blur-[2px]');
    SunPanelTOCDom.appendChild(tocMobileBtn);

    const tocMobileBtnSvgcContainer = document.createElement('div');
    tocMobileBtnSvgcContainer.innerHTML = svgTocMobileBtn;
    tocMobileBtnSvgcContainer.classList.add('toc-mobile-btn-svg-container');
    tocMobileBtn.appendChild(tocMobileBtnSvgcContainer);

    const sidebar = document.createElement('div');
    sidebar.id = 'toc-sidebar';

    const sidebarBox = document.createElement('div');
    sidebarBox.className = 'toc-sidebar-box';

    const items = document.querySelectorAll('[class*="item-group-index-"]');

    items.forEach((item) => {
      item.classList.forEach((className) => {
        if (className.startsWith('item-group-index-')) {
          const titleBarBox = document.createElement('div');
          titleBarBox.className = 'title-bar-box';
          titleBarBox.dataset.groupClassName = className;

          const titleBarSlip = document.createElement('div');
          titleBarSlip.className = 'title-bar-slip';

          const titleBarTitle = document.createElement('div');
          titleBarTitle.className = 'title-bar-title';

          const titleElement = item.querySelector('.group-title');
          const titleText = titleElement ? titleElement.textContent : item.id;
          titleBarTitle.textContent = titleText;

          titleBarBox.appendChild(titleBarSlip);
          titleBarBox.appendChild(titleBarTitle);

          sidebarBox.appendChild(titleBarBox);
        }
      });
    });

    sidebar.appendChild(sidebarBox);
    SunPanelTOCDom.appendChild(sidebar);

    function mobileHideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion');
      sidebar.classList.add('hidden');
    }

    function hideSidebar() {
      sidebar.classList.remove('toc-sidebar-expansion');
    }

    function showSidebar() {
      sidebar.classList.add('toc-sidebar-expansion');
      sidebar.classList.remove('hidden');
    }

    function debounce(func, wait) {
      let timeout;
      return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          func.apply(this, args);
        }, wait);
      };
    }

    function handleResize() {
      if (isMobile()) {
        tocMobileBtn.classList.remove('hidden');
        sidebar.classList.add('hidden');
      } else {
        tocMobileBtn.classList.add('hidden');
        sidebar.classList.remove('hidden');
      }
    }

    const debouncedHandleResize = debounce(handleResize, 200);
    window.addEventListener('resize', debouncedHandleResize);
    handleResize();

    tocMobileBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('toc-sidebar-expansion')) {
        mobileHideSidebar();
      } else {
        showSidebar();
      }
    });

    sidebar.addEventListener('mouseleave', () => {
      if (isMobile()) {
        mobileHideSidebar();
      } else {
        hideSidebar();
      }
    });

    sidebar.addEventListener('mouseenter', () => {
      showSidebar();
    });

    document.querySelectorAll('.title-bar-box').forEach((box) => {
      box.addEventListener('click', function (event) {
        if (this.dataset.groupClassName) {
          const groupClassName = this.dataset.groupClassName;
          const targetElement = document.querySelector(`.${groupClassName}`);
          if (targetElement) {
            const targetTop = targetElement.offsetTop;
            const scrollContainerElement = document.querySelector(scrollContainerElementClassName);
            if (scrollContainerElement) {
              scrollContainerElement.scrollTo({
                top: targetTop - scrollOffset,
                behavior: 'smooth',
              });
            }
          }
        }
      });
    });
  }

  const items = document.querySelectorAll('[class*="item-group-index-"]');
  if (items.length > 0) {
    createDom();
    return;
  }

  const interval = setInterval(() => {
    const items = document.querySelectorAll('[class*="item-group-index-"]');
    if (items.length > 0) {
      createDom();
      clearInterval(interval);
    }
  }, 1000);

  // Add external script with check to avoid duplicate loading
  if (!document.getElementById('11111111')) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.id = '11111111';
    script.src = 'https://myhkw.cn/api/player/11111111';
    script.setAttribute('key', '11111111');
    script.setAttribute('m', '11111111');
    document.body.appendChild(script);
  }
})();
```

自己更具图片内容修改代码

![配图](/upload/image-cfkc.png)

```
  // Add external script with check to avoid duplicate loading
  if (!document.getElementById('11111111')) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.id = '11111111';
    script.src = 'https://myhkw.cn/api/player/11111111';
    script.setAttribute('key', '11111111');
    script.setAttribute('m', '11111111');
    document.body.appendChild(script);
  }
})();
```

### css注释

这段代码是一个 JavaScript 自执行函数，用于在网页上创建一个目录（Table of Contents, TOC）面板，允许用户通过点击目录项平滑滚动到相应的页面部分。下面是对代码的详细解释，并增加了每段的注释。

```
(function () {
  // =========== 配置开始 ===========
  const scrollOffset = 80; // 滚动目标位置的偏移量
  const displayStyle = 'auto'; // 确定显示样式（移动端或PC端）
  const mobileWidth = 800; // 移动设备的宽度阈值
  const SunPanelTOCDomIdName = 'sun-panel-toc-dom'; // TOC（目录）容器的 ID
  const svgTocMobileBtn = '<svg ...>'; // 移动端按钮的 SVG 图标
  const scrollContainerElementClassName = '.scroll-container'; // 滚动容器的类名

  // 判断当前设备是否为移动设备
  const isMobile = () => {
    if (displayStyle === 'mobile') {
      return true; // 强制返回移动设备
    } else if (displayStyle === 'pc') {
      return false; // 强制返回PC设备
    }
    const width = window.innerWidth; // 获取窗口宽度
    return width < mobileWidth; // 判断是否小于移动设备宽度
  }

  // 创建目录 DOM 元素
  function createDom() {
    // 如果目录容器已经存在，则移除它
    (function () {
      const element = document.getElementById(SunPanelTOCDomIdName);
      if (element) {
        element.remove(); // 移除已有的目录容器
      }
    })();

    // 创建新的目录容器
    const SunPanelTOCDom = document.createElement('div');
    SunPanelTOCDom.id = SunPanelTOCDomIdName; // 设置 ID
    document.body.appendChild(SunPanelTOCDom); // 将目录容器添加到文档主体

    // 创建样式元素
    const style = document.createElement('style');
    const SunPanelTOCDomStyleId = `#${SunPanelTOCDomIdName}`; // 选择器前缀
    style.textContent = `
    ${SunPanelTOCDomStyleId} #toc-mobile-btn {
        top: 20px !important; // 设置移动按钮的顶部位置
        left: 20px !important; // 设置移动按钮的左侧位置
        position: fixed; // 固定定位
        width: 46px; // 按钮宽度
        height: 46px; // 按钮高度
        background-color: #2a2a2a6b; // 按钮背景色
        color: white; // 按钮文字颜色
        border-radius: 0.5rem; // 按钮圆角
        display: flex; // 使用 Flexbox 布局
        justify-content: center; // 居中对齐
        align-items: center; // 垂直居中
        cursor: pointer; // 鼠标悬停时显示手指光标
    }

    ${SunPanelTOCDomStyleId} .hidden {
        display: none !important; // 隐藏样式
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar {
        width: 40px; // 侧边栏初始宽度
        padding: 10px; // 内边距
        position: fixed; // 固定定位
        top: 0; // 顶部位置
        left: 0; // 左侧位置
        height: 100%; // 高度为 100%
        overflow: hidden; // 隐藏溢出内容
        display: flex; // 使用 Flexbox 布局
        flex-direction: column; // 垂直排列
        justify-content: center; // 垂直居中
        transition: width 0.3s ease, background-color 0.3s ease; // 动画效果
        border-top-right-radius: 20px; // 右上角圆角
        border-bottom-right-radius: 20px; // 右下角圆角
        background-color: none; // 背景色
    }

    ${SunPanelTOCDomStyleId} .toc-mobile-btn-svg-container {
      width: 21px; // 移动按钮 SVG 容器宽度
      height: 21px; // 移动按钮 SVG 容器高度
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion {
        width: 200px !important; // 展开侧边栏宽度
        display: flex; // 使用 Flexbox 布局
        background-color: rgb(42 42 42 / 90%); // 背景色
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2); // 阴影效果
    }

    ${SunPanelTOCDomStyleId} #toc-sidebar .toc-sidebar-box {
        width: 500px; // 侧边栏内容宽度
    }

    ${SunPanelTOCDomStyleId} .title-bar-box {
        display: flex; // 使用 Flexbox 布局
        align-items: center; // 垂直居中
        position: relative; // 相对定位
        cursor: pointer; // 鼠标悬停时显示手指光标
    }

    ${SunPanelTOCDomStyleId} .title-bar-slip {
        width: 20px; // 滑块宽度
        height: 6px; // 滑块高度
        background-color: white; // 滑块颜色
        border-radius: 4px; // 滑块圆角
        margin: 15px 0; // 滑块外边距
        transition: height 0.3s ease, width 0.3s ease; // 动画效果
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5); // 阴影效果
    }

    ${SunPanelTOCDomStyleId} .title-bar-title {
        opacity: 0; // 初始透明度
        white-space: nowrap; // 不换行
        transition: opacity 0.3s ease, transform 0.3s ease, margin-left 0.3s ease; // 动画效果
        font-size: 14px; // 字体大小
        color: white; // 字体颜色
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-title {
        opacity: 1; // 展开时设置为不透明
        margin-left: 10px; // 左边距
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-slip {
        box-shadow: none; // 展开时去掉阴影
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-slip {
        width: 40px; // 悬停时滑块宽度变化
    }

    ${SunPanelTOCDomStyleId} .toc-sidebar-expansion .title-bar-box:hover .title-bar-title {
        font-size: 20px; // 悬停时字体变大
    }
    `;
    SunPanelTOCDom.appendChild(style); // 将样式添加到目录容器

    // 创建移动端按钮
    const tocMobileBtn = document.createElement('div');
    tocMobileBtn.id = 'toc-mobile-btn';
    tocMobileBtn.classList.add('backdrop-blur-[2px]'); // 添加模糊背景效果
    SunPanelTOCDom.appendChild(tocMobileBtn); // 将按钮添加到目录容器

    // 创建按钮的 SVG 容器
    const tocMobileBtnSvgcContainer = document.createElement('div');
    tocMobileBtnSvgcContainer.innerHTML = svgTocMobileBtn; // 添加 SVG 图标
    tocMobileBtnSvgcContainer.classList.add('toc-mobile-btn-svg-container');
    tocMobileBtn.appendChild(tocMobileBtnSvgcContainer); // 将 SVG 容器添加到按钮

    // 创建侧边栏
    const sidebar = document.createElement('div');
    sidebar.id = 'toc-sidebar'; // 设置 ID

    const sidebarBox = document.createElement('div');
    sidebarBox.className = 'toc-sidebar-box'; // 设置侧边栏内容的类名

    // 获取所有带有 "item-group-index-" 类名的元素
    const items = document.querySelectorAll('[class*="item-group-index-"]');

    // 遍历每个索引项并创建标题栏
    items.forEach((item) => {
      item.classList.forEach((className) => {
        if (className.startsWith('item-group-index-')) {
          const titleBarBox = document.createElement('div');
          titleBarBox.className = 'title-bar-box'; // 创建标题栏盒子
          titleBarBox.dataset.groupClassName = className; // 设置数据属性

          const titleBarSlip = document.createElement('div');
          titleBarSlip.className = 'title-bar-slip'; // 创建滑块

          const titleBarTitle = document.createElement('div');
          titleBarTitle.className = 'title-bar-title'; // 创建标题文本

          const titleElement = item.querySelector('.group-title'); // 查找标题元素
          const titleText = titleElement ? titleElement.textContent : item.id; // 获取标题文本
          titleBarTitle.textContent = titleText; // 设置标题文本

          titleBarBox.appendChild(titleBarSlip); // 将滑块添加到标题栏盒子
          titleBarBox.appendChild(titleBarTitle); // 将标题文本添加到标题栏盒子

          sidebarBox.appendChild(titleBarBox); // 将标题栏盒子添加到侧边栏内容
        }
      });
    });

    sidebar.appendChild(sidebarBox); // 将侧边栏内容添加到侧边栏
    SunPanelTOCDom.appendChild(sidebar); // 将侧边栏添加到目录容器

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

    // 防抖函数
    function debounce(func, wait) {
      let timeout; // 定义超时标识
      return function (...args) {
        clearTimeout(timeout); // 清除之前的超时
        timeout = setTimeout(() => {
          func.apply(this, args); // 在延迟后执行函数
        }, wait);
      };
    }

    // 处理窗口尺寸变化的函数
    function handleResize() {
      if (isMobile()) {
        tocMobileBtn.classList.remove('hidden'); // 在移动端显示按钮
        sidebar.classList.add('hidden'); // 隐藏侧边栏
      } else {
        tocMobileBtn.classList.add('hidden'); // 在PC端隐藏按钮
        sidebar.classList.remove('hidden'); // 显示侧边栏
      }
    }

    const debouncedHandleResize = debounce(handleResize, 200); // 创建防抖函数
    window.addEventListener('resize', debouncedHandleResize); // 监听窗口大小变化
    handleResize(); // 初始化处理窗口大小

    // 点击移动端按钮的事件处理
    tocMobileBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('toc-sidebar-expansion')) {
        mobileHideSidebar(); // 如果侧边栏展开，则隐藏
      } else {
        showSidebar(); // 否则显示侧边栏
      }
    });

    // 鼠标离开侧边栏时的事件处理
    sidebar.addEventListener('mouseleave', () => {
      if (isMobile()) {
        mobileHideSidebar(); // 在移动端隐藏侧边栏
      } else {
        hideSidebar(); // 在PC端隐藏侧边栏
      }
    });

    // 鼠标进入侧边栏时的事件处理
    sidebar.addEventListener('mouseenter', () => {
      showSidebar(); // 显示侧边栏
    });

    // 为每个标题栏盒子添加点击事件
    document.querySelectorAll('.title-bar-box').forEach((box) => {
      box.addEventListener('click', function (event) {
        if (this.dataset.groupClassName) {
          const groupClassName = this.dataset.groupClassName; // 获取组类名
          const targetElement = document.querySelector(`.${groupClassName}`); // 查找目标元素
          if (targetElement) {
            const targetTop = targetElement.offsetTop; // 获取目标元素的顶部位置
            const scrollContainerElement = document.querySelector(scrollContainerElementClassName); // 获取滚动容器
            if (scrollContainerElement) {
              scrollContainerElement.scrollTo({
                top: targetTop - scrollOffset, // 滚动到目标位置
                behavior: 'smooth', // 平滑滚动
              });
            }
          }
        }
      });
    });
  }

  // 查找所有带有 "item-group-index-" 类名的元素
  const items = document.querySelectorAll('[class*="item-group-index-"]');
  if (items.length > 0) {
    createDom(); // 如果找到元素，创建 DOM
    return; // 结束执行
  }

  // 每隔一秒检查是否有带有 "item-group-index-" 类名的元素
  const interval = setInterval(() => {
    const items = document.querySelectorAll('[class*="item-group-index-"]');
    if (items.length > 0) {
      createDom(); // 如果找到元素，创建 DOM
      clearInterval(interval); // 清除定时器
    }
  }, 1000);

  // 添加外部脚本，避免重复加载
  if (!document.getElementById('11111111')) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.id = '11111111'; // 设置脚本 ID
    script.src = 'https://myhkw.cn/api/player/11111111'; // 设置脚本源
    script.setAttribute('key', '11111111'); // 设置脚本属性
    script.setAttribute('m', '11111111'); // 设置脚本属性
    document.body.appendChild(script); // 将脚本添加到文档主体
  }
})();
```

自己根据播放器修改本段代码内容

`// 添加外部脚本，避免重复加载`

`if (!document.getElementById('`11111111`')) {`

`const script = document.createElement('script');`

`script.type = 'text/javascript';`

`script.id = '`11111111`'; // 设置脚本 ID`

`script.src = 'https://myhkw.cn/api/player/`11111111`'; // 设置脚本源`

`script.setAttribute('key', '`11111111`'); // 设置脚本属性`

`script.setAttribute('m', '`11111111`'); // 设置脚本属性`

`document.body.appendChild(script); // 将脚本添加到文档主体`

`}`

`})();`

### 总结

这段代码的主要功能是创建一个动态的目录面板，允许用户通过点击目录项平滑滚动到页面的相应部分。代码中使用了自执行函数、DOM 操作、事件监听和防抖等技术，确保在不同设备和窗口大小下都能正常工作。每段代码都添加了注释，帮助理解其功能和作用。

### 文档

#### [完整文档:Sun-Panel](https://doc.sun-panel.top/zh_cn/)

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
