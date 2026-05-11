# /helix-browse - 浏览器控制技能

> 自动化浏览器操作

## 概述

`/helix-browse` 使用 Playwright/Selenium 进行浏览器自动化。

## 命令

```bash
helix browse "https://example.com"
helix browse "https://example.com" --action click --selector "#btn"
helix browse --screenshot  # 截图
```

## 支持引擎

| 引擎 | 优先级 |
|------|--------|
| Playwright | 1 (优先) |
| Selenium | 2 (备用) |

## 操作

| 操作 | 描述 |
|------|------|
| click | 点击元素 |
| type | 输入文本 |
| screenshot | 截图 |
| wait | 等待加载 |
| evaluate | 执行 JS |

## 示例

```bash
# 打开页面
helix browse "https://example.com"

# 点击按钮
helix browse "https://example.com" --action click --selector ".login"

# 截图
helix browse "https://example.com" --screenshot
```

## 配置

```yaml
browse:
  engine: playwright
  headless: true
  timeout: 30000
```

## 关联技能

- `/helix-test` - UI 测试
- `/helix-verify` - 验证
