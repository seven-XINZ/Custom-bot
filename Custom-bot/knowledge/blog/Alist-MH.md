# Alist 美化指南

> 标题：Alist 美化指南
> 分类：AList网盘
> 标签：alist、alist美化、小雅
> 原文：https://www.xinz.fun/archives/Alist-MH

> **导读**：这篇围绕「Alist 美化指南」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾AList网盘的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 窗口透明
2. 看板娘
3. 鼠标点击效果
4. Aplayer、Meting
5. Nnplayer
6. 备案信息 及 图标颜色
7. 运行时间
8. 网站访问量
9. 自定义头部代码
10. 看板娘代码
11. 自行替换鼠标样式说明
12. 自定义内容代码
13. 以及其余 3 个小节

## 窗口透明

```
<style>
    .hope-ui-light{
      background-image: url("https://www.dmoe.cc/random.php") !important;
      background-repeat:no-repeat;background-size:cover;background-attachment:fixed;background-position-x:center;
    }
    .obj-box {
      border-radius: 15px !important;
    }
    .hope-ui-light .obj-box {
      background-color: #ffffff70 !important;
    }
    .hope-c-PJLV .hope-c-PJLV-ikSuVsl-css {
        border-radius: 15px !important;
        background-color: #ffffff70 !important;
    }
    .hope-c-PJLV .hope-c-PJLV-ibtHApG-css {
        border-radius: 15px !important;
        background-color: #ffffff70 !important;
    }
</style>
```

## 看板娘

```
<script src="https://eqcn.ajz.miesnfu.com/wp-content/plugins/wp-3d-pony/live2dw/lib/L2Dwidget.min.js"></script>

<!-- 看板娘 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome/css/font-awesome.min.css">
<script src="https://cdn.jsdelivr.net/gh/stevenjoezhang/live2d-widget@latest/autoload.js"></script>
```

## 鼠标点击效果

```
<!--鼠标点击效果-->
<script src="https://cdn.jsdelivr.net/gh/TRHX/CDN-for-itrhx.com@3.0.8/js/maodian.js"></script>
```

## Aplayer、Meting

```
<!-- aplayer、meting -->
<!-- require APlayer -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.css">
<script src="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.js"></script>
<!-- require MetingJS -->
<script src="https://cdn.jsdelivr.net/npm/meting@2/dist/Meting.min.js"></script>

<!-- 不显示歌词 -->
<script>
     function removelrc() {
        //检测是否存在歌词按钮
        if (!document.querySelector(".aplayer-icon-lrc"))
            return;
        else
        {
            //触发以后立刻移除监听
            document.removeEventListener("DOMNodeInserted",removelrc);
            //稍作延时保证触发函数时存在按钮
            setTimeout(function() {
                //以触发按钮的方式隐藏歌词，防止在点击显示歌词按钮时需要点击两次才能出现的问题
                document.querySelector(".aplayer-icon-lrc").click();
            }, 1);
            console.log("success");
            return;
        }
    }

    document.addEventListener('DOMNodeInserted', removelrc)
</script>
```

**Meting Body部分**

```
<meting-js 
    server="netease"
    type="playlist"
    id="7292043675"
    fixed = true
>
</meting-js>

<!-- 吸附边缘 css -->
<style>
    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow,
    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow .aplayer-body {
        left: -66px !important;
    }

    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow:hover .aplayer-body {
        left: 0 !important;
    }
</style>
```

## Nnplayer

```
<script src="https://unpkg.com/nplayer@latest/dist/index.min.js"></script>
```

## 备案信息 及 图标颜色

