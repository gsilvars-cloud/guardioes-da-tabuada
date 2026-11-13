import patchlib
patchlib.P = 'site/v2/index.html'
g = patchlib.G()
g.rep("#gl,#arena{position:absolute;inset:0;width:100%;height:100%;display:block}", "#gl,#arena{position:absolute;inset:0;left:0;top:0;width:100%;height:100%;display:block;transform:none;border-radius:0;box-shadow:none}")
g.rep("if (p.pos < lo - 90 || p.pos > hi + 110 || Math.abs(p.wx) > 300) return null;", "if (p.pos < -70 || p.pos > hi + 110 || Math.abs(p.wx) > 330) return null;")
g.save()
