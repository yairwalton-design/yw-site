// Markdown content negotiation.
//
// When an agent asks for a page with "Accept: text/markdown", serve the
// markdown twin instead of the HTML. Same words, roughly a fifth of the
// tokens. Browsers never send that header, so people are unaffected.
//
// Everything here is written to fail open. Any unexpected condition falls
// through to next(), which serves the normal site. If this file is deleted
// the site keeps working exactly as it does now, minus the negotiation.

// Repo files that are not part of the site. The Pages build output directory
// is the repo root, so these upload with everything else. Serve 404 for them
// rather than the file. See the README for the permanent fix, which is to move
// the site into its own directory and point the build at that instead.
const NOT_THE_SITE = [/^\/README\.md$/i, /^\/tools(\/|$)/i, /^\/functions(\/|$)/i];

const MARKDOWN_FOR = {
  "/": "/index.md",
  "/index.html": "/index.md",
  "/subscribe.html": "/subscribe.md",
};

export async function onRequest(context) {
  const { request, next } = context;

  try {
    const path = new URL(request.url).pathname;
    if (NOT_THE_SITE.some((re) => re.test(path))) {
      return new Response("Not found\n", {
        status: 404,
        headers: { "content-type": "text/plain; charset=utf-8",
                   "x-robots-tag": "noindex, nofollow" },
      });
    }

    if (request.method !== "GET" && request.method !== "HEAD") return next();

    const accept = request.headers.get("accept") || "";
    if (!/(^|[\s,])text\/markdown([\s,;]|$)/i.test(accept)) return next();

    const url = new URL(request.url);
    const target = MARKDOWN_FOR[url.pathname];
    if (!target) return next();

    const asset = await next(new Request(new URL(target, url), request));
    if (!asset || !asset.ok) return next();

    const headers = new Headers(asset.headers);
    headers.set("content-type", "text/markdown; charset=utf-8");
    headers.set("content-location", target);
    headers.set("vary", "Accept");
    return new Response(asset.body, { status: 200, headers });
  } catch (err) {
    return next();
  }
}