```
<!--备案信息-->
</style>
<link href="https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/font-awesome/6.0.0/css/all.min.css" rel=" stylesheet ">
<div id="customize" style="display:none; text-align:center;">
    <br />
    <div style="font-size:15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <span class="nav-item">
            <a class="nav-link" href="https://github.com/Xhofe/alist" target="_blank">
                <i class="fa fa-heart" style="color:#9932CC;" aria-hidden="true"></i>
                由Alist驱动 |
            </a>
        </span>
        <span class="nav-item" style="margin-bottom: 5px;">
            <a class="nav-link" href="https://cloud1.waite.wang/@manage" target="_blank">
                <i class="fa fa-gear" style="color:#9932CC;" aria-hidden="true"></i>
                管理后台
            </a>
        </span> <br/>
        <span class="nav-item">
            <a class="nav-link" href="https://waite.wang/" target="_blank">
                <i class="fa-solid fa-copyright" style="color:#9932CC" aria-hidden="true"></i>
                2022 WAITE.WANG |
            </a>
        </span>
        <span class="nav-item">
            <a class="nav-link" href="https://beian.miit.gov.cn/" target="_blank">
                <i class="fa fa-balance-scale" style="color:#9932CC;" aria-hidden="true"></i>
                粤 ICP 备 2022028437 号 
            </a>
        </span>

    </div>
    <br />
</div>
<script>
    let interval = setInterval(() => {
        if (document.querySelector(".footer")) {
            document.querySelector("#customize").style.display = "";
            clearInterval(interval);
        }
    }, 200);
</script>
</font>

<style type="text/css">
    .footer {
        display: none !important;
    }

    .hope-c-ivMHWx-dvmlqS-cv {
        color: #9932CC !important;
    }

    .hope-c-PJLV-igVoCQk-css {
        color: #9932CC !important;
    }

    .hope-c-PJLV-ilcHcHe-css {
        color: #9932CC !important;
    }

    .hope-c-PJLV-ieavQQG-css {
        color: #9932CC !important;
    }
</style>
```

## 运行时间

```
<script type="text/javascript">
    function show_runtime() {
        window.setTimeout("show_runtime()", 1000);
        X = new Date("8/24/2022 10:28:00");
        Y = new Date();
        T = (Y.getTime() - X.getTime());
        M = 24 * 60 * 60 * 1000;
        a = T / M;
        A = Math.floor(a);
        b = (a - A) * 24;
        B = Math.floor(b);
        c = (b - B) * 60;
        C = Math.floor((b - B) * 60);
        D = Math.floor((c - C) * 60);
        runtime_span.innerHTML = "本站已运行 " + A + "天" + B + "小时" + C + "分" + D + "秒"
    }
    show_runtime();
</script>

<span id="runtime_span"></span>
```

## 网站访问量

```
<!-- 访问量 -->
<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>

本站总访问量 <span id="busuanzi_value_site_pv"></span> 次
```

## 自定义头部代码

