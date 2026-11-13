/* =========================================================
   ABERTURA: logo do OF Studio, tela de título e cinemática
   A cinemática é um quadrinho animado: pinturas (assets/cenas) com câmera, partículas,
   escrita à mão e perda de cor feitas em código. Pulável; pode ser revista nos Ajustes.
   ========================================================= */
const INTRO = (() => {
  const el = $('intro'), cvI = $('introCv'), c2 = cvI.getContext('2d');
  const SRC = {tabua:'assets/cenas/tabua.webp', lousa:'assets/cenas/lousa.webp', mapa:'assets/cenas/mapa.webp', vila:'assets/cenas/vila.webp'};
  const IMG = {};
  const img = k => { if (!IMG[k]){ const im = new Image(); im.src = SRC[k]; IMG[k] = im; } return IMG[k]; };
  const ok = im => im && im.complete && im.naturalWidth > 0;
  const canFilter = 'filter' in c2;
  let raf = 0, phase = null, st = 0, last = 0, W = 0, H = 0, sceneI = -1, parts = [], flags = {}, after = null, splash = null;
  const ease = t => t < .5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2)/2;
  const out3 = t => 1 - Math.pow(1 - t, 3);
  const c01 = v => Math.max(0, Math.min(1, v));
  function size(){
    const r = el.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(200, r.width); H = Math.max(120, r.height);
    cvI.width = Math.round(W*d); cvI.height = Math.round(H*d); c2.setTransform(d, 0, 0, d, 0, 0);
  }
  // pintura cobrindo a tela, com zoom z e foco (fx, fy) em frações da imagem
  function cover(im, z, fx, fy){
    if (!ok(im)){ c2.fillStyle = '#17153b'; c2.fillRect(0, 0, W, H); return {ox:0, oy:0, iw:W, ih:H}; }
    const s = Math.max(W/im.naturalWidth, H/im.naturalHeight)*z, iw = im.naturalWidth*s, ih = im.naturalHeight*s;
    const ox = clamp(W/2 - fx*iw, W - iw, 0), oy = clamp(H/2 - fy*ih, H - ih, 0);
    c2.drawImage(im, ox, oy, iw, ih);
    return {ox, oy, iw, ih};
  }
  const at = (m, x, y) => [m.ox + x*m.iw, m.oy + y*m.ih];
  // redesenha a mesma pintura sem cor, com força a (0 a 1), opcionalmente só numa faixa
  function gray(im, m, a, clip){
    if (a <= 0) return;
    c2.save();
    if (clip){ c2.beginPath(); c2.rect(clip[0], clip[1], clip[2], clip[3]); c2.clip(); }
    if (canFilter && ok(im)){ c2.globalAlpha = a; c2.filter = 'grayscale(1) brightness(1.08) contrast(.85)'; c2.drawImage(im, m.ox, m.oy, m.iw, m.ih); c2.filter = 'none'; }
    else { c2.globalAlpha = a*.78; c2.fillStyle = '#b9bac6'; c2.fillRect(0, 0, W, H); }
    c2.restore();
  }
  function glow(x, y, r, col, a){
    c2.save(); c2.globalCompositeOperation = 'lighter'; c2.globalAlpha = a;
    const g = c2.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, '#ffffff'); g.addColorStop(.3, col); g.addColorStop(1, 'rgba(0,0,0,0)');
    c2.fillStyle = g; c2.beginPath(); c2.arc(x, y, r, 0, 7); c2.fill(); c2.restore();
  }
  function spark(x, y, col, n, sp){
    for (let i = 0; i < n; i++){ const a = Math.random()*6.28, v = sp*(.3 + Math.random()*.7); parts.push({x, y, vx:Math.cos(a)*v, vy:Math.sin(a)*v - sp*.3, life:.6 + Math.random()*.9, max:1.5, col, sz:1.5 + Math.random()*3}); }
  }
  function drawParts(dt){
    for (const p of parts){ p.life -= dt; p.x += p.vx*dt; p.y += p.vy*dt; p.vy += (p.g || 0)*dt; }
    parts = parts.filter(p => p.life > 0);
    for (const p of parts){ c2.globalAlpha = c01(p.life/p.max*1.6); c2.fillStyle = p.col; c2.beginPath(); c2.arc(p.x, p.y, p.sz, 0, 7); c2.fill(); }
    c2.globalAlpha = 1;
  }
  function paper(){
    const g = c2.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#f1f1f5'); g.addColorStop(1, '#d9dae3');
    c2.fillStyle = g; c2.fillRect(0, 0, W, H);
    c2.fillStyle = 'rgba(150,150,170,.13)';
    for (const [x, y, rx, ry, r] of [[.2, .3, .22, .09, -.3], [.7, .22, .26, .08, .2], [.52, .58, .3, .07, -.1], [.85, .7, .2, .1, .4], [.12, .78, .18, .06, .1]]){ c2.beginPath(); c2.ellipse(W*x, H*y, W*rx, H*ry, r, 0, 7); c2.fill(); }
    c2.fillStyle = 'rgba(120,120,140,.16)'; c2.fillRect(0, H*.86, W, H*.14);
  }
  function tile(x, y, s, t){
    glow(x, y, s*(2.3 + .3*Math.sin(t*4)), '#ffd54f', .75);
    c2.save(); c2.translate(x, y); c2.rotate(-.08);
    c2.fillStyle = '#ffcf3f'; c2.strokeStyle = '#b8700c'; c2.lineWidth = Math.max(2, s*.09);
    c2.beginPath(); if (c2.roundRect) c2.roundRect(-s, -s*.62, s*2, s*1.24, s*.22); else c2.rect(-s, -s*.62, s*2, s*1.24); c2.fill(); c2.stroke();
    c2.fillStyle = '#5a3400'; c2.font = `400 ${s*.52}px "Titan One", sans-serif`; c2.textAlign = 'center'; c2.textBaseline = 'middle'; c2.fillText('1 × 3 = 3', 0, s*.03);
    c2.restore();
  }
  function grafiPic(pose, x, y, h, grayed, t){
    const im = GRAFI_IMG[pose]; if (!ok(im)) return;
    const w = im.naturalWidth*h/im.naturalHeight, bob = Math.sin(t*2.2)*h*.012;
    c2.save(); c2.translate(x, y + bob); c2.rotate(Math.sin(t*1.6)*.03);
    if (grayed){ if (canFilter) c2.filter = 'grayscale(1) brightness(1.1)'; else c2.globalAlpha = .55; }
    c2.drawImage(im, -w/2, -h, w, h); c2.filter = 'none'; c2.restore();
  }
  // Lorde Borracha, desenhado em código: borracha rosa de monóculo, bigode e capa de farelos
  function lorde(x, y, s, rot, t){
    c2.save(); c2.translate(x, y); c2.rotate(rot); c2.scale(s, s);
    c2.lineJoin = 'round'; c2.lineCap = 'round';
    c2.fillStyle = '#8f8a9c'; c2.strokeStyle = '#3d2a44'; c2.lineWidth = 5;                       // capa
    c2.beginPath(); c2.moveTo(-40, -52); c2.quadraticCurveTo(-120 - 12*Math.sin(t*3), 30, -92, 118); c2.lineTo(92, 118); c2.quadraticCurveTo(120 + 12*Math.sin(t*3 + 1), 30, 40, -52); c2.closePath(); c2.fill(); c2.stroke();
    c2.fillStyle = '#c9a9b8'; for (let i = 0; i < 14; i++){ c2.beginPath(); c2.arc(-80 + (i*37 % 160), 60 + (i*53 % 52), 4 + i % 3, 0, 7); c2.fill(); }
    c2.fillStyle = '#ff8fb3'; c2.strokeStyle = '#5a1f3a'; c2.lineWidth = 6;                       // corpo
    c2.beginPath(); c2.moveTo(-44, -70); c2.lineTo(30, -92); c2.quadraticCurveTo(46, -92, 46, -76); c2.lineTo(46, 78); c2.quadraticCurveTo(46, 92, 32, 92); c2.lineTo(-32, 92); c2.quadraticCurveTo(-46, 92, -46, 78); c2.closePath(); c2.fill(); c2.stroke();
    c2.fillStyle = '#7fb4e8'; c2.beginPath(); c2.rect(-46, 18, 92, 46); c2.fill(); c2.stroke();     // cinta azul
    c2.fillStyle = '#ffc2d6'; c2.beginPath(); c2.ellipse(-22, -62, 12, 5, -.3, 0, 7); c2.fill();
    c2.fillStyle = '#fff'; c2.lineWidth = 4;                                                       // olhos
    c2.beginPath(); c2.ellipse(-17, -30, 11, 13, 0, 0, 7); c2.fill(); c2.stroke();
    c2.beginPath(); c2.ellipse(17, -30, 11, 13, 0, 0, 7); c2.fill(); c2.stroke();
    c2.fillStyle = '#2a1030'; c2.beginPath(); c2.arc(-15, -27, 4.5, 0, 7); c2.arc(15, -27, 4.5, 0, 7); c2.fill();
    c2.strokeStyle = '#5a1f3a'; c2.lineWidth = 5; c2.beginPath(); c2.moveTo(-30, -48); c2.lineTo(-6, -42); c2.moveTo(30, -48); c2.lineTo(6, -42); c2.stroke();
    c2.strokeStyle = '#e8b93a'; c2.lineWidth = 4; c2.beginPath(); c2.arc(17, -30, 16, 0, 7); c2.stroke();   // monóculo
    c2.lineWidth = 2; c2.beginPath(); c2.moveTo(31, -22); c2.quadraticCurveTo(44, 4, 36, 18); c2.stroke();
    c2.strokeStyle = '#3d2a44'; c2.lineWidth = 5; c2.beginPath(); c2.moveTo(0, -8); c2.quadraticCurveTo(-14, 2, -26, -8); c2.moveTo(0, -8); c2.quadraticCurveTo(14, 2, 26, -8); c2.stroke();   // bigode
    c2.lineWidth = 3; c2.beginPath(); c2.moveTo(-8, 6); c2.quadraticCurveTo(0, 2, 8, 6); c2.stroke();
    c2.restore();
  }
  let sil = {};
  function bossShadow(i){                                    // sombra do chefão de cada ilha
    if (sil[i]) return sil[i];
    const f = SPR['boss' + (i + 1)] && SPR['boss' + (i + 1)][0]; if (!f || !ok(f.img)) return null;
    const c = document.createElement('canvas'); c.width = f.w; c.height = f.h; const x = c.getContext('2d');
    x.drawImage(f.img, 0, 0, f.w, f.h); x.globalCompositeOperation = 'source-in'; x.fillStyle = '#1b1033'; x.fillRect(0, 0, f.w, f.h);
    return (sil[i] = c);
  }
  const ISLE = [[.18, .71], [.21, .42], [.40, .28], [.56, .67], [.635, .36], [.81, .62], [.80, .23]];
  function hand(txt, x, y, px, col, n){                      // texto escrito à mão, letra por letra
    c2.font = `400 ${px}px "Patrick Hand", "Nunito", cursive`; c2.textAlign = 'left'; c2.textBaseline = 'middle';
    c2.fillStyle = col; c2.fillText(txt.slice(0, n), x, y);
    return c2.measureText(txt).width;
  }
  /* ---------- as seis cenas ---------- */
  const SC = [
    {dur:6.2, who:'Grafi', txt:'Toda manhã, as runas acendem e o mundo ganha cor.',
      draw(t, q, dt){
        const m = cover(img('tabua'), 1.42 - .34*ease(q), .5, .16 + .3*ease(q));
        for (let i = 0; i < 7; i++){ const [x, y] = at(m, .5, .25 + i*.065), a = Math.max(0, Math.sin(t*2.4 - i*.55))*.34*c01(t/1.2); glow(x, y, m.ih*.11, '#ffd54f', a); }
        if (Math.random() < dt*26){ const [x, y] = at(m, .43 + Math.random()*.15, .22 + Math.random()*.42); parts.push({x, y, vx:(Math.random() - .5)*14, vy:-18 - Math.random()*30, life:1.6, max:1.6, col:'#fff1a8', sz:1 + Math.random()*2.4}); }
      }},
    {dur:6.4, who:'Grafi', txt:'Ops! Rascunho. Cinquenta e seis!', pitch:1.3,
      draw(t, q){
        const m = cover(img('lousa'), 1 + .07*ease(q), .62, .5), px = m.ih*.12, [x0, y0] = at(m, .585, .38);
        c2.save(); c2.translate(x0, y0); c2.rotate(-.035);
        const full = '7 × 8 = ', n = Math.floor(t*5.2), w1 = hand(full, 0, 0, px, '#f4f1e6', Math.min(full.length, n));
        const wrong = c01(1 - (t - 3.1)/.5)*.65 + .35;
        if (n > full.length){ c2.globalAlpha = t > 3.1 ? wrong : 1; const w2 = hand('54', w1, 0, px, '#f4f1e6', n - full.length); c2.globalAlpha = 1;
          if (t > 2.7){ c2.strokeStyle = '#ff8a76'; c2.lineWidth = px*.08; c2.lineCap = 'round'; c2.beginPath(); c2.moveTo(w1 - px*.05, px*.12); c2.lineTo(w1 - px*.05 + (w2 + px*.1)*c01((t - 2.7)/.35), -px*.14); c2.stroke(); }
        }
        if (t > 3.5){ const k = Math.floor((t - 3.5)*5) + 1; c2.shadowColor = '#ffd54f'; c2.shadowBlur = 14; hand('56', w1 + px*.05, px*1.02, px*1.15, '#ffd54f', k); c2.shadowBlur = 0; }
        c2.restore();
        if (t > 3.9 && !flags.s2){ flags.s2 = 1; sfx('chord'); const [sx, sy] = at(m, .86, .55); spark(sx, sy, '#ffe27a', 34, 150); }
        if (!flags.s2b && t > 2.7){ flags.s2b = 1; sfx('bad'); }
      }},
    {dur:8.2, who:'Lorde Borracha', txt:'Erros. Rabiscos. Rascunhos. Que horror.', pitch:.55, enter(){ music(null); },
      draw(t, q, dt){
        const im = img('tabua'), m = cover(im, 1.14, .5, .44);
        const band = ease(c01((t - 2.6)/3.6)), bx = band*(W + 80) - 40;
        gray(im, m, 1, [0, 0, Math.max(0, bx), H]);
        c2.fillStyle = `rgba(30,28,50,${.4*c01(t/2)})`; c2.fillRect(0, 0, W, H);
        if (band > 0 && band < 1){ const g = c2.createLinearGradient(bx - 70, 0, bx + 24, 0); g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.7, 'rgba(255,255,255,.85)'); g.addColorStop(1, 'rgba(255,255,255,0)'); c2.fillStyle = g; c2.fillRect(bx - 70, 0, 94, H); }
        const drop = out3(c01(t/2.2)), s = H/430;
        const ly = -H*.35 + drop*H*.72 + Math.sin(t*2)*H*.015;
        const x = band > 0 ? W*.14 + band*W*.72 : W*.5 - drop*W*.36;
        lorde(x, ly, s, band > 0 && band < 1 ? .28 : Math.sin(t*1.3)*.05, t);
        if (Math.random() < dt*40) parts.push({x:x + (Math.random() - .5)*150*s, y:ly + (Math.random() - .2)*170*s, vx:(Math.random() - .5)*60, vy:20 + Math.random()*60, g:40, life:1.5, max:1.5, col:Math.random() < .5 ? '#d8c2cc' : '#a7a2b5', sz:1.5 + Math.random()*3});
        if (t > 2.1 && !flags.s3){ flags.s3 = 1; sfx('boom'); }
        if (t > 2.7 && !flags.s3b){ flags.s3b = 1; try { tone(210, 3.2, 'sawtooth', .05, 70); } catch(e) {} }
      }},
    {dur:7, who:'', txt:'',
      draw(t, q, dt){
        const im = img('mapa'), m = cover(im, 1, .5, .5);
        gray(im, m, ease(c01((t - .8)/4.6)));
        for (let i = 0; i < 7; i++){
          const ti = 1 + i*.62, [x, y] = at(m, ISLE[i][0], ISLE[i][1]), [cx, cy] = at(m, .5, .47);
          if (t < ti){ const k = ease(c01((t - (ti - 1))/1)); if (k > 0) glow(cx + (x - cx)*k, cy + (y - cy)*k - Math.sin(k*3.14)*H*.12, 9, '#ffd54f', .95); }
          else {
            if (!flags['i' + i]){ flags['i' + i] = 1; spark(x, y, '#cfc6e6', 12, 70); try { tone(170 - i*13, .5, 'triangle', .13, 120 - i*10); } catch(e) {} }
            const sh = bossShadow(i), k = easeOutBack(c01((t - ti)/.35));
            if (sh){ const h = m.ih*.2*k, w = sh.width*h/sh.height; c2.globalAlpha = .88; c2.drawImage(sh, x - w/2, y - h*.82, w, h); c2.globalAlpha = 1; }
          }
        }
      }},
    {dur:5, who:'', txt:'',
      draw(t){
        paper();
        grafiPic('triste', W*.3, H*.84, H*.44, true, t);
        if (t > 1.3){ if (!flags.s5){ flags.s5 = 1; try { tone(1318, .5, 'sine', .14); tone(1976, .7, 'sine', .07, null, .08); } catch(e) {} spark(W*.58, H*.74, '#ffe27a', 22, 110); }
          tile(W*.58, H*.76, H*.085*easeOutBack(c01((t - 1.3)/.4)), t); }
      }},
    {dur:1e9, who:'Grafi', txt:'Ainda tem uma! Você me ajuda a reescrever tudo?', pitch:1.3, enter(){ $('introGo').hidden = false; },
      draw(t){
        paper();
        grafiPic('oi', W*.3, H*.9, H*.66, false, t);
        tile(W*.5, H*.3 + Math.sin(t*2)*H*.012, H*.075, t);
      }},
  ];
  function caption(who, txt){ $('introCap').innerHTML = txt ? (who ? `<b>${who}</b>` : '') + txt : ''; }
  function scene(i){
    sceneI = i; st = performance.now(); parts = []; flags = {};
    const s = SC[i]; caption(s.who, s.txt);
    if (s.txt) speak(s.txt, s.pitch);
    if (s.enter) s.enter();
  }
  function frame(now){
    raf = requestAnimationFrame(frame);
    const dt = Math.min(.05, (now - last)/1000); last = now;
    const t = (now - st)/1000;
    c2.clearRect(0, 0, W, H);
    if (phase === 'logo'){
      c2.fillStyle = '#0c0a24'; c2.fillRect(0, 0, W, H);
      const p = out3(c01(t/1.1)), x0 = W*.5 - Math.min(W*.3, 250), x1 = x0 + Math.min(W*.6, 500)*p, y = H*.6, fs = Math.min(H*.2, W*.1);
      c2.save(); c2.beginPath(); c2.rect(0, 0, x1 + 6, H); c2.clip();
      c2.fillStyle = '#ffffff'; c2.font = `400 ${fs}px "Titan One", sans-serif`; c2.textAlign = 'center'; c2.textBaseline = 'alphabetic'; c2.fillText('OF Studio', W*.5, y - fs*.22);
      c2.restore();
      c2.strokeStyle = '#ffcf3f'; c2.lineWidth = Math.max(3, fs*.07); c2.lineCap = 'round'; c2.beginPath(); c2.moveTo(x0, y); c2.lineTo(x1, y); c2.stroke();
      if (p < 1){ c2.save(); c2.translate(x1, y); c2.rotate(-.9); c2.fillStyle = '#ffcf3f'; c2.fillRect(0, -fs*.06, fs*.5, fs*.12); c2.fillStyle = '#f2c9a0'; c2.beginPath(); c2.moveTo(0, -fs*.06); c2.lineTo(-fs*.14, 0); c2.lineTo(0, fs*.06); c2.fill(); c2.fillStyle = '#333'; c2.beginPath(); c2.moveTo(-fs*.09, -fs*.022); c2.lineTo(-fs*.14, 0); c2.lineTo(-fs*.09, fs*.022); c2.fill(); c2.restore(); }
      c2.globalAlpha = c01((t - 1.25)/.4); c2.fillStyle = '#b4aee6'; c2.font = `800 ${fs*.2}px Nunito, sans-serif`; c2.textAlign = 'center'; c2.fillText('apresenta', W*.5, y + fs*.42); c2.globalAlpha = 1;
      if (t > 2.5){ c2.fillStyle = `rgba(12,10,36,${c01((t - 2.5)/.35)})`; c2.fillRect(0, 0, W, H); }
      if (t > 2.85) title();
    } else if (phase === 'title'){
      const m = cover(img('vila'), 1.05 + .012*Math.sin(t*.5), .5, .5);
      const ids = S.deck.slice(0, 4);
      ids.forEach((id, i) => { const f = SPR[CARDS[id].spr][Math.floor(t*2.2 + i) % 6 === 0 ? 7 : 0]; if (!f || !ok(f.img)) return; const h = m.ih*.2*(CARDS[id].h/105), w = f.w*h/f.h, [x, y] = at(m, .44 + i*.12, .80 + (i % 2)*.03); c2.fillStyle = 'rgba(0,0,0,.22)'; c2.beginPath(); c2.ellipse(x, y, w*.34, h*.06, 0, 0, 7); c2.fill(); c2.drawImage(f.img, x - f.fx*h/f.h, y - h + Math.sin(t*2.6 + i)*h*.012, w, h); });
      grafiPic('oi', W*.13, H*.98, H*.5, false, t);
      c2.fillStyle = `rgba(12,10,36,${c01(1 - t/.5)})`; c2.fillRect(0, 0, W, H);
    } else if (phase === 'cine'){
      const s = SC[sceneI];
      s.draw(t, Math.min(1, t/s.dur), dt);
      drawParts(dt);
      const fin = c01(1 - t/.45), fout = s.dur < 1e8 ? c01((t - (s.dur - .4))/.4) : 0;
      if (fin > 0 || fout > 0){ c2.fillStyle = `rgba(12,10,36,${Math.max(fin, fout)})`; c2.fillRect(0, 0, W, H); }
      if (t >= s.dur) scene(sceneI + 1);
    } else if (phase === 'splash'){
      const s = SC[5]; s.draw((now - st)/1000);
      const k = c01((now - splash.t0)/900), R = Math.hypot(W, H)*1.1;
      ['#3f8cff', '#ffcf3f', '#ff5fd2', '#35d483', '#7bd36b'].forEach((col, i) => { const kk = out3(c01(k*1.25 - i*.06)); c2.fillStyle = col; c2.beginPath(); c2.arc(splash.x, splash.y, R*kk, 0, 7); c2.fill(); });
      if (k >= 1) finish();
    }
  }
  function open(){ el.hidden = false; size(); last = st = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(frame); }
  function hideAll(){ for (const id of ['introTtl', 'introTap', 'introGo', 'introSkip', 'introBy']) $(id).hidden = true; caption('', ''); }
  function logo(){ window.__introOn = true; phase = 'logo'; hideAll(); open(); for (const k in SRC) img(k); }
  function title(){ phase = 'title'; st = performance.now(); hideAll(); $('introTtl').hidden = false; $('introTap').hidden = false; $('introBy').hidden = false; }
  function cine(then){
    window.__introOn = true; after = then || null; phase = 'cine'; hideAll(); $('introSkip').hidden = false; open();
    music('intro'); scene(0);
  }
  function finish(){
    cancelAnimationFrame(raf); phase = null; el.hidden = true; hideAll(); window.__introOn = false;
    try { window.speechSynthesis && window.speechSynthesis.cancel(); } catch(e) {}
    if (!S.introSeen){ S.introSeen = true; save(); }
    const f = after; after = null;
    if (f) f(); else { show('home'); }
    music('menu');
  }
  el.addEventListener('pointerdown', e => {
    if (e.target.closest('#introSkip')){ ensureAudio(); sfx('tap'); finish(); return; }
    if (e.target.closest('#introGo')){
      ensureAudio(); sfx('chord'); sfx('turbo'); const r = el.getBoundingClientRect();
      $('introGo').hidden = true; caption('', ''); phase = 'splash'; splash = {x:e.clientX - r.left, y:e.clientY - r.top, t0:performance.now()};
      return;
    }
    if (phase === 'logo'){ title(); return; }
    if (phase === 'title'){ ensureAudio(); sfx('chord'); if (S.introSeen) finish(); else cine(); }
  });
  window.addEventListener('resize', () => { if (phase) size(); });
  return {logo, cine, finish, get phase(){ return phase; }, get scene(){ return sceneI; }, jump(i){ scene(i); }};
})();
$('introAgain').onclick = () => { ensureAudio(); sfx('tap'); INTRO.cine(() => show('settings')); };
