from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101311">
<title>Chess / You vs Machine</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{color-scheme:dark;--bg:#101311;--panel:#181d19;--line:#303832;--muted:#8f9a90;--green:#c6f276;--cream:#e9e2cf;--dark:#506353}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 48% 42%,#202a21 0,#101311 66%);color:#f0f1e9;font:14px 'DM Sans',sans-serif;min-height:100vh}
.app{min-height:100vh;max-width:1460px;margin:auto;padding:24px 36px 22px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding:0 0 20px}
.brand{display:flex;align-items:center;gap:13px;font-weight:800;letter-spacing:.13em;font-size:13px}
.brand-icon{height:34px;width:34px;border:1px solid #53614f;border-radius:50%;display:grid;place-items:center;color:var(--green);font-size:16px}
.brand small{display:block;color:var(--muted);font-size:9px;letter-spacing:.17em;margin-top:4px;font-weight:500}
.top-right{color:var(--muted);font:10px 'DM Mono',monospace;letter-spacing:.09em}
.layout{flex:1;display:grid;grid-template-columns:minmax(240px,1fr) minmax(400px,600px) minmax(240px,1fr);gap:32px;align-items:center;padding:24px 0}
.side{display:flex;flex-direction:column;gap:16px;min-width:0}
.eyebrow{font:10px 'DM Mono',monospace;color:var(--muted);letter-spacing:.15em;text-transform:uppercase}
.player{display:flex;align-items:center;gap:13px;padding:15px;background:#171c18;border:1px solid var(--line);border-radius:10px}
.avatar{width:40px;height:40px;border-radius:8px;background:#26342a;color:var(--green);display:grid;place-items:center;font-size:21px}
.avatar.robot{background:#2c302c;color:#d5ded4}
.player-info{flex:1}
.player-info strong{font-size:14px}
.player-info small{display:block;margin-top:4px;color:var(--muted);font-size:11px}
.turn{font:9px 'DM Mono',monospace;color:var(--green);letter-spacing:.1em}
.card{background:#171c18;border:1px solid var(--line);border-radius:10px;padding:17px}
.card h2{font-size:11px;text-transform:uppercase;letter-spacing:.13em;margin:0 0 15px}
.status{color:#e8ebdf;font-size:13px;line-height:1.55}
.moves{height:190px;overflow:auto;color:#cad1c6;font:12px/1.9 'DM Mono',monospace;scrollbar-color:#39423a transparent}
.moves .num{color:#768277;display:inline-block;width:26px}
.moves .latest{color:var(--green)}
.board-wrap{position:relative;width:100%;aspect-ratio:1.08/1;display:grid;place-items:center}
.board-frame{position:absolute;inset:0;transform:perspective(1150px) rotateX(11deg) scale(.94);transform-style:preserve-3d;filter:drop-shadow(0 28px 28px #0009)}
#board{width:100%;height:100%;display:grid;grid-template-columns:repeat(8,1fr);grid-template-rows:repeat(8,1fr);border:8px solid #292f29;border-radius:7px;overflow:hidden;box-shadow:0 0 0 1px #70806d66,0 0 38px #0008;transform:translateZ(0)}
.sq{position:relative;display:grid;place-items:center;cursor:pointer;user-select:none}
.sq.light{background:linear-gradient(135deg,#ddd5bd,#c9c1aa)}
.sq.dark{background:linear-gradient(135deg,#637765,#506352)}
.sq.selected{background:#b6bd59}
.sq.last{box-shadow:inset 0 0 0 999px #e4df6133}
.sq.legal:after{content:'';width:23%;height:23%;border-radius:50%;background:#17231745;position:absolute}
.sq.capture:after{content:'';position:absolute;inset:3%;border:3px solid #523f35a8;border-radius:50%}
.coord{position:absolute;font:9px 'DM Mono',monospace;opacity:.64;z-index:1;pointer-events:none}
.coord.file{right:4px;bottom:3px}
.coord.rank{left:4px;top:2px}
.light .coord{color:#586251}
.dark .coord{color:#ede7d8}
.piece{position:relative;z-index:2;width:79%;height:87%;filter:drop-shadow(0 4px 2px #0004);transition:transform .16s}
.sq:hover .piece{transform:translateY(-5px)}
.piece svg{width:100%;height:100%;overflow:visible}
.piece.white{color:#f2ead7}
.piece.black{color:#29322b}
.piece.white svg{filter:drop-shadow(0 1px 0 #fff8)}
.piece.black svg{filter:drop-shadow(0 1px 0 #829080)}
.board-hint{text-align:center;color:#879187;font:10px 'DM Mono',monospace;letter-spacing:.07em;margin-top:15px}
.controls{display:flex;gap:9px}
.btn{font:11px 'DM Sans',sans-serif;font-weight:700;border:1px solid #3a443b;border-radius:7px;background:#202720;color:#e8ece4;padding:11px 12px;cursor:pointer;transition:.18s}
.btn:hover{border-color:#82916d;background:#29322a}
.btn.primary{background:var(--green);border-color:var(--green);color:#172015}
.btn.primary:hover{background:#d5fa91}
.btn:disabled{opacity:.45;cursor:default}
.controls .btn{flex:1}
.settings{display:flex;align-items:center;justify-content:space-between;color:#cbd1c7;font-size:12px;padding:13px 0;border-bottom:1px solid #303832}
.settings:last-child{border:0;padding-bottom:0}
.settings select{background:#222922;color:#e7ebe2;border:1px solid #3a443b;border-radius:5px;padding:7px 22px 7px 9px;font:11px 'DM Sans',sans-serif;outline:none}
.capture-list{font-size:19px;min-height:25px;line-height:1.5;letter-spacing:2px;color:#bac2b6}
.foot{border-top:1px solid var(--line);padding-top:14px;display:flex;justify-content:space-between;color:#788379;font:9px 'DM Mono',monospace;letter-spacing:.08em}
.thinking{color:#d7c688!important}
.toast{position:fixed;bottom:36px;left:50%;transform:translate(-50%,15px);opacity:0;pointer-events:none;padding:11px 16px;border:1px solid #58634d;background:#202920;border-radius:8px;color:#eff3e8;font-size:12px;transition:.2s;z-index:9}
.toast.show{transform:translate(-50%,0);opacity:1}
.modal-bg{position:fixed;inset:0;background:#080a08b8;display:none;place-items:center;z-index:10}
.modal-bg.show{display:grid}
.modal{background:#1b211b;border:1px solid #465145;border-radius:14px;padding:28px;width:min(380px,90vw);text-align:center;box-shadow:0 20px 80px #0008}
.modal h2{margin:0 0 9px;font-size:21px}
.modal p{color:#aab2a7;line-height:1.6}
.promos{display:flex;justify-content:center;gap:8px;margin-top:18px}
.promos button{font-size:28px;padding:8px 12px}
@media(max-width:1000px){
  .app{padding:18px 20px}
  .layout{grid-template-columns:minmax(190px,1fr) minmax(360px,1.5fr);gap:20px}
  .right{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr}
  .right .player{grid-column:1/-1}
  .right .settings-card{grid-column:1/-1}
  .moves{height:106px}
}
@media(max-width:650px){
  .app{padding:13px 14px}
  .top{padding-bottom:13px}
  .top-right{font-size:8px}
  .layout{grid-template-columns:1fr;gap:15px;padding:17px 0}
  .board-wrap{grid-row:1;width:min(100%,520px);margin:auto}
  .left{grid-row:2}
  .right{grid-row:3;display:flex}
  .left .moves{height:105px}
  .board-hint{font-size:9px;margin-top:8px}
  .player{padding:11px}
  .card{padding:13px}
  .foot{font-size:8px}
}
</style>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js","chess.js":"https://cdn.jsdelivr.net/npm/chess.js@1.4.0/dist/esm/chess.js"}}
</script>
</head>
<body>
<div class="app">
  <header class="top">
    <div class="brand">
      <div class="brand-icon">♞</div>
      <div>QUIET SQUARE<small>HUMAN VS MACHINE · 3D CHESS</small></div>
    </div>
    <div class="top-right">STANDARD CHESS&nbsp; / &nbsp;YOU PLAY WHITE</div>
  </header>

  <main class="layout">
    <section class="side left">
      <div class="eyebrow">PLAYERS</div>
      <div class="player">
        <div class="avatar">♙</div>
        <div class="player-info"><strong>You</strong><small>White pieces</small></div>
        <div class="turn" id="humanTurn">YOUR TURN</div>
      </div>
      <div class="player">
        <div class="avatar robot">♟</div>
        <div class="player-info"><strong>Chess robot</strong><small id="robotNote">Ready to play</small></div>
        <div class="turn" id="robotTurn" style="color:#879187">ROBOT</div>
      </div>
      <div class="card"><h2>Game status</h2><div class="status" id="status">Your move. Select a white piece to see its legal moves.</div></div>
      <div class="card"><h2>Moves</h2><div class="moves" id="moves"><span style="color:#7e897f">Moves will appear here.</span></div></div>
    </section>

    <section>
      <div class="board-wrap"><div class="board-frame"><div id="board" aria-label="Chessboard"></div></div></div>
      <div class="board-hint">CLICK A WHITE PIECE, THEN CHOOSE A HIGHLIGHTED SQUARE</div>
    </section>

    <section class="side right">
      <div class="player">
        <div class="avatar robot">♟</div>
        <div class="player-info"><strong>Robot captures</strong><small>Pieces taken from you</small></div>
      </div>
      <div class="card"><div class="capture-list" id="whiteLost">—</div></div>
      <div class="player">
        <div class="avatar">♙</div>
        <div class="player-info"><strong>Your captures</strong><small>Robot pieces taken</small></div>
      </div>
      <div class="card"><div class="capture-list" id="blackLost">—</div></div>
      <div class="card settings-card">
        <h2>Game settings</h2>
        <div class="settings">
          <span>Robot strength</span>
          <select id="difficulty">
            <option value="1">Easy</option>
            <option value="2" selected>Balanced</option>
            <option value="3">Thoughtful</option>
          </select>
        </div>
        <div class="settings">
          <span>Board view</span>
          <button class="btn" id="flip">Flip board</button>
        </div>
      </div>
      <div class="controls">
        <button class="btn" id="undo">↶ &nbsp;Undo</button>
        <button class="btn" id="new">＋ &nbsp;New game</button>
      </div>
    </section>
  </main>

  <footer class="foot">
    <span>STANDARD RULES · CASTLING · EN PASSANT · PROMOTION</span>
    <span>PIECES: PROCEDURAL 3D MESHES · BLENDER-INSPIRED</span>
  </footer>
</div>
<div class="toast" id="toast"></div>
<div class="modal-bg" id="promo">
  <div class="modal">
    <h2>Promote your pawn</h2>
    <p>Choose a piece for your pawn to become.</p>
    <div class="promos" id="promoChoices"></div>
  </div>
</div>

<script type="module">
import * as THREE from 'three';
import {Chess} from 'chess.js';

const game=new Chess();
const boardEl=document.querySelector('#board');
const scene=new THREE.Scene();
let selected=null,legal=[],flipped=false,thinking=false,history=[],capturedW=[],capturedB=[],toastTimer;
const files='abcdefgh';
const vals={p:100,n:320,b:335,r:500,q:900,k:20000};
const glyph={wk:'♔',wq:'♕',wr:'♖',wb:'♗',wn:'♘',wp:'♙',bk:'♚',bq:'♛',br:'♜',bb:'♝',bn:'♞',bp:'♟'};

// Build chess pieces from sculpted lathe profiles and primitive details.
const renderer=new THREE.WebGLRenderer({alpha:true,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(128,128);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;

const camera=new THREE.PerspectiveCamera(35,1,.1,100);
camera.position.set(5.6,7.2,9.5);
camera.lookAt(0,.45,0);
scene.add(new THREE.HemisphereLight(0xe9efdf,0x313b30,2.1));
const key=new THREE.DirectionalLight(0xffebca,3.2);
key.position.set(-3,9,5);
key.castShadow=true;
scene.add(key);
const fill=new THREE.DirectionalLight(0xc2e0c6,1.6);
fill.position.set(5,5,-5);
scene.add(fill);

const matW=new THREE.MeshStandardMaterial({color:0xf1e8d3,roughness:.28,metalness:.08});
const matB=new THREE.MeshStandardMaterial({color:0x253129,roughness:.28,metalness:.19});
const trimW=new THREE.MeshStandardMaterial({color:0xc6aa72,roughness:.3,metalness:.7});
const trimB=new THREE.MeshStandardMaterial({color:0x72806a,roughness:.3,metalness:.68});

function lathe(profile,mat,group){
  const points=profile.map(v=>new THREE.Vector2(v[0],v[1]));
  const mesh=new THREE.Mesh(new THREE.LatheGeometry(points,32),mat);
  mesh.castShadow=true;
  mesh.receiveShadow=true;
  group.add(mesh);
  return mesh;
}
function cylinder(group,r,h,y,mat,segments=32){
  const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r*.92,r,h,segments,1),mat);
  mesh.position.y=y;
  mesh.castShadow=true;
  group.add(mesh);
  return mesh;
}
function sphere(group,r,x,y,z,mat,scale=[1,1,1]){
  const mesh=new THREE.Mesh(new THREE.SphereGeometry(r,20,14),mat);
  mesh.position.set(x,y,z);
  mesh.scale.set(...scale);
  mesh.castShadow=true;
  group.add(mesh);
  return mesh;
}
function makePiece(type,color){
  const group=new THREE.Group();
  const main=color==='w'?matW:matB;
  const trim=color==='w'?trimW:trimB;
  lathe([[0,.015],[.23,.015],[.265,.04],[.27,.08],[.24,.105],[.20,.13],[.19,.17],[.16,.21],[.14,.26],[.11,.3]],main,group);
  lathe([[.231,.075],[.25,.082],[.25,.099],[.22,.105]],trim,group);
  const t=type.toLowerCase();

  if(t==='p'){
    cylinder(group,.115,.11,.34,main);
    sphere(group,.105,0,.52,0,main,[.84,1,.84]);
    lathe([[.1,.38],[.13,.39],[.13,.42],[.1,.43]],trim,group);
  }
  if(t==='r'){
    lathe([[.105,.27],[.12,.37],[.17,.4],[.18,.44],[.145,.47],[.145,.68],[.19,.7],[.20,.76],[.18,.8],[.12,.8],[.115,.73],[.075,.73],[.07,.8],[.01,.8]],main,group);
    cylinder(group,.18,.04,.43,trim);
    for(let i=0;i<4;i++){
      const angle=i*Math.PI/2;
      const block=cylinder(group,.043,.09,.82,main,4);
      block.position.x=Math.sin(angle)*.135;
      block.position.z=Math.cos(angle)*.135;
    }
  }
  if(t==='n'){
    lathe([[.1,.27],[.15,.38],[.18,.43],[.13,.49],[.12,.55],[.15,.63],[.12,.7],[.045,.78],[0,.79]],main,group);
    const head=sphere(group,.13,0,.67,0,main,[.78,1.17,.78]);
    head.rotation.z=-.28;
    sphere(group,.068,0,.72,.075,main,[.8,.58,1.18]);
    sphere(group,.023,.025,.755,.107,trim);
    const ear=sphere(group,.045,-.055,.79,-.005,main,[.63,1.3,.65]);
    ear.rotation.z=-.4;
  }
  if(t==='b'){
    lathe([[.1,.26],[.14,.36],[.17,.4],[.13,.46],[.11,.54],[.15,.65],[.11,.73],[.05,.78],[0,.78]],main,group);
    sphere(group,.11,0,.76,0,trim,[1,.25,1]);
    const stem=cylinder(group,.026,.12,.88,trim);
    stem.rotation.z=.22;
  }
  if(t==='q'){
    lathe([[.1,.26],[.15,.37],[.17,.42],[.13,.5],[.12,.58],[.16,.66],[.18,.72],[.21,.76],[.2,.8],[.14,.8],[.13,.75],[.07,.75],[.06,.8],[0,.8]],main,group);
    for(let i=0;i<5;i++){
      const angle=i*2*Math.PI/5;
      sphere(group,.042,Math.sin(angle)*.17,.83,Math.cos(angle)*.17,trim);
    }
    sphere(group,.038,0,.89,0,trim);
  }
  if(t==='k'){
    lathe([[.1,.26],[.15,.37],[.17,.42],[.14,.5],[.12,.58],[.16,.66],[.17,.72],[.2,.76],[.18,.8],[.13,.8],[.12,.74],[.07,.74],[.06,.8],[0,.8]],main,group);
    cylinder(group,.026,.17,.91,trim);
    const bar=cylinder(group,.025,.13,.965,trim,16);
    bar.rotation.z=Math.PI/2;
    sphere(group,.04,0,1.03,0,trim);
  }
  return group;
}
for(const color of ['w','b']){
  for(const type of ['k','q','r','b','n','p'])makePiece(type,color);
}

function render(){
  boardEl.replaceChildren();
  legal=selected?game.moves({square:selected,verbose:true}):[];
  const targets=legal.map(m=>m.to);

  for(let row=0;row<8;row++){
    for(let col=0;col<8;col++){
      const file=flipped?7-col:col;
      const rank=flipped?7-row:row;
      const square=files[file]+(8-rank);
      const el=document.createElement('div');

      el.className='sq '+((rank+file)%2?'dark':'light');
      el.dataset.square=square;

      if(selected===square)el.classList.add('selected');
      if(history.length&&history.at(-1).includes(square))el.classList.add('last');
      if(targets.includes(square)){
        el.classList.add('legal');
        if(game.get(square))el.classList.add('capture');
      }
      if(col===0){
        const label=document.createElement('span');
        label.className='coord rank';
        label.textContent=8-rank;
        el.append(label);
      }
      if(row===7){
        const label=document.createElement('span');
        label.className='coord file';
        label.textContent=files[file];
        el.append(label);
      }

      const piece=game.get(square);
      if(piece){
        const wrap=document.createElement('div');
        wrap.className='piece '+(piece.color==='w'?'white':'black');
        wrap.setAttribute('aria-label',(piece.color==='w'?'White ':'Black ')+piece.type);
        wrap.innerHTML=pieceSVG(piece.type,piece.color);
        el.append(wrap);
      }
      el.onclick=()=>clickSquare(square);
      boardEl.append(el);
    }
  }
  updateUI();
}

function pieceSVG(type,color){
  const fill=color==='w'?'#f3ead7':'#27312a';
  const stroke=color==='w'?'#a48f66':'#899484';
  const paths={
    p:'M32 5a10 10 0 1 0 0 20 10 10 0 0 0 0-20M20 28h24l5 12-5 6H19l-5-6z',
    r:'M14 5h10v9h16V5h10v18H14zM20 26h24l5 14-5 6H19l-5-6z',
    n:'M13 46q4-10 12-16-3-12 7-23 1 11 9 11 5 0 8-4l-1 13-9 9 5 10z',
    b:'M32 5 19 22l5 8-7 10 3 6h24l3-6-7-10 5-8zM27 19h10',
    q:'M11 9a4 4 0 1 0 0 8 4 4 0 0 0 0-8m21-6a4 4 0 1 0 0 8 4 4 0 0 0 0-8m21 6a4 4 0 1 0 0 8 4 4 0 0 0 0-8M14 19l6 16h24l6-16-12 10-6-16-6 16z',
    k:'M28 3h8v12h11v8H36v12h-8V23H17v-8h11z'
  };
  return `<svg viewBox="0 0 64 64" aria-hidden="true"><path d="${paths[type]}" fill="${fill}" stroke="${stroke}" stroke-width="2.2" stroke-linejoin="round"/><path d="M17 48h30l5 7H12z" fill="${fill}" stroke="${stroke}" stroke-width="2" stroke-linejoin="round"/></svg>`;
}

function clickSquare(square){
  if(thinking||game.isGameOver())return;
  const piece=game.get(square);

  if(selected&&legal.some(move=>move.to===square)){
    const move=legal.find(move=>move.to===square);
    if(move.flags.includes('p'))return promote(square);
    play(selected,square);
    return;
  }

  if(piece&&piece.color==='w'&&game.turn()==='w'){
    selected=square;
  }else{
    selected=null;
  }
  render();
}

function play(from,to,promotion='q'){
  let move;
  try{move=game.move({from,to,promotion});}catch{return;}
  if(!move)return;

  history.push([from,to]);
  if(move.captured)(move.color==='w'?capturedB:capturedW).push(move.captured);
  selected=null;
  render();

  if(finishCheck())return;

  thinking=true;
  document.querySelector('#robotNote').textContent='Thinking…';
  document.querySelector('#robotTurn').textContent='THINKING';
  document.querySelector('#robotTurn').classList.add('thinking');
  setTimeout(robotMove,330);
}

function promote(to){
  const modal=document.querySelector('#promo');
  const choices=document.querySelector('#promoChoices');
  choices.replaceChildren();

  for(const [type,symbol] of [['q','♕'],['r','♖'],['b','♗'],['n','♘']]){
    const button=document.createElement('button');
    button.className='btn';
    button.textContent=symbol;
    button.onclick=()=>{
      modal.classList.remove('show');
      play(selected,to,type);
    };
    choices.append(button);
  }
  modal.classList.add('show');
}

function material(){
  let score=0;
  const board=game.board();

  for(let rank=0;rank<8;rank++){
    for(let file=0;file<8;file++){
      const piece=board[rank][file];
      if(!piece)continue;

      const center=3.5-Math.abs(file-3.5)+3.5-Math.abs(rank-3.5);
      let value=vals[piece.type];
      if(piece.type==='p')value+=(piece.color==='w'?6-rank:rank-1)*7;
      else if(piece.type!=='k')value+=center*5;
      score+=(piece.color==='b'?value:-value);
    }
  }
  return score;
}

function robotMove(){
  if(game.isGameOver()){thinking=false;return;}

  const depth=Number(document.querySelector('#difficulty').value);
  const moves=game.moves({verbose:true});
  let best=-Infinity,options=[];

  for(const move of moves){
    game.move(move);
    let score=minimax(depth-1,-Infinity,Infinity,false);
    game.undo();
    score+=Math.random()*10;

    if(score>best){best=score;options=[move];}
    else if(score>best-12)options.push(move);
  }

  const choice=options[Math.floor(Math.random()*options.length)];
  if(choice){
    const move=game.move({from:choice.from,to:choice.to,promotion:'q'});
    history.push([move.from,move.to]);
    if(move.captured)(move.color==='w'?capturedB:capturedW).push(move.captured);
  }

  thinking=false;
  document.querySelector('#robotNote').textContent='Ready to play';
  document.querySelector('#robotTurn').textContent='ROBOT';
  document.querySelector('#robotTurn').classList.remove('thinking');
  render();
  finishCheck();
}

function minimax(depth,alpha,beta,maximizing){
  if(depth===0||game.isGameOver()){
    return material()*(game.turn()==='w'?-1:1);
  }

  const moves=game.moves({verbose:true});
  moves.sort((a,b)=>(b.captured?vals[b.captured]:0)-(a.captured?vals[a.captured]:0));

  if(maximizing){
    let best=-Infinity;
    for(const move of moves){
      game.move(move);
      best=Math.max(best,minimax(depth-1,alpha,beta,false));
      game.undo();
      alpha=Math.max(alpha,best);
      if(beta<=alpha)break;
    }
    return best;
  }else{
    let best=Infinity;
    for(const move of moves){
      game.move(move);
      best=Math.min(best,minimax(depth-1,alpha,beta,true));
      game.undo();
      beta=Math.min(beta,best);
      if(beta<=alpha)break;
    }
    return best;
  }
}

function finishCheck(){
  const status=document.querySelector('#status');

  if(game.isCheckmate()){
    status.textContent=game.turn()==='w'
      ?'Checkmate. The robot wins this game.'
      :'Checkmate. You win!';
    document.querySelector('#robotNote').textContent='Game complete';
    return true;
  }

  if(game.isDraw()){
    status.textContent='Draw. Well played by both sides.';
    return true;
  }

  if(game.isCheck()){
    status.textContent=game.turn()==='w'
      ?'Check! Your king is under attack.'
      :'Check! The robot king is under attack.';
  }
  return false;
}

function updateUI(){
  const historyEl=document.querySelector('#moves');
  const moves=game.history({verbose:true});

  if(moves.length){
    historyEl.innerHTML=moves.reduce((html,move,index)=>{
      if(index%2===0){
        const white=move.san;
        const black=moves[index+1]?.san||'';
        const latest=index+1>=moves.length;
        return html+`<div><span class="num">${Math.floor(index/2)+1}.</span><span class="${latest?'latest':''}">${white}</span> <span class="${index+1===moves.length-1?'latest':''}">${black}</span></div>`;
      }
      return html;
    },'');
  }else{
    historyEl.innerHTML='<span style="color:#7e897f">Moves will appear here.</span>';
  }

  document.querySelector('#whiteLost').textContent=
    capturedW.length?capturedW.map(piece=>glyph['w'+piece]).join(' '):'—';
  document.querySelector('#blackLost').textContent=
    capturedB.length?capturedB.map(piece=>glyph['b'+piece]).join(' '):'—';
  document.querySelector('#undo').disabled=game.history().length===0||thinking;

  const status=document.querySelector('#status');
  if(!game.isGameOver()&&!game.isCheck()){
    status.textContent=thinking
      ?'The robot is considering its move…'
      :game.turn()==='w'
        ?'Your move. Select a white piece to see its legal moves.'
        :'The robot is choosing a move.';
  }

  document.querySelector('#humanTurn').textContent=
    game.turn()==='w'&&!game.isGameOver()?'YOUR TURN':'WHITE';
  document.querySelector('#robotTurn').textContent=thinking?'THINKING':'ROBOT';
}

function showToast(message){
  const toast=document.querySelector('#toast');
  toast.textContent=message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>toast.classList.remove('show'),1800);
}

document.querySelector('#flip').onclick=()=>{
  flipped=!flipped;
  render();
};

document.querySelector('#new').onclick=()=>{
  game.reset();
  selected=null;
  legal=[];
  history=[];
  capturedW=[];
  capturedB=[];
  thinking=false;
  document.querySelector('#robotNote').textContent='Ready to play';
  render();
  showToast('New game started — you play White');
};

document.querySelector('#undo').onclick=()=>{
  if(thinking)return;

  let count=game.history().length>=2?2:1;
  while(count--&&game.history().length){
    const move=game.undo();
    history.pop();
    if(move?.captured)(move.color==='w'?capturedB:capturedW).pop();
  }

  selected=null;
  render();
  showToast('Last move undone');
};

render();
</script>
</body>
</html>'''


@app.get('/')
def home():
    return render_template_string(PAGE)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)