```
<!--Alist V3建议添加的，已经默认添加了，如果你的没有建议加上-->
<script src="https://polyfill.io/v3/polyfill.min.js?features=String.prototype.replaceAll"></script>

<!--引入字体，全局字体使用-->
<link rel="stylesheet" href="https://npm.elemecdn.com/lxgw-wenkai-webfont@1.1.0/lxgwwenkai-regular.css" />

<!--评论系统使用的js-->
<script src='https://unpkg.com/valine/dist/Valine.min.js'></script>

<!--不蒜子计数器-->
<script async src="https://busuanzi.icodeq.com/busuanzi.pure.mini.js"></script>

<!-- Font6，自定义底部使用和看板娘使用的图标和字体文件-->
<link type='text/css' rel="stylesheet" href="https://npm.elemecdn.com/font6pro@6.0.1/css/fontawesome.min.css" media='all'>
<link href="https://npm.elemecdn.com/font6pro@6.0.1/css/all.min.css" rel="stylesheet">

<!--音乐播放器所用的文件-->
<!-- require APlayer -->
<link rel="stylesheet" href="https://npm.elemecdn.com/aplayer@1.10.1/dist/APlayer.min.css">
<script src="https://npm.elemecdn.com/aplayer@1.10.1/dist/APlayer.min.js"></script>
<!-- require MetingJS -->
<script src="https://npm.elemecdn.com/meting@2.0.1/dist/Meting.min.js"></script>

<style>
  /* 去除通知栏 右上角 X */
  .notify-render .hope-close-button{
    display: none;
  }
  /* 图片API用法点进去都会有食用说明的
  樱花：https://www.dmoe.cc
  夏沫：https://cdn.seovx.com
  搏天：https://api.btstu.cn/doc/sjbz.php
  姬长信：https://github.com/insoxin/API
  小歪：https://api.ixiaowai.cn/
  保罗：https://api.paugram.com
  墨天逸：https://api.mtyqx.cn
  岁月小筑：https://img.xjh.me
  东方Project：https://img.paulzzh.com
  */
  /*白天背景图*/
  .hope-ui-light{
    background-image: url("http://pic.rmb.bdstatic.com/bjh/7569b014a1abafd5481298763300ae1d.png") !important;
    background-repeat:no-repeat;background-size:cover;background-attachment:fixed;background-position-x:center;
  }
  /*夜间背景图*/
  .hope-ui-dark {
    background-image: url(http://pic.rmb.bdstatic.com/bjh/ebe942a9de49856f389c65f25a338335.png) !important;
    background-repeat:no-repeat;background-size:cover;background-attachment:fixed;background-position-x:center;
  }
  /*主列表夜间模式透明，50%这数值是控制透明度大小的*/
  .obj-box.hope-stack.hope-c-dhzjXW.hope-c-PJLV.hope-c-PJLV-iigjoxS-css{
    background-color:rgb(0 0 0 / 50%) !important;
  }
  /*readme夜间模式透明，50%这数值是控制透明度大小的*/
  .hope-c-PJLV.hope-c-PJLV-iiuDLME-css{
    background-color:rgb(0 0 0 / 50%) !important;
  }
  /*主列表透明*/
  .obj-box.hope-stack.hope-c-dhzjXW.hope-c-PJLV.hope-c-PJLV-igScBhH-css {
    background-color: rgba(255, 255, 255, 0.5) !important;
  }
  /*readme透明*/
  .hope-c-PJLV.hope-c-PJLV-ikSuVsl-css{
    background-color: rgba(255, 255, 255, 0.5) !important;
  }
  /*顶部右上角切换按钮透明*/
  .hope-c-ivMHWx-hZistB-cv.hope-icon-button{
    background-color: rgba(255, 255, 255, 0.3) !important;
  }
  /*右下角侧边栏按钮透明*/
  .hope-c-PJLV-ijgzmFG-css{
    background-color: rgba(255, 255, 255, 0.5) !important;
  }
  /*白天模式代码块透明*/
  .hope-ui-light pre{
    background-color: rgba(255, 255, 255, 0.1) !important;
  }
  /*夜间模式代码块透明*/
  .hope-ui-dark pre {
    background-color: rgba(255, 255, 255, 0) !important;
  }

  /*底部CSS，.App .table这三个一起的*/
  dibu {
    border-top: 0px;
    position: absolute;
    bottom: 0;
    width: 100%;
    margin: 0px;
    padding: 0px;
  }
  .App {
    min-height: 85vh;
  }
  .table {
    margin: auto;
  }

  /*去掉底部*/
  .footer {
    display: none !important;
  }

  /*全局字体*/
  *{font-family:LXGW WenKai}
  *{font-weight:bold}
  body {font-family: LXGW WenKai;}

  /*以下为评论系统专用*/
  /*适配大小契合度*/
  .newValine{
    width: min(96%, 940px);
    flex-direction: column;
    row-gap: var(--hope-space-2);
    border-radius: var(--hope-radii-xl);
    padding: var(--hope-space-2);
    box-shadow: var(--hope-shadows-lg);
  }
  /*评论区 - 白天模式透明度*/
  .hope-ui-light .newValine{
    background-color: rgba(255, 255, 255, 0.8) !important;
  }
  /*评论区 - 夜间模式透明度*/
  .hope-ui-dark .newValine{
    background-color:rgb(0 0 0 / 80%) !important;
  }
  /*输入栏里面跳舞的小人背景图*/
  .vedit{
    background-image:url(https://cdn.jsdelivr.net/gh/anwen-anyi/imgAnwen/images/OuNiJiang.gif); 
    background-size:contain;
    background-repeat:no-repeat;
    background-position:right bottom;
    transition:all 0.25s ease-in-out 0s;
  }
  textarea#comment-textarea:focus{
    background-position-y:120px;
    transition:all 0.25s ease-in-out 0s;
  }    

  /*渐变背景CSS*/
  #canvas-basic {
    position: fixed;
    display: block;
    width: 100%;
    height: 100%;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -999;
  }
</style>
```

## 看板娘代码

