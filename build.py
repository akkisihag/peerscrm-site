#!/usr/bin/env python3
# Build the deployed marketing site from the bundled source HTML.
# Usage: python3 build.py "/path/to/PeersCRM Website.html"  (defaults to the
# "PeersCRM Local Site 2" export). Injects favicon/meta into <head>, fixes the
# <title>, and appends the CTA + demo-modal + thumbnail wiring before </body>.
import sys, io, os, re

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
DEFAULT_SRC = os.path.expanduser('~/Downloads/PeersCRM Local Site 2/PeersCRM Website.html')
src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC

TITLE = 'PeersCRM — CRM for contractors &amp; growing businesses'
DESC = 'Projects, clients, subcontractors, and client-ready reports — everything your company runs on, together.'

HEAD = '''<link rel="icon" type="image/png" sizes="48x48" href="/favicon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="description" content="''' + DESC + '''">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.peerscrm.com/">
<meta property="og:title" content="PeersCRM — CRM for contractors & growing businesses">
<meta property="og:description" content="''' + DESC + '''">
<meta property="og:image" content="https://www.peerscrm.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="PeersCRM">
<meta name="twitter:description" content="''' + DESC + '''">
<meta name="twitter:image" content="https://www.peerscrm.com/og-image.png">
<style id="peers-responsive">
/* Mobile responsiveness: the exported design is desktop-only (only shrinks
   headings). These overrides stack the two-column sections, collapse the
   fixed-pixel grids, and stop content being clipped/overflowing on phones. */
@media (max-width: 860px){
  /* stack the alternating two-column feature blocks */
  .showcase{ flex-direction: column !important; gap: 28px !important; align-items: stretch !important; }
  .showcase > *{ width: 100% !important; max-width: 100% !important; }
  /* stack the hero (text + dashboard card); NOT the header (.page.fx.ac.jb) or footer (.wrap) */
  .page.fx.gap24:not(.wrap){ flex-wrap: wrap !important; }
  .page.fx.gap24:not(.wrap) > *{ flex: 1 1 100% !important; min-width: 0 !important; }
  /* fixed-pixel grids -> single column */
  .grid{ grid-template-columns: 1fr !important; }
  /* remove fixed section heights that clip content (e.g. the cut-off button) */
  .sect{ height: auto !important; min-height: 0 !important; }
  /* full-width container with side padding */
  .page{ max-width: 100% !important; padding-left: 20px !important; padding-right: 20px !important; box-sizing: border-box !important; }
  /* cap oversized content images WITHOUT distorting fixed-size logos (no height:auto) */
  img{ max-width: 100% !important; }
  html, body{ overflow-x: hidden !important; }
}
@media (max-width: 520px){
  .grid.tc, .page.grid{ grid-template-columns: 1fr !important; }
  .fx.ac.jc.gap8.wrap{ gap: 6px !important; }
}
</style>
'''

