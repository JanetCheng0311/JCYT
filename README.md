# JCYT — Static copy

This repository contains a static copy of the Framer site archived from https://jcyt.framer.website.

To publish on GitHub Pages from this repository (root):

1. Create a GitHub repo (e.g. `jcyt`) and add it as a remote.
2. Push the `main` branch and enable GitHub Pages from the repository Settings -> Pages -> Source: `main` branch `/ (root)`.

Commands to run locally:

```bash
cd /Users/janet/webpage
git remote add origin git@github.com:<your-username>/<repo>.git
git branch -M main
git push -u origin main
```

If you'd prefer Pages from the `gh-pages` branch, run:

```bash
git checkout -b gh-pages
git push -u origin gh-pages
```

If you want me to create the GitHub repo and push, provide a personal access token with `repo` scope or grant me push access (not required to proceed — I can prepare everything locally).
