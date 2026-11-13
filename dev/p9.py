import re, shutil, patchlib
shutil.copy('site/index.html', 'site/v2/index.html')
patchlib.P = 'site/v2/index.html'
g = patchlib.G()
# ---------- cabeça ----------
g.rep('viewport-fit=cover">', 'viewport-fit=cover">\n<base href="../">')
g.rep('<script src="data/sprites.js"></script>', '<script src="data/sprites.js"></script>\n<script src="vendor/three.min.js"></script>\n<script src="arena3d.js"></script>')
g.rep('<canvas id="arena" aria-label="Arena de batalha"></canvas>', '<canvas id="gl"></canvas>\n      <canvas id="arena" aria-label="Arena de batalha"></canvas>')
g.rep('<span>Toque numa carta e acerte a runa <i class="arrow">👈</i></span>', '<span>Arraste uma carta até o campo <i class="arrow">👆</i></span>')
g.rep("</style>", """
/* ---------- v2: arena 3D em pé ---------- */
.app::after{content:none!important;display:none!important}
#gl,#arena{position:absolute;inset:0;width:100%;height:100%;display:block}
#arena{pointer-events:none}
.ghost{position:fixed;left:0;top:0;z-index:30;width:70px;height:70px;margin:-84px 0 0 -35px;pointer-events:none;display:grid;place-items:center;filter:grayscale(1) drop-shadow(0 6px 6px rgba(0,0,0,.5));opacity:.65}
.ghost.ok{filter:drop-shadow(0 6px 6px rgba(0,0,0,.5));opacity:.95}
.ghost img{width:100%;height:100%;object-fit:contain}
.ghost[hidden]{display:none}
.hand .card{touch-action:none}
</style>""")
# ---------- mundo: duas pistas ----------
g.rep("function setWorld(w){ LW = Math.round(w); TOWX[0] = 160; TOWX[1] = LW - 160; SPAWNX[0] = 236; SPAWNX[1] = LW - 218; }", r"""/* v2: duas pistas. Cada pista é a mesma reta de antes; a pista 1 fica deslocada de OFF no x, então nada de uma pista
   alcança a outra. O castelo fica no "centro" (pista 2) e é atacado pelos portões, um em cada pista. */
const OFF = 100000, GUARDX = [330, 770];
const laneOf = x => Math.floor((x + OFF/2)/OFF), lpos = x => x - laneOf(x)*OFF;
function setWorld(w){ LW = 1100; TOWX[0] = 110; TOWX[1] = LW - 110; GUARDX[0] = 330; GUARDX[1] = LW - 330; SPAWNX[0] = 240; SPAWNX[1] = LW - 240; }
const ZONE = () => [TOWX[0] + 90, LW/2 - 40];                 // onde a criança pode soltar a carta
function twOf(team, x){ const l = Math.min(1, laneOf(x)), gd = B.guards[team][l]; return gd.alive ? gd : B.gates[team][l]; }
const allTowers = () => [B.towers[0], B.towers[1], B.guards[0][0], B.guards[0][1], B.guards[1][0], B.guards[1][1]];
const sideHp = i => (B.towers[i].hp/B.towers[i].maxhp*2 + B.guards[i][0].hp/B.guards[i][0].maxhp + B.guards[i][1].hp/B.guards[i][1].maxhp)/4;
function autoLane(team){                                      // pista com mais perigo; sem perigo, a da torre rival mais fraca
  const foe = B.ents.filter(e => e.alive && e.team !== team), th = [0, 1].map(l => foe.filter(e => laneOf(e.x) === l).reduce((a, e) => a + e.hp, 0));
  if (th[0] !== th[1]) return th[0] > th[1] ? 0 : 1;
  const gd = B.guards[1 - team];
  return gd[0].hp === gd[1].hp ? (Math.random() < .5 ? 0 : 1) : (gd[0].hp < gd[1].hp ? 0 : 1);
}
function mkGuard(team, lane, lvl){
  const k = 1 + .08*(lvl - 1);
  const t = {id:0, team, kind:'tower', guard:true, lane, x:GUARDX[team] + lane*OFF, z:14, r:46, hp:1500*k, dmg:46*k, hs:1.05, range:300, cd:1, alive:true, flash:0, collapse:0, recoil:0, face:team === 0 ? 1 : -1};
  t.maxhp = t.hp; return t;
}
function mkGate(team, lane, castle){ return {id:0, team, kind:'tower', gate:true, link:castle, lane, x:TOWX[team] + lane*OFF, z:14, r:74, hp:1, maxhp:1, dmg:castle.dmg, hs:castle.hs, range:castle.range, cd:1, alive:true, flash:0, collapse:0, recoil:0, face:castle.face}; }
function placeTowers(){ for (const tm of [0, 1]){ B.towers[tm].x = TOWX[tm] + 2*OFF; for (const l of [0, 1]){ B.guards[tm][l].x = GUARDX[tm] + l*OFF; B.gates[tm][l].x = TOWX[tm] + l*OFF; } } }""")
g.rep("x:TOWX[team], z:14, r:105, hp:3400*k,", "x:TOWX[team] + 2*OFF, z:14, r:105, hp:2600*k,")
g.rep("  B.towers = [mkTower(0, myLvl), mkTower(1, B.aiLvl)];", "  B.towers = [mkTower(0, myLvl), mkTower(1, B.aiLvl)];\n  B.guards = [[mkGuard(0, 0, myLvl), mkGuard(0, 1, myLvl)], [mkGuard(1, 0, B.aiLvl), mkGuard(1, 1, B.aiLvl)]];\n  B.gates = [0, 1].map(tm => [0, 1].map(l => mkGate(tm, l, B.towers[tm])));\n  B.bgp = {};")
g.rep("  B.towers.forEach((t, i) => { t.x = TOWX[i]; });\n  resizeArena();\n  buildBg(st.biome);", "  placeTowers();\n  GT3D.build(st.biome, {LW, TOWX, GUARDX});\n  resizeArena();")
g.rep("x:SPAWNX[team] + (team === 0 ? 10 : -10), z:ROWS[row]", "x:(o.pos != null ? o.pos : SPAWNX[team]) + (o.lane != null ? o.lane : autoLane(team))*OFF, z:ROWS[row]")
g.rep("  const u = spawnHero(team, id, {lvl, insp:o.insp, rev:o.rev, shine:o.shine});", "  const u = spawnHero(team, id, {lvl, insp:o.insp, rev:o.rev, shine:o.shine, lane:o.lane, pos:o.pos});")
n = g.t.count("B.towers[1 - u.team]"); assert n == 9, n
g.t = g.t.replace("B.towers[1 - u.team]", "twOf(1 - u.team, u.x)")
g.rep("twOf(1 - u.team, u.x); if (tw.alive && Math.abs(tw.x - px) <= 130 + tw.r)", "twOf(1 - u.team, px); if (tw.alive && Math.abs(tw.x - px) <= 130 + tw.r)")
g.rep("  const tw = B.towers[1 - team];", "  const tw = twOf(1 - team, x);")
g.rep("  u.x = clamp(nx, 30, LW - 30);", "  { const L0 = laneOf(u.x)*OFF; u.x = clamp(nx, L0 + 30, L0 + LW - 30); }")
g.rep("    if (o.kb) e.x = clamp(e.x + o.kb, 30, LW - 30);", "    if (o.kb){ const L0 = laneOf(e.x)*OFF; e.x = clamp(e.x + o.kb, L0 + 30, L0 + LW - 30); }")
g.rep("function dealDamage(e, amt, team, o){\n", "function dealDamage(e, amt, team, o){\n  if (e.link){ e.flash = .13; e = e.link; }                // bater no portão é bater no castelo\n")
g.rep("const key = e.kind === 'tower' ? 't' + e.team : e.id;", "const key = e.kind === 'tower' ? 't' + e.team + (e.guard ? e.lane : '') : e.id;")
g.rep("  if (e.kind === 'tower'){\n    e.collapse = .001;", """  if (e.kind === 'tower' && e.guard){                      // torre de guarda: abre a pista até o castelo
    e.collapse = .001; const gy = feetY(e);
    burst(e.x, gy - 60, '#ffd27a', 30, 240, 7, 1.1, {g:200}); burst(e.x, gy - 40, '#8a8aa8', 24, 190, 8, 1.3, {g:260});
    shake(.8); flash(.3); sfx('boom'); sfx('tower');
    showBanner(e.team === 1 ? 'Torre derrubada! Caminho livre!' : 'Sua torre caiu! Defenda o castelo!', e.team === 1 ? 'gold small' : 'red small');
    grafi(e.team === 1 ? 'viva' : 'ops', 1.6);
    return;
  }
  if (e.kind === 'tower'){
    e.collapse = .001; for (const gt of B.gates[e.team]) gt.alive = false;""")
