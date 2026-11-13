/* Guardiões da Tabuada: arena 3D (Three.js r149).
   O jogo continua simulando a batalha em "espaço de pista" (x ao longo da pista, y = altura). Este arquivo monta o mundo 3D
   (campo, rio, pontes, torres, castelos, enfeites), cuida da câmera e devolve a projeção de qualquer ponto da pista na tela,
   para o jogo desenhar heróis e efeitos por cima, na perspectiva certa. */
window.GT3D = (() => {
  const T = THREE, OFF = 100000;
  let renderer, scene, camera, W = 2, H = 2, ins = {top:60, bottom:170}, cfg = null, world = null, time = 0;
  let M = new Float32Array(16), fpx = 1, base = null, ready = false;
  const tmpM = new T.Matrix4(), ray = new T.Raycaster(), plane = new T.Plane(new T.Vector3(0, 1, 0), 0), v3 = new T.Vector3(), v2 = new T.Vector2();
  const LANE_X = 132, FIELD_W = 262;

  const BIO = {
    campo:  {sky:0x8fd6ff, fog:0xbfe6ff, g1:'#74c94f', g2:'#5db443', path:'#e3cf8f', out:0x4f9f3c, water:'#3aa6ee', w2:'#bfeaff', tree:[0x2f9e44, 0x1f7a36], trunk:0x7a5230, rock:0xa4acb5, sun:0xfff1cf, amb:0xbfdcff, lava:false},
    pantano:{sky:0x9fc4a8, fog:0xa9c9b0, g1:'#6a9a50', g2:'#4f7f48', path:'#b9b07a', out:0x3f6a40, water:'#4c8a66', w2:'#b7e3c0', tree:[0x3f7350, 0x2a543c], trunk:0x54402c, rock:0x7f8a7a, sun:0xf3f0c8, amb:0xa9c9b0, lava:false},
    sombra: {sky:0x2a2356, fog:0x2f2860, g1:'#5a4c94', g2:'#44397a', path:'#9c8fc9', out:0x30285c, water:'#6a48c0', w2:'#d3c2ff', tree:[0x4a3c86, 0x2f2660], trunk:0x2a2240, rock:0x5f5880, sun:0xcfc4ff, amb:0x6f66b0, lava:false},
    vulcao: {sky:0x4a2a26, fog:0x5a3026, g1:'#7a5644', g2:'#5c3f34', path:'#b89068', out:0x40291f, water:'#ff7a1c', w2:'#ffe08a', tree:[0x3c2c28, 0x2a1f1c], trunk:0x2a1c18, rock:0x4a3c3a, sun:0xffc890, amb:0x9a6a58, lava:true},
    neve:   {sky:0xcfeaff, fog:0xe4f3ff, g1:'#f1f8ff', g2:'#d8e9f8', path:'#bccfe2', out:0xd4e6f6, water:'#8fd6ff', w2:'#ffffff', tree:[0x2f7a66, 0xf4fbff], trunk:0x6a5038, rock:0xb9c8d6, sun:0xffffff, amb:0xd6ecff, lava:false},
    dourado:{sky:0xffe2a0, fog:0xffe9b8, g1:'#e8c95e', g2:'#d3ad45', path:'#f6e7b4', out:0xc79a38, water:'#58c6e6', w2:'#e9fbff', tree:[0xe2992c, 0xc7741f], trunk:0x7a5230, rock:0xc9b58a, sun:0xfff0c0, amb:0xffe6b0, lava:false},
    arcano: {sky:0x2a2a7a, fog:0x34329a, g1:'#4a5cb0', g2:'#37458f', path:'#a9b8ff', out:0x2a3378, water:'#b070ff', w2:'#f0dcff', tree:[0x9f7bff, 0x6f4fe0], trunk:0x3a3070, rock:0x6f78c0, sun:0xd8d0ff, amb:0x7f86e0, lava:false, crystal:true}
  };
  const TEAMC = [{stone:0xe4dcc6, dark:0xbdb49c, roof:0x3f7bff, flag:0x6fa8ff}, {stone:0x6a6284, dark:0x4a4462, roof:0xe0425c, flag:0xff7a8c}];

  function init(canvas){
    renderer = new T.WebGLRenderer({canvas, antialias:true, alpha:false, powerPreference:'high-performance'});
    renderer.outputEncoding = T.sRGBEncoding;
    renderer.toneMapping = T.NoToneMapping;
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap; renderer.shadowMap.autoUpdate = false;
    camera = new T.PerspectiveCamera(30, 1, 50, 9000);
    ready = true;
  }

  /* ---------- geometria da pista ---------- */
  const laneOf = x => Math.floor((x + OFF/2)/OFF);               // 0 e 1 = pistas; 2 = centro (castelos)
  function lateral(lane, pos){
    if (lane === 2) return 0;
    const s = lane === 0 ? -1 : 1, c = cfg;
    let t = 1;
    if (pos < c.GUARDX[0]) t = (pos - c.TOWX[0])/(c.GUARDX[0] - c.TOWX[0]);
    else if (pos > c.GUARDX[1]) t = (c.TOWX[1] - pos)/(c.TOWX[1] - c.GUARDX[1]);
    t = Math.max(0, Math.min(1, t)); t = t*t*(3 - 2*t);
    return s*(52 + (LANE_X - 52)*t);
  }
  const zOf = pos => cfg.LW/2 - pos;                              // time 0 fica perto da câmera

  /* ---------- texturas feitas em código ---------- */
  function rng(seed){ let s = seed; return () => (s = (s*16807) % 2147483647)/2147483647; }
  function groundTex(b){
    const cw = 512, ch = 1024, cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
    const c = cv.getContext('2d'), r = rng(7), c0 = cfg, FL = c0.LW + 240, FW = 2*FIELD_W + 0;
    const X = wx => (wx + FW/2)/FW*cw, Y = pos => (1 - (pos + 120)/FL)*ch;          // pos 0 embaixo
    c.fillStyle = b.g2; c.fillRect(0, 0, cw, ch);
    const bands = 14;                                                              // gramado em faixas, como campo aparado
    for (let i = 0; i < bands; i++){ c.fillStyle = i % 2 ? b.g1 : b.g2; c.fillRect(0, i*ch/bands, cw, ch/bands + 1); }
    for (let i = 0; i < 900; i++){                                                 // manchas de pincel
      const x = r()*cw, y = r()*ch, rad = 6 + r()*26; c.globalAlpha = .05 + r()*.07; c.fillStyle = r() < .5 ? '#ffffff' : '#000000';
      c.beginPath(); c.ellipse(x, y, rad, rad*.55, r()*3, 0, 7); c.fill();
    }
    c.globalAlpha = 1;
    for (const pass of [[58, 'rgba(0,0,0,.16)'], [48, b.path]]){                    // caminhos das duas pistas
      for (const lane of [0, 1]){
        c.strokeStyle = pass[1]; c.lineWidth = pass[0]*cw/FW*1.0; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
        for (let p = c0.TOWX[0] - 20; p <= c0.TOWX[1] + 20; p += 10){ const x = X(lateral(lane, p)), y = Y(p); if (p === c0.TOWX[0] - 20) c.moveTo(x, y); else c.lineTo(x, y); }
        c.stroke();
      }
    }
    for (let i = 0; i < 500; i++){ const lane = r() < .5 ? 0 : 1, p = c0.TOWX[0] + r()*(c0.TOWX[1] - c0.TOWX[0]); c.globalAlpha = .12; c.fillStyle = r() < .5 ? '#fff' : '#5a4020'; c.beginPath(); c.arc(X(lateral(lane, p) + (r() - .5)*40), Y(p), 1 + r()*2.4, 0, 7); c.fill(); }
    c.globalAlpha = 1;
    for (const tm of [0, 1]){                                                       // pátio de pedra dos castelos
      const y = Y(c0.TOWX[tm] + (tm ? 30 : -30)), g = c.createRadialGradient(cw/2, y, 10, cw/2, y, 150);
      g.addColorStop(0, 'rgba(235,225,200,.85)'); g.addColorStop(.7, 'rgba(235,225,200,.55)'); g.addColorStop(1, 'rgba(235,225,200,0)');
      c.fillStyle = g; c.beginPath(); c.ellipse(cw/2, y, 170, 120, 0, 0, 7); c.fill();
    }
    const vg = c.createLinearGradient(0, 0, cw, 0); vg.addColorStop(0, 'rgba(0,0,0,.28)'); vg.addColorStop(.12, 'rgba(0,0,0,0)'); vg.addColorStop(.88, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.28)');
    c.fillStyle = vg; c.fillRect(0, 0, cw, ch);
    const t = new T.CanvasTexture(cv); t.encoding = T.sRGBEncoding; t.anisotropy = 4; return t;
  }
  function waterTex(b){
    const cv = document.createElement('canvas'); cv.width = 256; cv.height = 128; const c = cv.getContext('2d'), r = rng(3);
    c.fillStyle = b.water; c.fillRect(0, 0, 256, 128);
    for (let i = 0; i < 46; i++){ c.strokeStyle = b.w2; c.globalAlpha = .18 + r()*.3; c.lineWidth = 1 + r()*2.5; c.lineCap = 'round'; const x = r()*256, y = r()*128, w = 14 + r()*40; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + w/2, y - 3 + r()*6, x + w, y); c.stroke(); if (x + w > 256){ c.beginPath(); c.moveTo(x - 256, y); c.lineTo(x + w - 256, y); c.stroke(); } }
    const t = new T.CanvasTexture(cv); t.encoding = T.sRGBEncoding; t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(7, 1); return t;
  }

  /* ---------- peças ---------- */
  const mat = (color, o) => new T.MeshStandardMaterial(Object.assign({color, roughness:.85, metalness:0, flatShading:true}, o || {}));
  function mesh(geo, m, x, y, z, sh){ const o = new T.Mesh(geo, m); o.position.set(x || 0, y || 0, z || 0); o.castShadow = sh !== false; o.receiveShadow = true; return o; }
  function roofed(g, m, R, h, y, x, z, roofH){
    g.add(mesh(new T.CylinderGeometry(R*.9, R, h, 10), m.stone, x, y + h/2, z));
    g.add(mesh(new T.CylinderGeometry(R*1.12, R*.95, h*.12, 10), m.dark, x, y + h*1.03, z));
    for (let i = 0; i < 8; i++){ const a = i/8*6.283; g.add(mesh(new T.BoxGeometry(R*.34, R*.3, R*.3), m.stone, x + Math.cos(a)*R*.98, y + h*1.09 + R*.15, z + Math.sin(a)*R*.98)); }
    g.add(mesh(new T.ConeGeometry(R*.98, roofH, 10), m.roof, x, y + h*1.09 + roofH/2 + R*.1, z));
    const pole = mesh(new T.CylinderGeometry(1.2, 1.2, roofH*.7, 5), m.dark, x, y + h*1.09 + roofH + roofH*.3, z); g.add(pole);
    const flag = mesh(new T.PlaneGeometry(R*.75, R*.42), m.flag, x + R*.38, y + h*1.09 + roofH + roofH*.5, z, false); flag.material.side = T.DoubleSide; g.add(flag); (g.userData.flags = g.userData.flags || []).push(flag);
  }
  function mats(team){ const c = TEAMC[team]; return {stone:mat(c.stone), dark:mat(c.dark), roof:mat(c.roof, {roughness:.6}), flag:mat(c.flag, {roughness:.7, flatShading:false}), gate:mat(0x241c30)}; }
  function makeGuard(team){
    const g = new T.Group(), m = mats(team); g.userData.m = m;
    g.add(mesh(new T.CylinderGeometry(40, 46, 10, 10), m.dark, 0, 5, 0));
    roofed(g, m, 30, 78, 8, 0, 0, 46);
    const f = team === 0 ? -1 : 1;
    g.add(mesh(new T.BoxGeometry(16, 26, 4), m.gate, 0, 22, f*29, false));
    for (const a of [-.6, .6]) g.add(mesh(new T.BoxGeometry(5, 12, 3), m.gate, Math.sin(a)*27, 62, f*Math.cos(a)*27, false));
    return g;
  }
  function makeCastle(team){
    const g = new T.Group(), m = mats(team), f = team === 0 ? -1 : 1; g.userData.m = m;
    g.add(mesh(new T.BoxGeometry(190, 12, 120), m.dark, 0, 6, 0));
    g.add(mesh(new T.BoxGeometry(150, 70, 84), m.stone, 0, 47, 0));
    for (let i = -3; i <= 3; i++){ g.add(mesh(new T.BoxGeometry(13, 12, 10), m.stone, i*22, 88, f*38)); g.add(mesh(new T.BoxGeometry(13, 12, 10), m.stone, i*22, 88, -f*38)); }
    g.add(mesh(new T.BoxGeometry(34, 46, 6), m.gate, 0, 35, f*42, false));
    { const arch = mesh(new T.CylinderGeometry(17, 17, 6, 14), m.gate, 0, 58, f*42, false); arch.rotation.x = Math.PI/2; g.add(arch); }
    roofed(g, m, 24, 104, 10, -78, f*30, 44);
    roofed(g, m, 24, 104, 10, 78, f*30, 44);
    roofed(g, m, 34, 140, 10, 0, -f*8, 64);
    const ban = mesh(new T.PlaneGeometry(20, 34), m.flag, 0, 64, f*45.5, false); ban.material.side = T.DoubleSide; g.add(ban);
    return g;
  }
  function tree(b, r, s){
    const g = new T.Group();
    if (b.crystal){ const m = mat(b.tree[r() < .5 ? 0 : 1], {emissive:b.tree[0], emissiveIntensity:.45, roughness:.3}); const o = mesh(new T.OctahedronGeometry(16*s, 0), m, 0, 22*s, 0); o.scale.y = 1.9; g.add(o); return g; }
    g.add(mesh(new T.CylinderGeometry(4*s, 6*s, 22*s, 6), mat(b.trunk), 0, 11*s, 0));
    if (b.lava){ const br = mesh(new T.CylinderGeometry(1.5*s, 3*s, 26*s, 5), mat(b.trunk), 6*s, 30*s, 0); br.rotation.z = -.5; g.add(br); return g; }
    const c1 = mat(b.tree[0]), c2 = mat(b.tree[1]);
    g.add(mesh(new T.ConeGeometry(24*s, 34*s, 7), c1, 0, 36*s, 0)); g.add(mesh(new T.ConeGeometry(18*s, 28*s, 7), c2, 0, 56*s, 0)); g.add(mesh(new T.ConeGeometry(11*s, 22*s, 7), c1, 0, 73*s, 0));
    return g;
  }

  /* ---------- mundo ---------- */
  function build(biome, c){
    cfg = c; const b = BIO[biome] || BIO.campo;
    if (scene){ scene.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material){ if (o.material.map) o.material.map.dispose(); o.material.dispose(); } }); }
    scene = new T.Scene(); scene.background = new T.Color(b.sky); scene.fog = new T.Fog(b.fog, 2300, 5200);
    world = {b, towers:[], water:null, drop:null, ring:null, flags:[]};
    scene.add(new T.HemisphereLight(b.amb, 0x5a5040, .62));
    const sun = new T.DirectionalLight(b.sun, .78); sun.position.set(-520, 900, 380); sun.castShadow = true;
    sun.shadow.mapSize.set(1024, 1024); const sc = sun.shadow.camera; sc.left = -520; sc.right = 520; sc.top = 820; sc.bottom = -820; sc.near = 100; sc.far = 2600; sun.shadow.bias = -.0012; sun.shadow.radius = 3;
    scene.add(sun); scene.add(sun.target);
    const L = c.LW, FL = L + 240;
    const out = mesh(new T.PlaneGeometry(9000, 9000), mat(b.out, {flatShading:false}), 0, -1.5, 0, false); out.rotation.x = -Math.PI/2; scene.add(out);
    { const rr = rng(41), pm = mat(new T.Color(b.out).multiplyScalar(.86), {flatShading:false}), pl = mat(new T.Color(b.out).multiplyScalar(1.12), {flatShading:false});
      for (let i = 0; i < 60; i++){ const o = mesh(new T.CircleGeometry(40 + rr()*110, 9), rr() < .5 ? pm : pl, (rr() - .5)*2400, -1.2 + i*.002, (rr() - .5)*2600, false); o.rotation.x = -Math.PI/2; scene.add(o); } }
    const field = mesh(new T.PlaneGeometry(2*FIELD_W, FL), new T.MeshStandardMaterial({map:groundTex(b), roughness:.95}), 0, 0, 0, false); field.rotation.x = -Math.PI/2; scene.add(field);
    for (const s of [-1, 1]){ const edge = mesh(new T.BoxGeometry(14, 10, FL), mat(TEAMC[1].dark), s*(FIELD_W + 7), 4, 0); scene.add(edge); }      // mureta lateral
    // rio e pontes
    const wm = new T.MeshStandardMaterial({map:waterTex(b), roughness:.25, metalness:.05, emissive:b.lava ? 0xff5a10 : 0x000000, emissiveIntensity:b.lava ? .9 : 0});
    const water = mesh(new T.PlaneGeometry(2600, 84), wm, 0, .8, 0, false); water.rotation.x = -Math.PI/2; scene.add(water); world.water = wm.map;
    for (const s of [-1, 1]) scene.add(mesh(new T.BoxGeometry(2600, 5, 9), mat(0x6a5a44), 0, 1.5, s*46));
    const wood = mat(0xb9864a), wood2 = mat(0x8a5f30);
    for (const lane of [0, 1]){
      const x = lateral(lane, L/2);
      scene.add(mesh(new T.BoxGeometry(92, 7, 118), wood, x, 3.6, 0));
      for (let i = -5; i <= 5; i++) scene.add(mesh(new T.BoxGeometry(92, 1.4, 2), wood2, x, 7.4, i*10.5, false));
      for (const s of [-1, 1]){ scene.add(mesh(new T.BoxGeometry(5, 5, 118), wood2, x + s*46, 15, 0)); for (const z of [-54, -18, 18, 54]) scene.add(mesh(new T.BoxGeometry(6, 16, 6), wood2, x + s*46, 9, z)); }
    }
    // torres e castelos
    for (const tm of [0, 1]){
      const cs = makeCastle(tm); cs.position.set(0, 0, zOf(c.TOWX[tm]) + (tm === 0 ? 46 : -46)); scene.add(cs); world.towers.push({key:'c' + tm, g:cs, top:185});
      for (const lane of [0, 1]){ const g = makeGuard(tm); g.position.set(lateral(lane, c.GUARDX[tm]), 0, zOf(c.GUARDX[tm])); scene.add(g); world.towers.push({key:'g' + tm + lane, g, top:140}); }
    }
    // enfeites em volta do campo
    const r = rng(biome.length*97 + 11);
    for (let i = 0; i < 70; i++){
      const side = r() < .5 ? -1 : 1, far = r() < .28;
      const x = far ? (r() - .5)*1500 : side*(FIELD_W + 60 + r()*520), z = far ? -(FL/2 + 90 + r()*700) : (r() - .5)*(FL + 500);
      if (Math.abs(z) < 70 && !far) continue;
      const t = tree(b, r, .9 + r()*.9); t.position.set(x, 0, z); t.rotation.y = r()*6; scene.add(t);
    }
    const rm = mat(b.rock);
    for (let i = 0; i < 26; i++){ const side = r() < .5 ? -1 : 1, s = 8 + r()*22; const o = mesh(new T.IcosahedronGeometry(s, 0), rm, side*(FIELD_W + 30 + r()*420), s*.45, (r() - .5)*(FL + 300)); o.scale.y = .7; o.rotation.set(r()*3, r()*3, 0); scene.add(o); }
    // marcador de onde a carta vai cair
    const zone = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({color:0x4fa0ff, transparent:true, opacity:.4, depthWrite:false, fog:false})); zone.rotation.x = -Math.PI/2; zone.position.y = 1.2; zone.visible = false; scene.add(zone);
    const ring = new T.Mesh(new T.RingGeometry(24, 40, 40), new T.MeshBasicMaterial({color:0xffd23f, transparent:true, opacity:1, depthWrite:false, depthTest:false, side:T.DoubleSide, fog:false})); ring.rotation.x = -Math.PI/2; ring.position.y = 2.2; ring.visible = false; scene.add(ring);
    world.zones = [zone, zone.clone()]; world.zones[1].material = zone.material; scene.add(world.zones[1]); world.ring = ring;
    scene.traverse(o => { if (o.userData && o.userData.flags) world.flags.push(...o.userData.flags); });
    renderer.shadowMap.needsUpdate = true;
    fit();
  }

  /* ---------- câmera ---------- */
  const YAW = .2, PITCH = 52*Math.PI/180;
  function place(d, tx, tz, yaw, pitch){
    yaw = yaw == null ? YAW : yaw; pitch = pitch == null ? PITCH : pitch;
    camera.position.set(tx + d*Math.sin(yaw)*Math.cos(pitch), d*Math.sin(pitch), tz + d*Math.cos(yaw)*Math.cos(pitch));
    camera.lookAt(tx, 0, tz); camera.updateMatrixWorld(true);
  }
  function bbox(){
    const c = cfg, L = c.LW, pts = [];
    for (const x of [-FIELD_W - 10, FIELD_W + 10]) for (const z of [L/2 + 95, -L/2 - 70]) pts.push([x, 0, z]);
    pts.push([0, 215, zOf(c.TOWX[1]) - 46], [-90, 150, zOf(c.TOWX[1]) - 20], [90, 150, zOf(c.TOWX[1]) - 20], [-LANE_X, 150, zOf(c.GUARDX[1])], [LANE_X, 150, zOf(c.GUARDX[1])]);
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (const p of pts){ v3.set(p[0], p[1], p[2]).project(camera); const sx = (v3.x*.5 + .5)*W, sy = (-v3.y*.5 + .5)*H; x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy); }
    return {x0, x1, y0, y1};
  }
  function fit(){
    if (!cfg || !ready) return;
    camera.aspect = W/H; camera.clearViewOffset(); camera.updateProjectionMatrix();
    const aw = W - 8, ah = Math.max(120, H - ins.top - ins.bottom);
    let d = 2200;
    for (let i = 0; i < 14; i++){ place(d, 0, 0); const b = bbox(); const s = Math.max((b.x1 - b.x0)/aw, (b.y1 - b.y0)/ah); d *= s; }
    place(d, 0, 0); const b = bbox();
    const ex = (b.x0 + b.x1)/2 - W/2, ey = (b.y0 + b.y1)/2 - (ins.top + ah/2);
    camera.setViewOffset(W, H, ex, ey, W, H); camera.updateProjectionMatrix();
    base = {d, ex, ey};
    if (scene && scene.fog){ scene.fog.near = d + 700; scene.fog.far = d + 3600; }
    fpx = (H/2)/Math.tan(camera.fov*Math.PI/360);
    syncM();
  }
  function syncM(){ camera.updateMatrixWorld(true); tmpM.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse); M.set(tmpM.elements); }
  function resize(w, h, insets, dpr){
    W = Math.max(2, w); H = Math.max(2, h); if (insets) ins = insets;
    if (!ready) return;
    renderer.setPixelRatio(Math.min(dpr || 1, 2)); renderer.setSize(W, H, false);
    fit();
  }

  /* ---------- projeção: ponto do mundo -> tela ---------- */
  function projW(wx, wy, wz){
    const w = M[3]*wx + M[7]*wy + M[11]*wz + M[15];
    return {sx:((M[0]*wx + M[4]*wy + M[8]*wz + M[12])/w*.5 + .5)*W, sy:(-(M[1]*wx + M[5]*wy + M[9]*wz + M[13])/w*.5 + .5)*H, k:fpx/w};
  }
  // x no espaço de pista (com o deslocamento da pista); row = faixa de profundidade do herói (0, 15, 30)
  function ground(x, row){
    const lane = laneOf(x), pos = x - lane*OFF;
    return projW(lateral(lane, pos) + ((row == null ? 15 : row) - 15)*1.5, 0, zOf(pos));
  }
  function towerTop(key){ const t = world && world.towers.find(q => q.key === key); if (!t) return null; const p = t.g.position; return projW(p.x, t.top*t.g.scale.y + p.y, p.z); }
  function pick(sx, sy){
    if (!cfg) return null;
    v2.set(sx/W*2 - 1, -(sy/H*2 - 1)); ray.setFromCamera(v2, camera);
    const hit = ray.ray.intersectPlane(plane, v3); if (!hit) return null;
    return {lane:hit.x < 0 ? 0 : 1, pos:cfg.LW/2 - hit.z, wx:hit.x};
  }
  function setDrop(on, lane, pos, lo, hi){
    if (!world) return;
    for (const l of [0, 1]){ const z = world.zones[l]; z.visible = !!on; if (on){ z.scale.set(FIELD_W - 16, hi - lo, 1); z.position.set((l ? 1 : -1)*(FIELD_W/2), 1.2, zOf((lo + hi)/2)); } }
    world.ring.visible = !!on && lane != null;
    if (on && lane != null) world.ring.position.set(lateral(lane, pos), 2.2, zOf(pos));
  }

  /* ---------- quadro ---------- */
  function frame(st, dt){
    if (!world || !base) return;
    time += dt;
    world.water.offset.x = (time*.035) % 1;
    for (let i = 0; i < world.flags.length; i++) world.flags[i].rotation.y = Math.sin(time*3 + i)*.35;
    world.zones[0].material.opacity = .34 + .1*Math.sin(time*5); world.ring.scale.setScalar(1 + .08*Math.sin(time*8));
    let dirty = false;
    for (const t of world.towers){
      const s = st.towers[t.key]; if (!s) continue;
      const col = s.collapse > 0 ? Math.min(1, s.collapse) : 0, e = col*col*(3 - 2*col);
      if (t.col !== e){ t.g.position.y = -e*58; t.g.rotation.z = e*.3*(t.key.charCodeAt(1) % 2 ? 1 : -1); t.g.rotation.x = e*.16; t.g.scale.y = 1 - e*.45; t.col = e; dirty = true; }
      const fl = s.flash > 0 ? 1 : 0;
      if (t.fl !== fl){ t.fl = fl; const m = t.g.userData.m; m.stone.emissive.setHex(fl ? 0x553333 : 0); m.roof.emissive.setHex(fl ? 0x442222 : 0); }
      const rc = 1 + (s.recoil > 0 ? s.recoil*.25 : 0); t.g.scale.x = t.g.scale.z = rc;
    }
    if (dirty) renderer.shadowMap.needsUpdate = true;
    // câmera: entrada, tremor e aproximação na queda do castelo
    let d = base.d, tx = 0, tz = 0, yaw = YAW, pitch = PITCH;
    if (st.intro > 0){ const q = st.intro*st.intro*(3 - 2*st.intro); d *= 1 + .55*q; yaw += .9*q; pitch -= .2*q; tz -= 120*q; }
    if (st.zoom){ const q = st.zoom.q; d *= 1 - .3*q; tx = st.zoom.wx*q*.8; tz = st.zoom.wz*q*.8; }
    place(d, tx, tz, yaw, pitch);
    if (st.shake > 0){ const a = st.shake*26, t = performance.now()*.03; camera.position.x += a*Math.sin(t*1.7); camera.position.y += a*.7*Math.sin(t*2.3); camera.updateMatrixWorld(true); }
    syncM();
    renderer.render(scene, camera);
  }
  const worldOf = x => { const lane = laneOf(x), pos = x - lane*OFF; return {wx:lateral(lane, pos), wz:zOf(pos)}; };
  return {init, build, resize, frame, ground, projW, pick, setDrop, towerTop, worldOf, laneOf, OFF, get ready(){ return ready && !!world; }, get size(){ return {W, H}; }};
})();
