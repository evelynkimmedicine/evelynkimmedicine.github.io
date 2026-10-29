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
