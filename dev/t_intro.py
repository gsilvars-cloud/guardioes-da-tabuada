from gt import game, sheet
names = []
with game(dsf=1) as pg:
    ev = pg.evaluate
    def shot(n): 
        pg.wait_for_timeout(200); f = f'tmp/in_{n}.png'; pg.screenshot(path=f); names.append(f)
    ev("() => { __GT.S.settings.speak = false; __GT.INTRO.logo(); }"); pg.wait_for_timeout(900); shot('logo')
    pg.wait_for_timeout(2600); shot('titulo')
    pg.mouse.click(400, 200); pg.wait_for_timeout(2500); shot('c1')
    for i, w in [(1, 4300), (2, 4200), (3, 5800), (4, 2600), (5, 1500)]:
        ev(f"() => __GT.INTRO.jump({i})"); pg.wait_for_timeout(w); shot(f'c{i+1}')
    print('fase', ev("() => __GT.INTRO.phase"), 'musica', ev("() => __GT.mus.key"))
    pg.click('#introGo'); pg.wait_for_timeout(450); shot('tinta'); pg.wait_for_timeout(1200)
    print('depois', ev("() => ({fase:__GT.INTRO.phase, seen:__GT.S.introSeen, hidden:document.getElementById('intro').hidden, mus:__GT.mus.key})"), pg.errs)
sheet(names, 'tmp/intro.jpg', 3)
