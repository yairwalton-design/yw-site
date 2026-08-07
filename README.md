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
| `index.html` | The main page. All its text lives here. |
| `press.html` | A press and speaking page. Finished, but deliberately NOT linked. See below. |
| `subscribe.html` | Email signup for when a piece is published. Needs one setup step, below. |
| `soon.html` | A coming soon splash. Not linked from anywhere. See below. |
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

## Analytics

The site is set up for Cloudflare Web Analytics: cookieless, no personal data,
no cookie banner needed. It is **not on yet**. Pick one of these, never both,
or every visit gets counted twice.

**Easiest, no code.** In the Cloudflare dashboard open the Pages project, go to
Settings, then Web Analytics, and click Enable. Cloudflare injects the tracking
for you and nothing in these files changes.

**In code.** Cloudflare dashboard, Web Analytics, Add a site, copy the token.
In `index.html` and `subscribe.html` find the ANALYTICS comment block near the
bottom of the head, paste the token over `YOUR-TOKEN-HERE`, and delete the
`<!--` and `-->` around the script tag.

Until you do one of these, the site runs zero JavaScript and makes zero
third-party requests.

---

## The press page is parked

`press.html` is written and works, but nothing links to it and it is not in the
sitemap. A speaking page before anything is published signals more than the
evidence supports, so it waits.

To turn it on later: add `<a href="/press.html">Press</a>` back to the nav in
`index.html` and `subscribe.html`, add it to `sitemap.xml`, and remove its
`noindex` line.

---

## The email signup needs five minutes of setup

`subscribe.html` posts to Buttondown, which is free up to 100 subscribers and does
not track anyone. Until you set up the account, the form does nothing.

1. Sign up at buttondown.com and pick a username.
2. In `subscribe.html`, find `YOUR-USERNAME` in the form action and replace it with
   the username you picked.
3. Commit and push, then test the form yourself with your own address.

The fallback line under the form tells people they can email you instead, so the
page is still honest and usable before you do any of this.

---

## The coming soon splash

`soon.html` is a stripped down holding page: the mark, your name, one sentence, and
your email. Nothing links to it, so nobody will find it unless you send it to them.

To make it the front door, rename `index.html` to something like `full.html` and
rename `soon.html` to `index.html`. To undo it, swap them back. Only do this if you
want the domain live before the rest is ready.

---

## Cloudflare Pages setup

Workers & Pages, then Create, then Pages, then Connect to Git, then pick `yw-site`.

Leave the build command **empty** and the output directory **empty**. Framework
preset **None**. There is nothing to build.

---

## Launch checklist

Right now the site is deliberately invisible to search engines. When it is ready:

1. Delete the `<meta name="robots" content="noindex, nofollow">` line from
   `index.html` and `subscribe.html`. Leave it in `soon.html`, `404.html` and
   `press.html`; none of those should appear in search results yet.
2. Delete the two `Disallow` lines in `robots.txt`.

   Both are required. Either one on its own keeps the site out of search results.
3. If the site is living somewhere other than `yairwalton.com`, update the domain
   everywhere it appears: the `canonical`, `og:url`, `og:image` and `twitter:image`
   tags in `index.html`, `press.html` and `subscribe.html`, plus `robots.txt` and
   `sitemap.xml`. A find and replace across the folder catches all of them.
4. Paste the live URL into the LinkedIn Post Inspector to confirm the preview image
   appears, then into Google's Rich Results Test to confirm the profile data reads.
5. Set up the email signup, above, and send yourself a test.
6. Turn on analytics, above.
7. Decide whether this still needs June or Ann to read it. The linked pages no longer
   name the employer or the program, so the usual review trigger does not apply on its
   face. The reach number is still there, and `press.html` still names both, so it is
   worth a look either way.

---

## Changing things

**Page weight.** The home page is about 290 KB on a first mobile visit, most of
it the Newsreader typeface at 129 KB. Repeat visits are nearly free because the
fonts are cached for a year. There is no CSP header, deliberately: it would
block either the structured data or Cloudflare's analytics depending on how it
was written.

**The disclaimer.** The footer now says "does not speak for my employer" rather than
naming anyone. If you put the employer back on the page, put the name back in the
disclaimer too.

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
