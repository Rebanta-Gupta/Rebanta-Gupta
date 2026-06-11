#!/usr/bin/env python3
"""
generate_readme.py
------------------
Reads projects.yaml and writes README.md.
Toggle any project's `visible: true/false` in the YAML, then run:

    python generate_readme.py
"""

import yaml
from collections import defaultdict

CONFIG_FILE = "projects.yaml"
OUTPUT_FILE = "README.md"

BADGE_MAP = {
    "Rust":       "https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white",
    "JavaScript": "https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E",
    "TypeScript": "https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white",
    "Python":     "https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54",
    "Java":       "https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white",
    "MATLAB":     "https://img.shields.io/badge/MATLAB-0076A8?style=for-the-badge&logo=mathworks&logoColor=white",
    "LaTeX":      "https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white",
    "React":      "https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=000000",
    "Vite":       "https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white",
    "p5.js":      "https://img.shields.io/badge/p5.js-ED225D?style=for-the-badge&logo=p5dotjs&logoColor=white",
    "Matter.js":  "https://img.shields.io/badge/Matter.js-4B5563?style=for-the-badge&logo=javascript&logoColor=white",
    "Streamlit":  "https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white",
    "SciPy":      "https://img.shields.io/badge/SciPy-0C55A5?style=for-the-badge&logo=scipy&logoColor=white",
    "Pandas":     "https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white",
    "NumPy":      "https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white",
    "Matplotlib": "https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white",
    "COMSOL":     "https://img.shields.io/badge/COMSOL-005CA9?style=for-the-badge&logoColor=white",
    "Git":        "https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white",
    "p5.play":    "https://img.shields.io/badge/p5.play-2C2C2C?style=for-the-badge&logo=github&logoColor=white",
}

def badge(tech):
    url = BADGE_MAP.get(tech)
    if url:
        return f"![{tech}]({url})"
    return f"`{tech}`"


def build_readme(config):
    p = config["profile"]
    icons = config.get("category_icons", {})
    stats = config.get("stats", {})

    lines = []

    # ── Header ──────────────────────────────────────────────
    lines.append(f"# Hi there, I'm {p['name']}! 👋\n")
    lines.append(p["bio"].strip() + "\n")

    # ── Contact ─────────────────────────────────────────────
    lines.append("")
    lines.append(f"- 📫 Email: **{p['email']}**")
    lines.append(f"- 💼 LinkedIn: {p['linkedin']}")
    lines.append(f"- 🌐 Portfolio: {p['portfolio']}")
    if p.get("resume_public"):
        lines.append("- 📄 Resume: *(available on request)*")
    lines.append("\n---\n")

    # ── Featured Projects ────────────────────────────────────
    visible = [proj for proj in config["projects"] if proj.get("visible")]

    if visible:
        lines.append("## 🚀 Featured Projects\n")

        # Group by category
        by_cat = defaultdict(list)
        for proj in visible:
            by_cat[proj["category"]].append(proj)

        for cat, projs in by_cat.items():
            icon = icons.get(cat, "📁")
            lines.append(f"### {icon} {cat}\n")
            for proj in projs:
                tech_badges = " ".join(badge(t) for t in proj.get("tech", []))
                lines.append(f"- **[{proj['name']}]({proj['url']})**: {proj['description']}")
                if tech_badges:
                    lines.append(f"  {tech_badges}")
                lines.append("")

        lines.append("---\n")

    # ── Tech Stack ───────────────────────────────────────────
    # Collect all unique tech from visible projects
    all_tech = []
    seen = set()
    for proj in visible:
        for t in proj.get("tech", []):
            if t not in seen:
                seen.add(t)
                all_tech.append(t)

    if all_tech:
        lines.append("## 🛠️ Languages & Technologies\n")
        lines.append(" ".join(badge(t) for t in all_tech))
        lines.append("\n---\n")

    # ── GitHub Stats ─────────────────────────────────────────
    if stats.get("visible"):
        username = stats["username"]
        theme = stats.get("theme", "github_dark")
        base = f"https://github-profile-summary-cards.vercel.app/api/cards"
        lines.append("## 📊 GitHub Stats\n")
        lines.append(f"![Profile Details]({base}/profile-details?username={username}&theme={theme})")
        lines.append(f"![Repos per Language]({base}/repos-per-language?username={username}&theme={theme})")
        lines.append(f"![Most Commit Language]({base}/most-commit-language?username={username}&theme={theme})")
        lines.append("\n---\n")

    # ── Footer ───────────────────────────────────────────────
    lines.append("[![Visit Count](https://visitcount.itsvg.in/api?id=Rebanta-Gupta&icon=0&color=12)](https://visitcount.itsvg.in)")

    return "\n".join(lines)


def main():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    readme = build_readme(config)

    with open(OUTPUT_FILE, "w") as f:
        f.write(readme)

    visible_count = sum(1 for p in config["projects"] if p.get("visible"))
    total_count = len(config["projects"])
    print(f"✅ README.md generated — {visible_count}/{total_count} projects visible.")


if __name__ == "__main__":
    main()