g.rep("  for (const t of B.towers) if (!t.alive && t.collapse > 0 && t.collapse < 1)", "  for (const t of allTowers()) if (!t.alive && t.collapse > 0 && t.collapse < 1)")
g.rep("  for (const t of B.towers) updateTower(t, dt);", "  for (const tm of [0, 1]) for (const l of [0, 1]){ const gd = B.guards[tm][l], gt = B.gates[tm][l]; updateTower(gd, dt); gt.alive = B.towers[tm].alive; if (!gd.alive) updateTower(gt, dt); }   // o castelo só atira na pista em que a guarda caiu\n  for (const t of B.towers){ if (t.flash > 0) t.flash -= dt; if (t.recoil > 0) t.recoil -= dt; }")
g.rep("  deploy(1, pick, 0, 0, {});", """  let ln = autoLane(1);                                 // defende a pista apertada; sem aperto, ataca a torre mais fraca
  if (!mine.length && Math.random() < .25) ln = 1 - ln;
  deploy(1, pick, 0, 0, {lane:ln, pos:SPAWNX[1] - rand(0, 70)});""")
g.rep("const pa = B.towers[0].hp/B.towers[0].maxhp, pb = B.towers[1].hp/B.towers[1].maxhp;", "const pa = sideHp(0), pb = sideHp(1);")
g.rep("    const hp = B.towers[0].hp/B.towers[0].maxhp;", "    const hp = sideHp(0);")
g.rep("$('crE').textContent = Math.max(0, Math.ceil(B.towers[1].hp/B.towers[1].maxhp*100));", "$('crE').textContent = Math.max(0, Math.ceil(sideHp(1)*100));")
g.rep("$('crP').textContent = Math.max(0, Math.ceil(B.towers[0].hp/B.towers[0].maxhp*100));", "$('crP').textContent = Math.max(0, Math.ceil(sideHp(0)*100));")
g.rep("const foes = B.ents.filter(e => e.alive && e.team === 1), tw = B.towers[1];", "const foes = B.ents.filter(e => e.alive && e.team === 1), tw = twOf(1, Math.random() < .5 ? 0 : OFF);")
g.rep("    ctx.setTransform(dpr*SCL, 0, 0, dpr*SCL, -B.cam*dpr*SCL, 0);", "    ctx.rotate(-(B.clock*7 + p.x*.02)); ctx.translate(-p.x, -p.y);")
g.rep("  if (B.bgp.embers &&", "  if (B.bgp && B.bgp.embers &&"); g.rep("  if (B.bgp.snow &&", "  if (B.bgp && B.bgp.snow &&")
# ---------- carta: arrastar e soltar ----------
g.rep("function selectSlot(i){", "function selectSlot(i, lane, pos){")
g.rep("  sfx('tap');\n  openQuiz(i, 0, 0);\n}", "  sfx('tap');\n  openQuiz(i, 0, 0);\n  if (B.quiz){ B.quiz.lane = lane; B.quiz.pos = pos; }\n}")
g.rep("  deploy(0, q.id, q.x, q.y, {insp, rev:isRev, shine:perfect});", "  deploy(0, q.id, q.x, q.y, {insp, rev:isRev, shine:perfect, lane:q.lane, pos:q.pos});")
g.rep("""$('hand').addEventListener('pointerdown', e => {
  const el = e.target.closest('.card[data-slot]'); if (!el) return;
  e.preventDefault();
  selectSlot(+el.dataset.slot);
});""", r"""/* ---------- arrastar a carta e soltar no campo (ou tocar na carta e depois no campo) ---------- */
let DRAG = null;
const ghost = document.createElement('div'); ghost.className = 'ghost'; ghost.hidden = true; $('battle').appendChild(ghost);
function dropAt(cx, cy){
  const r = $('arenaWrap').getBoundingClientRect(), p = GT3D.pick(cx - r.left, cy - r.top); if (!p) return null;
  const [lo, hi] = ZONE(); if (p.pos < lo - 90 || p.pos > hi + 110 || Math.abs(p.wx) > 300) return null;
  return {lane:p.lane, pos:clamp(p.pos, lo, hi)};
}
const canDrag = () => B && !B.over && B.intro <= 0 && !B.quiz && !B.storm && !B.paused;
$('hand').addEventListener('pointerdown', e => {
  const el = e.target.closest('.card[data-slot]'); if (!el) return;
  e.preventDefault(); if (!canDrag()) return;
  ensureAudio(); sfx('tap');
  const i = +el.dataset.slot; DRAG = {i, x0:e.clientX, y0:e.clientY, moved:false, pid:e.pointerId, d:null};
  B.sel = i; ghost.innerHTML = heroIcon(B.hand[i]);
});
addEventListener('pointermove', e => {
  if (!DRAG || e.pointerId !== DRAG.pid) return;
  if (!DRAG.moved && Math.hypot(e.clientX - DRAG.x0, e.clientY - DRAG.y0) > 12) DRAG.moved = true;
  if (!DRAG.moved) return;
  DRAG.d = dropAt(e.clientX, e.clientY);
  ghost.hidden = false; ghost.style.transform = `translate(${e.clientX}px,${e.clientY}px)`; ghost.classList.toggle('ok', !!DRAG.d);
});
function endDrag(e){
  if (!DRAG || (e && e.pointerId !== DRAG.pid)) return;
  const D = DRAG; DRAG = null; ghost.hidden = true; if (!B) return;
  if (D.moved){ B.sel = null; if (D.d) selectSlot(D.i, D.d.lane, D.d.pos); else showBanner('Solte no seu lado do campo', 'blue small'); }
  else showBanner('Agora toque no campo', 'blue small');     // toque simples: a carta fica escolhida e o próximo toque decide o lugar
}
addEventListener('pointerup', endDrag); addEventListener('pointercancel', endDrag);
$('arenaWrap').addEventListener('pointerdown', e => {
  if (!B || B.sel == null || DRAG || !canDrag()) return;
  const d = dropAt(e.clientX, e.clientY); if (!d) return;
  const i = B.sel; B.sel = null; selectSlot(i, d.lane, d.pos);
});""")
# ---------- tela: medidas e desenho ----------
g.rep("function worldFor(){ const m = measureArena(); return clamp(m.w/m.laneSc, 1100, 1800); }", "function worldFor(){ return 1100; }")
g.rep("function resizeArena(){\n  if (cur !== 'battle') return;\n  const {w, h, botH, laneSc} = measureArena();", r"""function resizeArena(){
  if (cur !== 'battle') return;
  const r = $('arenaWrap').getBoundingClientRect(), w = Math.max(280, r.width), h = Math.max(300, r.height);
  const st = document.body.style, n = B ? B.hand.length : 4;
  st.setProperty('--ch', clamp(Math.min(h*.15, (w - 30)/(n*1.12)), 50, 112).toFixed(1) + 'px');
  st.setProperty('--kh', clamp(h*.062, 34, 52).toFixed(1) + 'px');
  st.setProperty('--hud', clamp(w*.045, 14, 20).toFixed(1) + 'px');
  SCL = 1; VW = w; VH = h; UI = 1.7; GY = 250;
  dpr = Math.min(window.devicePixelRatio || 1, 2.5);
  cv.width = Math.round(w*dpr); cv.height = Math.round(h*dpr);
  const top = $('btTop').offsetHeight + 12, bot = h - ($('btBottom').getBoundingClientRect().top - r.top) + 16;
  GT3D.resize(w, h, {top, bottom:bot}, dpr);
}
function resizeArenaOld(){
  if (cur !== 'battle') return;
  const {w, h, botH, laneSc} = measureArena();""")
