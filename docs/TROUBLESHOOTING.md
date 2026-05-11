# GStack Fusion - Troubleshooting Guide

Common issues and solutions.

---

## Installation Issues

### Issue: Skills Not Available

**Symptom**:
```
Unknown command: /review
```

**Solution**:
```bash
# 1. Check skills directory
ls ~/.claude/skills/

# 2. Re-link skills
ln -sf /path/to/gstack-fusion/skills/* ~/.claude/skills/

# 3. Restart Claude Code
```

### Issue: Python Version Incompatible

**Symptom**:
```
SyntaxError: invalid syntax
```

**Solution**:
```bash
# Check Python version
python --version

# Need Python 3.10+
# Use pyenv to manage versions
pyenv install 3.10.0
pyenv local 3.10.0
```

---

## Runtime Issues

### Issue: Tests Failing

**Symptom**:
```
FAILED tests/test_example.py
```

**Debug Steps**:
```bash
# 1. Run detailed tests
pytest -v --tb=long

# 2. Check coverage
pytest --cov=src --cov-report=term-missing

# 3. Check if regression
git diff HEAD~10 tests/
```

### Issue: Lint Failures

**Symptom**:
```
Lint errors found:
src/main.py:42: F401 unused import
```

**Solution**:
```bash
# 1. Auto-fix
make lint-fix

# 2. Or manually fix and re-run
/review
```

### Issue: Type Check Failures

**Symptom**:
```
error: Missing return type annotation
```

**Solution**:
```bash
# 1. Add type annotation
def process_data(data: dict) -> list:
    ...

# 2. Or use mypy ignore
result = ambiguous_function()  # type: ignore
```

---

## Skill Issues

### Issue: /review Finds No Changes

**Symptom**:
```
Nothing to review — you're on the base branch
```

**Solution**:
```bash
# 1. Ensure on feature branch
git checkout -b feature/my-feature

# 2. Ensure there are changes
git status

# 3. Check base branch
git diff main...HEAD
```

### Issue: /qa Can't Find Application

**Symptom**:
```
No URL provided for testing
```

**Solution**:
```bash
# 1. Provide URL
/qa --url=http://localhost:3000

# 2. Or set in project config
# Create .gstack/config
echo "QA_URL=http://localhost:3000" > .gstack/config
```

### Issue: /ship Gate Fails

**Symptom**:
```
[GATE] Codex review: FAIL
```

**Solution**:
```bash
# 1. View issues found by Codex
# Fix issues marked [P1] or [P2]

# 2. Re-run review
/review

# 3. Try shipping again
/ship
```

---

## Permission Issues

### Issue: Cannot Write Files

**Symptom**:
```
Permission denied: /path/to/file
```

**Solution**:
```bash
# Check file permissions
ls -la /path/to/file

# If owner
chmod 644 /path/to/file

# If need write permission
chmod 755 /path/to/directory
```

### Issue: Git Permission Denied

**Symptom**:
```
Permission denied (publickey)
```

**Solution**:
```bash
# 1. Check SSH key
ssh -T git@github.com

# 2. Or use HTTPS
git remote set-url origin https://github.com/user/repo.git
```

---

## Performance Issues

### Issue: Skills Run Slow

**Symptom**:
```
Skill took 5+ minutes
```

**Optimize**:
```bash
# 1. Use fast mode
/qa --tier=quick
/review --fast

# 2. Reduce test scope
pytest tests/unit/ -v

# 3. Skip lint
/review --no-lint
```

### Issue: Out of Memory

**Symptom**:
```
Out of memory error
```

**Solution**:
```bash
# 1. Increase swap
sudo swapon -s

# 2. Or limit concurrency
export MAX_WORKERS=2
```

---

## Network Issues

### Issue: Cannot Connect to API

**Symptom**:
```
ConnectionError: API not reachable
```

**Solution**:
```bash
# 1. Check network
ping api.openai.com

# 2. Check proxy
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 3. Set proxy
export HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=http://proxy:8080
```

### Issue: Browser Won't Launch

**Symptom**:
```
Browser launch failed
```

**Solution**:
```bash
# 1. Check browser installation
which chromium
which google-chrome

# 2. Install browser (macOS)
brew install chromium

# 3. Set path
export BROWSER_PATH=/usr/bin/chromium
```

---

## Debugging Tips

### 1. Enable Debug Logs

```bash
# Set log level
export GSTACK_DEBUG=1
export LOG_LEVEL=DEBUG

# Run skill
/review
```

### 2. View Detailed Output

```bash
# Use verbose mode
/review -v
/qa --verbose
```

### 3. Isolate Issues

```bash
# Run specific test
pytest tests/test_specific.py -v

# Test specific module
pytest tests/unit/ -v
```

---

## Getting Help

### 1. View Documentation

```bash
# List all docs
ls docs/

# View specific topic
cat docs/QUICKSTART.md
cat docs/TUTORIALS.md
```

### 2. Check Version

```bash
# View GStack version
cat VERSION

# View dependencies
pip list | grep -i gstack
```

### 3. Report Issues

```bash
# Create issue
# 1. Describe the problem
# 2. Provide error logs
# 3. Provide reproduction steps
```

---

## Quick Diagnostic Checklist

```bash
# Run this script to diagnose common issues
#!/bin/bash
echo "=== GStack Fusion Diagnostic ==="
echo ""
echo "Python version: $(python --version)"
echo "Skills directory: $(ls ~/.claude/skills/ | wc -l) skills"
echo "Git status: $(git status --short | wc -l) changes"
echo ""
echo "Testing basic skills..."
/health 2>&1 | head -20
```

---

*If the issue persists, please report it in the project issues.*
