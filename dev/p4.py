from patchlib import G
g = G()
# ================= ÁLBUM =================
i = g.t.index('<section class="screen" id="book" hidden>'); j = g.t.index('<div class="bookstats" id="bookStats"></div>')
g.t = g.t[:i] + '''<section class="screen" id="book" hidden>
    <header class="top"><h2 class="ttl">Álbum da Tabuada</h2></header>
    <p class="sub">Cada conta é uma <b>figurinha</b>. Ela começa a lápis, ganha cor quando você acerta e fica <b>dourada</b> quando acerta rápido em dias diferentes. Complete uma página para dar a <b>Evolução Dourada</b> ao herói dela.</p>
    <div class="chips" id="albTabs"></div>
    <div class="albhead" id="albHead"></div>
    <div class="albpage" id="albPage"></div>
    <p class="cellinfo" id="albInfo">Toque numa figurinha para ver o truque dela.</p>
    <h3 class="sec">Tabela completa</h3>
    <p class="sub">Cada quadrinho é uma conta; 7 × 8 e 8 × 7 são a mesma.</p>
    ''' + g.t[j:]
g.rep('<span class="ic">📖</span>Tabuada</button>', '<span class="ic">📖</span>Álbum</button>')
g.rep("</style>", """
/* ---------- etapa 4: álbum de figurinhas, Evolução Dourada, Tempestade de Tinta ---------- */
#albTabs button{position:relative}
#albTabs button.done{border-color:var(--gold);color:var(--gold)}
#albTabs button.nv::after{content:"";position:absolute;right:-4px;top:-4px;width:11px;height:11px;border-radius:50%;background:#ff4d5e;border:2px solid #120f30}
.albhead{display:flex;align-items:center;gap:12px;margin:12px 0 8px;background:rgba(0,0,0,.22);border:1px solid var(--line);border-radius:14px;padding:8px 12px}
.albhead img{height:58px;width:auto;flex:none}
.albhead img.gold,.card.gold .pic,.rw img.gold{filter:sepia(.55) saturate(2.3) hue-rotate(-12deg) brightness(1.12) drop-shadow(0 0 6px #ffcf3f)}
.albhead .tx{flex:1;min-width:0;font-size:13px;color:var(--muted);display:grid;gap:5px}
.albhead .tx b{color:var(--text);font-size:15px}
.albpage{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}
.stk-card{position:relative;aspect-ratio:3/4;border-radius:12px;border:2px dashed #5a54b8;background:rgba(18,15,48,.55);color:#8f89d6;display:grid;grid-template-rows:auto auto 1fr;justify-items:center;align-content:start;padding:6px 4px 14px;gap:1px;overflow:hidden;min-width:0}
.stk-card .eq{font-weight:900;font-size:12px;white-space:nowrap}
.stk-card .res{font-family:var(--f-display);font-weight:400;font-size:clamp(17px,5.4vh,26px);line-height:1}
.stk-card .dots{display:grid;gap:1.5px;align-self:center;width:74%}
.stk-card .dots i{aspect-ratio:1;border-radius:50%;background:currentColor;opacity:.6}
.stk-card.k1,.stk-card.k2{border:2px solid #c9c9d6;background:repeating-linear-gradient(45deg,#f6f6fa 0 6px,#ececf3 6px 7px);color:#77778c}
.stk-card.k3{border:2px solid #fff;background:linear-gradient(0deg,hsl(var(--hue) 85% 64%) 0 50%,#f4f4f8 50%);color:#2a2266}
.stk-card.k4{border:3px solid #ffcf3f;background:linear-gradient(160deg,hsl(var(--hue) 88% 64%),hsl(calc(var(--hue) + 32) 82% 48%));color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.35);box-shadow:0 0 10px rgba(255,207,63,.5)}
.stk-card.k5{border:3px solid #fff;background:linear-gradient(120deg,#ff8ad8,#ffd36a,#7dd3ff,#c77dff,#ff8ad8);background-size:300% 100%;animation:rb 4s linear infinite;color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.45);box-shadow:0 0 14px rgba(255,255,255,.7)}
.stk-card .star{position:absolute;top:2px;right:5px;color:#fff6aa;font-size:13px}
.stk-card em{position:absolute;left:0;right:0;bottom:1px;font-style:normal;font-size:9px;font-weight:900;color:#b03a2e;background:#ffffffb0;text-shadow:none}
.stk-card em.nv{color:#fff;background:#ff4d5e;bottom:auto;top:42%;transform:rotate(-8deg);font-size:11px;padding:1px 0}
.stk-card.novo{animation:stickin .6s cubic-bezier(.2,1.6,.4,1) both}
.stk-card.pick{outline:3px solid #fff;outline-offset:1px}
@keyframes stickin{from{transform:scale(1.8) rotate(-14deg);opacity:0}}
.card.gold{border-color:#ffcf3f;box-shadow:inset 0 2px 0 rgba(255,255,255,.3),0 4px 0 #120f30,0 0 16px rgba(255,207,63,.85)}
.card.gold::before{content:"👑";position:absolute;left:50%;top:-11px;transform:translateX(-50%);font-size:14px;z-index:4}
.storm{position:absolute;right:10px;bottom:calc(22px + min(env(safe-area-inset-bottom,0px),10px));z-index:6;width:clamp(104px,18vw,160px);height:calc(var(--hud)*2.1);border-radius:999px;border:2px solid #ffffff66;background:rgba(14,10,50,.62);color:#fff;overflow:hidden;padding:0;font-size:calc(var(--hud)*.66);font-weight:900}
.storm .fill{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,#3f8cff,#b84dff,#ff5fd2);width:0;transition:width .3s}
.storm b{position:relative;text-shadow:0 1px 3px rgba(0,0,0,.7)}
.storm.full{border-color:#fff;animation:bossPulse 1s ease-in-out infinite;box-shadow:0 0 18px rgba(184,77,255,.95)}
.quiz.stormq{border-color:#ff5fd2;background:linear-gradient(170deg,rgba(46,34,140,.97),rgba(104,34,150,.97))}
.stormbar{height:8px;border-radius:4px;background:#120f30;overflow:hidden}
.stormbar b{display:block;height:100%;background:linear-gradient(90deg,#ff5fd2,#ffd36a)}
.quiz.stormq:not(.ok):not(.bad) > .stormbar{grid-column:1}
</style>""")
g.rep("function renderBook(){\n  const m = masteryCount();", r"""// ---------- álbum: uma página por tabuada, uma figurinha por conta ----------
const HERO_TAB = {arqueira:2, maga:5, tanque:10, bruma:3, fuinha:4, brasa:9, gelido:6, dinamite:7, trovao:8};
const HUE = [0, 210, 150, 330, 265, 45, 190, 25, 285, 5, 120];
const tabHero = n => ORDER.find(id => HERO_TAB[id] === n);
const tabFacts = n => Array.from({length:10}, (_, i) => FACT_BY[keyOf(n, i + 1)]);
const tabDone = n => tabFacts(n).every(f => isMastered(f.key));
const isGolden = id => !!HERO_TAB[id] && tabDone(HERO_TAB[id]);     // Evolução Dourada: a tabuada do herói inteira dominada
let albN = 0;
function stickerHTML(n, m){
  const k = keyOf(n, m), f = S.facts[k], st = stateOf(f), x = Math.min(n, m), y = Math.max(n, m);
  const retoque = st < 4 && f && f.ok >= 3 && f.errT.some(t => Date.now() - t < 7*DAY), novo = (S.albNew || []).includes(k);
  const dots = st >= 1 ? `<span class="dots" style="grid-template-columns:repeat(${y},1fr)">${'<i></i>'.repeat(x*y)}</span>` : '';
  return `<button type="button" class="stk-card k${st} ${novo ? 'novo' : ''}" data-a="${n}" data-b="${m}" style="--hue:${HUE[n]}" aria-label="${n} vezes ${m}, ${STATE_NAME[st]}">
    <span class="eq">${n} × ${m}</span><span class="res">${st >= 1 ? n*m : '?'}</span>${dots}${st >= 4 ? '<span class="star">★</span>' : ''}${novo ? '<em class="nv">NOVA!</em>' : retoque ? '<em>pede retoque</em>' : ''}</button>`;
}
function renderAlbum(){
  if (!albN){ albN = 2; for (let n = 2; n <= 10; n++) if (!tabDone(n)){ albN = n; break; } }
  const nv = S.albNew || [];
  $('albTabs').innerHTML = Array.from({length:10}, (_, i) => i + 1).map(n => `<button type="button" class="${n === albN ? 'on' : ''} ${tabDone(n) ? 'done' : ''} ${tabFacts(n).some(f => nv.includes(f.key)) ? 'nv' : ''}" data-n="${n}" aria-label="Página do ${n}">${n}</button>`).join('');
  const fs = tabFacts(albN), got = fs.filter(f => isMastered(f.key)).length, col = fs.filter(f => stateOf(S.facts[f.key]) >= 1).length, h = tabHero(albN), own = h && S.cards[h];
  $('albHead').innerHTML = `${h ? `<img class="${got === 10 ? 'gold' : ''}" alt="" src="${SPR[CARDS[h].spr][0].src}">` : ''}<span class="tx"><b>Página do ${albN}${h ? ' · herói: ' + CARDS[h].name : ''}</b>
    <span class="pg ${got === 10 ? 'max' : ''}"><i style="width:${got*10}%"></i><em>${got}/10 douradas · ${col}/10 no álbum</em></span>
    <span>${!h ? 'A página do 1 é só para aquecer.' : got === 10 ? `✨ Evolução Dourada conquistada: ${CARDS[h].name} luta 8% mais forte!` : `Deixe as 10 figurinhas douradas para ${CARDS[h].name} ganhar a Evolução Dourada${own ? '' : ' (quando você tiver esse herói)'}.`}</span></span>`;
  $('albPage').innerHTML = Array.from({length:10}, (_, i) => stickerHTML(albN, i + 1)).join('');
  if (nv.length){ const keys = fs.map(f => f.key); S.albNew = nv.filter(k => !keys.includes(k)); save(); }
}
$('albTabs').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; albN = +b.dataset.n; sfx('tap'); renderAlbum(); refreshBadges(); $('albInfo').textContent = 'Toque numa figurinha para ver o truque dela.'; });
$('albPage').addEventListener('click', e => {
  const b = e.target.closest('.stk-card'); if (!b) return; sfx('tap');
  for (const el of $('albPage').querySelectorAll('.pick')) el.classList.remove('pick'); b.classList.add('pick');
  const a = +b.dataset.a, m = +b.dataset.b, f = S.facts[keyOf(a, m)], st = stateOf(f);
  $('albInfo').innerHTML = st === 0 ? `<b>${a} × ${m}</b> ainda não apareceu nas batalhas. Quando aparecer, a figurinha entra no álbum a lápis.`
    : `<b>${a} × ${m} = ${a*m}</b> · ${STATE_NAME[st]}${f.n ? ` · ${f.ok} acerto${f.ok === 1 ? '' : 's'} em ${f.n}` : ''}<br>✏️ ${tipFor(a, m)}${st < 4 ? '<br>Para ficar dourada: acertar rápido em 3 dias diferentes.' : ''}`;
  if (st >= 1) speak(falaConta(a, m));
});
function renderBook(){
  renderAlbum();
  const m = masteryCount();""")
