# 域名解析与上线执行手册(身份证到位后照此 10 分钟落地)

> 现状:insightloomapp.com 在腾讯云购物车(¥83/首年);EdgeOne 项目 `insightloom`(ID makers-6niwnjzzqx2j)自动部署正常。
> 阻塞点:信息模板实名需身份证照片。其余全部准备就绪。

## 第 1 步 · 信息模板实名(~3 分钟)

1. 腾讯云控制台 → **域名注册** → 左侧「**信息模板**」→ 新建模板(个人)
2. 填:甘孟哲 / 身份证号 / 上传身份证正反面照片
3. 提交审核(通常几分钟~几小时;模板状态变「已实名」)

## 第 2 步 · 购买域名(~2 分钟)

1. 控制台 → 域名注册 → **我的购物车** → insightloomapp.com(¥83)
2. 域名信息选择刚实名的模板 → 提交订单 → 支付
3. 实名同步到注册局(CNNIC):.com 通常几分钟,最长 1~3 天

## 第 3 步 · DNS 解析(~3 分钟)

在 **DNS 解析 DNSPod**(控制台 → 我的资源 → DNS 解析)添加记录:

| 主机记录 | 记录类型 | 记录值 | 说明 |
|---|---|---|---|
| `www` | CNAME | *(第 4 步 EdgeOne 给出的 CNAME 目标)* | 主站 |
| `@` | CNAME | *(同上,或按 EdgeOne 指示用 A/跳转)* | 裸域 |

> 具体记录值以 EdgeOne「添加自定义域名」弹窗给出的为准,它会同时提示验证方式。

## 第 4 步 · EdgeOne 绑定(~2 分钟)

1. [EdgeOne 控制台](https://console.cloud.tencent.com/edgeone) → 项目 insightloom → **域名管理**
2. 「添加自定义域名」→ 填 `www.insightloomapp.com` → 复制它给出的 **CNAME 目标值** → 回第 3 步填入
3. 等生效(EdgeOne 免费版通常分钟级;证书自动签发)
4. 可选:再加一条裸域 `insightloomapp.com` 或在 DNSPod 配 URL 转发到 www

## 第 5 步 · ICP 备案(个人,1~2 周)

- 入口:腾讯云控制台 → **网站备案**(beian.cloud.tencent.com)
- 需要:身份证正反面、手机号(186****8231)、应急联系人、网站信息(个人博客/工具站,服务内容选"其他"或"信息查询服务")
- EdgeOne 免费版走"网站托管"类型备案,幕布/电子核验按提示自拍
- 备案号下来后:EdgeOne 域名配置里填备案号

> ⚠️ EdgeOne 国内加速节点要求备案;备案期间域名可先解析,但正式公开访问建议等备案完成。

## 第 6 步 · 上线验证清单(5 分钟)

- [ ] `https://www.insightloomapp.com` 打开,地址栏锁标(HTTPS)
- [ ] `http://` 自动跳 `https://`
- [ ] 裸域跳 www(或反之,与 DNS 配置一致)
- [ ] 手机 4G 网络打开一次(不走 Wi-Fi 缓存)
- [ ] 微信/TG 发链接,卡片标题+图正常(OG 生效)
- [ ] 51.la 统计 ID 接入(site/index.html,一行 script)
- [ ] 自测三轮:桌面 Chrome / 手机浏览器 / 隐身模式

## 回退

- 任何一步出问题:EdgeOne 默认域 `insightloom-dl0kzqhb.edgeone.cool` 始终可用(3h 预览令牌机制)
- 域名解析配错:DNSPod 记录可随时改,TTL 默认 600s,10 分钟内生效
