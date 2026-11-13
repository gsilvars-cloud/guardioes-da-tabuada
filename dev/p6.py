from patchlib import G
g = G()
g.rep("""    <button class="mastery-mini" id="masteryMini" type="button"></button>""", """    <button class="mastery-mini" id="afiarBtn" type="button"></button>
    <button class="mastery-mini" id="masteryMini" type="button"></button>""")
g.rep("  const m = masteryCount();\n  $('masteryMini').innerHTML", """  { const af = S.afiar || {best:0, day:-1}, done = af.day === dayNum(), sb = S.sombra;
    $('afiarBtn').innerHTML = `<span style="font-size:26px">⚡</span><span><b>${done ? 'Afiar runas' : 'Missão de hoje: afiar runas'}</b><small>60 segundos de contas rápidas${done ? ' · missão feita ✓' : ' · vale moedas'}${af.best ? ' · seu recorde: ' + af.best : ''}${sb ? ' · Sombra do Papai: ' + sb.n : ''}</small></span><span style="color:var(--muted)">›</span>`; }
  const m = masteryCount();
  $('masteryMini').innerHTML""")
g.rep("$('masteryMini').addEventListener('click', () => show('book'));", r"""$('masteryMini').addEventListener('click', () => show('book'));

/* ---------- Afiar runas: 60 s de contas rápidas, com recorde e a Sombra do Papai ---------- */
let AF = null;
const AF_T = 60;
function afPool(dad){
  if (dad) return FACTS.filter(f => f.a >= 3 && f.b >= 6 && f.b <= 9);                 // o adulto pega só as difíceis
  let pool = FACTS.filter(f => f.a > 1 && S.facts[f.key] && S.facts[f.key].seen);
  if (pool.length < 8) pool = pool.concat(FACTS.filter(f => f.a > 1 && f.diff <= 2 && !pool.includes(f)));
  return pool;
}
function startAfiar(dad){
  ensureAudio(); sfx('tap');
  AF = {dad:!!dad, n:0, miss:[], input:'', q:null, lock:false, endAt:performance.now() + AF_T*1000, pool:afPool(dad), timer:0};
  $('modal').innerHTML = `<div class="sheet wide afiar" role="dialog" aria-label="${dad ? 'Sombra do Papai' : 'Afiar runas'}">
    <div class="afhead"><b>${dad ? '👤 Sombra do Papai' : '⚡ Afiar runas'}</b><span class="aftime"><i id="afFill"></i></span><b id="afScore">0</b></div>
    <div class="afbody"><div class="afq" id="afQ"></div>
    <div class="afpad" id="afPad">${[1,2,3,4,5].map(n => `<button type="button" data-k="${n}">${n}</button>`).join('')}<button type="button" class="fn" data-k="back" aria-label="Apagar">⌫</button>${[6,7,8,9,0].map(n => `<button type="button" data-k="${n}">${n}</button>`).join('')}<span></span></div></div>
    <button class="xbtn" type="button" id="closeModal" aria-label="Fechar">✕</button></div>`;
  $('modal').hidden = false; $('closeModal').onclick = () => { stopAfiar(); closeModal(); };
  $('afPad').addEventListener('pointerdown', e => { const b = e.target.closest('button'); if (!b) return; e.preventDefault(); afKey(b.dataset.k); });
  afNext(); AF.timer = setInterval(afTick, 100);
}
function stopAfiar(){ if (AF){ clearInterval(AF.timer); AF = null; } }
function afNext(){
  let f; do f = weighted(AF.pool); while (AF.q && f.key === AF.q.key && AF.pool.length > 1);
  let a = f.a, b = f.b; if (Math.random() < .5) [a, b] = [b, a];
  AF.q = {key:f.key, a, b, ans:a*b, t0:performance.now()}; AF.input = ''; AF.lock = false; afDraw();
}
function afDraw(state){
  const q = AF.q;
  $('afQ').innerHTML = `<span>${q.a} × ${q.b} =</span><span class="q-ans ${state || (AF.input ? '' : 'empty')}">${state === 'bad' ? q.ans : AF.input || '?'}</span>`;
  $('afScore').textContent = AF.n;
}
function afKey(k){
  if (!AF || AF.lock || !AF.q) return;
  if (k === 'back'){ AF.input = AF.input.slice(0, -1); afDraw(); return; }
  if (!/^\d$/.test(k)) return;
  AF.input += k; const q = AF.q;
  if (AF.input.length < String(q.ans).length){ sfx('tap'); afDraw(); return; }
  const ok = +AF.input === q.ans, ms = performance.now() - q.t0;
  if (ok){ AF.n++; sfx('coin'); if (!AF.dad){ recordAnswer(q.key, true, ms, {}); } AF.lock = true; afDraw('good'); setTimeout(() => { if (AF) afNext(); }, 140); }
  else { sfx('bad'); if (!AF.miss.some(m => m.key === q.key)) AF.miss.push(q); AF.lock = true; afDraw('bad'); setTimeout(() => { if (AF) afNext(); }, 1100); }   // errar aqui não derruba a conta: só mostra a resposta
}
function afTick(){
  if (!AF) return;
  if ($('modal').hidden || !$('afFill')){ stopAfiar(); return; }
  const left = AF.endAt - performance.now();
  $('afFill').style.width = Math.max(0, left/(AF_T*10)).toFixed(1) + '%';
  if (left <= 0) afEnd();
}
function afEnd(){
  const a = AF; clearInterval(a.timer); AF = null; sfx('chord');
  let msg, extra = '';
  if (a.dad){
    S.sombra = {n:a.n, day:dayNum(), beaten:false}; save();
    msg = `Sombra gravada: <b>${a.n} conta${a.n === 1 ? '' : 's'}</b> em 60 segundos. Agora é a vez dela tentar passar.`;
  } else {
    const af = S.afiar = S.afiar || {best:0, day:-1}, d = dayNum(), first = af.day !== d, rec = a.n > af.best;
    let coins = first ? Math.min(30, a.n*2) : 0;
    if (rec) af.best = a.n;
    af.day = d;
    const sb = S.sombra;
    if (sb){
      if (a.n > sb.n){ if (!sb.beaten){ sb.beaten = true; coins += 40; } extra = `<p class="desc">👤 Você passou a <b>Sombra do Papai</b> (${sb.n})! Desafie ele a gravar outra.</p>`; }
      else extra = `<p class="desc">👤 Sombra do Papai: <b>${sb.n}</b>. ${a.n === sb.n ? 'Empate! Falta uma conta para passar.' : 'Faltaram ' + (sb.n - a.n + 1) + ' para passar.'}</p>`;
    }
    S.coins += coins; save();
    msg = `Você acertou <b>${a.n} conta${a.n === 1 ? '' : 's'}</b> em 60 segundos.${rec && a.n ? ' <b>Novo recorde!</b>' : af.best ? ' Seu recorde: ' + af.best + '.' : ''}${coins ? ' Ganhou 🪙 ' + coins + '.' : ''}`;
    if (S.settings.voice !== false) speak(a.n + (a.n === 1 ? ' conta certa!' : ' contas certas!'));
  }
  const miss = a.miss.slice(0, 4).map(q => `<div><b>${q.a} × ${q.b} = ${q.ans}</b><small>${tipFor(q.a, q.b)}</small></div>`).join('');
  $('modal').innerHTML = `<div class="sheet wide afiar" role="dialog" aria-label="Resultado"><div class="pai">
    <h3>${a.dad ? '👤 Sombra do Papai' : '⚡ Afiar runas'}</h3><p class="desc">${msg}</p>${extra}
    ${miss ? '<h4>Para lembrar</h4><div class="teim">' + miss + '</div>' : ''}
    <div class="acts"><button class="btn-gold" id="afAgain" type="button" style="font-size:17px">De novo</button><button class="btn-blue" id="afClose" type="button">Fechar</button></div>
    </div><button class="xbtn" type="button" id="closeModal" aria-label="Fechar">✕</button></div>`;
  const fin = () => { closeModal(); if (cur === 'home') renderHome(); else refreshWallet && 0; };
  $('closeModal').onclick = fin; $('afClose').onclick = fin; $('afAgain').onclick = () => startAfiar(a.dad);
  if (cur === 'home') renderHome();
}
addEventListener('keydown', e => { if (!AF) return; if (/^\d$/.test(e.key)) afKey(e.key); else if (e.key === 'Backspace') afKey('back'); });
$('afiarBtn').addEventListener('click', () => startAfiar(false));""")
g.rep("""    <h4>Por tabuada</h4>
    <div class="tbars">""", """    <h4>Sombra do Papai</h4>
    <p class="desc">Jogue 60 segundos de contas difíceis. O seu placar vira a sombra que ela tenta passar no "Afiar runas" da tela inicial. ${S.sombra ? 'Sombra atual: <b>' + S.sombra.n + '</b>' + (S.sombra.beaten ? ' (ela já passou!)' : '') + '.' : 'Ainda não há sombra gravada.'} ${S.afiar && S.afiar.best ? 'Recorde dela: <b>' + S.afiar.best + '</b>.' : ''}</p>
    <div class="acts"><button class="btn-blue" id="paiSombra" type="button">Gravar minha sombra (60 s)</button></div>
    <h4>Por tabuada</h4>
    <div class="tbars">""")
