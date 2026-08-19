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
| `subscribe.html` | Email signup for when a piece is published. Needs one setup step, below. |
| `soon.html` | A coming soon splash. Not linked from anywhere. See below. |
| `styles.css` | All the colors, fonts, and spacing. Edit this to change how it looks. |
| `404.html` | What someone sees at a URL that does not exist. |
| `assets/` | Portrait in two sizes, the link preview image, and the fonts. |
| `assets/fonts/` | The four typefaces, served from this site rather than from Google. |
| `tools/share-card.html` | Source for the link preview image. See below. |
| `robots.txt` | Tells search engines they are welcome, including AI crawlers. |
| `sitemap.xml` | The page list search engines read after launch. |
| `_headers` | Security and caching rules Cloudflare applies. You can ignore it. |
| `_redirects` | Sends www to the bare domain so search sees one address. Ignore it. |
| `favicon.ico`, `favicon.svg` | The tab icon. Google shows it beside mobile results. |
| `site.webmanifest` | Name and icons for when someone saves the site to a phone. |

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

## The email address must exist before you deploy

The site now says **yair@yairwalton.com** everywhere. That address does not
exist yet. Until you do the five minutes below, mail sent to it bounces and you
never find out somebody tried.

Cloudflare Email Routing is free and does not require paying for mail hosting.
It forwards to the inbox you already read.

1. Cloudflare dashboard, pick the `yairwalton.com` domain, then **Email**, then
   **Email Routing**, then **Get started**.
2. Cloudflare offers to add the DNS records for you. Let it.
3. Create address: `yair@yairwalton.com`, forwarding to your Gmail.
4. Gmail sends a verification link. Click it.
5. Send yourself a test from a different account and confirm it lands.

Optional, worth doing: in Gmail, Settings, Accounts, "Send mail as", add
`yair@yairwalton.com` so replies go out from that address rather than your Gmail.

If you decide not to do this, change the address back to your Gmail in
`index.html`, `subscribe.html` and `soon.html` before deploying.

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

## The press page is out of the folder, not lost

`press.html` was written and finished, but it named the employer, the program and
the award, all of which came off the rest of the site on purpose. Leaving it in
the folder would have deployed it to `/press.html` for anyone with the URL.

It lives in git history. To bring it back:

```bash
git checkout abec079 -- press.html assets/headshot-studio-1000.webp assets/yair-walton-headshot.jpg
```

Then rewrite it to match whatever the site says at that point, and add it back to
the nav and the sitemap.

---

## The signup form is switched off on purpose

`subscribe.html` currently asks people to email you, and that works today. The
Buttondown form is written but commented out, because a form posting to an account
that does not exist throws a 404 at whoever fills it in.

To switch it on:

1. Sign up at buttondown.com, free up to 100 subscribers, and pick a username.
2. In `subscribe.html` replace `YOUR-USERNAME` in the form action.
3. Delete the comment markers around the `<form>` block.
4. Push, then test it with your own address before telling anyone.

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

The site is **open to search engines**. `robots.txt` allows everyone including
the AI crawlers, and `index.html` and `subscribe.html` ask to be indexed with
large image previews. `soon.html` and `404.html` stay out of search on purpose.

Before anyone sees it:

1. Confirm `yair@yairwalton.com` actually receives mail. It is the only contact
   on the site. Steps are above. Do this first.
2. Deploy: Workers & Pages, Create, Pages, Connect to Git, pick `yw-site`. Build
   command empty, output directory empty, framework preset None.
3. Add `yairwalton.com` as a custom domain on the Pages project. If the site
   lives anywhere else instead, find and replace `https://yairwalton.com`
   across the folder first, or every canonical, preview image and schema ID
   points at the wrong place.
4. Turn on analytics. One click in Pages settings, or paste a token. Not both.
5. Paste the live URL into the LinkedIn Post Inspector and confirm the preview
   image appears. Then Google's Rich Results Test to confirm the profile data
   reads.
6. Add the site in Google Search Console, verify it, submit
   `https://yairwalton.com/sitemap.xml`. Same at Bing Webmaster Tools.
7. Put the URL in your LinkedIn profile. Inbound links are most of how a new
   site gets found, and that is the strongest one you control.
8. Decide whether June or Ann should read it first. The pages no longer name
   the employer or the program, so the usual trigger does not apply on its
   face, but the reach figure is still there.

Expect nothing for a few days. A new domain with no inbound links usually takes
somewhere between a few days and a few weeks to appear, even for your own name.

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
