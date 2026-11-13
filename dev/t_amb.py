import sys
from gt import game
from PIL import Image
bios = sys.argv[1:] or ['0']
names = []
with game(dsf=2) as pg:
    ev = pg.evaluate
    for si in bios:
        ev(f"() => {{ __GT.S.arena = 6; __GT.startBattle({si}); const B = __GT.B; B.intro = 0; __GT.deploy(0, 'arqueira', 0, 0, {{}}); __GT.deploy(0, 'tanque', 0, 0, {{}}); __GT.deploy(1, 'maga', 0, 0, {{}}); }}")
        pg.wait_for_timeout(9000)
        ev("() => { __GT.B.paused = true; }"); pg.wait_for_timeout(150)
        pg.screenshot(path=f'tmp/amb_{si}.png'); names.append(f'tmp/amb_{si}.png')
        ev("() => { __GT.B.over = true; __GT.show('home'); }"); pg.wait_for_timeout(200)
    print('erros', pg.errs[:3])
ims = [Image.open(n).convert('RGB').resize((844, 390)) for n in names]
c = Image.new('RGB', (844, 390*len(ims))); [c.paste(im, (0, i*390)) for i, im in enumerate(ims)]; c.save('tmp/amb_sheet.jpg', quality=84)
