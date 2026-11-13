from patchlib import G
g = G()
g.rep(".shieldbtn{position:absolute;left:50%;top:calc(var(--hud)*5.6);", ".shieldbtn{position:absolute;left:50%;top:52%;")
g.rep("  let pool = FACTS.filter(f => seen(f) && (!fo.length || fo.includes(f.a) || fo.includes(f.b)));\n  if (!pool.length) pool = FACTS.filter(seen);", "  const hard = f => f.a > 1 && f.b > 1 && f.a < 10 && f.b < 10;\n  let pool = FACTS.filter(f => seen(f) && hard(f) && (!fo.length || fo.includes(f.a) || fo.includes(f.b)));\n  if (!pool.length) pool = FACTS.filter(f => seen(f) && hard(f));\n  if (!pool.length) pool = FACTS.filter(seen);")
g.rep("""  $('modal').innerHTML = `<div class="sheet" role="dialog" aria-label="Área do pai"><h3>Área do pai</h3>
    <p class="desc">Para entrar""", """  $('modal').innerHTML = `<div class="sheet wide" role="dialog" aria-label="Área do pai" style="max-width:420px"><div class="pai"><h3>Área do pai</h3>
    <p class="desc">Para entrar""")
g.rep("""    <div class="acts"><button class="btn-gold" id="paiOk" type="button" style="font-size:17px">Entrar</button></div>
    <button class="xbtn\"""", """    <div class="acts"><button class="btn-gold" id="paiOk" type="button" style="font-size:17px">Entrar</button></div></div>
    <button class="xbtn\"""")
g.rep("  $('closeModal').onclick = closeModal;\n}\n$('paiBtn').onclick", "  $('modal').hidden = false; $('closeModal').onclick = closeModal;\n}\n$('paiBtn').onclick")
g.save()
