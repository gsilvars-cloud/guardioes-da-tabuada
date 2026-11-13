from patchlib import G
g = G()

# ---------- música ----------
g.rep("function tone(f, dur, type, vol, f2, delay){", r"""/* ---------- música (assets/audio) ----------
   Faixas de Kevin MacLeod (incompetech.com), licença CC BY 4.0. Toca por um <audio> ligado ao mesmo contexto dos efeitos,
   para o volume poder subir e descer também no iPhone. */
const MUSIC = {menu:['menu', .5], b1:['batalha1', .42], b2:['batalha2', .45], boss:['chefao', .5], intro:['abertura', .6]};
const mus = {el:null, gain:null, key:null, want:null};
function musicFade(el, gain, to, ms, then){
  const t0 = performance.now(), from = gain ? gain.gain.value : el.volume;
  const step = () => {
    const q = Math.min(1, (performance.now() - t0)/ms), v = from + (to - from)*q;
    try { if (gain) gain.gain.value = v; else el.volume = v; } catch(e) {}
    if (q < 1) setTimeout(step, 40); else if (then) then();
  };
  step();
}
function music(key){
  mus.want = key;
  if (!S.settings.sound || S.settings.music === false) key = null;
  if (mus.key === key) return;
  const old = mus.el, og = mus.gain;
  if (old) musicFade(old, og, 0, 450, () => { try { old.pause(); } catch(e) {} });
  mus.key = key; mus.el = null; mus.gain = null;
  if (!key) return;
  const [file, vol] = MUSIC[key];
  const el = new Audio('assets/audio/' + file + '.mp3'); el.loop = true; el.preload = 'auto'; el.setAttribute('playsinline', '');
  let gain = null;
  try { if (ac){ const src = ac.createMediaElementSource(el); gain = ac.createGain(); gain.gain.value = 0; src.connect(gain); gain.connect(ac.destination); } else el.volume = 0; } catch(e) { gain = null; }
  mus.el = el; mus.gain = gain;
  const p = el.play();
  if (p && p.catch) p.catch(() => { if (mus.el === el){ mus.key = null; mus.el = null; mus.gain = null; } });   // ainda sem toque na tela: tenta de novo no próximo toque
  musicFade(el, gain, vol, 900);
}
document.addEventListener('visibilitychange', () => { if (!mus.el) return; try { if (document.hidden) mus.el.pause(); else mus.el.play().catch(() => {}); } catch(e) {} });
function tone(f, dur, type, vol, f2, delay){""")
g.rep("""  if (ac && ac.state === 'suspended') ac.resume().catch(() => {});
}""", """  if (ac && ac.state === 'suspended') ac.resume().catch(() => {});
  if (mus.want && mus.key !== mus.want) music(mus.want);
}""")
g.rep("  if (id === 'battle') requestAnimationFrame(resizeArena);\n}", "  if (id === 'battle') requestAnimationFrame(resizeArena);\n  else if (!window.__introOn) music('menu');\n}")
g.rep("settings:{mode:'digitar', focus:[], sound:true, age:'m', speak:true, calm:false, hint:false}", "settings:{mode:'digitar', focus:[], sound:true, music:true, age:'m', speak:true, calm:false, hint:false}")
g.rep("""      <div class="seg" id="soundSeg"><button type="button" data-s="1">Ligado</button><button type="button" data-s="0">Desligado</button></div>""",
      """      <div class="seg" id="soundSeg"><button type="button" data-s="1">Ligado</button><button type="button" data-s="0">Desligado</button></div>
      <h3 style="margin-top:12px">Música</h3>
      <div class="seg" id="musicSeg"><button type="button" data-s="1">Ligada</button><button type="button" data-s="0">Desligada</button></div>""")
g.rep("  for (const [id, key] of [['speakSeg', 'speak'], ['calmSeg', 'calm'], ['hintSeg', 'hint']])\n    for (const b of $(id)", "  for (const [id, key] of [['speakSeg', 'speak'], ['calmSeg', 'calm'], ['hintSeg', 'hint'], ['musicSeg', 'music']])\n    for (const b of $(id)")
g.rep("for (const [id, key] of [['speakSeg', 'speak'], ['calmSeg', 'calm'], ['hintSeg', 'hint']])\n  $(id).addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.settings[key] = b.dataset.s === '1'; save(); ensureAudio(); sfx('tap');",
      "for (const [id, key] of [['speakSeg', 'speak'], ['calmSeg', 'calm'], ['hintSeg', 'hint'], ['musicSeg', 'music']])\n  $(id).addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; S.settings[key] = b.dataset.s === '1'; save(); ensureAudio(); sfx('tap'); if (key === 'music') music(mus.want);")
