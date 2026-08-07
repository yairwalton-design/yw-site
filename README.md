# yw-site

The personal site of **Yair Walton**. One page: who I am, what I work on, how to reach me.

Not connected to a domain yet. It lives at a temporary Cloudflare Pages address
while it is being built.

---

## What's in here

| File | What it is |
|---|---|
| `index.html` | All the text on the site. This is the file you edit to change words. |
| `styles.css` | All the colors, fonts, and spacing. Edit this to change how it looks. |
| `assets/` | The portrait image, in two sizes. |
| `_headers` | Security settings Cloudflare reads automatically. You can ignore it. |

There is no build step and nothing to install. It is plain HTML and CSS, so what
you see in the files is what ships.

---

## To see it on your computer

Double click `index.html`. It opens in your browser. That is the whole preview
process.

## To change the words

1. Open `index.html` in any text editor.
2. Find the sentence you want to change. It reads as normal English between the tags.
3. Save the file, then refresh your browser.

## To change the accent color

Open `styles.css`. Near the top there are two lines under "Accent, slate register".
The commented line below them holds the gold values. Swap them to move the site
from the civic register to the Jewish communal one.

---

## To publish a change

```bash
git add -A
git commit -m "Describe what you changed"
git push
```

Cloudflare Pages rebuilds on its own within about a minute of the push.

---

## Notes

- The site currently carries `noindex` in `index.html`, so search engines skip it.
  Remove that line when it is ready to be found.
- The disclaimer in the footer and the routing line in the contact section both
  need to stay on any public version.
