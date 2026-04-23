# Static Site Generator (Python)

A **static site generator** takes raw content files (like Markdown and images) and turns them into a fully functional static website—a mix of HTML, CSS, and assets that can be hosted anywhere.

This project follows a hands-on approach inspired by Boot.dev’s guide, focusing on building everything from scratch to understand how static sites actually work under the hood.

---

## Overview

Instead of relying on frameworks, this project builds a simple static site generator using Python. It:

* Reads content files (e.g. Markdown)
* Applies an HTML template
* Outputs ready-to-serve `.html` files
* Preserves directory structure
* Recursively processes nested folders

---

## ⚙️ How It Works

1. The program scans the `content/` directory recursively
2. For each file:
   * If it's a directory → recurse into it
   * If it's a file → generate a corresponding HTML file
3. Output files are written to the `public/` directory
4. Directory structure is preserved
5. File extensions are converted (e.g. `.md` → `.html`)

---

## 🛠 Example Logic

* Input:

  ```
  content/blog/post.md
  ```

* Output:

  ```
  public/blog/post.html
  ```

---

## ▶️ Usage

Run the `main.sh`:

```bash
python3 src/main.py
```

After running, your static site will be available in the `public/` folder.

