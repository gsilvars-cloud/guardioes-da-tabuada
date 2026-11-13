"""Passa os cenários que ainda não são aquarela (ou saíram com traço forte) pelo mesmo tratamento de pintura."""
import os, shutil, sys, numpy as np
from PIL import Image, ImageFilter
rs = np.random.RandomState(11)
def tex(w, h):
    low = np.array(Image.fromarray((rs.rand(24, 48)*255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32)/255
    return (.94 + .1*low)[..., None]*(.98 + .04*rs.rand(h, w).astype(np.float32))[..., None]
def paint_bg(im, lift=14, k=7):
    im = im.convert('RGB'); w, h = im.size; rgb = np.asarray(im).astype(np.float32)
    med = np.asarray(im.filter(ImageFilter.MedianFilter(k))).astype(np.float32)
    L = np.array([.299, .587, .114], np.float32); luma = rgb @ L; ml = med @ L
    dark = np.clip((110 - luma)/60, 0, 1)*np.clip((ml - luma + 6)/36, 0, 1)
    line = med*.55 + np.array([26, 18, 30], np.float32)
    out = rgb*(1 - dark[..., None]) + line*dark[..., None]
    soft = np.asarray(Image.fromarray(out.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)
    out = out*.6 + soft*.4
    g = out.mean(-1, keepdims=True); out = g + (out - g)*.92
    out = (out*(1 - lift/255) + lift)*tex(w, h)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))
if __name__ == '__main__':
    for key, lift in [('sombra', 10), ('dourado', 14), ('vulcao', 16), ('arcano', 14)]:
        p = f'site/assets/bg/{key}.webp'; b = f'site/assets/bg/{key}_pre.webp'
        if not os.path.exists(b): shutil.copy(p, b)
        paint_bg(Image.open(b), lift).save(p, 'WEBP', quality=88, method=6)
    for p in ['site/assets/cenas/vila.webp', 'site/assets/cenas/mapa.webp']:
        b = p.replace('.webp', '_pre.webp')
        if not os.path.exists(b): shutil.copy(p, b)
        paint_bg(Image.open(b), 10).save(p, 'WEBP', quality=88, method=6)
    print('cenários tratados')