BODY = r'''<script>
(function(){
  var APP_URL='https://app.peerscrm.com/';
  var TRIAL=('mailto:info@peerscrm.com?subject='+encodeURIComponent('PeersCRM Free Trial / Access Request')+'&body='+encodeURIComponent("Hi PeersCRM team,\n\nI'd like to try PeersCRM for free. Please send me an invite.\n\nName:\nCompany:\nPhone:\n\nThanks!"));
  var SALES=('mailto:info@peerscrm.com?subject='+encodeURIComponent('PeersCRM — Talk to Sales')+'&body='+encodeURIComponent("Hi PeersCRM team,\n\nI'd like to talk to sales about PeersCRM.\n\nName:\nCompany:\nPhone:\n\nThanks!"));
  var DEMO='__peers_demo__';
  var LOGIN=['sign in','log in','login'];
  var SIGNUP=['try for free','start free trial','start for free','sign up','get started'];
  var TALK=['talk to sales','contact sales'];
  var WATCH=['watch demo','watch now','watch now →','watch the full tour'];
  function txt(el){return (el.textContent||'').trim().replace(/\s+/g,' ').toLowerCase();}
  function pick(t){
    if(LOGIN.indexOf(t)>=0)return APP_URL;
    if(SIGNUP.indexOf(t)>=0)return TRIAL;
    if(TALK.indexOf(t)>=0)return SALES;
    if(WATCH.indexOf(t)>=0 || /play the.*demo/.test(t))return DEMO;
    return null;
  }
  function wire(){
    document.querySelectorAll('a,button').forEach(function(el){
      var d=pick(txt(el)); if(!d)return;
      if(el.tagName==='A' && d!==DEMO)el.setAttribute('href',d);
      el.setAttribute('data-peers',d);
    });
    document.querySelectorAll('.vidframe').forEach(function(el){ el.setAttribute('data-peers',DEMO); el.style.cursor='pointer'; });
    document.querySelectorAll('.vstripe').forEach(function(el){
      el.style.backgroundImage="linear-gradient(rgba(6,16,42,.30),rgba(6,16,42,.42)), url('/demo-thumb.svg')";
      el.style.backgroundSize='cover'; el.style.backgroundPosition='center'; el.style.backgroundRepeat='no-repeat';
    });
  }
  function openDemo(){
    if(document.getElementById('peersDemoModal'))return;
    var o=document.createElement('div'); o.id='peersDemoModal';
    o.style.cssText='position:fixed;inset:0;z-index:99999;background:rgba(6,12,34,.88);display:flex;align-items:center;justify-content:center;padding:24px;';
    var box=document.createElement('div'); box.style.cssText='position:relative;width:min(1100px,96vw);aspect-ratio:16/9;background:#000;border-radius:14px;overflow:hidden;box-shadow:0 24px 90px rgba(0,0,0,.55);';
    var f=document.createElement('iframe'); f.src='/demo.html?autoplay=1'; f.style.cssText='width:100%;height:100%;border:0;display:block;'; f.setAttribute('allow','autoplay; fullscreen; encrypted-media');
    var c=document.createElement('button'); c.setAttribute('aria-label','Close'); c.textContent='✕';
    c.style.cssText='position:fixed;top:18px;right:22px;width:42px;height:42px;border-radius:50%;border:0;background:#fff;color:#0b1220;font-size:18px;line-height:1;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.35);';
    function close(){ o.remove(); document.removeEventListener('keydown',esc); }
    function esc(e){ if(e.key==='Escape')close(); }
    c.addEventListener('click',close);
    o.addEventListener('click',function(e){ if(e.target===o)close(); });
    document.addEventListener('keydown',esc);
    box.appendChild(f); o.appendChild(box); o.appendChild(c); document.body.appendChild(o);
  }
  document.addEventListener('click',function(e){
    var el=e.target.closest&&e.target.closest('[data-peers]'); if(!el)return;
    var d=el.getAttribute('data-peers'); if(!d)return;
    e.preventDefault(); e.stopPropagation();
    if(d===DEMO)openDemo(); else window.location.href=d;
  },true);
  try{ new MutationObserver(wire).observe(document.documentElement,{childList:true,subtree:true}); }catch(_){}
  if(document.readyState!=='loading') wire(); else document.addEventListener('DOMContentLoaded',wire);
})();
</script>'''

html = io.open(src, encoding='utf-8', errors='ignore').read()

# Fix the browser-tab title (source ships "Bundled Page")
html = re.sub(r'<title>.*?</title>', '<title>' + TITLE + '</title>', html, count=1, flags=re.S)

# Inject head tags right after <head...>
m = re.search(r'<head[^>]*>', html)
if m:
    html = html[:m.end()] + '\n' + HEAD + html[m.end():]
else:
    html = HEAD + html

# Append body wiring before </body>
html = html.replace('</body>', BODY + '\n</body>', 1) if '</body>' in html else html + BODY

io.open(DEST, 'w', encoding='utf-8').write(html)
print('built index.html from', os.path.basename(src), '-> size', len(html))