g.rep("  $('modal').hidden = false; $('closeModal').onclick = closeModal;\n}\n$('paiBtn').onclick", "  $('modal').hidden = false; $('closeModal').onclick = closeModal; $('paiSombra').onclick = () => startAfiar(true);\n}\n$('paiBtn').onclick")
g.rep("    : best ? `A tabuada do ${best} está a", "    : !dom ? 'Ainda não há contas dominadas. O que mais ajuda agora é jogar um pouco todo dia, de 10 a 15 minutos.'\n    : best ? `A tabuada do ${best} está a")
g.rep("/* ---------- etapa 6: área do pai ---------- */", """/* ---------- etapa 6: afiar runas ---------- */
.afiar{max-width:min(94vw,640px)!important}
.afhead{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding-right:40px;font-family:var(--f-display);font-size:20px}
.afhead b{font-weight:400}
.aftime{height:10px;border-radius:5px;background:#120f30;overflow:hidden}
.aftime i{display:block;height:100%;width:100%;background:linear-gradient(90deg,#ff5fd2,#ffd36a)}
.afbody{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);gap:14px;align-items:center}
.afq{font-family:var(--f-display);font-size:clamp(26px,5vw,40px);display:flex;gap:10px;align-items:center;justify-content:center;white-space:nowrap}
.afq .q-ans{min-width:2.2ch;text-align:center;background:#120f30;border:2px solid var(--line);border-radius:12px;padding:2px 10px}
.afq .q-ans.empty{color:var(--muted)}
.afq .q-ans.good{border-color:var(--green);color:var(--green)}
.afq .q-ans.bad{border-color:#ff6b7a;color:#ff8a96}
.afpad{display:grid;grid-template-columns:repeat(6,1fr);gap:7px}
.afpad button{font-family:var(--f-display);font-size:22px;height:52px;border:0;border-bottom:4px solid #b9c0e6;border-radius:12px;background:#fff;color:#221a5a}
.afpad button.fn{background:var(--gold);border-bottom-color:#c98a1b}
@media (max-width:560px){.afbody{grid-template-columns:1fr}}
/* ---------- etapa 6: área do pai ---------- */""")
g.rep("get S(){ return S; }, SAVE_KEY,", "get S(){ return S; }, SAVE_KEY, startAfiar, afKey, afEnd, get AF(){ return AF; },")
g.save()