g.rep("S.settings.sound = b.dataset.s === '1'; save(); ensureAudio(); sfx('tap'); renderSettings(); });", "S.settings.sound = b.dataset.s === '1'; save(); ensureAudio(); sfx('tap'); music(mus.want); renderSettings(); });")
g.rep("""      <button type="button" class="btn-ghost danger" id="resetBtn">Apagar todo o progresso</button>""",
      """      <p style="font-size:12px">Música: Kevin MacLeod (incompetech.com), licença Creative Commons Atribuição 4.0. Um jogo do OF Studio.</p>
      <button type="button" class="btn-ghost danger" id="resetBtn">Apagar todo o progresso</button>""")
g.rep("  showBanner(boss ? 'Chefão à vista!' : 'Prepare-se!', boss ? 'red' : 'gold');", "  showBanner(boss ? 'Chefão à vista!' : 'Prepare-se!', boss ? 'red' : 'gold');\n  music(boss ? 'boss' : 'b1');")
g.rep("B.double = true; showBanner('Tinta dupla!', 'pink'); sfx('double'); }", "B.double = true; showBanner('Tinta dupla!', 'pink'); sfx('double'); if (!B.boss) music('b2'); }")
g.rep("  B.over = true; B.endT = towerDown ? 2.6 : 1.6; B.result = w;", "  B.over = true; B.endT = towerDown ? 2.6 : 1.6; B.result = w;\n  music(null); grafi(w === 0 ? 'viva' : w === 1 ? 'triste' : 'oi', 99);")

# ---------- estado novo da batalha ----------
g.rep("ai:{think:3.4}, result:null, crowns:[0, 0], cam:0, kills:[0, 0], flash:0};", "ai:{think:3.4}, result:null, crowns:[0, 0], cam:0, kills:[0, 0], flash:0, splats:[], says:[], hitstop:0, zoom:null, grafi:{pose:'oi', t:0}};")

# ---------- pausa de impacto ----------
g.rep("function shake(a){ if (!reduceMotion) B.shake = Math.max(B.shake, a); }",
      """function shake(a){ if (!reduceMotion){ B.shake = Math.max(B.shake, a); if (a >= .4) hitStop(a >= .8 ? .09 : .06); } }
function hitStop(t){ if (!reduceMotion && B) B.hitstop = Math.max(B.hitstop || 0, t); }
// respingo de tinta no chão, na cor de quem bateu
function splat(x, team, r){
  if (!B) return;
  B.splats.push({x:x + rand(-8, 8), z:rand(0, 34), r:(r || 1)*rand(.8, 1.25), team, life:6, seed:Math.random()*1000 | 0});
  if (B.splats.length > 46) B.splats.shift();
}
// falas curtas dos heróis
const SAY = {arqueira:['Na mira!', 'Alvo certo!'], maga:['Abracadabra!', 'Brilha, brilha!'], tanque:['Deixa comigo!', 'Firme!'], bruma:['Eu cuido!', 'Florzinha!'],
  fuinha:['Zum!', 'Peguei!'], brasa:['Grrr!', 'Fogo!'], gelido:['Brrr!', 'Gelou!'], dinamite:['Cabum!', 'Hihihi!'], trovao:['Pelo trovão!', 'Zás!'],
  boss1:['Quem ousa?'], boss2:['Hmmmm...'], boss3:['Sombras!'], boss4:['ROOOAR!'], boss5:['Que frio!'], boss6:['Meu ouro!'], boss7:['Insolente!']};
function say(u, txt){ if (!B || !txt) return; B.says = B.says.filter(s => s.u !== u); B.says.push({u, txt, life:1.5, max:1.5}); }
// Grafi, o mascote, reage do alto do castelo
function grafi(pose, t){ if (B && B.grafi && !(B.over && B.grafi.t > 50)){ B.grafi.pose = pose; B.grafi.t = t || 1.3; } }""")
g.rep("  B.timeScale += (B.tsTarget - B.timeScale)*Math.min(1, dt/.12);      // a câmera lenta entra e sai em ~150 ms",
      "  if (B.hitstop > 0){ B.hitstop -= dt; updateFx(dt*.2); return; }      // pausa de impacto: o golpe forte congela o jogo por um instante\n  B.timeScale += (B.tsTarget - B.timeScale)*Math.min(1, dt/.12);      // a câmera lenta entra e sai em ~150 ms")
