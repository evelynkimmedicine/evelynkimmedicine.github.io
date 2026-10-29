"""Build the blog from editable Markdown posts; no server is required."""
from pathlib import Path
from datetime import date, datetime
from collections import Counter
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
CONFIG = json.loads((ROOT / "site.json").read_text())
ORIGIN = CONFIG["url"].rstrip("/")
CATEGORIES = {"Publication", "Presentation", "Neuroscience", "Clinical Blog", "Photography"}


def escape(value):
    return html.escape(str(value), quote=True)


def safe_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def load_posts():
    posts = []
    used_ids = set()
    for path in sorted((ROOT / "content/posts").glob("*.md")):
        source = path.read_text()
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", source, re.S)
        if not match:
            raise ValueError(f"{path.name}: missing YAML header between --- lines")
        post = yaml.safe_load(match[1])
        for key in ("date", "title", "category", "image", "excerpt"):
            if not post.get(key):
                raise ValueError(f"{path.name}: missing {key}")
        if post["category"] not in CATEGORIES:
            raise ValueError(f"{path.name}: unknown category {post['category']}")
        if post.get("draft", False):
            continue
        published = date.fromisoformat(str(post["date"])[:10])
        post["date"] = published.isoformat()
        post["year"] = str(published.year)
        post["displayDate"] = f"{published:%B} {published.day}, {published.year}"
        post.setdefault("id", path.stem)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", post["id"]):
            raise ValueError(f"{path.name}: id must use lowercase letters, numbers, and hyphens")
        if post["id"] in used_ids:
            raise ValueError(f"Duplicate post id: {post['id']}")
        used_ids.add(post["id"])
        if not post["image"].startswith("/") or not (ROOT / post["image"].lstrip("/")).is_file():
            raise ValueError(f"{path.name}: image must point to an uploaded photo in /photos/")
        post.setdefault("categoryKo", post["category"])
        post.setdefault("subtitle", "")
        post.setdefault("sourceUrl", f"/posts/{post['id']}.html")
        post.setdefault("sourceLabel", "Post permalink")
        post.setdefault("tags", [])
        post.setdefault("likes", 0)
        post.setdefault("comments", [])
        post.setdefault("readTime", f"{max(1, len(match[2].split()) // 200)} min read")
        post["fullHtml"] = markdown.markdown(match[2], extensions=["extra", "sane_lists"])
        posts.append(post)
    if not posts:
        raise ValueError("At least one published post is required")
    return sorted(posts, key=lambda post: (post["date"], post["id"]))


def metadata(title, description, url, image, schema, kind="website"):
    values = {
        "description": description, "author": CONFIG["author"],
        "robots": "index, follow, max-image-preview:large",
        "twitter:card": "summary_large_image", "twitter:title": title,
        "twitter:description": description, "twitter:image": ORIGIN + image,
    }
    lines = [f'<meta name="{name}" content="{escape(value)}">' for name, value in values.items()]
    for name, value in {"type": kind, "title": title, "description": description, "url": url,
                        "site_name": CONFIG["author"], "image": ORIGIN + image}.items():
        lines.append(f'<meta property="og:{name}" content="{escape(value)}">')
    lines.extend([f'<link rel="canonical" href="{escape(url)}">',
                  '<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">',
                  f'<script type="application/ld+json">{safe_json(schema)}</script>'])
    return "\n".join(lines)


def head_for(base_head, title, description, url, image, schema, kind="website"):
    head = re.sub(r"<title>.*?</title>", f"<title>{escape(title)}</title>", base_head)
    extra_css = """<style>.post-prose ul{list-style:disc;padding-left:1.5rem;margin:1rem 0}.post-prose ol{list-style:decimal;padding-left:1.5rem;margin:1rem 0}.post-prose li{margin:.4rem 0}.post-prose h2{font-size:1.5rem;font-weight:700;margin:1.8rem 0 .8rem}.post-prose h3{font-size:1.2rem;font-weight:700;margin:1.5rem 0 .7rem}.post-prose a{color:#029e47;text-decoration:underline}.post-prose img{max-width:100%;height:auto;border-radius:.75rem}.post-prose pre{overflow:auto;padding:1rem;background:#f1f5f9;border-radius:.75rem}.post-prose table{display:block;overflow:auto;border-collapse:collapse;max-width:100%}.post-prose th,.post-prose td{border:1px solid #e2e8f0;padding:.5rem}</style>"""
    return head + extra_css + metadata(title, description, url, image, schema, kind)


def post_page(post, base_head):
    title = f"{post['title']} | {CONFIG['author']}"
    url = f"{ORIGIN}/posts/{post['id']}.html"
    schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"],
              "description": post["excerpt"], "datePublished": post["date"], "mainEntityOfPage": url,
              "author": {"@type": "Person", "name": CONFIG["author"], "url": ORIGIN + "/"},
              "image": ORIGIN + post["image"]}
    head = head_for(base_head, title, post["excerpt"], url, post["image"], schema, "article")
    tags = "".join(f'<span class="text-xs rounded-full bg-emerald-50 text-emerald-800 px-3 py-1">#{escape(tag)}</span>' for tag in post["tags"])
    return f'''<!DOCTYPE html><html lang="en"><head>{head}</head><body>
<header class="bg-white border-b border-slate-200"><div class="max-w-4xl mx-auto px-5 py-5"><a href="/" class="font-bold text-emerald-700">← {escape(CONFIG['author'])} · med.evelyn.log</a></div></header>
<main class="max-w-4xl mx-auto p-4 sm:p-8"><article class="bg-white border border-slate-200 rounded-2xl overflow-hidden">
<div class="p-6 sm:p-10"><p class="text-sm text-emerald-700 font-semibold">{escape(post['categoryKo'])}</p><h1 class="text-2xl sm:text-4xl font-bold text-slate-900 mt-3 leading-tight">{escape(post['title'])}</h1>
<p class="mt-4 text-slate-600">{escape(post['subtitle'])}</p><p class="mt-3 text-sm text-slate-500">{escape(CONFIG['author'])} · <time datetime="{post['date']}">{post['displayDate']}</time> · {escape(post['readTime'])}</p></div>
<img src="{escape(post['image'])}" alt="{escape(post.get('imageAlt', post['title']))}" class="w-full h-64 sm:h-80 object-cover">
<div class="p-6 sm:p-10 post-prose">{post['fullHtml']}<div class="flex flex-wrap gap-2 py-5">{tags}</div><a href="{escape(post['sourceUrl'])}" class="text-emerald-700 font-semibold underline">{escape(post['sourceLabel'])} ↗</a></div>
</article><nav class="py-8"><a href="/" class="font-semibold text-emerald-700">← All posts and biography</a></nav></main></body></html>'''


