#!/usr/bin/env python3
"""Skill 平铺兼容层同步：.claude/skills/<name>/SKILL.md（官方） → skills/<name>.md（社区工具平铺兼容）

背景：
- v2 主推 Claude Code 的官方文件夹格式（.claude/skills/<name>/SKILL.md）
- Reasonix / Cline 等社区工具仍用 v1 平铺格式（skills/*.md）作为适配参考，
  setup.sh / setup.ps1 的"兼容层"逻辑会把这层复制给这些工具
- 本脚本保证兼容层与官方格式内容一致，防止双格式漂移

用法：
  python scripts/sync-skills.py          # 写入模式：用官方内容重新生成兼容层
  python scripts/sync-skills.py --check  # 检查模式：有漂移则退出码 1（供 CI 使用）
"""
import sys
from pathlib import Path

if "__file__" in globals():
    ROOT = Path(__file__).resolve().parent.parent
else:
    ROOT = Path.cwd()

OFFICIAL_DIR = ROOT / ".claude" / "skills"
FLAT_DIR = ROOT / "skills"


def main():
    check = "--check" in sys.argv
    if not OFFICIAL_DIR.is_dir():
        print(f"[error] 未找到官方技能目录：{OFFICIAL_DIR}")
        sys.exit(1)
    FLAT_DIR.mkdir(parents=True, exist_ok=True)

    official = sorted(
        d for d in OFFICIAL_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )
    if not official:
        print("[error] 官方技能目录为空")
        sys.exit(1)

    drifted = []
    generated = []
    for d in official:
        name = d.name
        content = (d / "SKILL.md").read_text(encoding="utf-8-sig").strip() + "\n"
        dst = FLAT_DIR / f"{name}.md"
        if check:
            if not dst.exists() or dst.read_text(encoding="utf-8-sig").strip() != content.strip():
                drifted.append(name)
        else:
            dst.write_text(content, encoding="utf-8")
            generated.append(name)
            print(f"[sync] {name} -> {dst.relative_to(ROOT)}")

    if check:
        if drifted:
            print("DRIFT: " + ", ".join(drifted))
            sys.exit(1)
        print(f"OK: {len(official)} 个官方 Skill 与平铺兼容层一致")
        return

    # 删除官方已不存在的孤儿平铺文件
    official_names = {d.name for d in official}
    removed = []
    for f in sorted(FLAT_DIR.glob("*.md")):
        if f.stem not in official_names:
            print(f"[remove] 孤儿平铺文件 {f.name}（官方无对应 Skill）")
            f.unlink()
            removed.append(f.name)

    print(f"完成：生成/更新 {len(generated)} 个平铺文件，移除 {len(removed)} 个孤儿文件")


if __name__ == "__main__":
    main()
