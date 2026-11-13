"""Repinta todos os sprites (heróis, chefões, castelos) para combinar com os cenários em aquarela:
traço preto vira traço colorido escuro, sombreado mais macio, lavado de aquarela, borda com pigmento acumulado."""
import json, base64, io, sys, numpy as np
from PIL import Image, ImageFilter
rs = np.random.RandomState(7)
LOW = np.array(Image.fromarray((rs.rand(40, 40)*255).astype(np.uint8)).resize((1024, 1024), Image.BICUBIC)).astype(np.float32)/255
GRAIN = rs.rand(1024, 1024).astype(np.float32)
def paint(im):
    im = im.convert('RGBA'); w, h = im.size
    a = np.asarray(im).astype(np.float32); rgb = a[..., :3]; al = a[..., 3]/255
    # fundo neutro sob o alfa para os filtros não puxarem preto das bordas
    base = Image.fromarray(np.where(al[..., None] > .05, rgb, 128).astype(np.uint8))
    k = 9 if max(w, h) > 150 else 7
    med = np.asarray(base.filter(ImageFilter.MedianFilter(k))).astype(np.float32)
    luma = rgb @ np.array([.299, .587, .114], np.float32)
    mluma = med @ np.array([.299, .587, .114], np.float32)
    dark = np.clip((105 - luma)/60, 0, 1)*np.clip((mluma - luma + 10)/45, 0, 1)      # só o traço: escuro e mais escuro que a vizinhança
    line = med*.38 + np.array([34, 20, 26], np.float32)                               # traço colorido, como nos filmes pintados à mão
    out = rgb*(1 - dark[..., None]) + line*dark[..., None]
    soft = np.asarray(Image.fromarray(out.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))).astype(np.float32)
    out = out*.68 + soft*.32
    g = out.mean(-1, keepdims=True); out = g + (out - g)*.9                            # um pouco menos saturado
    wash = (.93 + .12*LOW[:h, :w])[..., None]*(.975 + .05*GRAIN[:h, :w])[..., None]   # lavado e grão do papel
    out = out*wash*np.array([1.025, 1.0, .965], np.float32) + np.array([6, 4, 0], np.float32)
    aim = Image.fromarray((al*255).astype(np.uint8))
    inner = np.asarray(aim.filter(ImageFilter.GaussianBlur(2.2))).astype(np.float32)/255
    pool = np.clip((al - inner)*2.2, 0, 1)                                            # pigmento acumulado na borda
    out = out*(1 - .22*pool[..., None])
    al2 = np.asarray(aim.filter(ImageFilter.GaussianBlur(.6))).astype(np.float32)
    return Image.fromarray(np.dstack([out.clip(0, 255), al2]).astype(np.uint8), 'RGBA')
def dec(src): return Image.open(io.BytesIO(base64.b64decode(src.split(',', 1)[1])))
def enc(im):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=90, method=6); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
if __name__ == '__main__':
    t = open('site/data/sprites_v1.js', encoding='utf-8').read(); i = t.index('{'); data = json.loads(t[i:].rstrip().rstrip(';'))
    if len(sys.argv) > 1:                                                              # amostra: antes e depois
        keys = sys.argv[1:]; tiles = []
        for k in keys:
            o = dec(data[k][0]['src']).convert('RGBA'); n = paint(o); tiles.append((o, n))
        H = 260; W = sum(int(o.width*H/o.height)*2 + 16 for o, _ in tiles)
        sheet = Image.new('RGB', (W, H), (150, 190, 120)); x = 0
        for o, n in tiles:
            for im in (o, n): s = im.resize((int(im.width*H/im.height), H), Image.LANCZOS); sheet.paste(s, (x, 0), s); x += s.width + 8
        sheet.save('tmp/repaint.jpg', quality=85); print('amostra', sheet.size)
    else:
        for k, frames in data.items():
            for f in frames: f['src'] = enc(paint(dec(f['src'])))
        open('site/data/sprites.js', 'w', encoding='utf-8').write('window.GT_SPRITES = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
        print('ok', len(data), 'grupos')
