import json, base64, io, re, os
from PIL import Image, ImageDraw
g = open('game_v7.html', encoding='utf-8').read()

def rep(old, new):
    global g
    assert g.count(old) == 1, (g.count(old), old[:80])
    g = g.replace(old, new)

rep('<title>Guardiões da Tabuada 3</title>', '<title>Guardiões da Tabuada</title>')
# cópia de segurança nos Ajustes
rep('''    <div class="set">
      <h3>Para pais e professores</h3>''', '''    <div class="set">
      <h3>Cópia de segurança</h3>
      <p>O progresso fica guardado neste aparelho. Guarde uma cópia de vez em quando: se o jogo for apagado ou você trocar de aparelho, é só trazer a cópia de volta.</p>
      <div class="confirm"><button type="button" class="btn-blue" id="bkOut">Guardar cópia</button><button type="button" class="btn-ghost" id="bkIn">Trazer cópia</button></div>
      <input type="file" id="bkFile" accept=".json,application/json" hidden>
      <p class="sub" id="bkMsg" style="margin:8px 0 0;font-size:12px"></p>
    </div>
    <div class="set">
      <h3>Para pais e professores</h3>''')
rep('''$('resetYes').onclick = () => { S = defaultSave(); save(); $('resetConfirm').hidden = true; show('home'); };''',
'''$('resetYes').onclick = () => { S = defaultSave(); save(); $('resetConfirm').hidden = true; show('home'); };
// cópia de segurança: guarda e traz de volta o progresso inteiro num arquivo
$('bkOut').onclick = async () => {
  const data = JSON.stringify({game:'guardioes-da-tabuada', when:new Date().toISOString(), save:S});
  const name = 'guardioes-progresso-' + new Date().toISOString().slice(0, 10) + '.json';
  try {
    const file = new File([data], name, {type:'application/json'});
    if (navigator.canShare && navigator.canShare({files:[file]})){ await navigator.share({files:[file], title:'Progresso dos Guardiões'}); $('bkMsg').textContent = 'Cópia guardada.'; return; }
  } catch(e){ if (e && e.name === 'AbortError') return; }
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], {type:'application/json'})); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  $('bkMsg').textContent = 'Cópia guardada no arquivo ' + name + '.';
};
$('bkIn').onclick = () => $('bkFile').click();
$('bkFile').onchange = async e => {
  const f = e.target.files[0]; e.target.value = ''; if (!f) return;
  try {
    const d = JSON.parse(await f.text()), sv = d && d.save;
    if (!sv || typeof sv !== 'object' || !sv.cards || !sv.settings) throw 0;
    localStorage.setItem(SAVE_KEY, JSON.stringify(sv)); S = load(); grantArenaChests(); save();
    $('bkMsg').textContent = 'Progresso trazido de volta!'; sfx('coin'); renderSettings(); refreshCoins();
  } catch(err){ $('bkMsg').textContent = 'Não consegui ler esse arquivo. Escolha a cópia guardada pelo jogo.'; }
};''')
rep("window.__GT = {get B(){ return B; }, get S(){ return S; },", "window.__GT = {get B(){ return B; }, get S(){ return S; }, SAVE_KEY,")

head = '''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Tabuada">
<meta name="theme-color" content="#17153b">
<meta name="robots" content="noindex">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
</head><body>
'''
tail = '''
<script>
if ('serviceWorker' in navigator) window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e) {}
</script>
</body></html>
'''
os.makedirs('site', exist_ok=True)
open('site/index.html', 'w', encoding='utf-8').write(head + g + tail)

# ícone a partir dos sprites embutidos
i = g.index('const SPR_DATA = ') + len('const SPR_DATA = '); j = g.index('\n', i)
spr = json.loads(g[i:j].rstrip().rstrip(';'))
def pic(name):
    src = spr[name][0]['src']; return Image.open(io.BytesIO(base64.b64decode(src.split(',', 1)[1]))).convert('RGBA')
def icon(n):
    im = Image.new('RGBA', (n, n), (23, 21, 59, 255)); d = ImageDraw.Draw(im)
    for y in range(n):
        t = y/n; d.line([(0, y), (n, y)], fill=(int(43 + 30*t), int(38 + 10*t), int(112 - 20*t), 255))
    for img, scale, cx, cy in [(pic('boss1'), .62, .62, .52), (pic('arqueira'), .62, .34, .6)]:
        r = n*scale/img.height; im2 = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
        im.alpha_composite(im2, (int(n*cx - im2.width/2), int(n*cy - im2.height/2)))
    return im.convert('RGB')
for n in (180, 192, 512): icon(n).save(f'site/icon-{n}.png')
json.dump({"name": "Guardiões da Tabuada", "short_name": "Tabuada", "start_url": "./index.html", "scope": "./", "display": "fullscreen", "orientation": "landscape",
           "background_color": "#17153b", "theme_color": "#17153b", "lang": "pt-BR",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open('site/manifest.webmanifest', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open('site/sw.js', 'w').write("""const V = 'tabuada-v7-1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
// com internet pega a versão nova; sem internet usa a guardada
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(V).then(ch => ch.put(e.request, c)); return r; }).catch(() => caches.match(e.request).then(m => m || caches.match('./index.html'))));
});
""")
open('site/.nojekyll', 'w').write('')
open('site/README.md', 'w', encoding='utf-8').write('# Guardiões da Tabuada\n\nJogo de tabuada em família. Abra `index.html` ou o endereço publicado no celular deitado.\n')
print('ok', os.path.getsize('site/index.html')//1024, 'KB')
