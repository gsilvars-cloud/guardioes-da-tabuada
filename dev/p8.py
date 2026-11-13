from patchlib import G
g = G()
g.rep('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">', '<meta name="viewport" id="vp" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">')
g.rep("html,body{height:100%}", "html,body{height:100%}\nhtml{touch-action:pan-x pan-y;-webkit-text-size-adjust:100%;overscroll-behavior:none}   /* sem zoom por dois toques ou pinça: a tela do jogo não pode ampliar */")
g.rep("let S = load();", """// iPhone: bloqueia o zoom da página (pinça e dois toques rápidos) e desfaz se o navegador ampliar mesmo assim
for (const ev of ['gesturestart', 'gesturechange', 'gestureend']) document.addEventListener(ev, e => e.preventDefault(), {passive:false});
document.addEventListener('dblclick', e => e.preventDefault(), {passive:false});
document.addEventListener('touchmove', e => { if (e.touches && e.touches.length > 1) e.preventDefault(); }, {passive:false});
{ let lastEnd = 0; document.addEventListener('touchend', e => { const now = Date.now(); if (now - lastEnd < 320 && !e.target.closest('input,textarea')) e.preventDefault(); lastEnd = now; }, {passive:false}); }
if (window.visualViewport) visualViewport.addEventListener('resize', () => {
  if (visualViewport.scale > 1.02){ const m = document.getElementById('vp'), c = m.content; m.content = c + ',minimum-scale=1'; setTimeout(() => { m.content = c; }, 60); }
});
let S = load();""")
g.save()