g.rep("""  const any = ORDER.some(canUp);
  $('tabbar').querySelector('[data-tab="deck"]').classList.toggle('dot', any);""", """  const any = ORDER.some(canUp);
  $('tabbar').querySelector('[data-tab="deck"]').classList.toggle('dot', any);
  $('tabbar').querySelector('[data-tab="book"]').classList.toggle('dot', !!(S.albNew && S.albNew.length));""")
g.rep("    if (res.mastered) B.newMastered++;", "    if (res.mastered){ B.newMastered++; (S.albNew = S.albNew || []).push(q.key); }")

# ================= EVOLUÇÃO DOURADA =================
g.rep("const c = CARDS[id], k = LVK(o.lvl || 1), tb = (o.insp ? 1.25 : 1)*(o.rev ? 1.1 : 1);", "const c = CARDS[id], gold = team === 0 && isGolden(id), k = LVK(o.lvl || 1), tb = (o.insp ? 1.25 : 1)*(o.rev ? 1.1 : 1)*(gold ? 1.08 : 1);")
g.rep("fly:!!c.fly, boss:!!c.boss, slow:0,", "fly:!!c.fly, boss:!!c.boss, slow:0, gold,")
g.rep("    if (u.boss) glow(u.x, fy - air - c.h*.45, c.h*.78, '#ff3a4a', .2 + .06*Math.sin(B.clock*4));", "    if (u.boss) glow(u.x, fy - air - c.h*.45, c.h*.78, '#ff3a4a', .2 + .06*Math.sin(B.clock*4));\n    if (u.gold) glow(u.x, fy - air - c.h*.45*bs, c.h*.7*bs, '#ffcf3f', .3 + .08*Math.sin(B.clock*4 + u.bob));")
g.rep("""    if (alive && !reduceMotion){ ctx.shadowColor = tm.c + 'cc'; ctx.shadowBlur = 5*dpr*SCL; }
    ctx.drawImage(f.img, -f.fx*k, -f.h*k, f.w*k, f.h*k);
    ctx.shadowBlur = 0;
  }""", """    if (alive && !reduceMotion){ ctx.shadowColor = (u.gold ? '#ffcf3f' : tm.c) + 'cc'; ctx.shadowBlur = (u.gold ? 9 : 5)*dpr*SCL; }
    if (u.gold && 'filter' in ctx) ctx.filter = 'sepia(.5) saturate(2.2) hue-rotate(-12deg) brightness(1.1)';
    ctx.drawImage(f.img, -f.fx*k, -f.h*k, f.w*k, f.h*k);
    ctx.shadowBlur = 0; if (u.gold && 'filter' in ctx) ctx.filter = 'none';
  }""")