g.rep("    B.endT -= dt; updateFx(dt*.6);", "    B.endT -= dt; if (B.zoom) B.zoom.t += dt; updateFx(dt*(B.zoom ? .4 : .6));")

# ---------- entrada: poeira ao pousar, fala ----------
g.rep("  if (u.spawnT > 0){ u.spawnT -= dt; return; }",
      """  if (u.spawnT > 0){
    u.spawnT -= dt;
    if (!u.landed && u.spawnT <= u.spawnDur*.56){ u.landed = true; if (!u.fly){ burst(u.x, feetY(u), 'rgba(255,255,255,.75)', 10, 85, 4, .45, {flat:true, g:-10}); if (u.boss || CARDS[u.card].r >= 22) shake(.2); } }
    return;
  }""")
g.rep("  sfx('spawn');\n  return u;", "  sfx('spawn');\n  if (team === 0 || Math.random() < .35){ const ls = SAY[id]; if (ls) say(u, ls[Math.floor(Math.random()*ls.length)]); }\n  return u;")
g.rep("  shake(.8); B.flash = .35; sfx('boom'); sfx('double');", "  shake(.8); B.flash = .35; sfx('boom'); sfx('double'); say(u, SAY[id][0]); grafi('ops', 2);")

# ---------- golpes: respingos ----------
g.rep("      shake(.12);\n    }\n    burst(u.x + u.face*c.range*.9", "      shake(.12); splat(tg.x - u.face*tg.r*.3, u.team, tg.kind === 'tower' ? 1.1 : .8);\n    }\n    burst(u.x + u.face*c.range*.9")
g.rep("function impact(p){\n  const gy = p.ty;", "function impact(p){\n  const gy = p.ty;\n  if (p.kind !== 'heal') splat(p.tx, p.team, p.splash ? 1.25 : .7);")
g.rep("  B.kills[1 - e.team]++;", "  B.kills[1 - e.team]++;\n  splat(e.x, 1 - e.team, 1.9); hitStop(.045); if (e.team === 1) grafi('viva', 1.2);")
g.rep("    shake(1); B.flash = .5; sfx('boom'); sfx('tower');\n    endMatch(e.team === 1 ? 0 : 1, true);",
      """    shake(1); B.flash = .5; sfx('boom'); sfx('tower');
    B.zoom = {x:e.x, y:gy - 90, t:0};                              // a câmera se aproxima do castelo que cai
    if (e.team === 1) for (const col of ['#3f8cff', '#ffcf3f', '#ff5fd2', '#35d483', '#b84dff']) burst(e.x + rand(-70, 70), gy - rand(60, 190), col, 16, 300, 6, 1.6, {g:230});
    endMatch(e.team === 1 ? 0 : 1, true);""")
g.rep("  for (const p of B.parts){ p.life -= dt;", "  for (const s of B.splats) s.life -= dt;\n  if (B.splats.length && B.splats[0].life <= 0) B.splats = B.splats.filter(s => s.life > 0);\n  for (const s of B.says) s.life -= dt;\n  if (B.says.length) B.says = B.says.filter(s => s.life > 0 && s.u.alive);\n  if (B.grafi.t > 0 && B.grafi.t < 50) B.grafi.t -= dt;\n  for (const p of B.parts){ p.life -= dt;")

# ---------- números de dano com peso ----------
g.rep("    if (tx){ tx.sum += amt; tx.txt = Math.round(tx.sum); tx.life = tx.max; }", "    if (tx){ tx.sum += amt; tx.txt = Math.round(tx.sum); tx.life = tx.max; tx.k = clamp(.9 + tx.sum/260, 1, 1.8); }")
g.rep("txt:Math.round(amt), col:team === 0 ? '#ffe27a' : '#ff9aa4', life:.8, max:.8});", "txt:Math.round(amt), col:team === 0 ? '#ffe27a' : '#ff9aa4', life:.8, max:.8, k:clamp(.9 + amt/260, 1, 1.8)});")
g.rep("    ctx.font = `900 ${(t.big ? 17 : 12)*UI*1.15}px Nunito, sans-serif`;", "    const pop = 1 + .5*Math.max(0, 1 - (t.max - t.life)/.14);\n    ctx.font = `900 ${(t.big ? 17 : 12)*UI*1.15*(t.k || 1)*pop}px Nunito, sans-serif`;")

