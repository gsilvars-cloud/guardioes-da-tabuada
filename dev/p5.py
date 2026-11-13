from patchlib import G
g = G()
# ================= CHEFÃO COM PONTO FRACO: escudo de runa =================
g.rep("  u.row = 1; u.z = ROWS[1]; u.spawnT = u.spawnDur = 1.5;", "  u.row = 1; u.z = ROWS[1]; u.spawnT = u.spawnDur = 1.5;\n  u.bsT = 9; u.bshield = false; u.vuln = 0;                 // primeiro escudo 9 s depois de chegar")
g.rep("  if (u.flash > 0) u.flash -= dt;\n  if (u.hurtT > 0) u.hurtT -= dt;", """  if (u.flash > 0) u.flash -= dt;
  if (u.boss && B.boss && u.team === 1 && u.spawnT <= 0){                       // escudo de runa do chefão
    if (u.vuln > 0) u.vuln -= dt;
    if (!u.bshield){ u.bsT -= dt; if (u.bsT <= 0){ u.bshield = true; u.bsLeft = 14; showBanner('Escudo de runa!', 'blue small'); sfx('double'); } }
    else { u.bsLeft -= dt; if (u.bsLeft <= 0){ u.bshield = false; u.bsT = 14; } }
  }
  if (u.hurtT > 0) u.hurtT -= dt;""")
g.rep("  if (e.kind === 'troop'){ const c = CARDS[e.card]; if (c.armor) amt *= 1 - c.armor; }", "  if (e.kind === 'troop'){ const c = CARDS[e.card]; if (c.armor) amt *= 1 - c.armor; if (e.bshield) amt *= .35; else if (e.vuln > 0) amt *= 2; }")
g.rep("/* ---------- a runa (a conta) ---------- */", r"""/* ---------- escudo do chefão: uma conta da ilha quebra o escudo ---------- */
function openShieldQuiz(){
  const u = B && B.bossU; if (!B || B.over || B.quiz || B.storm || B.paused || !u || !u.alive || !u.bshield) return;
  ensureAudio(); sfx('tap');
  const fo = focusList(), seen = f => S.facts[f.key] && S.facts[f.key].seen;
  let pool = FACTS.filter(f => seen(f) && (!fo.length || fo.includes(f.a) || fo.includes(f.b)));
  if (!pool.length) pool = FACTS.filter(seen);
  if (!pool.length) pool = FACTS.filter(f => f.diff <= 2);
  const f = weighted(pool); let a = f.a, b = f.b; if (Math.random() < .5) [a, b] = [b, a];
  const calm = !!S.settings.calm;
  B.quiz = {slot:-1, id:u.card, x:0, y:0, a, b, ans:a*b, input:'', t0:performance.now(), band:1, key:f.key, type:'shield', pk:{key:f.key, type:'shield'},
    state:'ask', closeAt:0, minClose:0, hinted:false, hint:false, calm};
  B.tsTarget = calm ? 0 : .2; renderQuiz(); $('quiz').hidden = false;
}
function breakShield(){
  const u = B.bossU; if (!u || !u.alive) return;
  u.bshield = false; u.bsT = 16; u.vuln = 4; u.stun = Math.max(u.stun || 0, 2.2);
  for (const e of B.ents) if (e.alive && e.team === 0){ e.stun = 0; e.slow = 0; }       // solta os heróis presos ou congelados
  const gy = feetY(u), c = CARDS[u.card];
  B.fx.push({type:'ring', x:u.x, y:gy, r0:20, r1:230, t:0, dur:.7, col:'#9fe3ff', w:9});
  B.fx.push({type:'ring', x:u.x, y:gy, r0:10, r1:150, t:0, dur:.5, col:'#ffffff', w:4});
  burst(u.x, gy - c.h*.5, '#bfefff', 34, 260, 5, .9, {kind:'star', g:60});
  shake(.6); B.flash = .3; sfx('boom'); sfx('chord'); grafi('viva', 1.6);
  showBanner('Escudo quebrado! Dano em dobro!', 'gold small');
}
$('shieldBtn').addEventListener('pointerdown', e => { e.preventDefault(); openShieldQuiz(); });

/* ---------- a runa (a conta) ---------- */""")
g.rep("  const badge = q.type === 'present' ? '<span class=\"band new\">conta nova</span>'", "  const badge = q.type === 'shield' ? '<span class=\"band rev\">Escudo do chefão 🛡️</span>' : q.type === 'present' ? '<span class=\"band new\">conta nova</span>'")
g.rep("  const q = B && B.quiz; if (!q) return;\n  const R = B.rn; R.count--; R.recent.pop();", "  const q = B && B.quiz; if (!q) return;\n  if (q.type === 'shield'){ closeQuiz(); return; }\n  const R = B.rn; R.count--; R.recent.pop();")
g.rep("  const res = recordAnswer(q.key, ok, ms, {hinted:q.hinted});\n  B.answered++;", """  if (q.type === 'shield'){                                // conta do escudo: vale para o aprendizado, não gasta tinta nem chama herói
    const rs = recordAnswer(q.key, ok, ms, {hinted:q.hinted});
    B.answered++; S.recent.push(ok ? 1 : 0); if (S.recent.length > 10) S.recent.shift();
    if (ok){ B.correct++; B.times.push(ms); if (rs.mastered){ B.newMastered++; (S.albNew = S.albNew || []).push(q.key); } speak(falaConta(q.a, q.b)); closeQuiz(); breakShield(); }
    else { B.wrong.push({a:q.a, b:q.b}); q.state = 'bad'; grafi('ops', 1.8); q.minClose = performance.now() + 1500; q.closeAt = performance.now() + 4000; speak(falaConta(q.a, q.b)); sfx('bad'); renderQuiz(); }
    return;
  }
  const res = recordAnswer(q.key, ok, ms, {hinted:q.hinted});
  B.answered++;""")
