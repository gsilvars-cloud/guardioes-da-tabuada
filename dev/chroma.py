import numpy as np
from PIL import Image, ImageFilter
def key(im):
    a = np.array(im.convert('RGB')).astype(np.float32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # "magentice": quanto o pixel puxa para o magenta do fundo
    m = np.minimum(r, b) - g
    alpha = np.clip((95 - m)/45, 0, 1)                 # m >= 95 fundo, m <= 50 personagem
    alpha[(b < 95)] = 1                                # vermelhos e amarelos ficam
    out = np.dstack([r, np.maximum(g, np.minimum(g, 255)), b, alpha*255])
    # tira o rosa das bordas
    edge = (alpha > 0) & (alpha < 1)
    lim = np.maximum(g, 0) + 40
    out[..., 0] = np.where(edge, np.minimum(r, lim + 60), r); out[..., 2] = np.where(edge, np.minimum(b, lim), b)
    return Image.fromarray(out.astype(np.uint8), 'RGBA')
def split_cols(im, n, pad=6):
    a = np.array(im)[..., 3] > 40; cols = a.sum(0) > 2
    runs = []; s = None
    for x, v in enumerate(cols):
        if v and s is None: s = x
        if not v and s is not None: runs.append((s, x)); s = None
    if s is not None: runs.append((s, len(cols)))
    runs = sorted(sorted(runs, key=lambda r: r[0] - r[1])[:n])
    out = []
    for x0, x1 in runs:
        sub = im.crop((max(0, x0 - pad), 0, min(im.width, x1 + pad), im.height)); bb = sub.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
        out.append(sub.crop((bb[0], max(0, bb[1] - pad), bb[2], min(sub.height, bb[3] + pad))))
    return out
