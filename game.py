from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LAST LIGHT — Dino Run</title>
<style>
  :root {
    color-scheme: dark;
    --ink: #090c12;
    --paper: #f1e9d8;
    --muted: #a69d90;
    --gold: #e7aa62;
    --red: #e57967;
    --line: rgba(241,233,216,.16);
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; min-height: 100%; background: var(--ink); }
  body {
    color: var(--paper);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    overflow: hidden;
  }
  .scene {
    position: relative;
    display: grid;
    place-items: center;
    min-height: 100vh;
    padding: 28px;
    overflow: hidden;
    background:
      radial-gradient(ellipse at 50% 65%, rgba(127, 63, 48, .22), transparent 52%),
      linear-gradient(180deg, #090c12 0%, #17141a 55%, #241a1b 100%);
  }
  .scene::before, .scene::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .scene::before {
    opacity: .22;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.18'/%3E%3C/svg%3E");
    mix-blend-mode: soft-light;
  }
  .scene::after {
    background: linear-gradient(90deg, rgba(3,5,9,.66), transparent 25%, transparent 75%, rgba(3,5,9,.66));
  }
  .frame {
    position: relative;
    z-index: 1;
    width: min(1100px, 100%);
    border: 1px solid var(--line);
    background: rgba(8,10,15,.56);
    box-shadow: 0 30px 100px rgba(0,0,0,.42);
    backdrop-filter: blur(10px);
  }
  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 19px 24px;
    border-bottom: 1px solid var(--line);
    font-size: 10px;
    letter-spacing: .2em;
    text-transform: uppercase;
  }
  .brand { display: flex; align-items: center; gap: 11px; }
  .brand-mark {
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--gold); box-shadow: 0 0 18px var(--gold);
  }
  .top-note { color: var(--muted); }
  .status { color: #a9c5a5; }
  .content { padding: clamp(22px, 5vw, 54px); }
  .eyebrow {
    color: var(--gold); font-size: 10px; letter-spacing: .32em;
    text-transform: uppercase;
  }
  h1 {
    margin: 12px 0 5px;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(46px, 8vw, 88px);
    font-weight: 400;
    letter-spacing: -.055em;
    line-height: .94;
  }
  .subtitle {
    margin: 13px 0 26px; color: var(--muted);
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(15px, 2.4vw, 20px); font-style: italic;
  }
  .game-wrap {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(241,233,216,.2);
    background: linear-gradient(180deg, #111923 0%, #302228 100%);
  }
  canvas { display: block; width: 100%; height: clamp(220px, 38vw, 340px); }
  .game-overlay {
    position: absolute; inset: 0; display: grid; place-items: center;
    text-align: center; background: rgba(8,10,15,.2);
    transition: opacity .25s ease, visibility .25s ease;
  }
  .game-overlay.hidden { opacity: 0; visibility: hidden; pointer-events: none; }
  .overlay-card { padding: 20px; }
  .overlay-title {
    margin: 0 0 8px; font: 400 clamp(25px, 4vw, 38px) Georgia, serif;
  }
  .overlay-copy { color: #c3b7a6; font-size: 12px; letter-spacing: .07em; }
  .play-button {
    margin-top: 20px; padding: 12px 23px;
    border: 1px solid rgba(231,170,98,.7); color: var(--paper);
    background: rgba(231,170,98,.12); cursor: pointer;
    font: inherit; font-size: 10px; letter-spacing: .2em; text-transform: uppercase;
    transition: background .2s, transform .2s;
  }
  .play-button:hover { background: rgba(231,170,98,.25); transform: translateY(-2px); }
  .hud {
    position: absolute; inset: 17px 18px auto;
    display: flex; justify-content: space-between;
    pointer-events: none; color: rgba(241,233,216,.78);
    font-size: 10px; letter-spacing: .16em; text-transform: uppercase;
  }
  .hud strong { color: var(--paper); font-size: 13px; letter-spacing: .08em; }
  .bottom {
    display: flex; align-items: center; justify-content: space-between;
    gap: 18px; padding-top: 20px;
  }
  .controls { display: flex; flex-wrap: wrap; gap: 15px 25px; color: var(--muted); font-size: 11px; }
  .key {
    display: inline-grid; place-items: center; min-width: 25px; height: 23px;
    margin-right: 7px; padding: 0 6px;
    border: 1px solid var(--line); color: var(--paper);
    font-size: 10px; letter-spacing: .08em;
  }
  .record { color: var(--muted); font-size: 10px; letter-spacing: .12em; text-align: right; text-transform: uppercase; }
  .record strong { display: block; margin-top: 5px; color: var(--gold); font-size: 16px; }
  @media (max-width: 560px) {
    .scene { padding: 12px; }
    .topbar { padding: 14px; font-size: 8px; }
    .top-note { display: none; }
    .content { padding: 25px 18px; }
    .bottom { align-items: flex-start; }
    .controls { gap: 12px; }
  }
</style>
</head>
<body>
<main class="scene">
  <section class="frame">
    <header class="topbar">
      <div class="brand"><span class="brand-mark"></span><span>Field Notes · No. 001</span></div>
      <div class="top-note">An endless-world survival study</div>
      <div class="status">● Offline ready</div>
    </header>

    <div class="content">
      <div class="eyebrow">The last horizon</div>
      <h1>LAST LIGHT</h1>
      <p class="subtitle">One more sunrise. One more run.</p>

      <div class="game-wrap">
        <canvas id="game" aria-label="Dinosaur running game"></canvas>
        <div class="hud">
          <div>Distance<br><strong id="score">00000</strong></div>
          <div style="text-align:right">Best run<br><strong id="best">00000</strong></div>
        </div>
        <div class="game-overlay" id="overlay">
          <div class="overlay-card">
            <h2 class="overlay-title" id="overlayTitle">The world is quiet.</h2>
            <div class="overlay-copy" id="overlayCopy">Press start when you are ready.</div>
            <button class="play-button" id="playButton">Begin the run</button>
          </div>
        </div>
      </div>

      <footer class="bottom">
        <div class="controls">
          <span><kbd class="key">SPACE</kbd>Jump</span>
          <span><kbd class="key">↓</kbd>Duck</span>
          <span><kbd class="key">R</kbd>Restart</span>
        </div>
        <div class="record">The distance is yours<strong id="footerBest">00000 m</strong></div>
      </footer>
    </div>
  </section>
</main>

<script>
(() => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const overlay = document.getElementById("overlay");
  const title = document.getElementById("overlayTitle");
  const copy = document.getElementById("overlayCopy");
  const button = document.getElementById("playButton");
  const scoreNode = document.getElementById("score");
  const bestNode = document.getElementById("best");
  const footerBest = document.getElementById("footerBest");

  let w = 0, h = 0, ground = 0, last = 0, raf = 0;
  let running = false, gameOver = false, score = 0, speed = 6;
  let obstacles = [], clouds = [], dust = [];
  let best = Number(localStorage.getItem("lastLightBest") || 0);
  const dino = { x: 80, y: 0, width: 34, height: 44, vy: 0, duck: false, step: 0 };
  const gravity = 0.72;

  function updateBest() {
    bestNode.textContent = String(best).padStart(5, "0");
    footerBest.textContent = String(best).padStart(5, "0") + " m";
  }
  updateBest();

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    w = rect.width; h = rect.height;
    canvas.width = Math.round(w * ratio); canvas.height = Math.round(h * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ground = h - 38;
    dino.x = Math.max(38, w * .11);
    if (!running) dino.y = ground - dino.height;
    clouds = [
      { x: w * .25, y: h * .23, s: 1 },
      { x: w * .68, y: h * .15, s: .7 },
      { x: w * .9, y: h * .31, s: .55 }
    ];
    draw();
  }
  window.addEventListener("resize", resize);

  function start() {
    cancelAnimationFrame(raf);
    score = 0; speed = 6; obstacles = []; dust = [];
    dino.height = 44; dino.duck = false; dino.vy = 0;
    dino.y = ground - dino.height; dino.step = 0;
    running = true; gameOver = false; last = performance.now();
    overlay.classList.add("hidden");
    raf = requestAnimationFrame(loop);
  }

  function end() {
    running = false; gameOver = true;
    if (score > best) {
      best = score;
      localStorage.setItem("lastLightBest", String(best));
      updateBest();
    }
    title.textContent = "The horizon caught you.";
    copy.textContent = "You traveled " + score + " metres. Every run leaves a mark.";
    button.textContent = "Run it again";
    overlay.classList.remove("hidden");
  }

  function jump() {
    if (!running) { start(); return; }
    if (dino.y >= ground - dino.height - 1) {
      dino.vy = -13.5;
      for (let i = 0; i < 7; i++) dust.push({ x: dino.x + 10, y: ground - 2, vx: -Math.random() * 2, vy: -Math.random() * 2, life: 18 });
    }
  }

  function setDuck(value) {
    if (!running) return;
    dino.duck = value;
    dino.height = value ? 27 : 44;
    if (dino.y + dino.height > ground) dino.y = ground - dino.height;
  }

  function spawnObstacle() {
    const bird = score > 180 && Math.random() < .28;
    const width = bird ? 38 : 19 + Math.random() * 14;
    const height = bird ? 18 : 26 + Math.random() * 22;
    obstacles.push({ x: w + 20, width, height, bird, phase: Math.random() * 6 });
  }

  function roundedRect(x, y, width, height, radius, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, width, height, radius);
    ctx.fill();
  }

  function drawBackground() {
    const sky = ctx.createLinearGradient(0, 0, 0, h);
    sky.addColorStop(0, "#101721");
    sky.addColorStop(.65, "#35242a");
    sky.addColorStop(1, "#171417");
    ctx.fillStyle = sky; ctx.fillRect(0, 0, w, h);

    const glow = ctx.createRadialGradient(w * .72, h * .48, 5, w * .72, h * .48, h * .65);
    glow.addColorStop(0, "rgba(221,133,88,.23)");
    glow.addColorStop(1, "rgba(221,133,88,0)");
    ctx.fillStyle = glow; ctx.fillRect(0, 0, w, h);

    ctx.fillStyle = "rgba(241,220,185,.76)";
    ctx.beginPath(); ctx.arc(w * .72, h * .43, Math.min(27, h * .09), 0, Math.PI * 2); ctx.fill();

    clouds.forEach((c, i) => {
      ctx.fillStyle = "rgba(227,205,190,.12)";
      ctx.beginPath();
      ctx.ellipse(c.x, c.y, 35 * c.s, 7 * c.s, 0, 0, Math.PI * 2);
      ctx.ellipse(c.x + 13 * c.s, c.y - 4 * c.s, 19 * c.s, 8 * c.s, 0, 0, Math.PI * 2);
      ctx.fill();
    });

    // Distant ridge
    ctx.fillStyle = "#241d23";
    ctx.beginPath(); ctx.moveTo(0, ground);
    for (let x = 0; x <= w + 30; x += 30) {
      const peak = ground - 45 - Math.sin(x * .013) * 19 - Math.cos(x * .027) * 12;
      ctx.lineTo(x, peak);
    }
    ctx.lineTo(w, ground); ctx.closePath(); ctx.fill();

    // Ground
    ctx.fillStyle = "#161519"; ctx.fillRect(0, ground, w, h - ground);
    ctx.strokeStyle = "rgba(231,170,98,.6)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, ground + .5); ctx.lineTo(w, ground + .5); ctx.stroke();

    ctx.strokeStyle = "rgba(241,233,216,.13)";
    for (let i = 0; i < 12; i++) {
      let x = ((i * 103 - (score * 3) % 103) % w + w) % w;
      ctx.beginPath(); ctx.moveTo(x, ground + 12); ctx.lineTo(x - 8, ground + 12); ctx.stroke();
    }
  }

  function drawDino() {
    const y = dino.y, x = dino.x, height = dino.height;
    const color = "#e8dcc7";
    const bodyY = y + (dino.duck ? 8 : 12);
    roundedRect(x + 7, bodyY + 8, 25, dino.duck ? 15 : 19, 6, color);
    roundedRect(x + 21, y + (dino.duck ? 2 : 0), 16, 17, 5, color);
    ctx.fillStyle = "#17171a";
    ctx.beginPath(); ctx.arc(x + 32, y + (dino.duck ? 7 : 6), 1.6, 0, Math.PI * 2); ctx.fill();
    // Tail
    ctx.fillStyle = color;
    ctx.beginPath(); ctx.moveTo(x + 8, bodyY + 12); ctx.lineTo(x - 3, bodyY + 4); ctx.lineTo(x + 5, bodyY + 19); ctx.fill();
    // Legs
    const moving = running && dino.y >= ground - height - 1;
    const swing = moving ? Math.sin(dino.step) * 5 : 0;
    ctx.strokeStyle = color; ctx.lineWidth = 5; ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(x + 14, bodyY + 22); ctx.lineTo(x + 13 + swing, ground - y);
    ctx.moveTo(x + 26, bodyY + 22); ctx.lineTo(x + 26 - swing, ground - y);
    ctx.stroke();
  }

  function drawObstacle(o) {
    if (o.bird) {
      const y = ground - 46 + Math.sin(o.phase) * 4;
      ctx.fillStyle = "#d58670";
      roundedRect(o.x + 8, y + 5, 25, 12, 6, "#c77a69");
      ctx.beginPath(); ctx.moveTo(o.x + 16, y + 10); ctx.lineTo(o.x + 3, y + 2 + Math.sin(o.phase * 2) * 5); ctx.lineTo(o.x + 20, y + 13); ctx.fill();
      ctx.beginPath(); ctx.arc(o.x + 31, y + 6, 2, 0, Math.PI * 2); ctx.fill();
    } else {
      const x = o.x, y = ground - o.height;
      roundedRect(x + 4, y, o.width - 8, o.height, 5, "#b97861");
      roundedRect(x, y + 12, 10, 5, 2, "#d08a6e");
      roundedRect(x + o.width - 9, y + 22, 10, 5, 2, "#d08a6e");
      ctx.fillStyle = "rgba(32,24,25,.6)";
      ctx.fillRect(x + o.width * .45, y + 7, 2, 5);
      ctx.fillRect(x + o.width * .28, y + o.height * .65, 3, 3);
    }
  }

  function draw() {
    if (!w || !h) return;
    drawBackground();
    obstacles.forEach(drawObstacle);
    dust.forEach(p => {
      ctx.fillStyle = "rgba(231,170,98," + Math.max(0, p.life / 18) + ")";
      ctx.fillRect(p.x, p.y, 3, 3);
    });
    drawDino();
  }

  function loop(now) {
    if (!running) return;
    const dt = Math.min((now - last) / 16.67, 2);
    last = now;
    score += Math.max(1, Math.floor(speed / 6));
    speed = Math.min(12, 6 + score / 550);
    scoreNode.textContent = String(score).padStart(5, "0");

    dino.vy += gravity * dt;
    dino.y += dino.vy * dt;
    if (dino.y > ground - dino.height) {
      dino.y = ground - dino.height; dino.vy = 0;
    }
    dino.step += .22 * dt;

    if (Math.random() < .018 * dt) spawnObstacle();
    obstacles.forEach(o => {
      o.x -= speed * dt;
      o.phase += .12 * dt;
    });
    obstacles = obstacles.filter(o => o.x + o.width > -10);

    clouds.forEach(c => {
      c.x -= speed * .08 * dt;
      if (c.x < -60) c.x = w + 45;
    });

    dust.forEach(p => {
      p.x += p.vx * dt; p.y += p.vy * dt; p.vy += .12 * dt; p.life -= dt;
    });
    dust = dust.filter(p => p.life > 0);

    const dx = dino.x + 5, dy = dino.y + 5;
    for (const o of obstacles) {
      const oy = o.bird ? ground - 46 : ground - o.height;
      const oh = o.bird ? 18 : o.height;
      if (dx + dino.width - 8 > o.x + 3 && dx < o.x + o.width - 3 && dy + dino.height - 7 > oy + 2 && dy < oy + oh - 2) {
        draw(); end(); return;
      }
    }
    draw();
    raf = requestAnimationFrame(loop);
  }

  button.addEventListener("click", start);
  window.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) e.preventDefault();
    if (e.code === "Space" || e.code === "ArrowUp") jump();
    if (e.code === "ArrowDown") setDuck(true);
    if (e.code === "KeyR") start();
  });
  window.addEventListener("keyup", e => {
    if (e.code === "ArrowDown") setDuck(false);
  });
  canvas.addEventListener("pointerdown", jump);
  resize();
})();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    # Keep Flask local to this computer.
    app.run(host="127.0.0.1", port=5000, debug=False)