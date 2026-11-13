/* =========================================================
   MUNDO VIVO: o vento passa pelo cenário pintado. Grama que balança, nuvens e suas sombras, pássaros,
   pétalas, borboletas, raios de sol e riscos de vento. Tudo desenhado por código, por cima da pintura,
   em duas camadas: atrás dos heróis (back) e na frente deles (front).
   ========================================================= */
const AMB = (() => {
  const CFG = {
    campo:  {grass:['#2f7d33','#4fa53f','#86cf58'], flower:['#fff3a0','#ff9ac0','#ffffff'], bits:'petal',   bitCol:['#ffd0e0','#ffffff','#ffe9a8'], nBits:22, birds:1,  fly:3, cloud:['#ffffff','#cfe1f4'], clouds:1,  rays:.11, shadow:.11, glint:'#f4ffd0'},
    pantano:{grass:['#245a38','#3f8048','#74ad62'], flower:['#d9f0a0','#c8a0ff'],           bits:'firefly', bitCol:['#e9ff9a','#b8ffb0'],           nBits:18, birds:.5, fly:1, cloud:['#e4f2e4','#a9c9b0'], clouds:.6, rays:.07, shadow:.12, mist:.11, glint:'#dcffc0'},
    sombra: {grass:['#231d48','#3b3374','#665ab0'], flower:['#b08cff'],                     bits:'firefly', bitCol:['#c9b8ff','#8fd0ff'],           nBits:16, birds:.7, bats:1, fly:0, cloud:['#6a5fa8','#3a3270'], clouds:.5, rays:0,   shadow:.12, mist:.15, glint:'#b8a8ff'},
    vulcao: {grass:['#40241c','#63382a','#96583a'], flower:['#ffb060'],                     bits:'ember',   bitCol:['#ffb066','#ff7a3a','#ffe08a'], nBits:14, birds:0,  fly:0, cloud:['#8a5a52','#5a3530'], clouds:.4, rays:.05, shadow:.1,  glint:'#ffc890'},
    neve:   {grass:['#a9c3d9','#d2e3f1','#ffffff'], flower:['#ffffff'],                     bits:'snow',    bitCol:['#ffffff','#eaf4ff'],           nBits:20, birds:.4, fly:0, cloud:['#ffffff','#d5e6f5'], clouds:.8, rays:.06, shadow:.07, glint:'#ffffff'},
    dourado:{grass:['#a8791f','#d2a236','#f2d268'], flower:['#fff3c0','#ffffff'],           bits:'pollen',  bitCol:['#fff0b0','#ffe27a'],           nBits:24, birds:.8, fly:2, cloud:['#fff6dc','#f0d6a0'], clouds:.8, rays:.13, shadow:.09, glint:'#fff6c8'},
    arcano: {grass:['#27357f','#4254b0','#8a9cff'], flower:['#d0b8ff','#8ff0ff'],           bits:'rune',    bitCol:['#c9b8ff','#8ff0ff','#ffffff'], nBits:16, birds:.3, fly:0, cloud:['#8f8fe0','#5050a8'], clouds:.5, rays:.05, shadow:.1,  mist:.08, glint:'#c8d0ff'}
  };
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let st = null, last = 0;
  const rng = seed => { let s = seed; return () => (s = (s*16807) % 2147483647)/2147483647; };
  const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  const mix = (a, b, k) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), A = p(a), B2 = p(b); return '#' + A.map((v, i) => Math.round(v + (B2[i] - v)*k).toString(16).padStart(2, '0')).join(''); };

  // tufo de grama pintado à mão: lâminas curvas, escuras atrás e claras na frente
  function mkTuft(pal, r, w, h, n, flower){
    const c = cv(w, h), x = c.getContext('2d');
    for (let i = 0; i < n; i++){
      const k = i/n, bx = w*(.18 + r()*.64), lean = (r() - .5)*w*.55, len = h*(.45 + r()*.5)*(.75 + .25*k), bw = w*(.035 + r()*.035);
      const tx = bx + lean, ty = h - len, cx = bx + lean*.25, cy = h - len*.6;
      x.fillStyle = pal[Math.min(pal.length - 1, Math.floor(k*pal.length + r()*.8))];
      x.beginPath(); x.moveTo(bx - bw, h); x.quadraticCurveTo(cx - bw*.7, cy, tx, ty); x.quadraticCurveTo(cx + bw*.9, cy, bx + bw, h); x.fill();
    }
    if (flower){ const fx = w*(.3 + r()*.4), fy = h*(.18 + r()*.25); x.strokeStyle = pal[1]; x.lineWidth = Math.max(1, w*.02); x.beginPath(); x.moveTo(fx, h); x.quadraticCurveTo(fx + w*.05, h*.6, fx, fy); x.stroke();
      x.fillStyle = flower; for (let i = 0; i < 5; i++){ const a = i/5*6.283; x.beginPath(); x.arc(fx + Math.cos(a)*w*.055, fy + Math.sin(a)*w*.055, w*.05, 0, 7); x.fill(); } x.fillStyle = '#ffd23f'; x.beginPath(); x.arc(fx, fy, w*.04, 0, 7); x.fill(); }
    return c;
  }
  // nuvem de aquarela: montes claros por cima, barriga sombreada
  function mkCloud(col, r){
    const c = cv(320, 150), x = c.getContext('2d'), n = 9 + Math.floor(r()*5);
    for (const pass of [1, 0]){
      for (let i = 0; i < n; i++){
        const px = 50 + (i/(n - 1))*220 + (r() - .5)*20, rad = 26 + Math.sin(i/(n - 1)*Math.PI)*34 + r()*10, py = 96 - rad*.55 + (pass ? 10 : 0);
        const g = x.createRadialGradient(px - rad*.2, py - rad*.3, rad*.15, px, py, rad); g.addColorStop(0, col[pass]); g.addColorStop(.75, col[pass]); g.addColorStop(1, col[pass] + '00');
        x.fillStyle = g; x.beginPath(); x.arc(px, py, rad, 0, 7); x.fill();
      }
    }
    x.globalCompositeOperation = 'destination-out'; const cut = x.createLinearGradient(0, 100, 0, 126); cut.addColorStop(0, 'rgba(0,0,0,0)'); cut.addColorStop(1, 'rgba(0,0,0,1)'); x.fillStyle = cut; x.fillRect(0, 100, 320, 50);
    return c;
  }
  function mkBlob(col){ const c = cv(128, 128), x = c.getContext('2d'), g = x.createRadialGradient(64, 64, 4, 64, 64, 64); g.addColorStop(0, col); g.addColorStop(1, col + '00'); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return c; }

  function setup(key, W, H, gy){
    const C = CFG[key] || CFG.campo, r = rng(key.length*131 + 7), dark = C.grass.map(c => mix(c, '#06140c', .42));
    st = {key, W, H, gy, C, t0:performance.now()/1000,
      tuft:[0, 1, 2, 3, 4].map(i => mkTuft(C.grass, r, 72, 64, 10 + Math.floor(r()*5), i === 1 || i === 3 ? C.flower[Math.floor(r()*C.flower.length)] : null)),
      big:[0, 1, 2].map(() => mkTuft(dark, r, 220, 170, 16 + Math.floor(r()*6), null)),
      cloudSpr:[0, 1, 2].map(() => mkCloud(C.cloud, r)), dark:mkBlob('#000000'), light:mkBlob('#ffffff'),
      back:[], front:[], fore:[], clouds:[], shadows:[], glints:[], bits:[], flies:[], flocks:[], lines:[], mist:[], nextFlock:2 + r()*4, nextLine:1 + r()*3};
    for (let x = -20; x < W + 30; x += 15 + r()*22) st.back.push({x, y:gy - 2 + r()*5, s:.34 + r()*.2, i:Math.floor(r()*5), ph:r()*6});
    for (let x = -20; x < W + 30; x += 46 + r()*95) st.front.push({x, y:gy + 52 + r()*10, s:.42 + r()*.22, i:Math.floor(r()*5), ph:r()*6});
    for (let x = -60; x < W + 60; x += 70 + r()*90){ if (x > W*.3 && x < W*.7) continue; st.fore.push({x, y:H + 14 + r()*12, s:.5 + r()*.45, i:Math.floor(r()*3), ph:r()*6}); }
    for (let i = 0; i < Math.round(5*C.clouds); i++) st.clouds.push({x:r()*(W + 400) - 200, y:(.04 + r()*.3)*gy, s:.55 + r()*.75, v:5 + r()*9, i:Math.floor(r()*3), a:.55 + r()*.35});
    for (let i = 0; i < 3; i++) st.shadows.push({x:r()*(W + 900) - 450, w:420 + r()*380, v:26 + r()*18});
    for (let i = 0; i < 46; i++) st.glints.push({x:r()*W, y:gy - 64 + r()*56, w:10 + r()*26, k:r()});
    for (let i = 0; i < 16; i++) st.glints.push({x:r()*W, y:gy + 64 + r()*(H - gy - 70), w:16 + r()*34, k:r()});
    for (let i = 0; i < C.nBits; i++) st.bits.push({x:r()*W, y:r()*(gy + 40), ph:r()*6, sz:.7 + r()*.8, c:C.bitCol[Math.floor(r()*C.bitCol.length)], v:.6 + r()*.8, ch:'1234567890×='[Math.floor(r()*12)]});
    for (let i = 0; i < C.fly; i++) st.flies.push({x:r()*W, y:gy - 20 - r()*70, ph:r()*6, c:['#ffe27a', '#ff9ac0', '#9fd8ff', '#ffffff'][Math.floor(r()*4)], sx:.5 + r()*.6});
    if (C.mist) for (let i = 0; i < 4; i++) st.mist.push({x:r()*(W + 600) - 300, y:gy - 26 + r()*50, w:380 + r()*300, v:7 + r()*8});
    st.r = r;
  }
  const env = t => .58 + .42*Math.sin(t*.31)*Math.sin(t*.13 + 1);                                   // rajadas: o vento cresce e descansa
  const gust = (x, t) => (.55*Math.sin(x*.006 - t*1.15) + .3*Math.sin(x*.017 - t*2.3 + 1.3) + .15*Math.sin(x*.041 - t*3.9))*env(t);

  function tuftAt(ctx, spr, o, t, k){
    const w = spr.width*o.s, h = spr.height*o.s, sh = (gust(o.x, t) + .25)*k + Math.sin(t*2.6 + o.ph)*.03;
    ctx.save(); ctx.translate(o.x, o.y); ctx.transform(1, 0, -sh, 1, 0, 0); ctx.drawImage(spr, -w/2, -h, w, h); ctx.restore();
  }
  function bird(ctx, x, y, s, flap, col){
    ctx.strokeStyle = col; ctx.lineWidth = 1.7*s; ctx.lineCap = 'round'; ctx.beginPath();
    ctx.moveTo(x - 7*s, y - flap*5*s); ctx.quadraticCurveTo(x - 3*s, y - 1.5*s - flap*2*s, x, y); ctx.quadraticCurveTo(x + 3*s, y - 1.5*s - flap*2*s, x + 7*s, y - flap*5*s); ctx.stroke();
  }

  function back(ctx, W, H, gy, key){
    if (!st || st.key !== key || Math.abs(st.W - W) > 2 || Math.abs(st.gy - gy) > 2) setup(key, W, H, gy);
    const now = performance.now()/1000, t = still ? 0 : now - st.t0, dt = still ? 0 : Math.min(.05, now - last), C = st.C; last = now; st.t = t;
    if (!still){
      if (C.rays){                                                                                  // raios de sol
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 4; i++){ const a = .42 + i*.17 + Math.sin(t*.22 + i)*.035, len = H*1.5, x0 = -W*.04, y0 = -H*.12, wd = .05 + .02*Math.sin(t*.4 + i*2);
          const g = ctx.createLinearGradient(x0, y0, x0 + Math.cos(a)*len, y0 + Math.sin(a)*len); g.addColorStop(0, 'rgba(255,250,220,' + (C.rays*(.8 + .2*Math.sin(t*.6 + i))).toFixed(3) + ')'); g.addColorStop(1, 'rgba(255,250,220,0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + Math.cos(a - wd)*len, y0 + Math.sin(a - wd)*len); ctx.lineTo(x0 + Math.cos(a + wd)*len, y0 + Math.sin(a + wd)*len); ctx.fill(); }
        ctx.restore();
      }
      for (const c of st.clouds){ c.x += c.v*dt*(.6 + env(t)); if (c.x - 170*c.s > W) c.x = -170*c.s - st.r()*200; ctx.globalAlpha = c.a; ctx.drawImage(st.cloudSpr[c.i], c.x - 160*c.s, c.y - 75*c.s, 320*c.s, 150*c.s); }
      ctx.globalAlpha = 1;
      // pássaros (ou morcegos) em bando
      st.nextFlock -= dt;
      if (st.nextFlock <= 0 && C.birds > 0){ st.nextFlock = (7 + st.r()*12)/C.birds; const s = .7 + st.r()*.9, dir = st.r() < .8 ? 1 : -1; st.flocks.push({x:dir > 0 ? -60 : W + 60, y:(.06 + st.r()*.4)*gy, s, v:(38 + st.r()*30)*s*dir, n:C.bats ? 2 + Math.floor(st.r()*3) : 3 + Math.floor(st.r()*5), ph:st.r()*6}); }
      for (const f of st.flocks){
        f.x += f.v*dt; const d = Math.sign(f.v);
        for (let i = 0; i < f.n; i++){ const row = Math.ceil(i/2), side = i % 2 ? 1 : -1, bx = f.x - d*row*15*f.s, by = f.y + side*row*7*f.s + Math.sin(t*1.3 + f.ph + i)*3*f.s + (C.bats ? Math.sin(t*9 + i*2)*4 : 0);
          bird(ctx, bx, by, f.s, Math.sin(t*(C.bats ? 17 : 8.5) + i*1.3 + f.ph), C.bats ? 'rgba(30,20,60,.8)' : 'rgba(40,50,70,.62)'); }
      }
      st.flocks = st.flocks.filter(f => f.x > -140 && f.x < W + 140);
      // sombras de nuvem correndo pelo campo
      ctx.globalAlpha = C.shadow;
      for (const s of st.shadows){ s.x += s.v*dt*(.6 + env(t)); if (s.x - s.w > W) s.x = -s.w - st.r()*300; ctx.drawImage(st.dark, s.x - s.w/2, gy - 78, s.w, H - gy + 120); }
      // o vento acendendo a grama: riscos de luz que seguem a rajada
      ctx.strokeStyle = C.glint; ctx.lineCap = 'round';
      for (const g of st.glints){ const v = gust(g.x, t); if (v < .12) continue; ctx.globalAlpha = Math.min(.5, v*v*.9)*(.5 + g.k*.5); ctx.lineWidth = 1.2 + g.k*1.2; ctx.beginPath(); ctx.moveTo(g.x - g.w/2, g.y + 2); ctx.quadraticCurveTo(g.x, g.y - 2 - v*3, g.x + g.w/2, g.y); ctx.stroke(); }
      ctx.globalAlpha = 1;
      for (const m of st.mist){ m.x += m.v*dt; if (m.x - m.w > W) m.x = -m.w; ctx.globalAlpha = C.mist*(.7 + .3*Math.sin(t*.5 + m.w)); ctx.drawImage(st.light, m.x - m.w/2, m.y - 34, m.w, 68); }
      ctx.globalAlpha = 1;
    }
    for (const o of st.back) tuftAt(ctx, st.tuft[o.i], o, t, .34);
  }

  function front(ctx, W, H, gy, key){
    if (!st || st.key !== key) return;
    const t = st.t || 0, dt = still ? 0 : .0166, C = st.C, e = env(t);
    for (const o of st.front) tuftAt(ctx, st.tuft[o.i], o, t, .4);
    if (!still){
      // pétalas, vaga-lumes, brasas, neve, pólen ou runas levados pelo vento
      for (const b of st.bits){
        const kind = C.bits;
        if (kind === 'petal' || kind === 'pollen'){ b.x += (26 + 70*e)*b.v*dt; b.y += (Math.sin(t*1.4 + b.ph)*14 + (kind === 'petal' ? 9 : -2))*dt; }
        else if (kind === 'snow'){ b.x += (8 + 30*e + Math.sin(t + b.ph)*10)*dt; b.y += (26 + 18*b.v)*dt; }
        else if (kind === 'ember'){ b.x += (6 + 22*e)*dt; b.y -= (22 + 16*b.v)*dt; }
        else { b.x += Math.sin(t*.7 + b.ph)*12*dt; b.y += Math.cos(t*.9 + b.ph*1.7)*9*dt - (kind === 'rune' ? 5*dt : 0); }
        if (b.x > W + 12) b.x = -12; if (b.x < -14) b.x = W + 10; if (b.y > gy + 60) b.y = -8; if (b.y < -12) b.y = gy + 50;
        const tw = .5 + .5*Math.sin(t*2.2 + b.ph*3);
        if (kind === 'petal'){ ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(t*1.8*b.v + b.ph); ctx.scale(1, .45 + .4*Math.sin(t*3 + b.ph)); ctx.globalAlpha = .9; ctx.fillStyle = b.c; ctx.beginPath(); ctx.ellipse(0, 0, 3.4*b.sz, 2*b.sz, 0, 0, 7); ctx.fill(); ctx.restore(); }
        else if (kind === 'rune'){ ctx.globalAlpha = .25 + .4*tw; ctx.fillStyle = b.c; ctx.font = '900 ' + (9*b.sz + 4) + 'px Nunito, sans-serif'; ctx.textAlign = 'center'; ctx.fillText(b.ch, b.x, b.y); }
        else { const rad = kind === 'snow' ? 1.6*b.sz : kind === 'pollen' ? 1.2*b.sz : 1.5*b.sz, glow = kind !== 'snow';
          if (glow){ ctx.globalAlpha = (.18 + .3*tw)*(kind === 'pollen' ? .6 : 1); ctx.drawImage(st.light, b.x - rad*5, b.y - rad*5, rad*10, rad*10); }
          ctx.globalAlpha = kind === 'snow' ? .9 : .45 + .55*tw; ctx.fillStyle = b.c; ctx.beginPath(); ctx.arc(b.x, b.y, rad, 0, 7); ctx.fill(); }
      }
      ctx.globalAlpha = 1;
      for (const f of st.flies){                                                                    // borboletas
        f.x += (Math.sin(t*.5 + f.ph)*22 + 9)*dt; f.y += Math.cos(t*.8 + f.ph*2)*16*dt; if (f.x > W + 20) f.x = -20; f.y = Math.max(gy - 110, Math.min(gy + 30, f.y));
        const wing = Math.abs(Math.sin(t*11 + f.ph)), s = 4.2*f.sx + 2.4; ctx.fillStyle = f.c; ctx.globalAlpha = .95;
        for (const d of [-1, 1]){ ctx.beginPath(); ctx.moveTo(f.x, f.y); ctx.quadraticCurveTo(f.x + d*s*wing, f.y - s*1.3, f.x + d*s*1.1*wing, f.y - s*.2); ctx.quadraticCurveTo(f.x + d*s*.9*wing, f.y + s*.9, f.x, f.y); ctx.fill(); }
      }
      // riscos de vento, como nos desenhos animados: uma linha que entra, faz uma volta e some
      st.nextLine -= dt;
      if (st.nextLine <= 0){ st.nextLine = (2.5 + st.r()*5)/(.5 + e); st.lines.push({x:-140, y:gy - 30 - st.r()*(gy*.5), t:0, v:230 + st.r()*150, len:110 + st.r()*90, amp:6 + st.r()*10, loop:st.r() < .5}); }
      ctx.strokeStyle = '#ffffff'; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      for (const l of st.lines){
        l.t += dt; l.x += l.v*dt; const a = Math.min(1, l.t/.4)*Math.max(0, 1 - l.x/(W + 200))*.55; ctx.globalAlpha = a; ctx.lineWidth = 1.6; ctx.beginPath();
        for (let i = 0; i <= 22; i++){ const q = i/22, px = l.x + q*l.len, lp = l.loop ? Math.exp(-Math.pow((q - .6)*6, 2)) : 0;
          const x = px - Math.sin(q*6.283*1.0)*lp*16, y = l.y + Math.sin(px*.012 + l.amp)*l.amp - lp*18*Math.sin(q*3.1416);
          if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y); }
        ctx.stroke();
      }
      st.lines = st.lines.filter(l => l.x < W + 60);
      ctx.globalAlpha = 1;
    }
    ctx.globalAlpha = .93; for (const o of st.fore) tuftAt(ctx, st.big[o.i], o, t, .5); ctx.globalAlpha = 1;
  }
  return {back, front, CFG};
})();
