from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Last Light — Dino Run</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; display: grid; place-items: center;
    color: #f4f0e8; font-family: Georgia, "Times New Roman", serif;
    background:
      radial-gradient(ellipse at 50% 80%, #34404a 0%, #171d26 45%, #090d13 100%);
    overflow: hidden;
  }
  .scene { width: min(1000px, 94vw); }
  header { display: flex; justify-content: space-between; align-items: end; margin-bottom: 16px; }
  .eyebrow { color: #d4aa6a; font: 11px Arial, sans-serif; letter-spacing: .32em; text-transform: uppercase; }
  h1 { margin: 6px 0 0; font-size: clamp(28px, 5vw, 48px); font-weight: 400; letter-spacing: .06em; }
  .score { text-align: right; font: 12px Arial, sans-serif; letter-spacing: .16em; color: #b7c1c5; }
  .score strong { display: block; color: #f5d59f; font-size: 25px; margin-top: 5px; }
  .frame { position: relative; border: 1px solid #d3b47c55; box-shadow: 0 20px 80px #0009; }
  canvas { display: block; width: 100%; height: auto; background: #111a22; }
  .overlay {
    position: absolute; inset: 0; display: grid; place-content: center; text-align: center;
    padding: 20px; background: linear-gradient(#09101a33, #09101a99);
  }
  .overlay.hidden { display: none; }
  .overlay h2 { margin: 0 0 10px; font-size: clamp(30px, 6vw, 54px); font-weight: 400; letter-spacing: .08em; }
  .overlay p { color: #d8d0c0; font: 13px/1.8 Arial, sans-serif; letter-spacing: .08em; }
  button {
    justify-self: center; margin-top: 12px; padding: 12px 25px; cursor: pointer;
    color: #f7e6c6; background: #a86c35; border: 1px solid #efc787;
    font: 12px Arial, sans-serif; letter-spacing: .2em; text-transform: uppercase;
  }
  button:hover { background: #c48243; }
  footer { display: flex; justify-content: space-between; gap: 12px; margin-top: 12px; color: #aab2b7; font: 11px Arial, sans-serif; letter-spacing: .1em; }
  @media (max-width: 600px) { footer { font-size: 9px; } }
</style>
</head>
<body>
<main class="scene">
  <header>
    <div><div class="eyebrow">A little game for the long night</div><h1>LAST LIGHT</h1></div>
    <div class="score">DISTANCE<strong id="score">00000</strong></div>
  </header>

  <div class="frame">
    <canvas id="game" width="960" height="400" aria-label="Dinosaur running game"></canvas>
    <div class="overlay" id="overlay">
      <h2 id="title">THE WORLD WENT QUIET</h2>
      <p id="message">A small survivor. One endless horizon.<br>Press SPACE or tap to begin — jump over the shadows.</p>
      <button id="start">Begin the run</button>
    </div>
  </div>
  <footer><span>SPACE / ↑ / TAP — JUMP</span><span>KEEP RUNNING. KEEP THE LIGHT.</span></footer>
</main>
<script>
(() => {
  const canvas = document.querySelector("#game"), ctx = canvas.getContext("2d");
  const overlay = document.querySelector("#overlay"), scoreEl = document.querySelector("#score");
  const title = document.querySelector("#title"), message = document.querySelector("#message");
  const dino = { x: 105, y: 0, w: 46, h: 52, vy: 0, grounded: true };
  let running = false, score = 0, speed = 5, obstacles = [], dust = [], last = 0, spawn = 0;

  function reset() {
    score = 0; speed = 5; obstacles = []; dust = []; spawn = 0;
    dino.y = ground() - dino.h; dino.vy = 0; dino.grounded = true;
    scoreEl.textContent = "00000";
  }
  function ground() { return canvas.height - 64; }

  function start() {
    reset(); running = true; overlay.classList.add("hidden");
    last = performance.now(); requestAnimationFrame(loop);
  }
  function jump() {
    if (!running) { start(); return; }
    if (dino.grounded) { dino.vy = -14; dino.grounded = false; }
  }
  document.querySelector("#start").addEventListener("click", start);
  canvas.addEventListener("pointerdown", jump);
  window.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "w", "W"].includes(e.key)) { e.preventDefault(); jump(); }
    if (e.key === "Enter" && !running) start();
  });

  function drawDino() {
    const x = dino.x, y = dino.y;
    ctx.fillStyle = "#e8d3ad";
    ctx.fillRect(x + 8, y + 17, 29, 25);
    ctx.fillRect(x + 26, y + 3, 22, 21);
    ctx.fillRect(x + 39, y + 9, 12, 8);
    ctx.fillRect(x, y + 25, 12, 8);
    ctx.fillStyle = "#18212a"; ctx.fillRect(x + 40, y + 7, 3, 3);
    const step = running && dino.grounded ? Math.floor(score / 5) % 2 : 0;
    ctx.fillStyle = "#e8d3ad";
    ctx.fillRect(x + 13, y + 40, 8, step ? 12 : 8);
    ctx.fillRect(x + 29, y + 40, 8, step ? 8 : 12);
  }

  function drawBackground() {
    const g = ctx.createLinearGradient(0, 0, 0, canvas.height);
    g.addColorStop(0, "#15212c"); g.addColorStop(1, "#59616a");
    ctx.fillStyle = g; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#f1c88b"; ctx.beginPath(); ctx.arc(740, 105, 38, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#283640";
    ctx.beginPath(); ctx.moveTo(0, 270); ctx.lineTo(130, 160); ctx.lineTo(260, 270);
    ctx.lineTo(400, 145); ctx.lineTo(590, 270); ctx.lineTo(750, 175); ctx.lineTo(960, 280);
    ctx.lineTo(960, 400); ctx.lineTo(0, 400); ctx.fill();
    ctx.fillStyle = "#222d34"; ctx.fillRect(0, ground(), canvas.width, 64);
    ctx.fillStyle = "#c5a77d";
    for (let x = -((score * 3) % 60); x < canvas.width; x += 60)
      ctx.fillRect(x, ground() + 18, 28, 2);
  }

  function drawCactus(o) {
    ctx.fillStyle = "#253b36";
    ctx.fillRect(o.x + 10, o.y, 15, o.h);
    ctx.fillRect(o.x, o.y + 15, 12, 7); ctx.fillRect(o.x, o.y + 7, 7, 16);
    ctx.fillRect(o.x + 23, o.y + 24, 12, 7); ctx.fillRect(o.x + 28, o.y + 16, 7, 16);
  }

  function loop(now) {
    if (!running) return;
    const dt = Math.min((now - last) / 16.67, 2); last = now;
    score += dt; speed = Math.min(12, 5 + score / 700);
    scoreEl.textContent = String(Math.floor(score * 2)).padStart(5, "0");

    dino.vy += 0.72 * dt; dino.y += dino.vy * dt;
    if (dino.y + dino.h >= ground()) { dino.y = ground() - dino.h; dino.vy = 0; dino.grounded = true; }

    spawn -= dt;
    if (spawn <= 0) {
      const h = 30 + Math.random() * 25;
      obstacles.push({ x: canvas.width + 10, y: ground() - h, w: 35, h });
      spawn = 65 + Math.random() * 55;
    }
    obstacles.forEach(o => o.x -= speed * dt);
    obstacles = obstacles.filter(o => o.x + o.w > 0);

    drawBackground();
    obstacles.forEach(drawCactus);
    drawDino();

    for (const o of obstacles) {
      if (dino.x + 35 > o.x + 4 && dino.x + 9 < o.x + o.w - 3 &&
          dino.y + dino.h - 4 > o.y) {
        running = false; title.textContent = "THE NIGHT CAUGHT UP";
        message.innerHTML = `You ran ${Math.floor(score * 2)} metres.<br>Take a breath. Then try again.`;
        document.querySelector("#start").textContent = "Run again";
        overlay.classList.remove("hidden"); return;
      }
    }
    requestAnimationFrame(loop);
  }

  reset(); drawBackground(); drawDino();
})();
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=True)
"""

To run it:

1. Install Flask: `pip install flask`
2. Start the game: `python app.py`
3. Open `http://127.0.0.1:5000` in Chrome.

**Note:** Flask serves the game from your computer, so it needs to be running while you play. For a game that works after the computer powers off, you’d need to save it as a standalone `.html` file and open that in Chrome; the computer itself must still be on.