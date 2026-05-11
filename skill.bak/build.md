# /helix-build - 代码生成技能

> 基于规格说明生成代码骨架

## 概述

`/helix-build` 读取 SPEC.md 文件并生成代码骨架。

## 命令

```bash
helix build SPEC.md
helix build SPEC.md -o ./output
helix build --framework fastapi  # 指定框架
```

## 输入

- SPEC.md 文件路径
- 可选的输出目录

## 输出

生成代码文件：

- 主应用文件
- 数据模型
- API 路由
- 测试文件模板

## 支持框架

| 框架 | 命令 |
|------|------|
| FastAPI | `--framework fastapi` |
| Flask | `--framework flask` |
| Django | `--framework django` |

## 示例

```bash
# 生成 FastAPI 项目
helix build SPEC.md --framework fastapi -o ./my-api

# 生成 Flask 项目
helix build SPEC.md --framework flask -o ./my-app
```

## 配置

```yaml
build:
  framework: fastapi
  output_dir: ./src
  include_tests: true
  include_docs: true
```

## 关联技能

- `/helix-spec` - 生成规格说明
- `/helix-verify` - 验证生成代码
