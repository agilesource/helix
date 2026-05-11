# /helix-design - 设计生成技能

> AI 驱动的设计生成

## 概述

`/helix-design` 生成 UI/UX 设计和前端代码。

## 命令

```bash
helix design "登录页面"
helix design "仪表盘" --style modern
helix design "移动端首页" --platform mobile
```

## 设计类型

| 类型 | 描述 |
|------|------|
| page | 页面设计 |
| component | 组件设计 |
| layout | 布局设计 |

## 输出

- HTML/CSS 代码
- 设计说明文档
- 响应式适配

## 示例

```bash
# 生成登录页面
helix design "登录页面" --style modern

# 生成移动端设计
helix design "用户资料" --platform mobile
```

## 配置

```yaml
design:
  style: modern
  platform: web
  output: html
```

## 关联技能

- `/helix-build` - 代码生成
- `/helix-browse` - 设计预览
