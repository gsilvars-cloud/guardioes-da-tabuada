from gt import game, sheet
names = []
with game(dsf=2) as pg:
    ev = pg.evaluate
    def tick(s, dt=1/30):
        ev(f"() => {{ for (let i = 0; i < {int(s/dt)}; i++) __GT.battleTick({dt}); }}")
    def shot(n):
        pg.wait_for_timeout(250); f = f'tmp/e1_{n}.png'; pg.screenshot(path=f); names.append(f)
    ev("() => { __GT.S.settings.sound = true; }")
    pg.mouse.click(400, 200)
    ev("() => { __GT.startBattle(0); const B = __GT.B; B.intro = 0; __GT.deploy(0, 'tanque'); __GT.deploy(0, 'arqueira'); __GT.deploy(1, 'maga'); }")
    tick(.4); shot('spawn')
    tick(9); ev("() => { __GT.deploy(0, 'maga'); __GT.deploy(1, 'tanque'); }"); tick(4); shot('luta')
    print('musica', ev("() => ({key:__GT.mus.key, playing: !!__GT.mus.el && !__GT.mus.el.paused, splats:__GT.B.splats.length, says:__GT.B.says.length})"))
    ev("() => { const B = __GT.B; B.towers[1].hp = 1; __GT.dealDamage(B.towers[1], 9, 0); }"); 
    for i in range(22): ev("() => __GT.battleTick(1/30)"); 
    shot('queda')
    print(pg.errs)
sheet(names, 'tmp/e1.jpg', 1)
