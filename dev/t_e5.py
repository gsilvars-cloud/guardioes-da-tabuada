from gt import game, sheet
names = []; fails = []
def check(c, m):
    print(('  ok   ' if c else '  FALHA ') + m)
    if not c: fails.append(m)
with game(dsf=1) as pg:
    ev = pg.evaluate
    ev("""() => { const S = __GT.S; for (const f of __GT.FACTS.slice(0, 20)) __GT.recordSeen ? 0 : 0;
      for (const f of __GT.FACTS.slice(0, 24)){ __GT.recordAnswer(f.key, true, 1500, {}); }
      __GT.recordAnswer('7x8', false, 5000, {}); __GT.recordAnswer('7x8', false, 5000, {}); __GT.recordAnswer('6x7', false, 5000, {});
      S.play = {}; const d = __GT.dayNum(); S.play[d] = 540; S.play[d-1] = 300; S.play[d-3] = 800; S.play[d-9] = 200; S.stats.answered = 60; S.stats.correct = 51; __GT.save(); }""")
    ev("() => { __GT.startBattle(0); const B = __GT.B; B.intro = 0; B.boss = B.boss || true; __GT.spawnBoss(); const u = B.bossU; u.spawnT = 0; u.bsT = .05; for (let i = 0; i < 6; i++) __GT.battleTick(1/30); }")
    pg.wait_for_timeout(250)
    r = ev("() => { const u = __GT.B.bossU; return {sh:u.bshield, btn:!document.getElementById('shieldBtn').hidden, hp:u.hp}; }")
    check(r['sh'] and r['btn'], f'escudo sobe e o botão aparece {r}')
    d1 = ev("() => { const u = __GT.B.bossU, h = u.hp; __GT.dealDamage(u, 100, null); return h - u.hp; }")
    ev("() => { __GT.B.paused = true; }"); pg.wait_for_timeout(120); pg.screenshot(path='tmp/s1.png'); names.append('tmp/s1.png'); ev("() => { __GT.B.paused = false; }")
    ev("() => __GT.openShieldQuiz()"); pg.wait_for_timeout(200)
    check(ev("() => __GT.B.quiz && __GT.B.quiz.type") == 'shield', 'abre a conta do escudo')
    pg.screenshot(path='tmp/s2.png'); names.append('tmp/s2.png')
    ev("() => __GT.checkAnswer(-1)"); pg.wait_for_timeout(150)
    check(ev("() => __GT.B.quiz && __GT.B.quiz.state === 'bad' && __GT.B.bossU.bshield"), 'errar mostra o truque e mantém o escudo')
    ev("() => { __GT.B.quiz = null; document.getElementById('quiz').hidden = true; __GT.B.tsTarget = 1; __GT.openShieldQuiz(); __GT.checkAnswer(__GT.B.quiz.ans); }"); pg.wait_for_timeout(200)
    r = ev("() => { const u = __GT.B.bossU; return {sh:u.bshield, v:u.vuln, st:u.stun, q:!!__GT.B.quiz}; }")
    check(not r['sh'] and r['v'] > 3 and r['st'] > 1 and not r['q'], f'acertar quebra o escudo, atordoa e abre dano em dobro {r}')
    d2 = ev("() => { const u = __GT.B.bossU, h = u.hp; __GT.dealDamage(u, 100, null); return h - u.hp; }")
    check(abs(d2/d1 - 2/.35) < .05, f'dano com escudo {d1:.1f} x dano vulnerável {d2:.1f}')
    ev("() => { __GT.B.paused = true; }"); pg.wait_for_timeout(120); pg.screenshot(path='tmp/s3.png'); names.append('tmp/s3.png'); ev("() => { __GT.B.paused = false; }")
    ev("() => { for (let i = 0; i < 200; i++) __GT.battleTick(1/30); }")
    check(ev("() => __GT.B.bossU.vuln <= 0"), 'vulnerabilidade acaba em 4 s')
    ev("() => { __GT.B.over = true; __GT.show('settings'); }"); pg.wait_for_timeout(200)
    ev("() => __GT.paiReport()"); pg.wait_for_timeout(250); pg.screenshot(path='tmp/s4.png'); names.append('tmp/s4.png')
    check(ev("() => document.querySelectorAll('.pai .teim div').length") >= 2, 'área do pai lista as contas com erro')
    ev("() => __GT.paiGate()"); pg.wait_for_timeout(200); pg.screenshot(path='tmp/s5.png'); names.append('tmp/s5.png')
    check(not pg.errs, f'sem erros {pg.errs[:2]}')
sheet(names, 'tmp/e5.jpg', 2)
print('FALHAS:', fails or 'nenhuma')