```
<!--看板娘 -自定义大小，隐藏对话框和对话框高度-->
<style type="text/css">
  #waifu #live2d {
    height: 350px!important;
    width: 350px!important;
  }
  #waifu-tips {
    top: -60px;
    /*display:none !important;隐藏对话框*/
  }
</style>

<!--看板娘加载指定模型-->
<script>
  localStorage.setItem('modelId', '7');
  localStorage.setItem('modelTexturesId', '3');
</script>

<!--自己选左右-->
<script src="https://api.itggg.cn/live2dnew/left/index.js"></script>
<script src="https://api.itggg.cn/live2dnew/right/index.js"></script>

<!--以下四个两个主用两个备用的,选一条使用即可-->
<!--自己选左右-->
<script src="https://api.itggg.cn/live2dnew/left/index.js"></script>
<script src="https://api.itggg.cn/live2dnew/right/index.js"></script>

<!--备用的，自己选左右-->
<script src="https://luluossfile.lulufind.com/work/teacher_u20221017ce7b5991_1666420843832_19934968_file.js"></script>
<script src="https://luluossfile.lulufind.com/work/teacher_u20221017bb6d7454_1666420849979_19584065_file.js"></script>
```

## 自行替换鼠标样式说明

```
<!--较为个性化的鼠标指针样式，可结合个人需要自行修改-->
<style>
  body {
    cursor: url(https://luluossfile.lulufind.com/work/teacher_u20221021b3a89013_1666841028833_10660845_file.cur), default;
  }
  select{
    cursor: url(https://luluossfile.lulufind.com/work/teacher_u2021090299b56677_1666842679271_10490748_file.cur), pointer;
  }
  button,a:hover{
    cursor: url(https://luluossfile.lulufind.com/work/teacher_u20221017ac9f1124_1666842626270_11086578_file.cur), pointer;
  }
  input{
    cursor:url(https://luluossfile.lulufind.com/work/teacher_u2021090299b56677_1666842633386_14976764_file.cur), text;    
  }
  textarea,input:focus{
    cursor:url(https://luluossfile.lulufind.com/work/teacher_u202210176ba36766_1666842640146_15845280_file.cur), text;    
  }
  code{
    cursor: url(https://luluossfile.lulufind.com/work/teacher_u20221021b3a89013_1666842646779_15864973_file.cur), default;    
  }
  pre>code{
    cursor: url(https://luluossfile.lulufind.com/work/teacher_u202210176ba36766_1666842653500_10010236_file.cur), default;    
  }
</style>
```

## 自定义内容代码

