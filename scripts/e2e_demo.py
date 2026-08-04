"""端到端模拟:env-detect + env-setup + dev-loop 在测试项目上的真实执行(演示用,不修改真实项目)。"""
import json, os, shutil, subprocess, tempfile, datetime

def run(cmd, cwd=None, timeout=600):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=True)
        return (r.returncode, (r.stdout or '')[:300] + (r.stderr or '')[:300])
    except Exception as e:
        return (-1, str(e))

work = tempfile.mkdtemp(prefix='agentenv-demo-')
print('test dir:', work)

# 1. project-scaffold:生成 argparse CLI 骨架
proj = os.path.join(work, 'demo-app')
os.makedirs(os.path.join(proj, 'src', 'demo'))
os.makedirs(os.path.join(proj, 'tests'))
open(os.path.join(proj, 'pyproject.toml'), 'w', encoding='utf-8').write(
    '[project]\nname = "demo"\nversion = "0.1.0"\nrequires-python = ">=3.10"\ndependencies = []\n\n'
    '[project.scripts]\ndemo = "demo.main:main"\n\n'
    '[dependency-groups]\ndev = ["pytest", "ruff"]\n\n'
    '[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n\n'
    '[tool.hatch.build.targets.wheel]\npackages = ["src/demo"]\n'
    '[tool.ruff]\nline-length = 100\n')
open(os.path.join(proj, 'src', 'demo', '__init__.py'), 'w').write('')
open(os.path.join(proj, 'src', 'demo', 'main.py'), 'w', encoding='utf-8').write(
    'import argparse\n\ndef build_parser() -> argparse.ArgumentParser:\n    p = argparse.ArgumentParser(prog="demo", description="A tiny CLI.")\n    p.add_argument("--name", default="world", help="who to greet")\n    return p\n\ndef main() -> None:\n    args = build_parser().parse_args()\n    print(f"Hello, {args.name}!")\n\nif __name__ == "__main__":\n    main()\n')
open(os.path.join(proj, 'tests', 'test_main.py'), 'w', encoding='utf-8').write(
    'from demo.main import build_parser\n\ndef test_parser_default():\n    args = build_parser().parse_args([])\n    assert args.name == "world"\n\ndef test_parser_name():\n    args = build_parser().parse_args(["--name", "Bob"])\n    assert args.name == "Bob"\n')
open(os.path.join(proj, '.env.example'), 'w').write('API_KEY=\n')
open(os.path.join(proj, '.gitignore'), 'w').write('.venv/\n__pycache__/\n.env\n')
print('[scaffold] argparse CLI 骨架生成')

# 2. env-detect:探测
code, out = run('py --version', cwd=proj)
print('[detect] python:', out.strip())
code, out = run('uv --version', cwd=proj)
print('[detect] uv:', out.strip())
env = {
    "detected_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "project_type": "cli",
    "stack": {"language": ["python"], "framework": [], "package_manager": "uv", "lockfile": None},
    "runtimes": {"required": ["python", "uv", "git"], "installed": {}, "missing": []},
    "commands": {"install": "uv sync --locked", "run": "uv run demo", "test": "uv run pytest -q", "lint": "uv run ruff check ."},
    "dotenv_example": True, "has_agents_md": False, "notes": ["演示项目"]
}
json.dump(env, open(os.path.join(proj, '.agentenv.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('[detect] .agentenv.json 生成,project_type=cli')

# 3. env-setup:依赖安装(锁文件优先)+ 冒烟
install_cmd = 'uv sync --locked' if os.path.exists(os.path.join(proj, 'uv.lock')) else 'uv sync'
code, out = run(install_cmd, cwd=proj, timeout=600)
print('[setup]', install_cmd, '->', code, out.strip()[:120])

# 4. dev-loop:验证序列,失败自动修复
code, out = run('uv run pytest -q', cwd=proj, timeout=180)
print('[dev-loop] test ->', code, out.strip()[:120])
code, out = run('uv run ruff check .', cwd=proj, timeout=120)
print('[dev-loop] lint ->', code, out.strip()[:160])
code, out = run('uv run ruff check . --fix', cwd=proj, timeout=120)
print('[dev-loop] lint 自动修复(ruff --fix) ->', code)
code, out = run('uv run ruff check .', cwd=proj, timeout=120)
print('[dev-loop] lint 复查 ->', code, '(0=通过)')
code, out = run('uv run ruff format .', cwd=proj, timeout=120)
print('[dev-loop] format(ruff format) ->', code)
code, out = run('uv run demo --name Bob', cwd=proj, timeout=120)
print('[dev-loop] 冒烟 run ->', code, out.strip()[:80])
print('[setup] lockfile:', os.path.exists(os.path.join(proj, 'uv.lock')))

shutil.rmtree(work, ignore_errors=True)
print('cleaned up.')
