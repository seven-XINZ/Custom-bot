# Koishi 新人快速入门

> 标题：Koishi 新人快速入门
> 分类：机器人Bot
> 标签：docker、Linux、Windows、debian、Koishi、bot
> 原文：https://www.xinz.fun/archives/Koishilest

> **导读**：这篇围绕「Koishi 新人快速入门」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾机器人Bot的读者。执行前建议先备份原配置，并在测试环境验证。

## 操作路线

1. 入门资源
2. 安装和首次运行
3. 安装插件
4. Blockly 相关

由于 Koishi 的功能较为强大和复杂，刚刚入门 Koishi 的新用户可能会遇到各种各样的问题；特设立此贴作为 Koishi 的快速入门贴以进行扫盲。下面的内容是入门 Koishi 所必须的基础内容。

**在论坛或用户群提问之前，你应当至少快速浏览过一遍下面的全部内容。尽量避免提出本贴已经涵盖到的基础性问题。**

---

## 入门资源

下面的内容推荐在上手 Koishi 前先快速浏览一遍。

### Koishi 官方文档

![配图](https://forum.koishi.xyz/uploads/default/original/1X/e8c5395ceef43b839a1298f8d843dc928e3284ca.png)[koishi.chat](https://koishi.chat/zh-CN/)

### [Koishi](https://koishi.chat/zh-CN/)

创建跨平台、可扩展、高性能的机器人

Koishi 官方文档是一切的开始。官方文档的「入门」章节提供了一般性的入门指导，推荐先浏览一遍。

### 视频教程

[bilibili.com](https://www.bilibili.com/video/BV1nG4y1y7zc/)

![配图](https://forum.koishi.xyz/uploads/default/original/1X/9287efb6de893f2c672e0a675fdc83d79b32a1f7.png)

### [Koishi机器人教程01-Koishi入门\_哔哩哔哩\_bilibili 281](https://www.bilibili.com/video/BV1nG4y1y7zc/)

开发 孤梦星影视频制作 Il-Harper相关内容参加评论区置顶。请勿转载本视频到其他任何视频网站。, 视频播放量 14976、弹幕量 5、点赞数 344、投硬币枚数 182、收藏人数 494、转发人数 110, 视频作者 孤梦星影, 作者简介...

入门教程展示了 Koishi 的安装以及插件的安装和使用方法，建议至少完整观看一遍，并跟随操作。

[bilibili.com](https://www.bilibili.com/video/BV1Zx4y1G7ou/)

![配图](https://forum.koishi.xyz/uploads/default/original/1X/26c421f36a314daf695f1b073e48d3cf4d7d9fb8.png)

### [Koishi机器人教程02-进阶\_哔哩哔哩\_bilibili 54](https://www.bilibili.com/video/BV1Zx4y1G7ou/)

开发 孤梦星影视频制作 Il-Harper相关内容参加评论区置顶。请勿转载本视频到其他任何视频网站。, 视频播放量 8736、弹幕量 1、点赞数 154、投硬币枚数 81、收藏人数 132、转发人数 8, 视频作者 孤梦星影, 作者简介...

进阶教程简单介绍了 Koishi 内置的几个常用的基础功能。其中最重要的是以下两句话：

- **不要随意下载来源不明的插件，因为它们可能导致 Koishi 无法运行，甚至更严重的后果。**
- **如果没有必要，那么不要改动任何配置。**

这两句话在官方文档和视频中均有提到，请牢记。

## 安装和首次运行

Koishi 应当永远从 Koishi 官方网站 [https://koishi.chat 757](https://koishi.chat/) 上直接下载最新版安装。在你完全熟悉 Koishi 之前，不推荐使用非标准版本或第三方版本。

安卓用户请下载标注有 **扩展包** 或 **完整包** 的安装包

### 以下是常见的安装问题：

- Win 7 相关：

![配图](https://forum.koishi.xyz/user_avatar/forum.koishi.xyz/ilharp/48/4_2.png) [请问 Windows 7 能使用 Koishi 吗？](https://forum.koishi.xyz/t/topic/283) [互助](https://forum.koishi.xyz/c/question/5)

> 我在 win7 上打开官方的安装包，然后提示不支持什么的…… 请问 win7 有办法使用 Koishi 吗？

- Linux 启动：

![配图](https://forum.koishi.xyz/user_avatar/forum.koishi.xyz/ilharp/48/4_2.png) [linux 运行显示 panic: runtime error: invalid memory address or nil pointer dereference](https://forum.koishi.xyz/t/topic/318) [互助](https://forum.koishi.xyz/c/question/5)

> 我在 Linux 系统上启动 Koishi，然后出现如下提示： panic: runtime error: invalid memory address or nil pointer dereference 后面还有很长，我就不复制了 这个是什么原因呢

- 安卓相关：

![配图](https://forum.koishi.xyz/user_avatar/forum.koishi.xyz/ilharp/48/4_2.png) [安卓上 Koishi无法启动](https://forum.koishi.xyz/t/topic/309) [互助](https://forum.koishi.xyz/c/question/5)

> 提示 project not found: /home/koishi-app 重装以后提示 spawn xdg-open ENOENT 请问是什么原因呢？

## 安装插件

- 提示「安装失败」：

![配图](https://forum.koishi.xyz/user_avatar/forum.koishi.xyz/ilharp/48/4_2.png) [安装插件的时候显示安装失败](https://forum.koishi.xyz/t/topic/292) [互助](https://forum.koishi.xyz/c/question/5)

> 就像这样 [image]

## Blockly 相关

- Blockly 论坛贴：

![配图](https://forum.koishi.xyz/user_avatar/forum.koishi.xyz/timebather/48/124_2.png) [Blockly插件 : 可视化积木编程!无需敲代码! 实现你机器人自己的运行逻辑!](https://forum.koishi.xyz/t/topic/213) [Blockly](https://forum.koishi.xyz/c/blockly/17)

> koishi-plugin-blockly [[npm]](https://www.npmjs.com/package/koishi-plugin-blockly) [Download] [[Install Size]](https://packagephobia.com/result?p=koishi-plugin-blockly) [[Package Quality]](https://packagequality.com/#?package=koishi-plugin-blockly) [[Koishi]](https://koishi.chat/) 使用Blockly在你的Koishi里使用可视化编程! Use blockly plugin to programming with blocks and no-code needed! 如何使用? How to use it? …

- **Blockly 教程视频**：

[bilibili.com](https://www.bilibili.com/video/BV1uG4y1U7YG/)

![配图](https://forum.koishi.xyz/uploads/default/original/1X/3a961348c91bd2f3c9e947ff69af558fb757b649.png)

### [「无需写代码, 十分钟搭建自己的QQ机器人! Koishi低代码可视化编程插件blockly介绍」\_哔哩哔哩\_bilibili 69](https://www.bilibili.com/video/BV1uG4y1U7YG/)

相关内容参见评论区置顶。请勿转载本视频到其他任何视频网站。, 视频播放量 146363、弹幕量 180、点赞数 5310、投硬币枚数 2361、收藏人数 8795、转发人数 1239, 视频作者 h4m5ter, 作者简介...

---

如果对本贴有任何建议或认为应当添加其他内容的话，可以直接在下面进行回复。

**官网**:[Koishi](https://koishi.chat/zh-CN/)

**转载自官方论坛**:[论坛](https://forum.koishi.xyz/t/topic/556)

**如需转载请注明来源以及官方**

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