```
<!--延迟加载-->
<!--如果要写自定义内容建议都加到这个延迟加载的范围内-->
<div id="customize" style="display: none;">
    <div>
        <!--音乐播放器-->
        <meting-js fixed="true" autoplay="false" theme="#409EFF" list-folded="true" auto="QQ音乐或者网易云的链接"></meting-js>

        <!--评论模块还有下面的script也是-->
        <center>
            <div class="newValine" id="vcomments"></div>
        </center>
        <script>
            new Valine({
                visitor: true,
                el: '#vcomments',
                avatar: 'wavatar',
                appId: 'Your appId',
                appKey: 'Your appKey',
                placeholder: "有什么问题欢迎评论区留言~么么哒"
            }) 
        </script>

        <br />
        <center class="dibu">
            <div style=" line-height: 20px;font-size: 9pt;font-weight: bold;">
                <span>
                    "
                    <span style="color: rgb(13, 109, 252); font-weight: bold;" id="hitokoto">
                        <a href="#" id="hitokoto_text">
                            "人生最大的遗憾,就是在最无能为力的时候遇到一个想要保护一生的人."
                        </a>
                    </span> "
                </span>
                <p style="margin-left: 10rem;font-size: 8pt;">
                    <small>
                        —— Anwen's Cloud
                    </small>
                </p>
            </div>

            <div style="font-size: 13px; font-weight: bold;">
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxxxxxx"
                        target="_blank">
                        <i class="fab fa-qq" style="color:#409EFF" aria-hidden="true">
                        </i>
                        QQ |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="mailto:xxxxx@foxmail.com" target="_blank">
                        <i class="fa-duotone fa-envelope-open" style="color:#409EFF" aria-hidden="true">
                        </i>
                        邮箱 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxx" target="_blank">
                        <i class="fas fa-edit" style="color:#409EFF" aria-hidden="true">
                        </i>
                        博客 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxxxx" target="_blank">
                        <i class="fas fa-comment-lines" style="color:#409EFF;" aria-hidden="true">
                        </i>
                        留言 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxxx" target="_blank">
                        <i class="fa fa-cloud-download" style="color:#409EFF;" aria-hidden="true">
                        </i>
                        云盘 |
                    </a>
                </span>
                <!--后台入口-->
                <span class="nav-item">
                    <a class="nav-link" href="/@manage" target="_blank">
                        <i class="fa-solid fa-folder-gear" style="color:#409EFF;" aria-hidden="true">
                        </i>
                        管理 |
                    </a>
                </span>
                <!--版权，请尊重作者-->
                <span class="nav-item">
                    <a class="nav-link" href="https://github.com/Xhofe/alist" target="_blank">
                        <i class="fa-solid fa-copyright" style="color:#409EFF;" aria-hidden="true">
                        </i>
                        Alist
                    </a>
                </span>
                <br />
                <!--添加一个访问量-->
                <span>
                    本"<span style="color: rgb(13, 109, 252); font-weight: bold;"><a href="#">目录</a></span>"访问量 <span id="busuanzi_value_page_pv" style="color: rgb(13, 109, 252); font-weight: bold;"></span> 次 本站总访问量 <span id="busuanzi_value_site_pv" style="color: rgb(13, 109, 252); font-weight: bold;"></span>                次 本站总访客数 <span id="busuanzi_value_site_uv" style="color: rgb(13, 109, 252); font-weight: bold;"></span> 人
                </span>
                <br />
                <!--添加备案信息-->
                <span class="nav-item">
                    <a class="nav-link" href="https://beian.miit.gov.cn/#/Integrated/index" target="_blank">
                        <i class="fa-solid fa-shield-check" style="color:#409EFF;" aria-hidden="true">
                        </i>
                        冀 ICP备2222000777号
                    </a>
                </span>
            </div>
        </center>
        <br />
        <br />
    </div>

    <!--一言API-->
    <script src="https://v1.hitokoto.cn/?encode=js&select=%23hitokoto" defer></script>
<!--延迟加载范围到这里结束-->
</div>
<!--延迟加载配套使用JS-->
<script>
    let interval = setInterval(() => {
        if (document.querySelector(".footer")) {
            document.querySelector("#customize").style.display = "";
            clearInterval(interval);
        }
    }, 200);
</script>

<!-- 渐变背景初始化,如果要使用渐变背景把下面的那一行注释去掉即可-->
<!-- 下面的几行都是渐变的一套,自定义头部内还有一个关联的自定义CSS -->
<!--<canvas id="canvas-basic"></canvas> -->
<script src="https://npm.elemecdn.com/granim@2.0.0/dist/granim.min.js"></script>
<script>
var granimInstance = new Granim({
    element: '#canvas-basic',
    direction: 'left-right',
    isPausedWhenNotInView: true,
    states : {
        "default-state": {
            gradients: [
                ['#a18cd1', '#fbc2eb'],
                 ['#fff1eb', '#ace0f9'],
                 ['#d4fc79', '#96e6a1'],
                 ['#a1c4fd', '#c2e9fb'],
                 ['#a8edea', '#fed6e3'],
                 ['#9890e3', '#b1f4cf'],
                 ['#a1c4fd', '#c2e9fb'],
                 ['#fff1eb', '#ace0f9']

            ]
        }
    }
});
</script>
```

## 网页点击鼠标特效

```
<!-- 网页鼠标点击特效 - 核心价值观关键字 -->
<script>
    (function () {
        var a_idx = 0;
        window.onclick = function (event) {
            var a = new Array("❤富强❤", "❤民主❤", "❤文明❤", "❤和谐❤", "❤自由❤", "❤平等❤", "❤公正❤", "❤法治❤", "❤爱国❤",
                "❤敬业❤", "❤诚信❤", "❤友善❤");
            var heart = document.createElement("b"); //创建b元素
            heart.onselectstart = new Function('event.returnValue=false'); //防止拖动

            document.body.appendChild(heart).innerHTML = a[a_idx]; //将b元素添加到页面上
            a_idx = (a_idx + 1) % a.length;
            heart.style.cssText = "position: fixed;left:-100%;"; //给p元素设置样式

            var f = 13, // 字体大小
                x = event.clientX - f / 2 - 30, // 横坐标
                y = event.clientY - f, // 纵坐标
                c = randomColor(), // 随机颜色
                a = 1, // 透明度
                s = 0.8; // 放大缩小

            var timer = setInterval(function () { //添加定时器
                if (a <= 0) {
                    document.body.removeChild(heart);
                    clearInterval(timer);
                } else {
                    heart.style.cssText = "font-size:16px;cursor: default;position: fixed;color:" +
                        c + ";left:" + x + "px;top:" + y + "px;opacity:" + a + ";transform:scale(" +
                        s + ");";

                    y--;
                    a -= 0.016;
                    s += 0.002;
                }
            }, 15)
        }
        // 随机颜色
        function randomColor() {
            return "rgb(" + (~~(Math.random() * 255)) + "," + (~~(Math.random() * 255)) + "," + (~~(Math
                .random() * 255)) + ")";
        }
    }());
</script>
```

