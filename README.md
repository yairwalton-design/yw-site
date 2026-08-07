# yw-site

The personal site of **Yair Walton**. One page: the idea, the work, who I am, how to reach me.

Not connected to a domain yet. It runs at a temporary Cloudflare Pages address
while it is being built.

There is no build step and nothing to install. Plain HTML and CSS, so the file
you open is the file that ships.

---

## What's in here

| File | What it is |
|---|---|
| `index.html` | All the text on the site. Edit this to change words. |
| `styles.css` | All the colors, fonts, and spacing. Edit this to change how it looks. |
| `404.html` | What someone sees at a URL that does not exist. |
| `assets/` | Portrait in two sizes, the link preview image, and the fonts. |
| `assets/fonts/` | The four typefaces, served from this site rather than from Google. |
| `tools/share-card.html` | Source for the link preview image. See below. |
| `robots.txt` | Tells search engines to stay out. Change this at launch. |
| `sitemap.xml` | The page list search engines read after launch. |
| `_headers` | Security and caching rules Cloudflare applies. You can ignore it. |

---

## The three things you will actually do

**See it on your computer.** Double click `index.html`. That is the whole preview process.

**Change the words.** Open `index.html` in any text editor. The sentences read as
normal English between the tags. Save, then refresh your browser.

**Publish a change.**

```bash
git add -A
git commit -m "Describe what you changed"
git push
```

Cloudflare rebuilds on its own within about a minute.

---

## Cloudflare Pages setup

Workers & Pages, then Create, then Pages, then Connect to Git, then pick `yw-site`.

Leave the build command **empty** and the output directory **empty**. Framework
preset **None**. There is nothing to build.

---

## Launch checklist

Right now the site is deliberately invisible to search engines. When it is ready:

1. Delete the `<meta name="robots" content="noindex, nofollow">` line in `index.html`.
2. Delete the two `Disallow` lines in `robots.txt`.

   Both are required. Either one on its own keeps the site out of search results.
3. If the site is living somewhere other than `yairwalton.com`, update the domain in
   four places: the `canonical` link, `og:url`, `og:image`, and `twitter:image` in
   `index.html`, plus the two URLs in `robots.txt` and `sitemap.xml`.
4. Paste the live URL into the LinkedIn Post Inspector to confirm the preview image
   appears, then into Google's Rich Results Test to confirm the profile data reads.

---

## Changing things

**The accent color.** Near the top of `styles.css`, under "Accent, slate register."
The commented line below holds the gold values. Swap them to move from the civic
register to the Jewish communal one.

**Dark mode.** The site follows whatever the visitor's device is set to. Both
palettes live at the top of `styles.css`.

**The photo order on phones.** The headline comes first and the portrait follows.
To lead with the photo instead, there is a one line note in the narrow section at
the bottom of `styles.css`.

**The link preview image.** `assets/share-card.png` is what shows up when the site
gets posted to LinkedIn or pasted into a message. To change it, edit
`tools/share-card.html` and screenshot it at exactly 1200 by 630.

---

## Notes

- The disclaimer in the footer and the routing line in the contact section both need
  to stay on any public version.
- Fonts are self hosted, so nothing about a visitor is sent to Google, and the
  typography survives networks that block outside font services.
