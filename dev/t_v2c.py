import subprocess, sys, time, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8797', '--directory', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(.8)
BOT = """(args) => { const [si, boss, skill] = args; const S = __GT.S; S.settings.sound = false; S.settings.speak = false;
  __GT.startBattle(si, boss); const B = __GT.B; B.intro = 0; let next = 1, log = {guards:[], t:0};
  const gd = () => [B.guards[0][0].alive, B.guards[0][1].alive, B.guards[1][0].alive, B.guards[1][1].alive].map(Number).join('');
  let last = gd();
  for (let i = 0; i < 30*260 && !B.over; i++){
    __GT.battleTick(1/30); next -= 1/30;
    if (next <= 0){ next = skill; const opts = B.hand.filter(id => __GT.CARDS[id].cost <= B.mana[0]); if (opts.length){ const id = opts[Math.floor(Math.random()*opts.length)]; B.mana[0] -= __GT.CARDS[id].cost; __GT.deploy(0, id, 0, 0, {lane:__GT.autoLane(0), pos:260 + Math.random()*200}); } }
    const g = gd(); if (g !== last){ log.guards.push([Math.round(150 - B.t), g]); last = g; }
    if (i % 300 === 0) __GT.renderArena();
  }
  log.over = B.over; log.result = B.result; log.left = Math.round(B.t); log.hp = [__GT.sideHp(0).toFixed(2), __GT.sideHp(1).toFixed(2)]; log.kills = B.kills; log.ot = B.overtime;
  return log; }"""
try:
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = br.new_context(viewport={'width':390,'height':844}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8797/v2/index.html?direto'); pg.wait_for_timeout(1500)
        for si, boss, skill in [(0, False, 3.2), (0, False, 5.0), (0, False, 2.4), (0, True, 3.0)]:
            r = pg.evaluate(BOT, [si, boss, skill]); print(si, boss, skill, json.dumps(r))
        # tempestade e escudo na arena nova
        r = pg.evaluate("""() => { __GT.startBattle(0, true); const B = __GT.B; B.intro = 0; __GT.spawnBoss(); const u = B.bossU; u.spawnT = 0; u.bsT = .05; for (let i = 0; i < 6; i++) __GT.battleTick(1/30);
          __GT.openShieldQuiz(); __GT.checkAnswer(B.quiz.ans); B.ink = 1; __GT.startStorm(); for (let i = 0; i < 4; i++) __GT.stormAnswer(B.storm.q.ans); for (let i = 0; i < 40; i++) __GT.battleTick(1/30); __GT.renderArena();
          return {sh:u.bshield, vuln:u.vuln > 0, lane:__GT.laneOf(u.x), hp:u.hp/u.maxhp}; }""")
        print('chefão/tempestade:', r)
        print('erros:', errs[:4])
        br.close()
finally:
    srv.terminate()
