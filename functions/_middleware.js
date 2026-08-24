// Markdown content negotiation.
//
// When an agent asks for a page with "Accept: text/markdown", serve the
// markdown twin instead of the HTML. Same words, roughly a fifth of the
// tokens. Browsers never send that header, so people are unaffected.
//
// Everything here is written to fail open. Any unexpected condition falls
// through to next(), which serves the normal site. If this file is deleted
// the site keeps working exactly as it does now, minus the negotiation.

const MARKDOWN_FOR = {
  "/": "/index.md",
  "/index.html": "/index.md",
  "/subscribe.html": "/subscribe.md",
};

export async function onRequest(context) {
  const { request, next } = context;

  try {
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
