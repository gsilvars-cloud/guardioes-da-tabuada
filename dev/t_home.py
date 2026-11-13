from gt import game, sheet
names = []
with game(dsf=1) as pg:
    ev = pg.evaluate
    ev("() => { const S = __GT.S; S.arena = 3; S.sel = 3; S.trophies = 1100; S.best = {0:3, 1:2, 2:1}; for (const id of ['bruma','fuinha','brasa']) S.cards[id] = {lvl:2, n:1}; S.deck = ['arqueira','maga','tanque','brasa']; for (const k of ['1x2','2x2','2x5','5x5','2x10','1x5','3x4','3x3','2x3']) __GT.S.facts[k] = {seen:true,n:3,ok:3,err:0,hd:[1,2,3],fd:[1,2,3],lastOk:true,times:[1000],errT:[],domDay:3,leg:false,due:99999,dueB:0}; __GT.save(); __GT.show('home'); }")
    pg.wait_for_timeout(600); pg.screenshot(path='tmp/h1.png'); names.append('tmp/h1.png')
    ev("() => document.getElementById('home').scrollTo(0, 330)"); pg.wait_for_timeout(300); pg.screenshot(path='tmp/h2.png'); names.append('tmp/h2.png')
    ev("() => document.getElementById('home').scrollTo(0, 700)"); pg.wait_for_timeout(300); pg.screenshot(path='tmp/h3.png'); names.append('tmp/h3.png')
    ev("() => { __GT.S.trophies = 1400; __GT.show('home'); document.getElementById('home').scrollTo(0,0); }"); pg.wait_for_timeout(300); pg.screenshot(path='tmp/h4.png'); names.append('tmp/h4.png')
    print(pg.errs)
sheet(names, 'tmp/home.jpg', 2)
