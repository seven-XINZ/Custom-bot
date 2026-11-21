# windows暂停更新3000天

> 标题：windows暂停更新3000天
> 分类：Windows与其他
> 标签：Windows
> 原文：https://www.xinz.fun/archives/windows暂停更新3000天

> **导读**：这篇围绕「windows暂停更新3000天」整理实际操作经验，重点记录步骤、配置和容易忽略的细节，适合需要一份中文落地记录时查阅。
>
> 适合正在折腾Windows与其他的读者。执行前建议先备份原配置，并在测试环境验证。

Win+R

```
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" /v FlightSettingsMaxPauseDays /t reg_dword /d 3000 /f
```

问:为什么不直接关闭更新 答:[1.windows](http://1.windows)家庭版没有组策略管理器
2.打不开windows商店，或无法自动下载组件

## 小结

按上面的步骤完成配置后，建议先做一次完整验证：确认服务能正常启动、端口可访问、关键功能可用，再接入日常使用。遇到路径、端口或域名不一致时，按文中标注替换成自己的实际值。
