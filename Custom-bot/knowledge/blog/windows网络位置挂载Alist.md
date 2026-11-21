# windows网络位置挂载Alist

> 标题：windows网络位置挂载Alist
> 分类：AList网盘
> 标签：api、nas、群晖、alist、alist美化、https
> 原文：https://www.xinz.fun/archives/windows网络位置挂载Alist

> **导读**：这篇围绕「windows网络位置挂载Alist」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾AList网盘的读者。执行前建议先备份原配置，并在测试环境验证。

在本地挂载的过程中，无论是添加网络位置，还是映射网络驱动器，都会出现文件路径不对、网络错误无法访问等错误
步骤1：
按下 “windows徽标键” + “R”，打开运行窗口，输入regedit，点击确定后，打开注册表编辑器窗口。

步骤2：
将路径定位到以下路径： *计算机\HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters* 。双击右侧界面中的 BasicAuthLevel 条目，将数值数据修改为“2”，点击确定后关闭注册表编辑器

步骤3：
按下 “windows徽标键” + “R”，打开运行窗口，输入services.msc，点击确定后，打开“服务”界面。找到 “WebClient”
服务，右键点击打开选项菜单，选择重新启动，稍等几秒，待完成后，关闭“服务”界面。

完成上述三个步骤后，WebClient 服务已经允许使用 http 协议进行挂载。

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