g.rep("    if (u.gold) glow(u.x, fy - air - c.h*.45*bs, c.h*.7*bs, '#ffcf3f', .3 + .08*Math.sin(B.clock*4 + u.bob));", """    if (u.gold) glow(u.x, fy - air - c.h*.45*bs, c.h*.7*bs, '#ffcf3f', .3 + .08*Math.sin(B.clock*4 + u.bob));
    if (u.bshield){                                        // bolha do escudo de runa
      const cy = fy - air - c.h*.5, pr = 1 + .03*Math.sin(B.clock*5);
      ctx.save(); ctx.globalAlpha = P.al*.9; ctx.strokeStyle = '#bfefff'; ctx.lineWidth = 4; ctx.fillStyle = 'rgba(120,200,255,.16)';
      ctx.beginPath(); ctx.ellipse(u.x, cy, c.h*.5*pr*(c.shw || 1), c.h*.62*pr, 0, 0, 7); ctx.fill(); ctx.stroke();
      ctx.globalAlpha = P.al*.5; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(u.x, cy, c.h*.42*pr*(c.shw || 1), c.h*.54*pr, 0, 0, 7); ctx.stroke(); ctx.restore();
    }
    if (u.vuln > 0) glow(u.x, fy - air - c.h*.45, c.h*.8, '#fff3a0', .4 + .15*Math.sin(B.clock*14));""")
g.rep("const nm = '👑 ' + CARDS[u.card].name + (u.slow > 0 ? ' ❄️' : '');", "const nm = '👑 ' + CARDS[u.card].name + (u.bshield ? ' 🛡️' : u.vuln > 0 ? ' 💥 dano em dobro' : '') + (u.slow > 0 ? ' ❄️' : '');")
g.rep("""    <button class="storm" id="stormBtn" """, """    <button class="shieldbtn" id="shieldBtn" type="button" hidden>🛡️ Quebrar o escudo!</button>
    <button class="storm" id="stormBtn" """)
