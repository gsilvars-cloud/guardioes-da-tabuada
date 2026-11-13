import subprocess, sys, time, contextlib
from playwright.sync_api import sync_playwright
@contextlib.contextmanager
def game(w=844, h=390, port=8793, dsf=1):
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(.8)
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(); ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dsf, accept_downloads=True); pg = ctx.new_page(); pg.errs = []
            pg.on('pageerror', lambda e: pg.errs.append(str(e)))
            pg.goto(f'http://localhost:{port}/index.html'); pg.wait_for_timeout(1500)
            pg.evaluate("() => { if (window.__GT) __GT.S.settings.sound = false; }")
            yield pg
            br.close()
    finally:
        srv.terminate()
def sheet(names, out, cols=2):
    from PIL import Image
    ims = [Image.open(n).convert('RGB') for n in names]; w, h = ims[0].size
    c = Image.new('RGB', (w*cols, h*((len(ims) + cols - 1)//cols)))
    for i, im in enumerate(ims): c.paste(im.resize((w, h)), ((i % cols)*w, (i//cols)*h))
    c.save(out, quality=82)