# ---------- esticar e amassar ----------
g.rep("""    const e = easeOutBack(clamp(p*1.5, 0, 1)); P.sx = P.sy = .3 + .7*e;
    P.dy = -Math.max(0, 1 - p*2.4)*46;
    return P;""", """    const e = easeOutBack(clamp(p*1.5, 0, 1)); P.sx = P.sy = .3 + .7*e;
    P.dy = -Math.max(0, 1 - p*2.4)*46;
    if (p > .42 && !u.fly){ const l = Math.sin(clamp((p - .42)/.32, 0, 1)*Math.PI); P.sy *= 1 - .17*l; P.sx *= 1 + .13*l; }     // amassa ao pousar
    return P;""")
g.rep("  if (u.hurtT > 0){ P.i = 5; P.dx = -u.face*7*(u.hurtT/.26); P.rot = -.05; return P; }",
      "  if (u.hurtT > 0){ const h = u.hurtT/.26; P.i = 5; P.dx = -u.face*7*h; P.rot = -.05; P.sx = 1 + .07*h; P.sy = 1 - .07*h; return P; }")
g.rep("      if (ph < a.hit){ P.i = 3; P.dx = -u.face*5*(ph/a.hit); P.sx = 1 + .02*(ph/a.hit); }",
      "      if (ph < a.hit){ const w = ph/a.hit; P.i = 3; P.dx = -u.face*6*w; P.sx = 1 - .05*w; P.sy = 1 + .05*w; }")
g.rep("P.dx = u.face*(c.melee ? 15 : 5)*q*(1 - clamp((ph - a.hit - .14)/.1, 0, 1)); P.sx = 1 + .03*(1 - q); }",
      "P.dx = u.face*(c.melee ? 17 : 6)*q*(1 - clamp((ph - a.hit - .14)/.1, 0, 1)); P.sx = 1 + .11*(1 - q); P.sy = 1 - .07*(1 - q); }")

# ---------- entrada desenhada: traço de lápis, depois a cor enche ----------
g.rep("""  if (alive && !reduceMotion){ ctx.shadowColor = tm.c + 'cc'; ctx.shadowBlur = 5*dpr*SCL; }
  ctx.drawImage(f.img, -f.fx*k, -f.h*k, f.w*k, f.h*k);
  ctx.shadowBlur = 0;""", """  if (alive && u.spawnT > 0){
    const sp = 1 - u.spawnT/u.spawnDur, fill = clamp((sp - .1)/.72, 0, 1), hh = f.h*k;
    ctx.save();
    if ('filter' in ctx){ ctx.filter = 'grayscale(1) brightness(1.75) contrast(.7)'; ctx.globalAlpha = P.al*.92; } else ctx.globalAlpha = P.al*.3;
    ctx.drawImage(f.img, -f.fx*k, -hh, f.w*k, hh);
    ctx.restore();
    if (fill > 0){
      ctx.save(); ctx.beginPath(); ctx.rect(-f.fx*k - 6, -hh*fill, f.w*k + 12, hh*fill + 6); ctx.clip();
      ctx.drawImage(f.img, -f.fx*k, -hh, f.w*k, hh); ctx.restore();
      if (fill < 1){ ctx.fillStyle = tm.l; ctx.globalAlpha = .85; ctx.fillRect(-f.fx*k, -hh*fill - 1.5, f.w*k, 3); ctx.globalAlpha = P.al; }
    }
  } else {
    if (alive && !reduceMotion){ ctx.shadowColor = tm.c + 'cc'; ctx.shadowBlur = 5*dpr*SCL; }
    ctx.drawImage(f.img, -f.fx*k, -f.h*k, f.w*k, f.h*k);
    ctx.shadowBlur = 0;
  }""")

# ---------- desenho: respingos, falas, Grafi, aproximação ----------
g.rep("  drawGround();\n  for (const t of B.towers) drawTower(t);", "  drawGround();\n  drawSplats();\n  for (const t of B.towers) drawTower(t);\n  drawGrafi();")
g.rep("  for (const u of list) drawHero(u);", "  for (const u of list) drawHero(u);\n  drawSays();")
g.rep("  if (B.shake > 0 && !reduceMotion) ctx.translate(rand(-1, 1)*B.shake*9, rand(-1, 1)*B.shake*7);\n  drawBg();",
      """  if (B.shake > 0 && !reduceMotion) ctx.translate(rand(-1, 1)*B.shake*9, rand(-1, 1)*B.shake*7);
  if (B.zoom && !reduceMotion){ const z = 1 + .17*easeOutCubic(Math.min(1, B.zoom.t/1.5)), zx = B.zoom.x - B.cam, zy = B.zoom.y; ctx.translate(zx*(1 - z), zy*(1 - z)); ctx.scale(z, z); }
  drawBg();""")
