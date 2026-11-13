from gt import game, sheet
names = []; fails = []
def check(c, m):
    print(('  ok   ' if c else '  FALHA ') + m)
    if not c: fails.append(m)
MK = "(st) => ({seen:true,n:4,ok:st>=2?4:0,err:0,hd:st>=3?[1,2]:st>=2?[1]:[],fd:st>=4?[1,2,3]:[],lastOk:true,times:[1200],errT:[],domDay:st>=4?3:null,leg:st>=5,due:99999,dueB:0})"
with game(dsf=1) as pg:
    ev = pg.evaluate
    ev(f"""() => {{ const mk = {MK}; const S = __GT.S; for (let b = 1; b <= 10; b++) S.facts[Math.min(2,b)+'x'+Math.max(2,b)] = mk(4);
      S.facts['3x7'] = mk(3); S.facts['3x8'] = mk(2); S.facts['3x9'] = mk(1); S.facts['3x3'] = mk(5); S.facts['3x4'] = mk(4); S.albNew = ['3x4']; __GT.save(); }}""")
    check(ev("() => __GT.isGolden('arqueira')") is True and ev("() => __GT.isGolden('maga')") is False, 'Pluma (tabuada do 2 dominada) ganha a Evolução Dourada; Faísca não')
    ev("() => { __GT.show('book'); }"); pg.wait_for_timeout(300)
    check(ev("() => document.querySelectorAll('#albPage .stk-card').length") == 10, 'página do álbum com 10 figurinhas')
    pg.click('#albTabs button[data-n="3"]'); pg.wait_for_timeout(300); pg.screenshot(path='tmp/a1.png'); names.append('tmp/a1.png')
    check(ev("() => document.querySelectorAll('#albPage .k4, #albPage .k5').length") == 3, 'página do 3 mostra 3 douradas (3×2, 3×3 lendária, 3×4)')
    check(ev("() => (__GT.S.albNew || []).length") == 0, 'figurinha nova deixa de ser nova depois de vista')
    pg.click('#albTabs button[data-n="2"]'); pg.wait_for_timeout(300); pg.screenshot(path='tmp/a2.png'); names.append('tmp/a2.png')
    ev("() => __GT.show('deck')"); pg.wait_for_timeout(300); pg.screenshot(path='tmp/a3.png'); names.append('tmp/a3.png')
    check(ev("() => document.querySelectorAll('#deckGrid .card.gold').length") == 1, 'carta dourada no baralho')
    # batalha: força dourada, duas faces, tempestade
    r = ev("() => { __GT.startBattle(0); const B = __GT.B; B.intro = 0; const a = __GT.spawnHero(0, 'arqueira', {lvl:1}), b = __GT.spawnHero(1, 'arqueira', {lvl:1}); return [a.maxhp/b.maxhp, a.gold, b.gold]; }")
    check(abs(r[0] - 1.08) < .001 and r[1] and not r[2], f'herói dourado luta 8% mais forte (só o da criança) {r}')
    r = ev("""() => { const B = __GT.B; B.mana[0] = 10; __GT.openQuiz(0, 0, 0); const q1 = B.quiz, k = q1.key, f1 = q1.a + 'x' + q1.b; __GT.checkAnswer(q1.ans); __GT.closeQuiz && 0;
      B.quiz = null; document.getElementById('quiz').hidden = true; B.mana[0] = 10; B.rn.vq.push({key:k, due:0}); __GT.openQuiz(0, 0, 0); const q2 = B.quiz, f2 = q2.a + 'x' + q2.b, m0 = B.mana[0]; __GT.checkAnswer(q2.ans);
      return {k, f1, f2, same:q2.key === k, faced:!!B.faced[k], sq:q1.a === q1.b}; }""")
    check(r['same'] and (r['sq'] or (r['f1'] != r['f2'] and r['faced'])), f'a mesma runa volta virada e vale Runa de duas faces {r}')
    ev("() => { const B = __GT.B; B.quiz = null; document.getElementById('quiz').hidden = true; B.tsTarget = 1; B.ink = 1; __GT.deploy(1, 'tanque'); for (let i = 0; i < 30; i++) __GT.battleTick(1/30); }")
    pg.wait_for_timeout(200)
    check(ev("() => !document.getElementById('stormBtn').hidden && document.getElementById('stormBtn').classList.contains('full')"), 'barra cheia mostra o botão da Tempestade')
    pg.screenshot(path='tmp/a4.png'); names.append('tmp/a4.png')
    ev("() => __GT.startStorm()"); pg.wait_for_timeout(150)
    check(ev("() => !!__GT.B.storm && __GT.B.ink === 0"), 'Tempestade começa e zera a barra')
    ev("() => { for (let i = 0; i < 4; i++) __GT.stormAnswer(__GT.B.storm.q.ans); }"); pg.wait_for_timeout(300)
    pg.screenshot(path='tmp/a5.png'); names.append('tmp/a5.png')
    r = ev("() => ({n:__GT.B.storm.n, stars:__GT.B.projs.filter(p => p.kind === 'star').length})")
    check(r['n'] == 4 and r['stars'] >= 1, f'cada acerto lança um raio {r}')
    hp0 = ev("() => __GT.B.towers[0].hp")
    ev("() => __GT.stormAnswer(-1)")
    check(ev("() => __GT.B.storm === null && __GT.B.towers[0].hp") == hp0, 'errar só encerra a Tempestade, sem punição')
    ev("() => { for (let i = 0; i < 60; i++) __GT.battleTick(1/30); }")
    check(not pg.errs, f'sem erros {pg.errs[:2]}')
sheet(names, 'tmp/e4.jpg', 2)
print('FALHAS:', fails or 'nenhuma')
