# yw-site

The personal site of **Yair Walton**. One page: the idea, the work, who I am, how to reach me.

Live at **https://yairwalton.com**, deployed from this repo by Cloudflare Pages.
Every push to `main` rebuilds it within about a minute.

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
| `BingSiteAuth.xml` | Bing ownership proof. Must stay at the root forever. |
| `llms.txt` | A plain text summary of the site for AI assistants. |
| `index.md`, `subscribe.md` | Markdown twins of the two pages, for AI agents. |
| `functions/_middleware.js` | Serves the markdown when an agent asks for it. |
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

## Email is live on Google Workspace

**yair@yairwalton.com** works. Mail for the domain goes to Google Workspace
(`MX 1 smtp.google.com`), not to Cloudflare Email Routing.

The authentication records are all in place:

| Record | Value | State |
|---|---|---|
| SPF | `v=spf1 include:_spf.google.com ~all` | One record. Correct. |
| DKIM | `google._domainkey` | Signing as the domain. |
| DMARC | `v=DMARC1; p=none; rua=...@dmarc-reports.cloudflare.net` | Monitoring. |

Two things to know if you go looking at Cloudflare's Email Security panel:

- It reports **"Multiple SPF records found."** That is wrong. There is exactly
  one, confirmed against both 1.1.1.1 and 8.8.8.8. Its own recommendation tells
  you to append `~all` to a record it is displaying with `~all` already on the
  end. Ignore the whole panel.
- It flags **SPF `~all` as a warning** and wants `-all`. Leave it. Google's own
  Workspace guidance recommends `~all`, and `-all` breaks mail that gets
  forwarded. Once DMARC is enforcing, DMARC decides the outcome anyway.

**Do not jump DMARC to `p=quarantine` or `p=reject` yet.** `p=none` exists so you
can read reports before enforcing. The record went in on 2026-08-24, so there is
nothing to read yet. Give it two to four weeks, check the DMARC Management
dashboard, and only tighten if every legitimate sender is passing. If you later
send mail through anything other than Workspace, such as Buttondown for the
essays, it has to be authorized before you enforce or those emails vanish.

BIMI shows as "Fail" and should be ignored. It needs a registered trademark and
a Verified Mark Certificate at roughly $1,000 a year.

---

## Analytics

Cloudflare Web Analytics is **on**, via auto-install. Cookieless, no personal
data, no cookie banner needed. RUM was enabled on 2026-08-08 and Cloudflare
injects the beacon at the edge, which is why you will not find it in these files.

**Do not uncomment the ANALYTICS block in `index.html` or `subscribe.html`.**
That is the in-code alternative to auto-install, and running both fires the
beacon twice, so every visit counts double with nothing to warn you.

To read the numbers: Cloudflare dashboard, Web Analytics, pick the site. There is
no backfill, so the data starts from when it was switched on, not from launch.

---

## The press page is in git history, not in the folder

A press page was written and finished, then taken out of the deployable folder
because its copy no longer matched the rest of the site. Any file left in the
folder deploys, whether or not anything links to it.

It is recoverable from git history. Find it with `git log --diff-filter=D
--name-only`, restore it with `git checkout <commit> -- <files>`, then rewrite it
to match whatever the site says at that point and add it back to the nav and the
sitemap.

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

Done:

- [x] `yair@yairwalton.com` receives mail, on Google Workspace.
- [x] Deployed to Cloudflare Pages from this repo.
- [x] `yairwalton.com` attached as the custom domain.
- [x] Cloudflare Web Analytics on, via auto-install.
- [x] Google Search Console verified, and the site is indexable.
- [x] URL added to the LinkedIn profile.
- [x] SPF, DKIM and DMARC in place.

Still open:

- [ ] Submit `https://yairwalton.com/sitemap.xml` in Search Console, and again
      at Bing Webmaster Tools.