g.rep("""class="card dk b${bd} ${own ? 'l' + lv : 'locked'} ${can ? 'can' : ''} ${extra || ''}\"""", """class="card dk b${bd} ${own ? 'l' + lv : 'locked'} ${own && isGolden(id) ? 'gold' : ''} ${can ? 'can' : ''} ${extra || ''}\"""")
g.rep("""class="card b${bd} l${lv}" data-slot""", """class="card b${bd} l${lv} ${isGolden(id) ? 'gold' : ''}" data-slot""")
g.rep("""    <p class="desc" style="color:var(--gold)">✨ ${c.ability}</p>""", """    <p class="desc" style="color:var(--gold)">✨ ${c.ability}</p>
    ${HERO_TAB[id] ? `<p class="desc" style="font-size:13px">${isGolden(id) ? '👑 <b>Evolução Dourada</b> conquistada: +8% de força.' : `👑 Herói da <b>tabuada do ${HERO_TAB[id]}</b>: deixe douradas as 10 figurinhas dessa página no Álbum para a Evolução Dourada (+8% de força).`}</p>` : ''}""")
g.rep("  B.aiLvl = cfg.lvl;", "  B.aiLvl = cfg.lvl;\n  B.goldBefore = ORDER.filter(isGolden);")
g.rep("  END = {won, lost, w, crowns,", "  const newGold = ORDER.filter(id => isGolden(id) && !B.goldBefore.includes(id));\n  END = {newGold, won, lost, w, crowns,")
g.rep("    ${streak}${bossMsg}${arena}${gateMsg}${hint}", """    ${streak}${bossMsg}${arena}${gateMsg}${hint}
    ${E.newGold.length ? `<div class="newarena">👑 <b>Evolução Dourada!</b><br>${E.newGold.map(id => CARDS[id].name).join(' e ')} agora ${E.newGold.length > 1 ? 'lutam' : 'luta'} 8% mais forte.</div>` : ''}
    ${E.newMastered ? `<p class="reward-line" style="margin:0">📒 ${E.newMastered} figurinha${E.newMastered > 1 ? 's douradas novas' : ' dourada nova'} no Álbum!</p>` : ''}""")

