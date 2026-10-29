# Evelyn Nayoung Kim's website

Intended GitHub Pages address: https://evelynkimmedicine.github.io/

This repository preserves the supplied Naver-style blog design and separates the posts and photos from the layout. GitHub Actions builds the site whenever a change is committed to `main`.

## Add a new post in your browser

1. Open `content/posts` on GitHub.
2. Choose **Add file → Create new file**.
3. Name it `YYYY-MM-DD-short-title.md`, such as `2026-10-29-a-new-beginning.md`.
4. Copy the contents of `POST_TEMPLATE.md` into the editor.
5. Change the date, title, category, photo path, short excerpt, and tags. Set `draft: false` when ready to publish, or remove the `draft` line.
6. Write the post below the second `---` line. Choose **Commit changes** and save to `main`.

The homepage, filters, archive counts, article page, and sitemap update automatically after the **Publish website** workflow completes. Draft posts are omitted from the published site, but their source files are visible in this public repository. Keep unpublished private material outside the repository.

Categories must be exactly one of: `Publication`, `Presentation`, `Neuroscience`, `Clinical Blog`, or `Photography`.

## Add a photo

Open `photos` and choose **Add file → Upload files**. Give the image a simple filename such as `research-lab.jpg`. In the post header, write:

```yaml
image: /photos/research-lab.jpg
```

To add more photos inside the article:

```markdown
![A short description of the photo](/photos/research-lab.jpg)
```

Uploading a photo stores it; adding its path to a post displays it on the website.

## Edit an existing post

Open its file in `content/posts`, click the pencil, edit, and commit the change. Keep the `id` field in existing posts unchanged so their published links continue working. A new post does not need an `id`; its filename becomes its ID.

## Edit the biography or design

- `content/biography.html`: the CV and biography panel, with its current formatting.
- `site.json`: the site address, search description, title, and sharing image.
- `templates/home.html`: the homepage layout, sidebar profile, navigation, and interactive controls.
- `photos`: the image files. `evelyn-portrait.jpg` is the profile photo and `blog-header.jpg` is the banner.

## First-time publishing

The repository name must be `evelynkimmedicine.github.io`. In **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. Run **Actions → Publish website → Run workflow** if the initial commit has already finished before Pages was enabled. The repository must be public to use GitHub Pages on GitHub Free.

The intended address becomes live only after GitHub reports a successful Pages deployment. Search indexing is separate from publishing; verify the new URL in Search Console and submit `https://evelynkimmedicine.github.io/sitemap.xml`.

## Local build

Python 3.10 or newer is required.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 -m http.server --directory dist 8000
```

The generated `dist` directory is ignored by Git. GitHub Actions regenerates it from the editable content.

## Existing interactive controls

The original comment, like, and neighbor buttons use temporary browser memory. They do not provide shared saved comments, actual visitor analytics, or Naver account integration. The supplied sample counters and existing comments are preserved from the original HTML.