```
<!-- 网页鼠标点击特效 - 爱心 -->
<script type="text/javascript">
         ! function (e, t, a) {
            function r() {
                for (var e = 0; e < s.length; e++) s[e].alpha <= 0 ? (t.body.removeChild(s[e].el), s.splice(e, 1)) : (s[
                        e].y--, s[e].scale += .004, s[e].alpha -= .013, s[e].el.style.cssText = "left:" + s[e].x +
                    "px;top:" + s[e].y + "px;opacity:" + s[e].alpha + ";transform:scale(" + s[e].scale + "," + s[e]
                    .scale + ") rotate(45deg);background:" + s[e].color + ";z-index:99999");
                requestAnimationFrame(r)
            }
            function n() {
                var t = "function" == typeof e.onclick && e.onclick;
                e.onclick = function (e) {
                    t && t(), o(e)
                }
            }

            function o(e) {
                var a = t.createElement("div");
                a.className = "heart", s.push({
                    el: a,
                    x: e.clientX - 5,
                    y: e.clientY - 5,
                    scale: 1,
                    alpha: 1,
                    color: c()
                }), t.body.appendChild(a)
            }

            function i(e) {
                var a = t.createElement("style");
                a.type = "text/css";
                try {
                    a.appendChild(t.createTextNode(e))
                } catch (t) {
                    a.styleSheet.cssText = e
                }
                t.getElementsByTagName("head")[0].appendChild(a)
            }

            function c() {
                return "rgb(" + ~~(255 * Math.random()) + "," + ~~(255 * Math.random()) + "," + ~~(255 * Math
                    .random()) + ")"
            }
            var s = [];
            e.requestAnimationFrame = e.requestAnimationFrame || e.webkitRequestAnimationFrame || e
                .mozRequestAnimationFrame || e.oRequestAnimationFrame || e.msRequestAnimationFrame || function (e) {
                    setTimeout(e, 1e3 / 60)
                }, i(
                    ".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"
                ), n(), r()
        }(window, document);

</script>
```

```
1
2
<!--鼠标点击效果-->
<script src="https://cdn.jsdelivr.net/gh/TRHX/CDN-for-itrhx.com@3.0.8/js/maodian.js"></script>
```

## 音乐播放器添加说明

### 核心代码（记得引用头部内的喔~）

#### QQ音乐

```
<meting-js fixed="true" autoplay="false" theme="#409EFF" list-folded="true" auto="https://y.qq.com/n/yqq/playlist/7927599544.html"></meting-js>
```

#### 网易云

```
<meting-js 
    fixed="true" 
    autoplay="false" 
    theme="#409EFF" 
    list-folded="true" 
    server="netease" 
    type="playlist" 
    id="2195404116">
  </meting-js>
```

#### 加上歌词

```
<meting-js
    name="rainymood"
    artist="rainymood"
    url="https://rainymood.com/audio1110/0.m4a"
    cover="https://rainymood.com/i/badge.jpg"
    fixed="true">
    <pre hidden>
        [00:00.00]This
        [00:04.01]is
        [00:08.02]Waite
    </pre>
</meting-js>
```

### 音乐的一些其他参数

| 选项 | 默认 | 描述 |
| --- | --- | --- |
| id | require | require song id / playlist id / album id / search keyword |
| server | require | music platform: netease, tencent, kugou, xiami, baidu |
| type | require | song, playlist, album, search, artist |
| auto | options | music link, support: netease, tencent, xiami |
| fixed | false | enable fixed mode |
| mini | false | enable mini mode |
| autoplay | false | audio autoplay |
| theme | #2980b9 | main color |
| loop | all | player loop play, values: 'all', 'one', 'none' |
| order | list | player play order, values: 'list', 'random' |
| preload | auto | values: 'none', 'metadata', 'auto' |
| volume | 0.7 | default volume, notice that player will remember user setting, default volume will not work after user set volume themselves |
| mutex | true | prevent to play multiple player at the same time, pause other play |
| lrc-type | 0 | lyric type |
| list-folded | false | indicate whether list should folded at first |
| list-max-height | 340px | list max height |
| storage-name | metingjs | localStorage key that store player setting |

