import re
from patchlib import G
g = G()
# --- tremor: senos somados sobre trauma ao quadrado, em tempo real (antes era um sorteio por quadro) ---
g.rep("  if (B.shake > 0 && !reduceMotion) ctx.translate(rand(-1, 1)*B.shake*9, rand(-1, 1)*B.shake*7);",
      "  if (B.shake > 0 && !reduceMotion){ const k = B.shake*B.shake*(S.settings.soft ? .3 : 1), t = performance.now()*.03; ctx.translate(14*k*Math.sin(t*1.7), 10*k*Math.sin(t*2.3)); }")
# --- clarão: no máximo 3 por segundo, e mais fraco no modo suave ---
n = len(re.findall(r"B\.flash = (\.\d+);", g.t)); assert n == 8, n
g.t = re.sub(r"B\.flash = (\.\d+);", r"flash(\1);", g.t)
g.rep("function hitStop(t){", """const flashLog = [];
function flash(a){                                         // no máximo 3 clarões por segundo; no modo suave vira um clarão leve
  const now = performance.now(); while (flashLog.length && now - flashLog[0] > 1000) flashLog.shift();
  if (flashLog.length >= 3) return; flashLog.push(now);
  B.flash = Math.max(B.flash, S.settings.soft ? a*.3 : a);
}
function hitStop(t){""")
g.rep("""    <div class="set">
      <h3>Som</h3>""", """    <div class="set">
      <h3>Efeitos de tela</h3>
      <p>Nos golpes fortes a tela treme e dá um clarão. O modo suave reduz os dois.</p>
      <div class="seg" id="softSeg"><button type="button" data-s="0">Completo</button><button type="button" data-s="1">Suave</button></div>
    </div>
    <div class="set">
      <h3>Som</h3>""")
g.rep("['hintSeg', 'hint'], ['musicSeg', 'music']])", "['hintSeg', 'hint'], ['musicSeg', 'music'], ['softSeg', 'soft']])", 2)
# --- a música abaixa enquanto a voz fala ---
g.rep("    if (voicePT) u.voice = voicePT;\n    ss.speak(u);", "    if (voicePT) u.voice = voicePT;\n    u.onstart = () => duck(true); u.onend = u.onerror = () => duck(false);\n    ss.speak(u);")
g.rep("  const t0 = performance.now(), from = gain ? gain.gain.value : el.volume;\n  const step = () => {", "  const t0 = performance.now(), from = gain ? gain.gain.value : el.volume, id = el._fd = (el._fd || 0) + 1;\n  const step = () => {\n    if (el._fd !== id) return;                             // um fade mais novo assumiu")
g.rep("function music(key){", """let duckT = 0;
function duck(on){                                         // a música abaixa enquanto a voz fala a conta e volta depois
  clearTimeout(duckT); if (!mus.el || !mus.key) return;
  const vol = MUSIC[mus.key][1];
  musicFade(mus.el, mus.gain, on ? vol*.35 : vol, on ? 150 : 400);
  if (on) duckT = setTimeout(() => duck(false), 6000);     // se o aparelho não avisar o fim da fala, volta sozinha
}
function music(key){""")
# --- efeitos repetidos variam um pouco de tom ---
g.rep("function tone(f, dur, type, vol, f2, delay){\n  if (!ac || !S.settings.sound) return;", "let sfxVar = 1;\nfunction tone(f, dur, type, vol, f2, delay){\n  if (!ac || !S.settings.sound) return;\n  f *= sfxVar; if (f2) f2 *= sfxVar;")
g.rep("function sfx(n, arg){\n  if (!ac || !S.settings.sound) return;", "function sfx(n, arg){                                     // golpes repetidos variam um pouco de tom para não soar metralhadora\n  sfxVar = /^(hit|arrow|zap|spawn|coin)$/.test(n) ? 1 + (Math.random() - .5)*.14 : 1;\n  try { sfxRaw(n, arg); } finally { sfxVar = 1; }\n}\nfunction sfxRaw(n, arg){\n  if (!ac || !S.settings.sound) return;")
# --- cópia de reserva automática do progresso ---
g.rep("    const s = JSON.parse(localStorage.getItem(SAVE_KEY) || 'null');\n    if (s && typeof s === 'object'){", "    const s = readSave(SAVE_KEY) || readSave(BAK_KEY);      // save estragado ou sumido: usa a reserva da sessão anterior\n    if (s && typeof s === 'object'){")
g.rep("function load(){", "const BAK_KEY = SAVE_KEY + '-bak';\nfunction readSave(k){ try { const s = JSON.parse(localStorage.getItem(k) || 'null'); return s && typeof s === 'object' ? s : null; } catch(e) { return null; } }\nfunction load(){")
g.rep("let S = load();", "let S = load();\ntry { const raw = localStorage.getItem(SAVE_KEY); if (raw && readSave(SAVE_KEY)) localStorage.setItem(BAK_KEY, raw); } catch(e) {}   // guarda o save bom do começo da sessão")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, BAK_KEY, flash, flashLog, duck, load,")
g.save()
