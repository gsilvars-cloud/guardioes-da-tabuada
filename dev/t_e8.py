import subprocess, sys, time
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8795', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(); ctx = br.new_context(viewport={'width':844,'height':390}, has_touch=True, is_mobile=True, device_scale_factor=2); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8795/index.html?direto'); pg.wait_for_timeout(1500)
        ev = pg.evaluate
        print('touch-action html:', ev("() => getComputedStyle(document.documentElement).touchAction"))
        # dois toques rápidos no mesmo ponto e toques rápidos em botões diferentes
        pg.touchscreen.tap(300, 200); pg.touchscreen.tap(300, 200); pg.wait_for_timeout(400)
        print('escala após dois toques:', ev("() => visualViewport.scale"))
        y0 = ev("() => document.querySelector('#home').scrollTop")
        ev("() => document.querySelector('#home').scrollBy(0, 300)"); print('rolagem da tela inicial:', y0, '->', ev("() => document.querySelector('#home').scrollTop"))
        ev("() => document.querySelector('#home').scrollTo(0, 0)")
        # toques rápidos em sequência continuam valendo (afiar runas)
        ev("() => { __GT.S.settings.sound = false; for (const f of __GT.FACTS.slice(0, 30)) __GT.recordAnswer(f.key, true, 1500, {}); __GT.startAfiar(false); }"); pg.wait_for_timeout(300)
        for i in range(4):
            a = str(ev("() => __GT.AF.q.ans"))
            for ch in a:
                b = pg.locator(f'#afPad button[data-k="{ch}"]').bounding_box(); pg.touchscreen.tap(b['x'] + b['width']/2, b['y'] + b['height']/2)
            pg.wait_for_timeout(200)
        print('toques rápidos no teclado: acertos =', ev("() => __GT.AF.n"), '(esperado 4)')
        print('erros:', errs[:2])
        br.close()
finally:
    srv.terminate()