# ================= RUNA DE DUAS FACES + medidor da Tempestade =================
g.rep("splats:[], says:[], hitstop:0, zoom:null,", "splats:[], says:[], hitstop:0, zoom:null, ink:0, storm:null, faces:{}, faced:{},")
g.rep("  let [a, b] = pk.key.split('x').map(Number); if (Math.random() < .5) [a, b] = [b, a];", "  let [a, b] = pk.key.split('x').map(Number); if (Math.random() < .5) [a, b] = [b, a];\n  if (a !== b && B.faces[pk.key] === a + 'x' + b && pk.type !== 'present') [a, b] = [b, a];      // mostra a outra face da runa já acertada nesta batalha")
g.rep("  if (perfect){ B.mana[0] = Math.min(10, B.mana[0] + (c.cost <= 2 ? .5 : 1)); B.perfect++; grafi('viva', 1.1); }", """  if (perfect){ B.mana[0] = Math.min(10, B.mana[0] + (c.cost <= 2 ? .5 : 1)); B.perfect++; grafi('viva', 1.1); }
  let twoFaces = false;
  if (!present){
    B.ink = Math.min(1, B.ink + (perfect ? .2 : .1));                         // enche a Tempestade de Tinta
    const face = q.a + 'x' + q.b;
    if (q.a !== q.b && B.faces[q.key] && B.faces[q.key] !== face && !B.faced[q.key]){ B.faced[q.key] = true; twoFaces = true; B.mana[0] = Math.min(10, B.mana[0] + 1); }
    else if (!B.faces[q.key]) B.faces[q.key] = face;
  }""")