g.rep("  const sb = $('stormBtn'), full = B.ink >= 1;", "  $('shieldBtn').hidden = !(B.bossU && B.bossU.alive && B.bossU.bshield) || !!B.quiz || !!B.storm || B.over;\n  const sb = $('stormBtn'), full = B.ink >= 1;")
g.rep("</style>", """
/* ---------- etapa 5: escudo do chefão ---------- */
.shieldbtn{position:absolute;left:50%;top:calc(var(--hud)*5.6);transform:translateX(-50%);z-index:6;font-family:var(--f-display);font-weight:400;font-size:calc(var(--hud)*1.05);color:#06263d;background:linear-gradient(#e6f8ff,#8fd3ff);border:0;border-bottom:4px solid #2f7fb0;border-radius:14px;padding:7px 18px;box-shadow:0 0 18px rgba(143,211,255,.9);animation:tappulse .9s ease-in-out infinite}
/* ---------- etapa 6: área do pai ---------- */
.pai{display:grid;gap:10px}
.pai h4{margin:6px 0 0;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pai .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.pai .kpis div{background:rgba(0,0,0,.22);border:1px solid var(--line);border-radius:12px;padding:7px 8px}
.pai .kpis b{display:block;font-family:var(--f-display);font-weight:400;font-size:20px}
.pai .kpis span{font-size:11px;color:var(--muted);font-weight:800}
.pai .days{display:grid;grid-template-columns:repeat(14,1fr);gap:3px;align-items:end;height:64px}
.pai .days i{display:block;background:linear-gradient(#8ff0b8,#35d483);border-radius:3px 3px 0 0;min-height:2px}
.pai .days i.z{background:#3a3760}
.pai .teim{display:grid;gap:5px;font-size:13px}
.pai .teim div{background:rgba(0,0,0,.22);border-radius:10px;padding:6px 10px}
.pai .teim b{font-family:var(--f-display);font-weight:400;font-size:16px;margin-right:6px}
.pai .teim small{color:var(--muted);display:block}
.sheet.wide{max-width:min(94vw,820px);grid-template-columns:1fr}
</style>""")

# ================= ÁREA DO PAI =================
g.rep("  S.stats.battles++;\n  S.coins += coins;", "  S.stats.battles++;\n  { const d = dayNum(); S.play = S.play || {}; S.play[d] = (S.play[d] || 0) + Math.round(B.clock); for (const k of Object.keys(S.play)) if (+k < d - 40) delete S.play[k]; }   // tempo jogado por dia, para a área do pai\n  S.coins += coins;")
g.rep("""    <div class="set">
      <h3>Cópia de segurança</h3>""", """    <div class="set">
      <h3>Área do pai</h3>
      <p>Um resumo do que ela já aprendeu, onde trava e quanto jogou. Abre com uma conta de adulto.</p>
      <button type="button" class="btn-blue" id="paiBtn">Abrir a área do pai</button>
    </div>
    <div class="set">
      <h3>Cópia de segurança</h3>""")