g.rep("function roundRect(x, y, w, h, r){", """function drawSplats(){
  for (const s of B.splats){
    const a = Math.min(1, s.life/2.2)*.5, y = GY + 8 + s.z; let sd = s.seed + 1;
    const rn = () => (sd = (sd*16807) % 2147483647)/2147483647;
    ctx.globalAlpha = a; ctx.fillStyle = TEAM[s.team].c;
    ctx.beginPath(); ctx.ellipse(s.x, y, 17*s.r, 5.5*s.r, 0, 0, 7); ctx.fill();
    for (let i = 0; i < 5; i++){ const an = rn()*6.28, d = (14 + rn()*16)*s.r, rr = (2 + rn()*4)*s.r; ctx.beginPath(); ctx.ellipse(s.x + Math.cos(an)*d, y + Math.sin(an)*d*.32, rr, rr*.42, 0, 0, 7); ctx.fill(); }
    ctx.globalAlpha = a*.6; ctx.fillStyle = TEAM[s.team].l; ctx.beginPath(); ctx.ellipse(s.x - 4*s.r, y - 1.2*s.r, 7*s.r, 1.8*s.r, 0, 0, 7); ctx.fill();
  }
  ctx.globalAlpha = 1;
}
const GRAFI_IMG = {};
for (const k of ['oi', 'viva', 'ops', 'triste']){ const im = new Image(); im.src = 'assets/grafi/' + k + '.webp'; GRAFI_IMG[k] = im; }
function drawGrafi(){
  const t = B.towers[0], G = B.grafi; if (!t.alive && t.collapse > .3) return;
  const pose = G.t > 0 ? G.pose : (t.hp < t.maxhp*.35 ? 'triste' : 'oi'), im = GRAFI_IMG[pose];
  if (!im || !im.complete || !im.naturalWidth) return;
  const fr = SPR.castelo0[0], ch = fr.h*(CASTW/fr.w), by = feetY(t) + 6, h = 50, w = im.naturalWidth*h/im.naturalHeight;
  const hop = pose === 'viva' ? Math.abs(Math.sin(B.clock*9))*9 : Math.sin(B.clock*2.4)*1.6;
  ctx.save(); ctx.translate(t.x - 8, by - ch*.93 - hop);
  ctx.rotate(pose === 'viva' ? Math.sin(B.clock*9)*.08 : Math.sin(B.clock*1.7)*.035);
  ctx.drawImage(im, -w/2, -h, w, h); ctx.restore();
}
function drawSays(){
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  for (const s of B.says){
    const u = s.u, c = CARDS[u.card], age = s.max - s.life, pop = easeOutBack(Math.min(1, age/.16)), al = Math.min(1, s.life/.25);
    const fs = 10.5*UI, y = feetY(u) - airOf(u) - c.h*(u.boss ? 1 : 1.04) - 24*UI;
    ctx.font = `900 ${fs}px Nunito, sans-serif`;
    const w = ctx.measureText(s.txt).width + 14*UI, h = fs + 9*UI;
    ctx.save(); ctx.globalAlpha = al; ctx.translate(u.x, y); ctx.scale(pop, pop);
    ctx.fillStyle = '#ffffff'; roundRect(-w/2, -h/2, w, h, h/2); ctx.fill();
    ctx.beginPath(); ctx.moveTo(-5*UI, h/2 - 1); ctx.lineTo(0, h/2 + 6*UI); ctx.lineTo(5*UI, h/2 - 1); ctx.fill();
    ctx.strokeStyle = 'rgba(20,10,50,.25)'; ctx.lineWidth = 1; roundRect(-w/2, -h/2, w, h, h/2); ctx.stroke();
    ctx.fillStyle = '#2a2266'; ctx.fillText(s.txt, 0, .5);
    ctx.restore();
  }
}
function roundRect(x, y, w, h, r){""")

# ---------- Grafi reage às respostas ----------
g.rep("    q.state = 'bad';\n    q.minClose = performance.now() + 1500;", "    q.state = 'bad'; grafi('ops', 1.8);\n    q.minClose = performance.now() + 1500;")
g.rep("  if (perfect){ B.mana[0] = Math.min(10, B.mana[0] + (c.cost <= 2 ? .5 : 1)); B.perfect++; }", "  if (perfect){ B.mana[0] = Math.min(10, B.mana[0] + (c.cost <= 2 ? .5 : 1)); B.perfect++; grafi('viva', 1.1); }")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, music, mus, splat, say, grafi, hitStop,")
g.save()
