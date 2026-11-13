import subprocess, sys, time
from playwright.sync_api import sync_playwright
shots = []
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8797', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = br.new_context(viewport={'width':390,'height':844}, device_scale_factor=2, has_touch=True, is_mobile=True); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8797/v2/index.html?direto'); pg.wait_for_timeout(1800)
        ev = pg.evaluate
        ev("() => { __GT.S.settings.sound = false; __GT.startBattle(0); }"); pg.wait_for_timeout(600)
        pg.screenshot(path='tmp/v2_a.png'); shots.append('tmp/v2_a.png')
        ev("() => { const B = __GT.B; B.intro = 0; B.mana[0] = 10; B.mana[1] = 10; for (const [t, id, l, p] of [[0,'tanque',0,420],[0,'arqueira',0,330],[0,'maga',1,480],[1,'tanque',1,700],[1,'arqueira',0,760],[1,'maga',1,820]]) __GT.deploy(t, id, 0, 0, {lane:l, pos:p}); }")
        pg.wait_for_timeout(5000)
        pg.screenshot(path='tmp/v2_b.png'); shots.append('tmp/v2_b.png')
        r = ev("() => ({ents:__GT.B.ents.length, lanes:__GT.B.ents.map(e => __GT.laneOf(e.x)), hp:[__GT.sideHp(0), __GT.sideHp(1)], fps:0})"); print(r)
        # arrastar uma carta até o campo
        c = pg.locator('#hand .card').first.bounding_box(); x0, y0 = c['x'] + c['width']/2, c['y'] + c['height']/2
        cdp = ctx.new_cdp_session(pg)
        def touch(t, x, y): cdp.send('Input.dispatchTouchEvent', {'type':t, 'touchPoints':[] if t == 'touchEnd' else [{'x':x, 'y':y}]})
        touch('touchStart', x0, y0); pg.wait_for_timeout(60)
        for i in range(1, 9): touch('touchMove', x0 + (135 - x0)*i/8, y0 + (430 - y0)*i/8); pg.wait_for_timeout(30)
        pg.wait_for_timeout(150); pg.screenshot(path='tmp/v2_c.png'); shots.append('tmp/v2_c.png')
        touch('touchEnd', 0, 0); pg.wait_for_timeout(400)
        q = ev("() => __GT.B.quiz && ({lane:__GT.B.quiz.lane, pos:Math.round(__GT.B.quiz.pos), id:__GT.B.quiz.id})"); print('quiz após soltar:', q)
        pg.screenshot(path='tmp/v2_d.png'); shots.append('tmp/v2_d.png')
        if q:
            n0 = ev("() => __GT.B.ents.filter(e => e.team === 0).length"); ev("() => __GT.checkAnswer(__GT.B.quiz.ans)"); pg.wait_for_timeout(1600)
            u = ev("() => { const u = __GT.B.ents.filter(e => e.team === 0).pop(); return {n:__GT.B.ents.filter(e => e.team === 0).length, lane:__GT.laneOf(u.x), pos:Math.round(__GT.lpos(u.x))}; }"); print('herói no campo:', n0, '->', u)
        print('erros:', errs[:3])
        br.close()
finally:
    srv.terminate()
from PIL import Image
ims = [Image.open(s).convert('RGB').resize((390, 844)) for s in shots]; c = Image.new('RGB', (390*len(ims), 844)); [c.paste(im, (i*390, 0)) for i, im in enumerate(ims)]; c.save('tmp/v2_sheet.jpg', quality=82)
