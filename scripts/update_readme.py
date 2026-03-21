import yaml
from pathlib import Path


MEETING_ROOT = Path("group-meetings") 
README_PATH = Path("README.md")      
TABLE_START = "<!-- MEETING_TABLE_START -->"
TABLE_END = "<!-- MEETING_TABLE_END -->"


def generate_meeting_table():
    """遍历组会文件夹，生成Markdown表格"""
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

        rows.append(
            f"| {date} | {topic} | {speaker} | {slides_link} | {paper_str} | {notes_link} |"
        )

    table = "\n".join([
        "| 📅 会议日期 | 📌 主题 | 👤 主讲人 | 📊 PPT | 📄 相关论文 | 📝 会议纪要 |",
        "|--------|------|--------|-----|---------|----------|",
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
        new_content = content.split(TABLE_START)[0] + \
                      TABLE_START + "\n" + generate_meeting_table() + "\n" + \
                      TABLE_END + \
                      content.split(TABLE_END)[1]
    else:
        new_content = content + f"\n\n{TABLE_START}\n{TABLE_END}"

    README_PATH.write_text(new_content, encoding="utf-8")
    print("README表格更新完成！")

if __name__ == "__main__":
    update_readme()