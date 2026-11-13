import subprocess, time, json, os, sys
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8791', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1); fails = []
def check(c, m):
    print(('  ok   ' if c else '  FALHA ') + m)
    if not c: fails.append(m)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 844, 'height': 390}, accept_downloads=True); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8791/index.html'); pg.wait_for_timeout(2500)
        ev = pg.evaluate
        check(ev("() => document.title") == 'Guardiões da Tabuada', 'título certo')
        check(ev("() => navigator.serviceWorker.getRegistration().then(r => !!r && !!r.active)"), 'funciona offline (service worker ativo)')
        check(ev("() => document.querySelectorAll('#stages .stage').length") == 7, 'jogo carregou com 7 arenas')
        # progresso persiste ao recarregar
        ev("() => { const S = __GT.S; S.settings.sound = false; S.coins = 777; S.trophies = 150; S.cards.arqueira.lvl = 3; __GT.save(); }")
        pg.reload(); pg.wait_for_timeout(1500)
        r = ev("() => ({c:__GT.S.coins, t:__GT.S.trophies, l:__GT.S.cards.arqueira.lvl})")
        check(r == {'c': 777, 't': 150, 'l': 3}, f'progresso continua depois de fechar e abrir {r}')
        # cópia de segurança: guardar
        ev("() => __GT.show('settings')"); pg.wait_for_timeout(300)
        with pg.expect_download() as d: pg.click('#bkOut')
        path = d.value.path(); data = json.load(open(path, encoding='utf-8'))
        check(data['save']['coins'] == 777 and data['game'] == 'guardioes-da-tabuada', 'Guardar cópia gera o arquivo com o progresso')
        os.makedirs('tmp', exist_ok=True); open('tmp/copia.json', 'w', encoding='utf-8').write(json.dumps(data))
        # apagar tudo e trazer de volta
        ev("() => { localStorage.clear(); }"); pg.reload(); pg.wait_for_timeout(1200)
        check(ev("() => __GT.S.coins") == 60, 'depois de apagar, começa do zero')
        ev("() => { __GT.S.settings.sound = false; __GT.show('settings'); }")
        pg.set_input_files('#bkFile', 'tmp/copia.json'); pg.wait_for_timeout(500)
        r = ev("() => ({c:__GT.S.coins, t:__GT.S.trophies, l:__GT.S.cards.arqueira.lvl, m:document.getElementById('bkMsg').textContent})")
        check(r['c'] == 777 and r['t'] == 150 and r['l'] == 3 and 'volta' in r['m'], f'Trazer cópia restaura o progresso {r}')
        pg.reload(); pg.wait_for_timeout(1000)
        check(ev("() => __GT.S.coins") == 777, 'progresso restaurado continua salvo')
        open('tmp/ruim.json', 'w').write('{"x":1}')
        ev("() => __GT.show('settings')"); pg.set_input_files('#bkFile', 'tmp/ruim.json'); pg.wait_for_timeout(300)
        check('Não consegui' in ev("() => document.getElementById('bkMsg').textContent") and ev("() => __GT.S.coins") == 777, 'arquivo errado é recusado sem estragar o progresso')
        pg.screenshot(path='tmp/settings.png')
        # uma batalha roda
        ev("() => { __GT.show('home'); __GT.startBattle(0); const B = __GT.B; B.intro = 0; for (let i = 0; i < 200; i++) __GT.battleTick(.05); }")
        check(ev("() => !!__GT.B && __GT.B.t < 150"), 'batalha roda')
        check(not errs, f'sem erros de página {errs[:2]}')
        br.close()
finally:
    srv.terminate()
print('FALHAS:', fails or 'nenhuma')