g.rep("$('resetBtn').onclick = () => { $('resetConfirm').hidden = false; };", r"""// ---------- área do pai: portão com conta de adulto e relatório ----------
function paiGate(){
  const a = 12 + Math.floor(Math.random()*7), b = 6 + Math.floor(Math.random()*4);
  $('modal').innerHTML = `<div class="sheet" role="dialog" aria-label="Área do pai"><h3>Área do pai</h3>
    <p class="desc">Para entrar, responda: quanto é <b>${a} × ${b}</b>?</p>
    <input id="paiIn" inputmode="numeric" autocomplete="off" style="font:inherit;font-size:22px;padding:8px 12px;border-radius:10px;border:2px solid var(--line);background:#120f30;color:#fff;width:8ch">
    <p class="desc" id="paiMsg" style="color:#ff8a96;font-size:13px;min-height:1em"></p>
    <div class="acts"><button class="btn-gold" id="paiOk" type="button" style="font-size:17px">Entrar</button></div>
    <button class="xbtn" type="button" id="closeModal" aria-label="Fechar">✕</button></div>`;
  $('modal').hidden = false; $('closeModal').onclick = closeModal;
  const go = () => { if (+$('paiIn').value === a*b) paiReport(); else { $('paiMsg').textContent = 'Não é isso. Tente de novo.'; $('paiIn').value = ''; } };
  $('paiOk').onclick = go; $('paiIn').onkeydown = e => { if (e.key === 'Enter') go(); };
  setTimeout(() => { try { $('paiIn').focus(); } catch(e) {} }, 50);
}
function paiReport(){
  const d = dayNum(), play = S.play || {}, days = Array.from({length:14}, (_, i) => Math.round((play[d - 13 + i] || 0)/60)), mx = Math.max(10, ...days);
  const week = days.slice(7).reduce((a, b) => a + b, 0), dj = days.slice(7).filter(v => v > 0).length;
  const acc = S.stats.answered ? Math.round(S.stats.correct/S.stats.answered*100) : 0, dom = masteryCount();
  const teim = FACTS.filter(f => { const x = S.facts[f.key]; return x && x.err >= 1 && stateOf(x) < 4; })
    .sort((x, y) => (isStubborn(S.facts[y.key]) - isStubborn(S.facts[x.key])) || (S.facts[y.key].err - S.facts[x.key].err)).slice(0, 5);
  let best = null, bv = -1;                                    // tabuada mais perto de ficar toda dourada
  for (let n = 2; n <= 10; n++){ const got = tabFacts(n).filter(f => isMastered(f.key)).length; if (got < 10 && got > bv){ bv = got; best = n; } }
  const sug = !S.stats.answered ? 'Ela ainda não jogou o bastante para uma sugestão.'
    : teim.length && isStubborn(S.facts[teim[0].key]) ? `A conta ${teim[0].a} × ${teim[0].b} está teimosa. Vale treinar junto, usando o truque abaixo.`
    : best ? `A tabuada do ${best} está a ${10 - bv} conta${10 - bv > 1 ? 's' : ''} de ficar toda dourada. Coloque o ${best} em foco nesta semana.` : 'Todas as tabuadas estão douradas. Agora é manter o ritmo de revisão.';
  $('modal').innerHTML = `<div class="sheet wide" role="dialog" aria-label="Área do pai"><div class="pai">
    <h3>Área do pai</h3>
    <div class="kpis"><div><b>${dom}/55</b><span>contas dominadas</span></div><div><b>${acc}%</b><span>de acerto geral</span></div><div><b>${week} min</b><span>nos últimos 7 dias</span></div><div><b>${dj}/7</b><span>dias com jogo</span></div></div>
    <h4>Sugestão da semana</h4><p class="desc">${sug}</p>
    <h4>Minutos por dia, últimos 14 dias</h4>
    <div class="days">${days.map(v => `<i class="${v ? '' : 'z'}" style="height:${Math.max(3, v/mx*100)}%" title="${v} min"></i>`).join('')}</div>
    <h4>Contas em que ela mais erra</h4>
    <div class="teim">${teim.length ? teim.map(f => { const x = S.facts[f.key], ms = medianMs(x); return `<div><b>${f.a} × ${f.b} = ${f.a*f.b}</b>${x.err} erro${x.err > 1 ? 's' : ''} em ${x.n} tentativa${x.n > 1 ? 's' : ''}${ms ? ' · tempo ' + secTxt(ms) : ''} · ${STATE_NAME[stateOf(x)]}<small>${tipFor(f.a, f.b)}</small></div>`; }).join('') : '<div>Nenhuma conta com erro ainda.</div>'}</div>
    <h4>Por tabuada</h4>
    <div class="tbars">${Array.from({length:9}, (_, i) => i + 2).map(n => { const fs = tabFacts(n), got = fs.filter(f => isMastered(f.key)).length, tr = fs.reduce((a, f) => a + (S.facts[f.key] ? S.facts[f.key].n : 0), 0), ok = fs.reduce((a, f) => a + (S.facts[f.key] ? S.facts[f.key].ok : 0), 0);
      return `<div class="tbar"><span>Tabuada do ${n}</span><span class="bar"><b style="width:${got*10}%"></b></span><span title="acerto">${tr ? Math.round(ok/tr*100) + '%' : '—'}</span></div>`; }).join('')}</div>
    <p class="desc" style="font-size:12px;color:var(--muted)">A barra mostra quantas das 10 contas estão dominadas; o número à direita é o acerto naquela tabuada. O mapa completo, conta por conta, está na aba Álbum. Foco, Modo Calmo e cópia de segurança ficam nos Ajustes.</p>
    </div><button class="xbtn" type="button" id="closeModal" aria-label="Fechar">✕</button></div>`;
  $('closeModal').onclick = closeModal;
}
$('paiBtn').onclick = () => { sfx('tap'); paiGate(); };
$('resetBtn').onclick = () => { $('resetConfirm').hidden = false; };""")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, openShieldQuiz, breakShield, paiReport, paiGate,")
g.save()
