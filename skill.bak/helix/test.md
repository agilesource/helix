# /helix-test - 测试生成技能

> 智能测试用例生成

## 概述

`/helix-test` 基于代码和规格生成测试用例。

## 命令

```bash
helix test
helix test --type unit      # 单元测试
helix test --type integration  # 集成测试
helix test --coverage       # 带覆盖率
```

## 测试类型

| 类型 | 描述 |
|------|------|
| unit | 单元测试 |
| integration | 集成测试 |
| e2e | 端到端测试 |

## 输出

生成测试文件：

- `test_<module>.py`
- 覆盖率报告

## 示例

```bash
# 生成单元测试
helix test --type unit

# 生成带覆盖率的测试
helix test --coverage --threshold 80
```

## 配置

```yaml
test:
  type: unit
  framework: pytest
  coverage_threshold: 80
```

## 关联技能

- `/helix-verify` - 运行测试
