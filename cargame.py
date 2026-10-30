from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>APEX / Supercar Run</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Mono:wght@400;500&display=swap');
:root{--lime:#d7ff36;--glass:rgba(10,15,19,.72)}
*{box-sizing:border-box}
body{margin:0;background:#10171b;color:#f5f6f2;font-family:'Barlow Condensed',sans-serif;overflow:hidden}
#game{position:fixed;inset:0}
canvas{display:block;width:100%;height:100%}
.grain{position:fixed;inset:0;pointer-events:none;opacity:.11;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.22'/%3E%3C/svg%3E")}
.topbar{position:fixed;left:0;right:0;top:0;padding:25px 4vw;display:flex;justify-content:space-between;align-items:center;pointer-events:none}
.brand{font-size:20px;font-weight:900;letter-spacing:.22em}
.brand b{color:var(--lime)}
.tag{font:10px 'DM Mono';letter-spacing:.16em;color:#d1d6d2}
.hud{position:fixed;top:100px;left:4vw;display:flex;gap:12px}
.stat{background:var(--glass);border:1px solid #ffffff20;padding:12px 16px;min-width:106px;backdrop-filter:blur(12px)}
.label{font:9px 'DM Mono';color:#a6b0b1;letter-spacing:.16em}
.value{font-size:27px;font-weight:800;line-height:1.05;margin-top:4px}
.value small{font-size:12px;color:var(--lime);letter-spacing:.08em}
.rightHud{position:fixed;top:100px;right:4vw;text-align:right}
.level{font-size:13px;letter-spacing:.18em;color:var(--lime);font-weight:800}
.carname{font-size:30px;font-weight:900;text-transform:uppercase;line-height:1}
.condition{font:10px 'DM Mono';color:#b8c1c2;margin-top:8px;letter-spacing:.12em}
.progress{height:3px;background:#ffffff38;margin-top:14px;width:190px;margin-left:auto}
.progress i{display:block;height:100%;background:var(--lime);width:0;transition:width .2s}
.bottom{position:fixed;bottom:26px;left:4vw;right:4vw;display:flex;justify-content:space-between;align-items:end;pointer-events:none}
.hint{font:10px 'DM Mono';color:#e2e5df;letter-spacing:.12em;text-shadow:0 2px 8px #000}
.hint span{color:var(--lime)}
.legend{display:flex;gap:5px}
.legend b{font:9px 'DM Mono';padding:7px 9px;background:#101619a8;border:1px solid #ffffff27;color:#d7dcda;letter-spacing:.08em}
.legend b.active{color:var(--lime);border-color:var(--lime)}
.overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(90deg,rgba(7,12,16,.78),rgba(7,12,16,.18) 70%),linear-gradient(0deg,rgba(5,10,14,.55),transparent 40%);transition:opacity .35s,visibility .35s}
.overlay.hidden{opacity:0;visibility:hidden;pointer-events:none}
.panel{width:min(510px,88vw);margin-left:-35vw}
.eyebrow{font:11px 'DM Mono';letter-spacing:.2em;color:var(--lime);margin-bottom:14px}
.panel h1{font-size:clamp(58px,9vw,108px);line-height:.77;letter-spacing:-.035em;margin:0 0 25px;font-weight:900;text-transform:uppercase}
.panel h1 em{font-style:normal;color:var(--lime)}
.panel p{font-size:17px;line-height:1.35;color:#d1d6d2;max-width:360px;margin:0 0 27px}
.button{cursor:pointer;background:var(--lime);color:#121711;border:0;padding:14px 25px;font:900 15px 'Barlow Condensed';letter-spacing:.15em;text-transform:uppercase;min-width:168px}
.button:hover{background:#edff9b}
.note{font:9px 'DM Mono';color:#c0c5c1;margin-top:15px;letter-spacing:.1em}
.toast{position:fixed;top:38%;left:50%;transform:translate(-50%,-50%) scale(.9);font-size:clamp(34px,7vw,74px);font-weight:900;letter-spacing:.04em;text-align:center;text-shadow:0 4px 24px #000;opacity:0;transition:.3s;pointer-events:none}
.toast.show{opacity:1;transform:translate(-50%,-50%) scale(1)}
.toast small{display:block;font:11px 'DM Mono';color:var(--lime);letter-spacing:.2em;margin-top:12px}
.touch{position:fixed;bottom:75px;left:0;right:0;display:none;justify-content:space-between;padding:0 8vw}
.touch button{width:64px;height:64px;border-radius:50%;border:1px solid #ffffff66;background:#10161999;color:white;font-size:26px;touch-action:none}
.touch button:active{background:var(--lime);color:#111}
@media(max-width:700px){
  .panel{margin:0;width:84vw}
  .panel h1{font-size:68px}
  .topbar{padding:18px 5vw}
  .tag{font-size:8px}
  .hud{left:5vw;top:75px;gap:6px}
  .stat{padding:9px 10px;min-width:82px}
  .value{font-size:22px}
  .rightHud{top:75px;right:5vw}
  .carname{font-size:22px}
  .progress{width:130px}
  .bottom{bottom:17px;left:5vw;right:5vw}
  .hint{font-size:8px}
  .legend b{font-size:7px;padding:6px}
  .touch{display:flex}
}
</style>
</head>
<body>
<div id="game"></div>
<div class="grain"></div>

<div class="topbar">
  <div class="brand">APEX<b> / RUN</b></div>
  <div class="tag">EXTREME ROAD SERIES&nbsp; — &nbsp;01 / 03</div>
</div>

<div class="hud">
  <div class="stat">
    <div class="label">DISTANCE</div>
    <div class="value"><span id="distance">000</span><small> KM</small></div>
  </div>
  <div class="stat">
    <div class="label">SCORE</div>
    <div class="value" id="score">0000</div>
  </div>
</div>

<div class="rightHud">
  <div class="level" id="levelLabel">LEVEL 01</div>
  <div class="carname" id="carName">VORTEX GT</div>
  <div class="condition" id="condition">SNOW PASS · ICE</div>
  <div class="progress"><i id="progress"></i></div>
</div>

<div class="bottom">
  <div class="hint">STEER <span>← →</span> &nbsp; / &nbsp; <span>A D</span><br>BOOST <span>↑</span> &nbsp; BRAKE <span>↓</span></div>
  <div class="legend">
    <b class="active" id="biome0">01 SNOW</b>
    <b id="biome1">02 MUD</b>
    <b id="biome2">03 HIGHWAY</b>
  </div>
</div>

<div class="touch">
  <button id="left">‹</button>
  <button id="right">›</button>
</div>

<div class="overlay" id="overlay">
  <div class="panel">
    <div class="eyebrow">THREE WORLDS. THREE MACHINES.</div>
    <h1>OWN<br>THE <em>ROAD.</em></h1>
    <p>Push through blinding snow, tear across the mud, then unleash the apex predator on the highway.</p>
    <button class="button" id="start">START ENGINE&nbsp; ↗</button>
    <div class="note">ARROWS / WASD TO DRIVE &nbsp; · &nbsp; AVOID THE TRAFFIC</div>
  </div>
</div>
<div class="toast" id="toast"></div>

<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js';

const root = document.querySelector('#game');
const renderer = new THREE.WebGLRenderer({antialias:true, alpha:false});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.18;
root.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color('#9bb7c3');
scene.fog = new THREE.Fog('#9bb7c3',36,170);

const camera = new THREE.PerspectiveCamera(52,innerWidth/innerHeight,.1,400);
camera.position.set(0,6.2,12.5);
camera.lookAt(0,1,-8);

scene.add(new THREE.HemisphereLight(0xdcecff,0x313535,2));
const sun = new THREE.DirectionalLight(0xfff0d4,3.1);
sun.position.set(-8,15,3);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
scene.add(sun);

const mats = {
  road:new THREE.MeshStandardMaterial({color:'#343b3e',roughness:.84}),
  line:new THREE.MeshStandardMaterial({color:'#d8dbcf',roughness:.7}),
  snow:new THREE.MeshStandardMaterial({color:'#e7f2f1',roughness:.96}),
  mud:new THREE.MeshStandardMaterial({color:'#5c4631',roughness:1}),
  grass:new THREE.MeshStandardMaterial({color:'#55705d',roughness:1}),
  tire:new THREE.MeshStandardMaterial({color:'#111416',roughness:.9}),
  glass:new THREE.MeshPhysicalMaterial({color:'#15232b',metalness:.55,roughness:.17,clearcoat:1}),
  lamp:new THREE.MeshStandardMaterial({color:'#f5f8df',emissive:'#cdd8a2',emissiveIntensity:1.6}),
  red:new THREE.MeshStandardMaterial({color:'#f44032',emissive:'#7b100a',emissiveIntensity:1})
};

const ground = new THREE.Mesh(new THREE.PlaneGeometry(500,500),mats.snow);
ground.rotation.x = -Math.PI/2;
ground.position.y = -.22;
scene.add(ground);

const road = new THREE.Mesh(new THREE.PlaneGeometry(12,400),mats.road);
road.rotation.x = -Math.PI/2;
road.position.set(0,-.16,-160);
scene.add(road);

for (const x of [-6,6]) {
  const edge = new THREE.Mesh(new THREE.BoxGeometry(.18,.22,400),mats.line);
  edge.position.set(x,-.04,-160);
  scene.add(edge);
}

const dashes = [];
for (let z=14;z>-390;z-=12) {
  for (const x of [-2,2]) {
    const dash = new THREE.Mesh(new THREE.BoxGeometry(.1,.025,5),mats.line);
    dash.position.set(x,-.035,z);
    scene.add(dash);
    dashes.push(dash);
  }
}

// Three procedural supercars: a different car is shown at each level.
const cars = [
  {name:'VORTEX GT',color:'#d6ff36',accent:'#1d2420'},
  {name:'RALLYE X',color:'#ff5b37',accent:'#f2e9d4'},
  {name:'NIGHTFALL RS',color:'#6bd8ff',accent:'#17242e'}
];
let carGroup;

function buildCar(which) {
  if (carGroup) scene.remove(carGroup);

  const cfg = cars[which];
  const paint = new THREE.MeshPhysicalMaterial({
    color:cfg.color,metalness:.72,roughness:.2,clearcoat:1,clearcoatRoughness:.12
  });
  const trim = new THREE.MeshStandardMaterial({
    color:cfg.accent,metalness:.5,roughness:.27
  });

  carGroup = new THREE.Group();
  scene.add(carGroup);
  carGroup.position.set(0,0,2.7);

  function box(w,h,d,mat,x,y,z) {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    carGroup.add(mesh);
    return mesh;
  }

  // Low chassis, pointed nose, glass cabin and aerodynamic details.
  const lower = box(1.9,.38,4.3,paint,0,.57,0);
  lower.scale.set(1,.9,1);

  const nose = new THREE.Mesh(new THREE.ConeGeometry(.99,1.85,4),paint);
  nose.rotation.x = -Math.PI/2;
  nose.rotation.z = Math.PI/4;
  nose.scale.set(1,.4,1);
  nose.position.set(0,.69,-1.12);
  nose.castShadow = true;
  carGroup.add(nose);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.44,.78,1.95),mats.glass);
  cabin.position.set(0,1.03,.14);
  cabin.rotation.x = -.1;
  cabin.scale.set(1,1,.92);
  cabin.castShadow = true;
  carGroup.add(cabin);

  box(.1,.045,1.35,trim,0,.83,-1.35);
  box(2.02,.13,.22,trim,0,.36,-2.04);
  box(1.65,.11,.25,trim,0,.43,2.02);
  box(.12,.45,.09,paint,-.82,1.15,1.65);
  box(.12,.45,.09,paint,.82,1.15,1.65);

  for (const x of [-.69,.69]) {
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(.43,.43,.32,20),mats.tire);
    wheel.rotation.z = Math.PI/2;
    wheel.position.set(x,.43,-1.27);
    wheel.castShadow = true;
    carGroup.add(wheel);

    const hub = new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,.34,12),trim);
    hub.rotation.z = Math.PI/2;
    hub.position.copy(wheel.position);
    carGroup.add(hub);

    const rear = wheel.clone();
    rear.position.z = 1.36;
    carGroup.add(rear);

    const rearHub = hub.clone();
    rearHub.position.z = 1.36;
    carGroup.add(rearHub);
  }

  for (const x of [-.63,.63]) {
    box(.4,.12,.07,mats.lamp,x,.65,-2.04);
    box(.37,.15,.07,mats.red,x,.63,2.09);
  }

  box(1.8,.07,.18,trim,0,.27,-2.11);
  box(.12,.3,.44,trim,-.88,.72,.5);
  box(.12,.3,.44,trim,.88,.72,.5);

  const shadow = new THREE.Mesh(
    new THREE.CircleGeometry(1.45,24),
    new THREE.MeshBasicMaterial({color:'#11181a',transparent:true,opacity:.48})
  );
  shadow.rotation.x = -Math.PI/2;
  shadow.scale.set(1.15,1.5,1);
  shadow.position.set(0,.03,.05);
  carGroup.add(shadow);
}

buildCar(0);

// Roadside trees and traffic recycle toward the car.
const scenery = [];

function tree(x,z,kind) {
  const group = new THREE.Group();
  group.position.set(x,0,z);

  if (kind === 'pine') {
    const trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(.1,.15,1.8,7),
      new THREE.MeshStandardMaterial({color:'#55483b'})
    );
    trunk.position.y = .9;
    group.add(trunk);

    for (let i=0;i<3;i++) {
      const crown = new THREE.Mesh(
        new THREE.ConeGeometry(1.1-i*.17,2.1,7),
        new THREE.MeshStandardMaterial({color:i===0?'#355353':'#426b68'})
      );
      crown.position.y = 1.7+i*.8;
      group.add(crown);
    }
  } else {
    const trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(.12,.22,2.3,7),
      new THREE.MeshStandardMaterial({color:'#534434'})
    );
    trunk.position.y = 1.15;
    group.add(trunk);

    const crown = new THREE.Mesh(
      new THREE.SphereGeometry(1.3,8,7),
      new THREE.MeshStandardMaterial({color:'#667c51'})
    );
    crown.position.y = 2.7;
    group.add(crown);
  }

  scene.add(group);
  scenery.push({obj:group});
}

for (let z=-14;z>-260;z-=11) {
  tree(-9-Math.random()*6,z,Math.random()<.5?'pine':'leaf');
  tree(9+Math.random()*6,z-4,Math.random()<.5?'pine':'leaf');
}

function obstacle(z,lane) {
  const group = new THREE.Group();
  group.position.set(lane*3,0,z);

  const body = new THREE.Mesh(
    new THREE.BoxGeometry(1.55,.72,2.8),
    new THREE.MeshStandardMaterial({
      color:['#d94932','#e8e5da','#20282d'][Math.floor(Math.random()*3)],
      metalness:.25,
      roughness:.4
    })
  );
  body.position.y = .63;
  group.add(body);

  const top = new THREE.Mesh(new THREE.BoxGeometry(1.18,.46,1.25),mats.glass);
  top.position.set(0,1.17,.05);
  group.add(top);

  for (const x of [-.52,.52]) {
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,.16,10),mats.tire);
    wheel.rotation.z = Math.PI/2;
    wheel.position.set(x,.35,.78);
    group.add(wheel);

    const otherWheel = wheel.clone();
    otherWheel.position.z = -.78;
    group.add(otherWheel);
  }

  scene.add(group);
  return group;
}

let obstacles = [];

function populate() {
  obstacles.forEach(object => scene.remove(object));
  obstacles = [];

  for (let i=0;i<13;i++) {
    const lane = [-1,0,1][Math.floor(Math.random()*3)];
    obstacles.push(obstacle(-34-i*28,lane));
  }
}
populate();

const biomes = [
  {sky:'#a8c7d5',ground:mats.snow,road:'#40484c',condition:'SNOW PASS · ICE'},
  {sky:'#b5a187',ground:mats.mud,road:'#493a2c',condition:'REDLINE BASIN · MUD'},
  {sky:'#8796a2',ground:mats.grass,road:'#292f34',condition:'COASTAL RUN · HIGHWAY'}
];

let running=false;
let gameOver=false;
let level=0;
let distance=0;
let score=0;
let speed=0;
let targetX=0;
let keys={};
let last=performance.now();
let biome=0;

const toast = document.querySelector('#toast');

function message(title,subtitle) {
  toast.innerHTML = `${title}<small>${subtitle}</small>`;
  toast.classList.add('show');
  setTimeout(()=>toast.classList.remove('show'),2100);
}

function setLevel(nextLevel) {
  level = nextLevel;
  buildCar(nextLevel);
  document.querySelector('#levelLabel').textContent = `LEVEL 0${nextLevel+1}`;
  document.querySelector('#carName').textContent = cars[nextLevel].name;
  message(`LEVEL 0${nextLevel+1}`,`${cars[nextLevel].name} · NEW MACHINE UNLOCKED`);
}

function crash() {
  running = false;
  gameOver = true;
  document.querySelector('.panel h1').innerHTML = 'WIPE<br><em>OUT.</em>';
  document.querySelector('.eyebrow').textContent = 'THE ROAD ALWAYS GETS ANOTHER SAY';
  document.querySelector('.panel p').textContent =
    `You covered ${Math.floor(distance)} km and scored ${score.toString().padStart(4,'0')}. The next run is yours.`;
  document.querySelector('#start').textContent = 'RUN IT BACK  ↗';
  document.querySelector('.note').textContent = 'YOUR BEST MACHINE IS WAITING';
  document.querySelector('#overlay').classList.remove('hidden');
}

function start() {
  document.querySelector('#overlay').classList.add('hidden');

  if (gameOver) {
    distance=0;
    score=0;
    level=0;
    setLevel(0);
    targetX=0;
    carGroup.position.x=0;
    populate();
    gameOver=false;
  }

  running=true;
  speed=26;
  last=performance.now();
}

document.querySelector('#start').addEventListener('click',start);

addEventListener('keydown',event=>{
  keys[event.key.toLowerCase()]=true;
  if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(event.key)) event.preventDefault();
  if (event.key==='Enter'&&!running) start();
});

addEventListener('keyup',event=>keys[event.key.toLowerCase()]=false);

function touchControl(id,key) {
  const button = document.querySelector(id);

  button.addEventListener('pointerdown',event=>{
    event.preventDefault();
    keys[key]=true;
  });

  ['pointerup','pointerleave','pointercancel'].forEach(type=>
    button.addEventListener(type,()=>keys[key]=false)
  );
}
touchControl('#left','arrowleft');
touchControl('#right','arrowright');

function setBiome(nextBiome) {
  if (nextBiome===biome) return;

  biome=nextBiome;
  const current=biomes[nextBiome];
  scene.background.set(current.sky);
  scene.fog.color.set(current.sky);
  ground.material=current.ground;
  road.material.color.set(current.road);
  document.querySelector('#condition').textContent=current.condition;

  [0,1,2].forEach(index=>
    document.querySelector('#biome'+index).classList.toggle('active',index===nextBiome)
  );
}

function frame(now) {
  requestAnimationFrame(frame);
  const dt=Math.min((now-last)/1000,.05);
  last=now;

  if (running) {
    const boost=keys.arrowup||keys.w;
    speed=THREE.MathUtils.lerp(speed,boost?46:30,dt*1.6);
    if (keys.arrowdown||keys.s) speed=THREE.MathUtils.lerp(speed,12,dt*2.5);

    const steer=(keys.arrowleft||keys.a?-1:0)+(keys.arrowright||keys.d?1:0);
    targetX=THREE.MathUtils.clamp(targetX+steer*dt*8,-4.25,4.25);
    carGroup.position.x=THREE.MathUtils.lerp(carGroup.position.x,targetX,dt*7);
    carGroup.rotation.z=THREE.MathUtils.lerp(carGroup.rotation.z,-steer*.09,dt*5);
    carGroup.position.y=.018*Math.sin(now*.02);

    distance+=speed*dt/22;
    score+=Math.floor(speed*dt*2);

    document.querySelector('#distance').textContent =
      Math.floor(distance).toString().padStart(3,'0');
    document.querySelector('#score').textContent =
      score.toString().padStart(4,'0');
    document.querySelector('#progress').style.width = `${distance%100}%`;

    const nextLevel=Math.min(2,Math.floor(distance/100));
    if (nextLevel>level) setLevel(nextLevel);

    setBiome(Math.min(2,Math.floor(distance/55)));

    obstacles.forEach(object=>{
      object.position.z+=speed*dt;

      if (object.position.z>5) {
        object.position.z=-320-Math.random()*60;
        object.position.x=[-3,0,3][Math.floor(Math.random()*3)];
        score+=100;
      }

      if (object.position.z>0&&object.position.z<3.1&&
          Math.abs(object.position.x-carGroup.position.x)<1.55) {
        crash();
      }
    });

    scenery.forEach(item=>{
      item.obj.position.z+=speed*dt*.78;
      if (item.obj.position.z>18) item.obj.position.z=-255-Math.random()*35;
    });

    dashes.forEach(dash=>{
      dash.position.z+=speed*dt;
      if (dash.position.z>20) dash.position.z=-390;
    });
  }

  camera.position.x=THREE.MathUtils.lerp(camera.position.x,carGroup.position.x*.22,.035);
  camera.lookAt(carGroup.position.x*.18,1,-7);
  renderer.render(scene,camera);
}

requestAnimationFrame(frame);

addEventListener('resize',()=>{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

@app.get("/")
def game():
    return render_template_string(PAGE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)