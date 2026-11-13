import subprocess, sys, time
from playwright.sync_api import sync_playwright
shots = []
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8797', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = br.new_context(viewport={'width':390,'height':844}, device_scale_factor=1, has_touch=True, is_mobile=True); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8797/v2/index.html?direto'); pg.wait_for_timeout(1800)
        ev = pg.evaluate
        def shot(n): pg.screenshot(path=f'tmp/w_{n}.png'); shots.append(f'tmp/w_{n}.png')
        ev("() => { __GT.S.settings.sound = false; for (const f of __GT.FACTS.slice(0, 30)) __GT.recordAnswer(f.key, true, 1500, {}); __GT.save(); __GT.show('home'); }"); pg.wait_for_timeout(400); shot('home')
        ev("() => __GT.show('deck')"); pg.wait_for_timeout(300); shot('deck')
        ev("() => __GT.show('book')"); pg.wait_for_timeout(300); shot('book')
        ev("() => __GT.show('settings')"); pg.wait_for_timeout(300); shot('set')
        ev("() => { __GT.startBattle(0); const B = __GT.B; B.intro = 0; B.mana[0] = 10; __GT.deploy(1, 'tanque', 0, 0, {lane:1, pos:700}); B.sel = 0; }"); pg.wait_for_timeout(700); shot('zone')
        ev("() => { __GT.B.sel = null; __GT.selectSlot2(1, 1, 380); }"); pg.wait_for_timeout(500); shot('quiz')
        ev("() => __GT.checkAnswer(-1)"); pg.wait_for_timeout(400); shot('bad')
        ev("() => { const B = __GT.B; B.quiz = null; document.getElementById('quiz').hidden = true; B.tsTarget = 1; __GT.dealDamage(B.towers[1], 99999, 0); }"); pg.wait_for_timeout(4500); shot('end')
        print('erros:', errs[:3])
        br.close()
finally:
    srv.terminate()
from PIL import Image
ims = [Image.open(s).convert('RGB').resize((273, 591)) for s in shots]; c = Image.new('RGB', (273*4, 591*2)); [c.paste(im, ((i % 4)*273, (i//4)*591)) for i, im in enumerate(ims)]; c.save('tmp/w_sheet.jpg', quality=80)
