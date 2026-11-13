/* Guardiões da Tabuada: cenário vivo pintado por código (WebGL). Um único programa desenha, a cada quadro, céu, sol ou lua,
   nuvens que andam, raios de luz, serras em camadas com névoa, campo com sombra de nuvem e vento na grama, e a estrada. */
window.GTSKY = (() => {
  const FS = `precision highp float;
uniform vec2 R; uniform float T, LANE; uniform vec3 SKT, SKB, SUN, FOG, HF, HN, GR, PA; uniform vec2 SP; uniform vec4 FX;
float h1(float n){ return fract(sin(n*127.1)*43758.5453); }
float h2(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7)))*43758.5453); }
float n1(float x){ float i = floor(x), f = fract(x); f = f*f*(3. - 2.*f); return mix(h1(i), h1(i + 1.), f); }
float n2(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3. - 2.*f); return mix(mix(h2(i), h2(i + vec2(1., 0.)), f.x), mix(h2(i + vec2(0., 1.)), h2(i + vec2(1., 1.)), f.x), f.y); }
float fbm(vec2 p){ float a = .5, s = 0.; for (int i = 0; i < 5; i++){ s += a*n2(p); p = p*2.03 + 7.1; a *= .5; } return s; }
float ridge(float x, float sc, float sd){ return n1(x*sc + sd)*.6 + n1(x*sc*2.3 + sd*1.7)*.28 + n1(x*sc*5.1 + sd*2.9)*.12; }
void main(){
  vec2 uv = gl_FragCoord.xy/R; float asp = R.x/R.y; vec2 p = vec2(uv.x*asp, uv.y);
  float hz = LANE + .15, night = FX.x;
  float sy = clamp((uv.y - hz)/(1. - hz), 0., 1.);
  vec3 col = mix(SKB, SKT, pow(sy, .7));
  vec2 sp = vec2(SP.x*asp, SP.y); float ds = distance(p, sp);
  col += SUN*(.5*exp(-ds*3.) + .3*exp(-ds*9.));
  col = mix(col, mix(vec3(1., .97, .86), vec3(.95, .96, 1.), night), smoothstep(.05, .044, ds));
  if (night > 0.){ vec2 g = floor(p*110.); float s = h2(g); col += night*step(.988, s)*(.45 + .55*sin(T*2. + s*40.))*sy; }
  if (FX.y > 0.){ float a = sin(p.x*3. + T*.3 + sin(p.x*7. - T*.2)*.6); float band = exp(-pow((uv.y - (.74 + .07*a))*8., 2.)); col += FX.y*band*mix(vec3(.2, .95, .6), vec3(.6, .4, 1.), .5 + .5*sin(p.x*2. + T*.2))*(.45 + .55*n2(vec2(p.x*9., T*.5))); }
  vec2 cp = vec2(p.x*1.3 + T*.014, uv.y*3.4); float w = fbm(cp*1.7 + T*.02); float c = fbm(cp + w*.55);
  float cm = smoothstep(.47, .74, c)*smoothstep(hz + .02, hz + .16, uv.y);
  float lit = clamp((c - fbm(cp + vec2(.06, .1) + w*.55))*4. + .55, 0., 1.);
  vec3 cc = mix(mix(SKB, FOG, .55)*.9, mix(vec3(1.), FOG*1.25, night*.8) + SUN*.22, lit);
  col = mix(col, cc, cm*.9);
  vec2 d = p - sp; float ang = atan(d.y, d.x); col += SUN*n1(ang*9. + T*.05)*n1(ang*23. - T*.03)*.16*exp(-ds*1.5)*(1. - night*.7);
  if (FX.z > 0.){ float vx = .68*asp, vh = hz + .34 - abs(p.x - vx)*.62 + .02*n1(p.x*14.); float vm = smoothstep(vh + .004, vh - .004, uv.y);
    vec3 vc = mix(HF*.6, FOG, .3); float top = smoothstep(hz + .22, hz + .34, uv.y); vc += vec3(1., .35, .05)*top*(.6 + .4*sin(T*1.3))*exp(-abs(p.x - vx)*14.);
    vc += vec3(1., .4, .05)*.5*smoothstep(.02, .0, abs(p.x - vx - .03*sin(uv.y*40.)))*step(hz + .05, uv.y);
    col = mix(col, vc, vm); col += vec3(1., .3, .05)*.35*exp(-distance(p, vec2(vx, hz + .36))*7.); }
  for (int i = 0; i < 4; i++){
    float fi = float(i), k = fi/3., base = hz - .01 - fi*.022, amp = mix(.2, .06, k);
    float hgt = base + amp*ridge(p.x + fi*13.7, mix(1.1, 2.7, k), 3.3 + fi*5.);
    float tr = (i >= 2) ? .02*abs(fract(p.x*mix(34., 56., k) + n1(p.x*9.)*2.) - .5)*2.*(.4 + .6*n1(p.x*5. + fi*3.)) : 0.;
    float m = smoothstep(hgt + tr + .003, hgt + tr - .003, uv.y);
    vec3 hc = mix(mix(FOG, HF, .3 + .3*k), HN, k*k);
    if (i < 2) hc = mix(hc, vec3(.97, .98, 1.), FX.w*smoothstep(base + amp*.5, base + amp*.75, uv.y)*.9);
    hc = mix(hc, FOG, (1. - k)*.3 + .35*smoothstep(base + amp*.6, base - .02, uv.y)*(1. - k*.5));
    hc += SUN*.12*(1. - k)*exp(-abs(p.x - sp.x)*1.6);
    col = mix(col, hc, m);
  }
  col = mix(col, FOG, .4*exp(-abs(uv.y - hz + .05)*26.)*(.55 + .45*n2(vec2(p.x*2. - T*.04, 3.))));
  float gy = hz - .078;
  if (uv.y < gy + .012){
    float gm = smoothstep(gy + .012, gy - .004, uv.y), dp = clamp((gy - uv.y)/gy, 0., 1.);
    vec2 gp = vec2((p.x - .5*asp)/(.28 + dp*1.3), dp*6.); float mo = fbm(gp*3.);
    vec3 g = mix(mix(GR, FOG, .4), GR*.8, dp); g *= .86 + .28*mo;
    g *= 1. - .24*smoothstep(.52, .78, fbm(vec2(gp.x*.45 + T*.06, gp.y*.5 + 3.)));
    float wv = pow(sin(gp.x*4.5 - T*1.7 + mo*6.)*.5 + .5, 7.)*smoothstep(0., .25, dp);
    g += (GR*.5 + vec3(.1, .1, .04))*wv*.55*(1. - FX.z)*(1. - .5*night);
    float rd = smoothstep(.06, .03, abs(uv.y - LANE + .012));
    g = mix(g, PA*(.86 + .2*n2(vec2(p.x*14., uv.y*46.)))*(.94 + .1*mo), rd*.92);
    g *= 1. - .3*smoothstep(LANE - .1, 0., uv.y);
    col = mix(col, g, gm);
  }
  col *= .95 + .09*fbm(p*13.);
  col *= 1. - .3*pow(length(uv - .5)*1.2, 2.8);
  col += (h2(gl_FragCoord.xy + fract(T)*61.) - .5)*.02;
  gl_FragColor = vec4(col, 1.);
}`;
  const FS2 = `precision highp float;
uniform vec2 R; uniform float T, LANE, NIGHT; uniform sampler2D TX; uniform vec4 RC; uniform vec3 SUN; uniform vec2 SP;
float h1(float n){ return fract(sin(n*127.1)*43758.5453); }
float h2(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7)))*43758.5453); }
float n1(float x){ float i = floor(x), f = fract(x); f = f*f*(3. - 2.*f); return mix(h1(i), h1(i + 1.), f); }
float n2(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3. - 2.*f); return mix(mix(h2(i), h2(i + vec2(1., 0.)), f.x), mix(h2(i + vec2(0., 1.)), h2(i + vec2(1., 1.)), f.x), f.y); }
float fbm(vec2 p){ float a = .5, s = 0.; for (int i = 0; i < 5; i++){ s += a*n2(p); p = p*2.03 + 7.1; a *= .5; } return s; }
void main(){
  vec2 uv = gl_FragCoord.xy/R; float asp = R.x/R.y; vec2 p = vec2(uv.x*asp, uv.y);
  float hz = LANE + .2;
  // o vento passa pela pintura: a grama de baixo e as copas das árvores balançam em ondas
  float env = .62 + .38*sin(T*.31)*sin(T*.13 + 1.);
  float gust = (sin(p.x*3.2 - T*1.3) + .5*sin(p.x*7.1 - T*2.2 + 1.3))*env;
  float fine = sin(p.x*64. + uv.y*38. + T*3.1)*env;
  float low = smoothstep(LANE - .03, 0., uv.y), mid = smoothstep(hz - .04, hz + .08, uv.y)*smoothstep(hz + .46, hz + .14, uv.y);
  vec2 off = vec2((gust*.0042 + fine*.0011)*low + (gust*.0017 + fine*.0007)*mid, fine*.0007*low);
  vec2 st = vec2(uv.x + off.x, 1. - (uv.y + off.y));
  vec3 col = texture2D(TX, clamp((st - RC.xy)/RC.zw, 0., 1.)).rgb;
  // nuvens andando por cima do céu pintado
  vec2 cp = vec2(p.x*1.1 + T*.02, uv.y*2.6); float c = fbm(cp + fbm(cp*1.8 + T*.015)*.5);
  float cm = smoothstep(.5, .76, c)*smoothstep(hz + .12, hz + .32, uv.y);
  col = mix(col, mix(vec3(1.), col, .3), cm*.5*(1. - NIGHT*.75));
  // sombra de nuvem correndo pelo campo e a luz do vento na grama
  float gm = smoothstep(hz + .02, hz - .08, uv.y), dp = clamp((hz - uv.y)/hz, 0., 1.);
  vec2 gp = vec2((p.x - .5*asp)/(.3 + dp*1.3), dp*6.); float mo = fbm(gp*3.);
  col *= 1. - .24*gm*smoothstep(.5, .78, fbm(vec2(gp.x*.45 + T*.06, gp.y*.5 + 3.)));
  float wv = pow(sin(gp.x*4.5 - T*1.7 + mo*6.)*.5 + .5, 7.)*gm*smoothstep(0., .2, dp);
  col += col*wv*.4*(1. - smoothstep(.07, .03, abs(uv.y - LANE + .012)))*(1. - NIGHT*.5);
  // luz: brilho e raios
  vec2 sp = vec2(SP.x*asp, SP.y), d = p - sp; float ds = length(d), ang = atan(d.y, d.x);
  col += SUN*(n1(ang*9. + T*.05)*n1(ang*23. - T*.03)*.24*exp(-ds*1.25) + .1*exp(-ds*2.4));
  col *= 1. - .26*pow(length(uv - .5)*1.2, 2.8);
  col += (h2(gl_FragCoord.xy + fract(T)*61.) - .5)*.018;
  gl_FragColor = vec4(col, 1.);
}`;
  const c = h => [(h >> 16 & 255)/255, (h >> 8 & 255)/255, (h & 255)/255];
  const BIO = {
    campo:  {SKT:0x2f7fd6, SKB:0xbfe6f5, SUN:0xffe2a0, FOG:0xcfe6ee, HF:0x5f8fb0, HN:0x2f7a3a, GR:0x5fae48, PA:0xd9c08a, SP:[.8, .8],  FX:[0, 0, 0, 0]},
    pantano:{SKT:0x3f8f7a, SKB:0xc9eccf, SUN:0xf3ffc0, FOG:0xbfe0c4, HF:0x3f7a5c, HN:0x1f5234, GR:0x4a8f4a, PA:0xa89a68, SP:[.3, .82], FX:[0, 0, 0, 0]},
    sombra: {SKT:0x140f38, SKB:0x5a3f8a, SUN:0xb8a8ff, FOG:0x4a3c7a, HF:0x30285e, HN:0x191338, GR:0x3a2f6a, PA:0x8a7fb0, SP:[.74, .8], FX:[1, 0, 0, 0]},
    vulcao: {SKT:0x3a1020, SKB:0xff8a4a, SUN:0xff9a40, FOG:0x9a4a38, HF:0x5a2a2a, HN:0x2a1414, GR:0x5a362c, PA:0xa8704a, SP:[.2, .62], FX:[0, 0, 1, 0]},
    neve:   {SKT:0x5fa8e6, SKB:0xe6f3ff, SUN:0xffffff, FOG:0xe4f0fa, HF:0x8fb0d0, HN:0x4f7a9a, GR:0xf0f6fc, PA:0xc4d4e4, SP:[.25, .78], FX:[0, 0, 0, 1]},
    dourado:{SKT:0xf08a3a, SKB:0xffe6a8, SUN:0xfff0b0, FOG:0xffdca0, HF:0xc98a4a, HN:0x8a5a24, GR:0xdcae44, PA:0xf3e2b0, SP:[.7, .6],  FX:[0, 0, 0, 0]},
    arcano: {SKT:0x0c0f40, SKB:0x3a3f9a, SUN:0xa8b8ff, FOG:0x3c44a0, HF:0x2a3080, HN:0x141a50, GR:0x34409a, PA:0xa9b8ff, SP:[.5, .84], FX:[1, 1, 0, 0]}
  };
  let gl = null, prog = null, prog2 = null, U = {}, U2 = {}, cv = null, ok = false, t0 = performance.now(); const TEX = {};
  function init(canvas){
    try {
      cv = canvas; gl = canvas.getContext('webgl', {antialias:false, alpha:false, powerPreference:'high-performance'}); if (!gl) return false;
      const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
      const mk = fs => { const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, 'attribute vec2 a; void main(){ gl_Position = vec4(a, 0., 1.); }')); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.bindAttribLocation(pr, 0, 'a'); gl.linkProgram(pr); if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr)); return pr; };
      prog = mk(FS); prog2 = mk(FS2);
      for (const n of ['R', 'T', 'LANE', 'NIGHT', 'TX', 'RC', 'SUN', 'SP']) U2[n] = gl.getUniformLocation(prog2, n);
      const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
      for (const n of ['R', 'T', 'LANE', 'SKT', 'SKB', 'SUN', 'FOG', 'HF', 'HN', 'GR', 'PA', 'SP', 'FX']) U[n] = gl.getUniformLocation(prog, n);
      ok = true;
    } catch (e){ console.error('GTSKY', e); ok = false; }
    return ok;
  }
  function texOf(key, im){
    if (TEX[key]) return TEX[key];
    const tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, im); return TEX[key] = tx;
  }
  // im = pintura da ilha (quando já carregou); rc = [x0, y0, w, h] da pintura em fração da tela, y a partir de cima
  function draw(key, lane, w, h, dpr, im, rc){
    if (!ok) return false;
    if (im){
      const s2 = Math.min(dpr || 1, 2)*.85, W2 = Math.max(2, Math.round(w*s2)), H2 = Math.max(2, Math.round(h*s2));
      if (cv.width !== W2 || cv.height !== H2){ cv.width = W2; cv.height = H2; }
      const b2 = BIO[key] || BIO.campo; gl.viewport(0, 0, W2, H2); gl.useProgram(prog2);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texOf(key, im)); gl.uniform1i(U2.TX, 0);
      gl.uniform2f(U2.R, W2, H2); gl.uniform1f(U2.T, (performance.now() - t0)/1000); gl.uniform1f(U2.LANE, lane); gl.uniform1f(U2.NIGHT, b2.FX[0]);
      gl.uniform4fv(U2.RC, rc); gl.uniform3fv(U2.SUN, c(b2.SUN)); gl.uniform2fv(U2.SP, b2.SP);
      gl.drawArrays(gl.TRIANGLES, 0, 3); return true;
    }
    gl.useProgram(prog);
    const s = Math.min(dpr || 1, 2)*.62, W = Math.max(2, Math.round(w*s)), H = Math.max(2, Math.round(h*s));
    if (cv.width !== W || cv.height !== H){ cv.width = W; cv.height = H; }
    const b = BIO[key] || BIO.campo; gl.viewport(0, 0, W, H);
    gl.uniform2f(U.R, W, H); gl.uniform1f(U.T, (performance.now() - t0)/1000); gl.uniform1f(U.LANE, lane);
    for (const n of ['SKT', 'SKB', 'SUN', 'FOG', 'HF', 'HN', 'GR', 'PA']) gl.uniform3fv(U[n], c(b[n]));
    gl.uniform2fv(U.SP, b.SP); gl.uniform4fv(U.FX, b.FX);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    return true;
  }
  return {init, draw, get ok(){ return ok; }};
})();