g.rep("  if (insp) bits.push('Este herói está INSPIRADO ✨');", "  if (twoFaces) bits.push(`🔁 Runa de duas faces: ${q.a} × ${q.b} = ${q.b} × ${q.a}! +1 de tinta 💧`);\n  if (insp) bits.push('Este herói está INSPIRADO ✨');")
g.rep("  q.closeAt = performance.now() + (newInsp || isRev ||", "  q.closeAt = performance.now() + (twoFaces ? 1500 : 0) + (newInsp || isRev ||")

# ================= TEMPESTADE DE TINTA =================
g.rep("""    <div class="streak" id="streak"></div>""", """    <div class="streak" id="streak"></div>
    <button class="storm" id="stormBtn" type="button" hidden aria-label="Tempestade de Tinta"><span class="fill" id="stormFill"></span><b id="stormTxt">Tempestade</b></button>""")
g.rep("  if (!B || B.over || B.intro > 0 || B.quiz || i >= B.hand.length) return;", "  if (!B || B.over || B.intro > 0 || B.quiz || B.storm || i >= B.hand.length) return;")
g.rep("/* ---------- a runa (a conta) ---------- */", r"""/* ---------- Tempestade de Tinta: o golpe especial da criança ----------
   A barra enche com os acertos (Perfeito enche o dobro). Cheia, vale 8 s de contas rápidas, só das que ela já sabe;
   cada acerto lança um raio de tinta no lado rival. Errar não pune: só encerra. Não mexe no domínio das runas. */
const STORM_T = 8;
function stormPool(){
  let p = FACTS.filter(f => stateOf(S.facts[f.key]) >= 4);
  if (p.length < 6) p = p.concat(FACTS.filter(f => stateOf(S.facts[f.key]) === 3));
  if (p.length < 6) p = p.concat(FACTS.filter(f => f.diff <= 2 && !p.includes(f)));
  return p;
}
function startStorm(){
  if (!B || B.over || B.quiz || B.storm || B.ink < 1 || B.intro > 0 || B.paused) return;
  ensureAudio(); B.ink = 0;
  B.storm = {endAt:performance.now() + STORM_T*1000, n:0, pool:stormPool(), lastKey:null, q:null};
  B.tsTarget = .35; showBanner('Tempestade de Tinta!', 'pink'); sfx('turbo'); sfx('chord'); grafi('viva', 2.5);
  $('quiz').hidden = false; stormNext();
}
function stormNext(){
  const st = B.storm, pool = st.pool.filter(f => f.key !== st.lastKey), f = pool[Math.floor(Math.random()*pool.length)];
  let a = f.a, b = f.b; if (Math.random() < .5) [a, b] = [b, a];
  st.q = {a, b, ans:a*b, input:'', opts:null}; st.lastKey = f.key;
  renderStorm();
}
function renderStorm(){
  const st = B.storm, q = st.q, left = Math.max(0, st.endAt - performance.now())/1000;
  let body;
  if (S.settings.mode === 'opcoes'){ if (!q.opts) q.opts = makeOptions(q); body = `<div class="choices">${q.opts.map(v => `<button type="button" data-v="${v}">${v}</button>`).join('')}</div>`; }
  else body = `<div class="keypad">${[1,2,3,4,5].map(n => `<button type="button" data-k="${n}">${n}</button>`).join('')}<button type="button" class="fn" data-k="back" aria-label="Apagar">⌫</button>${[6,7,8,9,0].map(n => `<button type="button" data-k="${n}">${n}</button>`).join('')}<button type="button" class="fn" data-k="ok" aria-label="Confirmar">✓</button></div>`;
  $('quiz').className = 'quiz stormq';
  $('quiz').innerHTML = `<div class="q-head"><span class="who"><b>🌩️ Tempestade de Tinta</b><span class="band rev">${st.n} raio${st.n === 1 ? '' : 's'}</span></span></div>
    <div class="q-row"><span>${q.a} × ${q.b} =</span><span class="q-ans ${q.input ? '' : 'empty'}" id="qAns">${q.input || '?'}</span></div>
    <div class="stormbar"><b id="stormBar" style="width:${(left/STORM_T*100).toFixed(1)}%"></b></div>` + body;
}
function stormBolt(){
  const foes = B.ents.filter(e => e.alive && e.team === 1), tw = B.towers[1];
  const tg = foes.length && Math.random() < .7 ? foes[Math.floor(Math.random()*foes.length)] : tw;
  const x = tg.x + rand(-24, 24), gy = GY + rand(4, 30), dmg = 85*LVK(deckAvg());
  B.projs.push({kind:'star', team:0, x0:x - 150, y0:GY - 330, x:x - 150, y:GY - 330, tx:x, ty:gy, t:0, dur:.3, arc:0, dmg, splash:70, ang:Math.atan2(gy - GY + 330, 150), trail:[], rot:rand(0, 6)});
}
function stormAnswer(val){
  const st = B.storm; if (!st) return;
  if (val === st.q.ans){ st.n++; stormBolt(); sfx('note', st.n % 5); stormNext(); } else { sfx('bad'); endStorm(); }
}
function stormKey(k){
  const st = B.storm; if (!st) return; const q = st.q;
  if (k === 'back') q.input = q.input.slice(0, -1);
  else if (k === 'ok'){ if (q.input) stormAnswer(+q.input); return; }
  else if (/^[0-9]$/.test(k)){ if (q.input.length >= 3) return; q.input += k; sfx('tap'); if (q.input.length >= String(q.ans).length){ stormAnswer(+q.input); return; } }
  const el = $('qAns'); if (el){ el.textContent = q.input || '?'; el.classList.toggle('empty', !q.input); }
}
function endStorm(){
  const st = B.storm; if (!st) return;
  B.storm = null; B.tsTarget = 1; $('quiz').hidden = true; $('quiz').innerHTML = '';
  if (!B.over) showBanner(st.n ? `${st.n} raio${st.n > 1 ? 's' : ''} de tinta!` : 'A tempestade passou', 'pink small');
  if (st.n >= 5) grafi('viva', 1.5);
}
$('stormBtn').addEventListener('pointerdown', e => { e.preventDefault(); startStorm(); });

/* ---------- a runa (a conta) ---------- */""")
g.rep("$('quiz').addEventListener('pointerdown', e => {\n  if (!B || !B.quiz) return;", """$('quiz').addEventListener('pointerdown', e => {
  if (B && B.storm){ e.preventDefault(); const sk = e.target.closest('[data-k]'), sv = e.target.closest('[data-v]'); if (sk) stormKey(sk.dataset.k); else if (sv) stormAnswer(+sv.dataset.v); return; }
  if (!B || !B.quiz) return;""")