- [ ] Finish Bing verification. Both proofs are deployed: `BingSiteAuth.xml` at
      the root, and an `msvalidate.01` meta tag in the `index.html` head. Neither
      may ever be deleted, or Bing silently unverifies the site. If Bing still
      fails, it is fetching the `www` hostname, which `_redirects` 301s to the
      bare domain. Use Bing's CNAME method instead: name
      `14536cdafd9c4cc6ae01adc80bce385b`, value `verify.bing.com`. DNS has no
      hostname redirect to trip over.
- [ ] Hit **Validate Fix** on the Search Console `mainEntity` error. The schema
      correction has been live for a while and should clear.
- [ ] Re-run the **LinkedIn Post Inspector**. Both photos were replaced on
      2026-08-24, and LinkedIn caches preview cards hard, so anyone you send the
      link to still gets the old card until you refresh it.
- [ ] Review DMARC reports in two to four weeks before tightening `p=none`.
- [ ] Decide whether this needs a colleague preview before it circulates. The
      pages name no organization, so the usual trigger does not apply on its
      face, but the reach figure is still on it.

Expect nothing for a few days. A new domain with no inbound links usually takes
somewhere between a few days and a few weeks to appear, even for your own name.

---

## Changing things

**Page weight.** The home page is about 290 KB on a first mobile visit, most of
it the Newsreader typeface at 129 KB. Repeat visits are nearly free because the
fonts are cached for a year. There is no CSP header, deliberately: it would
block either the structured data or Cloudflare's analytics depending on how it
was written.

**The disclaimer.** The footer says "does not speak for my employer" and names no
organization. If an organization is ever named on the page, name it in the
disclaimer too, so the two stay consistent.

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

## Reading the site as an agent would

Three ways in, in order of how much they save:

```bash
curl -H "Accept: text/markdown" https://yairwalton.com/   # negotiated
curl https://yairwalton.com/index.md                      # direct
curl https://yairwalton.com/llms.txt                      # site summary
```

`index.md` is about 2 KB against 10 KB of HTML, so an assistant reading the
markdown spends roughly a fifth of the tokens and is likelier to take in the
whole page rather than a truncated slice of markup.

**The markdown is maintained by hand.** There is no build step. If you change a
sentence in `index.html`, change it in `index.md` and `llms.txt` too, or agents
will quote a stale version of you. This is the one real maintenance cost of the
setup.

`functions/_middleware.js` does the negotiation. It is written to fail open:
anything unexpected falls through to the normal site. Deleting the file is a
safe rollback, and costs only the negotiated path; the `.md` URLs keep working.

`robots.txt` carries a `Content-Signal` line: `search=yes, ai-input=yes,
ai-train=no`.

The first two are what get you found and quoted accurately, and they carry all
of the visibility. `ai-train=no` withholds permission to use the text as model
training data. It is off because permitting it would gain a site this size
essentially nothing, and it is the only one of the three that cannot be undone:
a signal can be changed later, but text already absorbed into a trained model
stays absorbed. That matters more once the essays are up than it does for a bio
paragraph, which is the point of settling it now.

Two things it does not do. It does not affect the Agent Readiness score, which
checks that the line exists and not what it says. And it is a declared
preference honored voluntarily, like `robots.txt` itself, so it binds
well-behaved crawlers and not others.

**The line is repeated in all six groups on purpose.** A crawler that matches a
named group ignores the `*` group completely, so a signal written only under `*`
would never reach GPTBot or ClaudeBot, the crawlers it is aimed at. If you change
it, change it in every group.

## This file is on the live site

The Pages project has an empty build output directory, which makes the repo root
the site. Everything here deploys, including this README, at
`https://yairwalton.com/README.md`, and `tools/` alongside it.

`_headers` marks both `noindex` so they stay out of search results. That stops
them being findable, not being readable: anyone with the URL can open them.

**So keep this file free of anything you would not put on the site.** No
colleague names, no internal review notes, no reasoning about what was left off
the page and why. Operational instructions only. Anything genuinely private
belongs somewhere that is not this repo.

## Notes

- The disclaimer in the footer and the routing line in the contact section both need
  to stay on any public version.
- Fonts are self hosted, so nothing about a visitor is sent to Google, and the
  typography survives networks that block outside font services.
