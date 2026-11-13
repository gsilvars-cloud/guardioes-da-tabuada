from gt import game
fails = []
def check(c, m):
    print(('  ok   ' if c else '  FALHA ') + m)
    if not c: fails.append(m)
with game(dsf=1) as pg:
    ev = pg.evaluate
    ev("() => { __GT.S.coins = 777; __GT.S.trophies = 150; __GT.save(); }"); pg.reload(); pg.wait_for_timeout(1200)
    check(ev("() => JSON.parse(localStorage.getItem(__GT.BAK_KEY)).coins") == 777, 'reserva guarda o save bom no começo da sessão')
    ev("() => localStorage.setItem(__GT.SAVE_KEY, '{estragado')"); pg.reload(); pg.wait_for_timeout(1200)
    check(ev("() => __GT.S.coins") == 777, 'save estragado: o jogo volta pela reserva')
    ev("() => { __GT.save(); localStorage.removeItem(__GT.SAVE_KEY); }"); pg.reload(); pg.wait_for_timeout(1200)
    check(ev("() => __GT.S.coins") == 777, 'save sumido: o jogo volta pela reserva')
    ev("() => { __GT.S.settings.sound = false; __GT.startBattle(0); __GT.B.intro = 0; }")
    r = ev("() => { const B = __GT.B; for (let i = 0; i < 6; i++){ B.flash = 0; __GT.flash(.5); } return [__GT.flashLog.length, B.flash]; }")
    check(r[0] == 3 and r[1] == 0, f'no máximo 3 clarões por segundo {r}')
    r = ev("() => { const B = __GT.B; __GT.flashLog.length = 0; B.flash = 0; __GT.S.settings.soft = true; __GT.flash(.5); const a = B.flash; __GT.S.settings.soft = false; return a; }")
    check(abs(r - .15) < 1e-9, f'modo suave enfraquece o clarão {r}')
    ev("() => { __GT.duck(true); __GT.duck(false); __GT.B.shake = 1; __GT.hitStop(.09); for (let i = 0; i < 40; i++) __GT.battleTick(1/30); }"); pg.wait_for_timeout(300)
    ev("() => { __GT.B.over = true; __GT.show('settings'); }"); pg.wait_for_timeout(200)
    pg.click('#softSeg button[data-s="1"]'); pg.wait_for_timeout(100)
    check(ev("() => __GT.S.settings.soft === true && document.querySelector('#softSeg button[data-s=\"1\"]').classList.contains('on')"), 'ajuste Efeitos de tela: Suave')
    pg.click('#softSeg button[data-s="0"]')
    check(not pg.errs, f'sem erros {pg.errs[:2]}')
print('FALHAS:', fails or 'nenhuma')