def build():
    posts = load_posts()
    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    (OUT / "posts").mkdir(parents=True)
    for folder in ("assets", "photos"):
        shutil.copytree(ROOT / folder, OUT / folder, ignore=shutil.ignore_patterns(".*"))
    home = (ROOT / "templates/home.html").read_text()
    base_head = re.search(r"<head>(.*?)</head>", home, re.S)[1]
    schema = {"@context": "https://schema.org", "@type": "ProfilePage", "url": ORIGIN + "/",
              "name": CONFIG["author"], "mainEntity": {"@type": "Person", "name": CONFIG["author"],
              "alternateName": CONFIG["author_korean"], "url": ORIGIN + "/"}}
    head = head_for(base_head, CONFIG["title"], CONFIG["description"], ORIGIN + "/", CONFIG["image"], schema)
    home = home.replace(base_head, head, 1)
    home = home.replace("/* BLOG_DATA */", safe_json(posts))
    home = home.replace("<!-- BIOGRAPHY -->", (ROOT / "content/biography.html").read_text())
    directory = []
    feed = []
    for index, post in enumerate(posts, 1):
        href = f"/posts/{post['id']}.html"
        directory.append(f'<div class="px-5 py-2.5 flex items-center justify-between gap-3 text-xs"><a href="{href}" class="text-slate-800 hover:text-emerald-700">#{index:02} · {escape(post["title"])}</a><time class="text-slate-400 shrink-0" datetime="{post["date"]}">{post["date"]}</time></div>')
        feed.append(f'<article class="bg-white rounded-2xl border border-slate-200 p-6 naver-shadow"><p class="text-xs text-emerald-700">{escape(post["categoryKo"])} · {post["displayDate"]}</p><h2 class="mt-3 text-xl font-bold"><a href="{href}">{escape(post["title"])}</a></h2><img class="mt-4 w-full h-44 object-cover rounded-xl" src="{escape(post["image"])}" alt="{escape(post["title"])}"><p class="mt-4 text-slate-600">{escape(post["excerpt"])}</p><a class="inline-block mt-4 font-semibold text-emerald-700" href="{href}">Read post →</a></article>')
        (OUT / "posts" / f"{post['id']}.html").write_text(post_page(post, base_head))
    home = home.replace("<!-- POST_DIRECTORY -->", "\n".join(directory)).replace("<!-- POST_FEED -->", "\n".join(feed))
    years = Counter(post["year"] for post in posts)
    year_buttons = "".join(f'<button type="button" data-year="{year}" class="year-btn px-2.5 py-1.5 rounded-lg text-xs font-medium bg-slate-50 text-slate-700 border border-slate-200">{year} ({count})</button>' for year, count in sorted(years.items()))
    home = home.replace("<!-- YEAR_FILTERS -->", year_buttons)
    counts = Counter(post["category"] for post in posts)
    tokens = {"TOTAL": len(posts), "RESEARCH": counts["Publication"] + counts["Presentation"],
              "PUBLICATION": counts["Publication"], "PRESENTATION": counts["Presentation"],
              "NEURO": counts["Neuroscience"], "CLINICAL": counts["Clinical Blog"], "PHOTO": counts["Photography"],
              "ARCHIVE_SPAN": f"{posts[0]['year']}–{posts[-1]['year']}"}
    for name, value in tokens.items():
        home = home.replace(f"@@{name}@@", str(value))
    for category, count in {"all": len(posts), **counts}.items():
        pattern = r'(<button\b[^>]*data-cat="' + re.escape(category) + r'"[^>]*>)(.*?)(</button>)'
        def replace_count(match):
            middle = re.sub(r"(<span\b[^>]*>)\d+(</span>)", lambda m: m[1] + str(count) + m[2], match[2])
            return match[1] + middle + match[3]
        home = re.sub(pattern, replace_count, home, flags=re.S)
    home = home.replace("</body>", '<noscript><p style="padding:1rem;text-align:center">Use the post title links to read articles. JavaScript enables filters and reader controls.</p></noscript></body>')
    if "@@" in home or "/* BLOG_DATA */" in home:
        raise ValueError("Unresolved template placeholder")
    (OUT / "index.html").write_text(home)
    (OUT / "home.html").write_text(home)
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    sitemap = ET.Element(ns + "urlset")
    for url in [ORIGIN + "/"] + [f"{ORIGIN}/posts/{post['id']}.html" for post in posts]:
        item = ET.SubElement(sitemap, ns + "url")
        ET.SubElement(item, ns + "loc").text = url
    ET.ElementTree(sitemap).write(OUT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (OUT / ".nojekyll").touch()
    print(f"Built {len(posts)} posts and homepage for {ORIGIN}")


if __name__ == "__main__":
    build()
