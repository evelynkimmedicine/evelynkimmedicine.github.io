# Evelyn Kim — personal website

Live website: https://evelynkimmedicine.github.io/

## Edit a post

Open a Markdown file in `content/posts`, click the pencil, edit, and commit to `main`. The website publishes automatically through GitHub Actions.

## Add a post

Copy `POST_TEMPLATE.md` into `content/posts/YYYY-MM-DD-title.md`. Change the title, date, category, image, excerpt, and tags. Remove `draft: true` or set `draft: false` to publish. Keep existing post IDs unchanged.

Categories: Publication, Presentation, Neuroscience, Clinical Blog, MCAT.

The homepage displays newest posts first. Numbers follow chronological publication order: the oldest is #01. Category and search filters retain those numbers.

## Add photos

Upload images to `photos`. Use `image: /photos/your-photo.jpg` in the post header or `![Description](/photos/your-photo.jpg)` inside a post.

## Edit MCAT, biography, or layout

- `content/mcat.md`: MCAT page content.
- `content/biography.html`: biography and CV panel.
- `templates/home.html`: homepage profile, banner, and navigation.
- `assets/blog.js`: search, filters, layouts, and article reader.
- `site.json`: title, description, and site address.

The website has no comments, reactions, visitor counters, or social neighbor features. External content links are restricted to existing DOI and project links. Photography has been removed from the published archive.

## Build

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build.py
```

GitHub Pages uses the GitHub Actions source and publishes `dist`. The root `index.html` is a fallback copy of the website, not the editing source. The build generates the root homepage, the article pages, MCAT, and sitemap.

## MCAT study log

The MCAT tab and `/mcat.html` use `templates/mcat.html`, `assets/mcat.css`, `assets/mcat-core.js`, and `assets/mcat.js`. Sessions are stored in a password-protected D1 backend on the existing Sites hosting. The runtime password is configured as a secret there; never add it to this public repository. Weeks start Monday; daily averages count elapsed calendar days, including zero-study days, in America/New_York. The exam countdown targets March 19, 2027.