g.rep("function renderArena(){\n  if (!B || !B.bg) return;", r"""/* v2: o mundo é desenhado em 3D (arena3d.js); heróis, projéteis e efeitos continuam em 2D, cada um projetado no ponto certo do campo */
const KS = 1.5;                                             // heróis e efeitos um pouco maiores que a escala do campo, para ler bem no celular
function atG(x, row, fn){ const q = GT3D.ground(x, row); ctx.save(); ctx.translate(q.sx, q.sy); ctx.scale(q.k*KS, q.k*KS); ctx.translate(-x, -(GY + 6 + row)); fn(); ctx.restore(); }
function scr(x, y){ const q = GT3D.ground(x, 15); return {sx:q.sx, sy:q.sy - q.k*KS*(GY + 21 - y), k:q.k*KS}; }
function drawProj3(p){
  if (p.t < 0) return;
  const S0 = GT3D.ground(p.x, 15), k = S0.k*KS, gy = GY + 21;
  const loc = (x, y) => { const q = scr(x, y); return {x:p.x + (q.sx - S0.sx)/k, y:gy + (q.sy - S0.sy)/k}; };
  const tr = p.trail, ang = p.ang; p.trail = tr.map(q => loc(q.x, q.y));
  const n = p.trail.length;
  if (n > 1){ const a = p.trail[n - 2], b = p.trail[n - 1]; if (Math.hypot(b.x - a.x, b.y - a.y) > .01) p.ang = Math.atan2(b.y - a.y, b.x - a.x); }
  else { const a = loc(p.x0, p.y0), b = loc(p.tx, p.ty); p.ang = Math.atan2(b.y - a.y, b.x - a.x); }
  ctx.save(); ctx.translate(S0.sx, S0.sy); ctx.scale(k, k); ctx.translate(-p.x, -gy); drawProj(p); ctx.restore();
  p.trail = tr; p.ang = ang;
}
function drawParts3(){
  for (const p of B.parts){
    const q = scr(p.x, p.y), a = Math.max(0, p.life/p.max); ctx.globalAlpha = a;
    if (p.kind === 'star') drawStar(q.sx, q.sy, p.sz*2.2*(.5 + a*.5)*q.k*1.25, p.col, p.life*5);
    else { ctx.fillStyle = p.col; ctx.beginPath(); ctx.arc(q.sx, q.sy, Math.max(.8, p.sz*(.4 + a*.6)*q.k*1.25), 0, 7); ctx.fill(); }
  }
  ctx.globalAlpha = 1; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  for (const t of B.texts){
    const q = scr(t.x, t.y), pop = 1 + .5*Math.max(0, 1 - (t.max - t.life)/.14); ctx.globalAlpha = Math.min(1, t.life/t.max*2.2);
    ctx.font = `900 ${(t.big ? 19 : 14)*(t.k || 1)*pop}px Nunito, sans-serif`; ctx.lineWidth = 3.5; ctx.strokeStyle = 'rgba(20,10,50,.85)'; ctx.lineJoin = 'round';
    ctx.strokeText(t.txt, q.sx, q.sy); ctx.fillStyle = t.col; ctx.fillText(t.txt, q.sx, q.sy);
  }
  ctx.globalAlpha = 1;
}
function drawTowerBars(){
  for (const tm of [0, 1]) for (const [key, t, w] of [['c' + tm, B.towers[tm], 62], ['g' + tm + 0, B.guards[tm][0], 42], ['g' + tm + 1, B.guards[tm][1], 42]]){
    if (!t.alive) continue; const p = GT3D.towerTop(key); if (!p) continue;
    const f = clamp(t.hp/t.maxhp, 0, 1), x = p.sx - w/2, y = p.sy - 12, h = key[0] === 'c' ? 9 : 7;
    ctx.fillStyle = 'rgba(14,10,50,.78)'; roundRect(x - 2, y - 2, w + 4, h + 4, 5); ctx.fill();
    ctx.fillStyle = TEAM[tm].c; roundRect(x, y, Math.max(4, w*f), h, 3.5); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(x + 2, y + 1, Math.max(0, w*f - 4), 2);
    if (key[0] === 'c'){ const s = Math.ceil(t.hp); ctx.font = '900 11px Nunito, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'bottom'; ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(14,10,50,.9)'; ctx.strokeText(s, p.sx, y - 2); ctx.fillStyle = '#fff'; ctx.fillText(s, p.sx, y - 2); }
  }
}
function drawGrafi3(){
  const t = B.towers[0], G = B.grafi; if (!t.alive) return;
  const pose = G.t > 0 ? G.pose : (t.hp < t.maxhp*.35 ? 'triste' : 'oi'), im = GRAFI_IMG[pose]; if (!im || !im.complete || !im.naturalWidth) return;
  const p = GT3D.towerTop('c0'); if (!p) return;
  const h = 44, w = im.naturalWidth*h/im.naturalHeight, hop = pose === 'viva' ? Math.abs(Math.sin(B.clock*9))*8 : Math.sin(B.clock*2.4)*1.5;
  ctx.save(); ctx.translate(p.sx - 52, p.sy + 52 - hop); ctx.rotate(pose === 'viva' ? Math.sin(B.clock*9)*.08 : Math.sin(B.clock*1.7)*.035); ctx.drawImage(im, -w/2, -h, w, h); ctx.restore();
}
function renderArena(){
  if (!B || !GT3D.ready || !B.guards) return;
  const tw = {}; for (const tm of [0, 1]){ tw['c' + tm] = B.towers[tm]; for (const l of [0, 1]) tw['g' + tm + l] = B.guards[tm][l]; }
  let zoom = null; if (B.zoom && !reduceMotion){ const wo = GT3D.worldOf(B.zoom.x); zoom = {q:easeOutCubic(Math.min(1, B.zoom.t/1.5)), wx:wo.wx, wz:wo.wz}; }
  const drop = DRAG ? (DRAG.d || null) : B.quiz && B.quiz.lane != null ? {lane:B.quiz.lane, pos:B.quiz.pos} : B.sel != null && !B.quiz ? null : undefined;
  if (drop === undefined) GT3D.setDrop(false); else { const [lo, hi] = ZONE(); GT3D.setDrop(true, drop ? drop.lane : null, drop ? drop.pos : 0, lo, hi); }
  GT3D.frame({towers:tw, intro:reduceMotion ? 0 : clamp((B.intro - .5)/(B.introMax - .5), 0, 1), shake:reduceMotion ? 0 : B.shake*B.shake*(S.settings.soft ? .3 : 1), zoom}, 1/60);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, VW, VH);
  const splats = B.splats; for (const s of splats){ B.splats = [s]; atG(s.x, s.z || 0, drawSplats); } B.splats = splats;
  const list = B.ents.map(u => ({u, sy:GT3D.ground(u.x, u.z).sy})).sort((a, b) => a.sy - b.sy);
  for (const o of list) atG(o.u.x, o.u.z, () => drawHero(o.u));
  drawTowerBars(); drawGrafi3();
  const says = B.says; for (const s of says){ B.says = [s]; atG(s.u.x, s.u.z, drawSays); } B.says = says;
  for (const p of B.projs) drawProj3(p);
  for (const f of B.fx) atG(f.x, 15, () => drawFx(f));
  drawParts3();
  if (B.timeScale < .95){ ctx.fillStyle = 'rgba(40,30,110,.18)'; ctx.fillRect(0, 0, VW, VH); }
  if (B.flash > 0){ ctx.fillStyle = `rgba(255,255,255,${B.flash*.8})`; ctx.fillRect(0, 0, VW, VH); }
  drawBossBar();
}
function renderArenaOld(){
  if (!B || !B.bg) return;""")
g.rep("let S = load();", "try { GT3D.init(document.getElementById('gl')); } catch(e) { console.error('3D', e); }\nlet S = load();")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, OFF, laneOf, lpos, twOf, sideHp, autoLane, GUARDX, TOWX, ZONE, dropAt, selectSlot2:selectSlot, get DRAG(){ return DRAG; },")
g.save()
