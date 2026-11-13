import subprocess, sys, time
from playwright.sync_api import sync_playwright
bios = sys.argv[1:] or ['campo']
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8796', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(.8)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']); ctx = br.new_context(viewport={'width':390,'height':844}, device_scale_factor=2); pg = ctx.new_page()
        pg.on('pageerror', lambda e: print('ERR', e)); pg.on('console', lambda m: print('LOG', m.text) if m.type in ('error', 'warning') else None)
        for b in bios:
            pg.goto(f'http://localhost:8796/v2/_t3d.html?b={b}'); pg.wait_for_function('window.DONE', timeout=20000); pg.wait_for_timeout(500)
            print(b, 'sprites', pg.evaluate('KEYS.slice(0,8)'))
            pg.screenshot(path=f'tmp/3d_{b}.png')
        br.close()
finally:
    srv.terminate()
