import re
from pathlib import Path
from urllib.parse import unquote

import yaml


MEETING_ROOT = Path("group-meetings")
README_PATH = Path("README.md")
TABLE_START = "<!-- MEETING_TABLE_START -->"
TABLE_END = "<!-- MEETING_TABLE_END -->"

_SLIDES_OR_NOTES = re.compile(
    r"group-meetings/([^)]+?)/(?:slides\.pdf|notes\.md)", re.IGNORECASE
)


def _is_table_separator_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "---" in s


def _extract_folder_from_row(line: str) -> str | None:
    m = _SLIDES_OR_NOTES.search(line)
    return unquote(m.group(1)) if m else None


def parse_preserved_other_materials(readme_content: str) -> tuple[dict[str, str], dict[str, str]]:
    """从当前 README 表格解析「其他资料」：按文件夹名、或按 日期|主题 索引。"""
    by_folder: dict[str, str] = {}
    by_date_topic: dict[str, str] = {}
    if TABLE_START not in readme_content or TABLE_END not in readme_content:
        return by_folder, by_date_topic

    section = readme_content.split(TABLE_START, 1)[1].split(TABLE_END, 1)[0]
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or _is_table_separator_row(line):
            continue
        if "📅 会议日期" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        inner = parts[1:-1]
        if len(inner) < 7:
            continue
        other = inner[6]
        folder = _extract_folder_from_row(line)
        if folder:
            by_folder[folder] = other
        else:
            by_date_topic[f"{inner[0]}|{inner[1]}"] = other
    return by_folder, by_date_topic


def _other_cell(
    by_folder: dict[str, str],
    by_date_topic: dict[str, str],
    folder_name: str,
    date: str,
    topic: str,
) -> str:
    if folder_name in by_folder:
        return by_folder[folder_name]
    return by_date_topic.get(f"{date}|{topic}", "")


def generate_meeting_table(
    by_folder: dict[str, str] | None = None,
    by_date_topic: dict[str, str] | None = None,
):
    """遍历组会文件夹，生成Markdown表格"""
    by_folder = by_folder or {}
    by_date_topic = by_date_topic or {}
    rows = []

    for folder in sorted(MEETING_ROOT.iterdir(), key=lambda x: x.name, reverse=True):
        if not folder.is_dir():
            continue

        meta_file = folder / "meta.yml"
        if not meta_file.exists():
            continue

        try:
            meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        except Exception:
            continue

        date = meta.get("date", "-")  
        topic = meta.get("topic", "-")
        speaker = meta.get("speaker", "-")

    
        paper_links = []
        papers = meta.get("papers", [])
        if isinstance(papers, dict):
            papers = [papers]

        for paper in papers:
            title = paper.get("title", "论文")
            url = paper.get("url")
            file = paper.get("file") 

            if url:
                paper_links.append(f"[{title}]({url})")
            elif file:
                paper_path = folder / file
                if paper_path.exists():
                    paper_links.append(f"[{title}]({paper_path})")

        paper_str = "<br>".join(paper_links) if paper_links else "-"

        slides_path = str(folder / "slides.pdf").replace(" ", "%20")
        slides_link = f"[Slides]({slides_path})" if (folder / "slides.pdf").exists() else "-"

        notes_path = str(folder / "notes.md").replace(" ", "%20")
        notes_link = f"[Notes]({notes_path})" if (folder / "notes.md").exists() else "-"

        other = _other_cell(by_folder, by_date_topic, folder.name, date, topic)
        rows.append(
            f"| {date} | {topic} | {speaker} | {slides_link} | {paper_str} | {notes_link} | {other} |"
        )

    table = "\n".join([
        "| 📅 会议日期 | 📌 主题 | 👤 主讲人 | 📊 PPT | 📄 相关论文 | 📝 会议纪要 | 其他资料 |",
        "|--------|------|--------|-----|---------|----------|----------|",
        *rows
    ])
    return table

def update_readme():
    """将生成的表格写入README.md"""
    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = f"# 实验室组会记录\n\n{TABLE_START}\n{TABLE_END}"

    if TABLE_START in content and TABLE_END in content:
        bf, bdt = parse_preserved_other_materials(content)
        new_content = content.split(TABLE_START)[0] + \
                      TABLE_START + "\n" + generate_meeting_table(bf, bdt) + "\n" + \
                      TABLE_END + \
                      content.split(TABLE_END)[1]
    else:
        new_content = content + f"\n\n{TABLE_START}\n{TABLE_END}"

    README_PATH.write_text(new_content, encoding="utf-8")
    print("README表格更新完成！")

if __name__ == "__main__":
    update_readme()