#!/usr/bin/env python3
"""
Novel Writer - Automated EPUB Exporter
Exports markdown chapter(s) to beautiful EPUB format.
Supports single chapter or batch export, targeting Desktop project directory.
"""

import sys
import os
import re
import argparse
from pathlib import Path

def get_desktop_dir(novel_name: str) -> Path:
    desktop = Path.home() / "Desktop"
    # Match existing directories on Desktop (case/space-insensitive)
    norm_target = re.sub(r'[\s\-_]', '', novel_name).lower()
    for entry in desktop.iterdir():
        if entry.is_dir():
            norm_entry = re.sub(r'[\s\-_]', '', entry.name).lower()
            if norm_entry == norm_target:
                return entry
    # Default to desktop/novel_name
    target_dir = desktop / novel_name
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

def export_chapter_epub(md_file: Path, output_file: Path, title: str = None, author: str = "Author", lang: str = "zh"):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title from first line if not provided
    first_line = content.strip().split("\n")[0] if content.strip() else "Chapter"
    clean_title = title or re.sub(r"^#+\s*", "", first_line).strip() or md_file.stem

    try:
        from ebooklib import epub
        import markdown

        html_body = markdown.markdown(content, extensions=["extra"])
        book = epub.EpubBook()
        book.set_identifier(f"novel-{md_file.stem}")
        book.set_title(clean_title)
        book.set_language(lang)
        book.add_author(author)

        css_style = (
            "body { font-family: Georgia, 'Songti SC', serif; line-height: 1.8; margin: 1.8em; color: #1c1c20; }\n"
            "h1, h2 { font-weight: bold; margin-bottom: 0.6em; color: #111; }\n"
            "p { margin-bottom: 0.9em; text-indent: 0; }\n"
            "em { font-style: italic; }\n"
            "hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }\n"
            "blockquote { border-left: 3px solid #888; margin: 1.2em 0; padding-left: 1em; color: #555; }\n"
        )
        style_item = epub.EpubItem(
            uid="style_nav",
            file_name="style/default.css",
            media_type="text/css",
            content=css_style.encode("utf-8")
        )
        book.add_item(style_item)

        ch_item = epub.EpubHtml(title=clean_title, file_name="chapter.xhtml", lang=lang)
        ch_item.content = f"<html><body>{html_body}</body></html>".encode("utf-8")
        ch_item.add_item(style_item)
        book.add_item(ch_item)

        book.toc = [epub.Link("chapter.xhtml", clean_title, "chapter")]
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ["nav", ch_item]

        output_file.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(str(output_file), book, {})
        print(f"✅ EPUB 导出成功: {output_file}")
        return True

    except Exception as e:
        # Fallback to pandoc
        import subprocess
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["pandoc", str(md_file), "-o", str(output_file), "--metadata", f"title={clean_title}"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ Pandoc 导出成功: {output_file}")
            return True
        else:
            print(f"❌ 导出失败: {res.stderr}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Novel Writer EPUB Exporter")
    parser.add_argument("target", help="Chapter markdown file or project directory")
    parser.add_argument("--desktop", action="store_true", help="Output directly to ~/Desktop/{NovelName}/")
    parser.add_argument("--name", help="Novel name for desktop folder matching", default="")
    parser.add_argument("--lang", help="Language (zh or en)", default="zh")
    parser.add_argument("--output", help="Explicit output file path")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"❌ 目标路径不存在: {target_path}")
        sys.exit(1)

    novel_name = args.name or target_path.parent.name if target_path.is_file() else target_path.name
    out_dir = get_desktop_dir(novel_name) if args.desktop else (target_path.parent if target_path.is_file() else target_path)

    if target_path.is_file() and target_path.suffix == ".md":
        dest_file = Path(args.output) if args.output else (out_dir / f"{target_path.stem}.epub")
        export_chapter_epub(target_path, dest_file, lang=args.lang)
    elif target_path.is_dir():
        # Export all chapter-*.md
        chapters = sorted(target_path.glob("chapter-[0-9]*.md"))
        if not chapters:
            print(f"⚠️ 在 {target_path} 下未找到 chapter-*.md 文件")
            return
        for ch in chapters:
            dest_file = out_dir / f"{ch.stem}.epub"
            export_chapter_epub(ch, dest_file, lang=args.lang)

if __name__ == "__main__":
    main()