g.rep("  if (cur !== 'battle' || !B) return;\n  if (B.quiz){", """  if (cur !== 'battle' || !B) return;
  if (B.storm){
    if (/^[0-9]$/.test(e.key)){ e.preventDefault(); if (S.settings.mode === 'opcoes'){ const o = B.storm.q.opts; if (o && o[+e.key - 1] !== undefined) stormAnswer(o[+e.key - 1]); } else stormKey(e.key); }
    else if (e.key === 'Backspace'){ e.preventDefault(); stormKey('back'); } else if (e.key === 'Enter'){ e.preventDefault(); stormKey('ok'); }
    return;
  }
  if (B.quiz){""")
g.rep("  if (B.quiz && B.quiz.closeAt && performance.now() >= B.quiz.closeAt) closeQuiz();", """  if (B.quiz && B.quiz.closeAt && performance.now() >= B.quiz.closeAt) closeQuiz();
  if (B.storm){ const l = B.storm.endAt - performance.now(), sb = $('stormBar'); if (sb) sb.style.width = Math.max(0, l/(STORM_T*10)).toFixed(1) + '%'; if (l <= 0) endStorm(); }""")
g.rep("  if (B.quiz) closeQuiz(true);\n  B.sel = null; renderHand();", "  if (B.quiz) closeQuiz(true);\n  if (B.storm) endStorm();\n  B.sel = null; renderHand();")
g.rep("$('streak').classList.toggle('insp', B.inspired); }\n}", """$('streak').classList.toggle('insp', B.inspired); }
  const sb = $('stormBtn'), full = B.ink >= 1;
  sb.hidden = B.ink <= 0 || !!B.storm || B.over; $('stormFill').style.width = (B.ink*100).toFixed(0) + '%';
  if (sb.classList.contains('full') !== full){ sb.classList.toggle('full', full); $('stormTxt').textContent = full ? '🌩️ Tempestade!' : 'Tempestade'; if (full) sfx('chord'); }
}""")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, startStorm, stormAnswer, endStorm, isGolden, tabDone, renderAlbum, HERO_TAB,")
g.save()