## 自用

```
<!--如果要写自定义内容建议都加到这个延迟加载的范围内-->
<div id="customize" style="display: none;">
    <div>
        <!--音乐播放器-->
        <meting-js list-folded="true" server="netease" type="playlist" id="7292043675" fixed=true>
            <pre hidden>
                [00:00.00]This
                [00:04.01]is
                [00:08.02]Waite
            </pre>
        </meting-js>
        <br />
        <center class="dibu">
            <div style=" line-height: 20px;font-size: 9pt;font-weight: bold;">
                <span>
                    "
                    <span style="color: rgb(121, 15, 104); font-weight: bold; font-size: 15px;" id="hitokoto">
                        <a href="#" id="hitokoto_text">
                            "人生最大的遗憾,就是在最无能为力的时候遇到一个想要保护一生的人."
                        </a>
                    </span> "
                </span>
                <p style="margin-left: 10rem;font-size: 8pt;">
                    <small>
                        —— Waite's Cloud
                    </small>
                </p>
            </div>

            <div style="font-size: 13px; font-weight: bold;">
                <span class="nav-item">
                    <a class="nav-link" href="tencent://message/?uin=1657724340" target="_blank">
                        <i class="fab fa-qq" style="color:#9932CC" aria-hidden="true">
                        </i>
                        QQ |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="mailto:waite0603@qq.com" target="_blank">
                        <i class="fa-duotone fa-envelope-open" style="color:#9932CC" aria-hidden="true">
                        </i>
                        邮箱 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="https://waite.wang/" target="_blank">
                        <i class="fas fa-edit" style="color:#9932CC" aria-hidden="true">
                        </i>
                        博客 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="#" target="_blank">
                        <i class="fa fa-cloud-download" style="color:#9932CC;" aria-hidden="true">
                        </i>
                        云盘 |
                    </a>
                </span>
                <!--后台入口-->
                <span class="nav-item">
                    <a class="nav-link" href="/@manage" target="_blank">
                        <i class="fa-solid fa-folder-gear" style="color:#9932CC;" aria-hidden="true">
                        </i>
                        管理 |
                    </a>
                </span>
                <!--版权，请尊重作者-->
                <span class="nav-item">
                    <a class="nav-link" href="https://github.com/Xhofe/alist" target="_blank">
                        <i class="fa-solid fa-copyright" style="color:#9932CC;" aria-hidden="true">
                        </i>
                        Alist
                    </a>
                </span>
                <br />
                <!--添加一个访问量-->
                <span>
                    本"<span style="color: rgb(121, 15, 104); font-weight: bold;"><a href="#">目录</a></span>"访问量 <span
                        id="busuanzi_value_page_pv" style="color: rgb(121, 15, 104); font-weight: bold;"></span> 次
                    本站总访问量 <span id="busuanzi_value_site_pv"
                        style="color: rgb(121, 15, 104); font-weight: bold;"></span> 次 本站总访客数 <span
                        id="busuanzi_value_site_uv" style="color: rgb(121, 15, 104); font-weight: bold;"></span> 人
                </span>
                <br />
                <!--添加备案信息-->
                <span class="nav-item">
                    <a class="nav-link" href="https://beian.miit.gov.cn/#/Integrated/index" target="_blank">
                        <i class="fa-solid fa-shield-check" style="color:#9932CC;" aria-hidden="true">
                        </i>
                        粤 ICP 备 2022028437 号
                    </a>
                </span>
            </div>
        </center>
        <br />
        <br />
    </div>

    <!--一言API-->
    <script src="https://v1.hitokoto.cn/?encode=js&select=%23hitokoto" defer></script>
    <!--延迟加载范围到这里结束-->
</div>
<!--延迟加载配套使用JS-->
<script>
    let interval = setInterval(() => {
        if (document.querySelector(".footer")) {
            document.querySelector("#customize").style.display = "";
            clearInterval(interval);
        }
    }, 200);

    function removelrc() {
        //检测是否存在歌词按钮
        if (!document.querySelector(".aplayer-icon-lrc"))
            return;
        else {
            //触发以后立刻移除监听
            document.removeEventListener("DOMNodeInserted", removelrc);
            //稍作延时保证触发函数时存在按钮
            setTimeout(function () {
                //以触发按钮的方式隐藏歌词，防止在点击显示歌词按钮时需要点击两次才能出现的问题
                document.querySelector(".aplayer-icon-lrc").click();
            }, 1);
            console.log("success");
            return;
        }
    }

    document.addEventListener('DOMNodeInserted', removelrc)
</script>

</script>

<style>
    /* 去除通知栏 右上角 X */
    .notify-render .hope-close-button {
        display: none;
    }

    /* 图片API用法点进去都会有食用说明的
    樱花：https://www.dmoe.cc
    夏沫：https://cdn.seovx.com
    搏天：https://api.btstu.cn/doc/sjbz.php
    姬长信：https://github.com/insoxin/API
    小歪：https://api.ixiaowai.cn/
    保罗：https://api.paugram.com
    墨天逸：https://api.mtyqx.cn
    岁月小筑：https://img.xjh.me
    东方Project：https://img.paulzzh.com
    */
    .footer {
        display: none !important;
    }

    .hope-c-ivMHWx-dvmlqS-cv {
        color: #9932CC !important;
    }

    .hope-c-PJLV-igVoCQk-css {
        color: #9932CC !important;
    }

    .hope-c-PJLV-ilcHcHe-css {
        color: #9932CC !important;
    }

    .hope-c-PJLV-ieavQQG-css {
        color: #9932CC !important;
    }

    /*白天背景图*/
    .hope-ui-light {
        background-image: url("https://img.waite.wang/images/2022/11/27/640x420.jpg") !important;
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
        background-position-x: center;
    }

    /*夜间背景图*/
    .hope-ui-dark {
        background-image: url("https://img.waite.wang/images/2022/11/27/640x420-1.jpg") !important;
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
        background-position-x: center;
    }

    /*主列表夜间模式透明，50%这数值是控制透明度大小的*/
    .obj-box.hope-stack.hope-c-dhzjXW.hope-c-PJLV.hope-c-PJLV-iigjoxS-css {
        background-color: rgb(0 0 0 / 50%) !important;
    }

    /*readme夜间模式透明，50%这数值是控制透明度大小的*/
    .hope-c-PJLV.hope-c-PJLV-iiuDLME-css {
        background-color: rgb(0 0 0 / 50%) !important;
    }

    /*主列表透明*/
    .obj-box.hope-stack.hope-c-dhzjXW.hope-c-PJLV.hope-c-PJLV-igScBhH-css {
        background-color: rgba(255, 255, 255, 0.5) !important;
    }

    /*readme透明*/
    .hope-c-PJLV.hope-c-PJLV-ikSuVsl-css {
        background-color: rgba(255, 255, 255, 0.5) !important;
    }

    /*顶部右上角切换按钮透明*/
    .hope-c-ivMHWx-hZistB-cv.hope-icon-button {
        background-color: rgba(255, 255, 255, 0.3) !important;
    }

    /*右下角侧边栏按钮透明*/
    .hope-c-PJLV-ijgzmFG-css {
        background-color: rgba(255, 255, 255, 0.5) !important;
    }

    /*白天模式代码块透明*/
    .hope-ui-light pre {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /*夜间模式代码块透明*/
    .hope-ui-dark pre {
        background-color: rgba(255, 255, 255, 0) !important;
    }

    /*底部CSS，.App .table这三个一起的*/
    dibu {
        border-top: 0px;
        position: absolute;
        bottom: 0;
        width: 100%;
        margin: 0px;
        padding: 0px;
    }

    .App {
        min-height: 85vh;
    }

    .table {
        margin: auto;
    }

    /*去掉底部*/
    .footer {
        display: none !important;
    }

    /*全局字体*/
    * {
        font-family: LXGW WenKai
    }

    * {
        font-weight: bold
    }

    body {
        font-family: LXGW WenKai;
    }

    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow,
    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow .aplayer-body {
        left: -66px !important;
    }

    .aplayer.aplayer-withlist.aplayer-fixed.aplayer-narrow:hover .aplayer-body {
        left: 0 !important;
    }
</style>
```

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
