from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RIDE / THREE — Superbike Run</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:#111;color:#f5f3ed;font-family:Arial,sans-serif}
#game{position:fixed;inset:0}
canvas{display:block}
.hud{position:fixed;inset:0;pointer-events:none;padding:24px 4vw;display:flex;justify-content:space-between;text-transform:uppercase;letter-spacing:.14em;text-shadow:0 2px 8px #000}
.brand{font-weight:900;font-size:18px}
.brand span,.accent{color:#c9f45b}
.stage{text-align:right;font-size:12px;line-height:1.8}
.title{position:absolute;left:5vw;top:19%;font-size:clamp(42px,8vw,88px);font-weight:900;line-height:.86;letter-spacing:-.05em}
#headline{transition:opacity .45s ease,visibility .45s ease}
body.playing #headline,#headline.headline-hidden{opacity:0;visibility:hidden;display:none}
.title small{font-size:12px;letter-spacing:.22em;color:#c9f45b;display:block;margin-bottom:16px}
.stats{position:absolute;left:5vw;bottom:105px;display:flex;gap:30px;font-size:10px}
.stats b{font-size:25px;display:block;margin-top:5px;letter-spacing:0}
.help{position:absolute;right:5vw;bottom:112px;text-align:right;font-size:11px;line-height:1.8}
.bar{position:absolute;bottom:0;left:0;right:0;height:68px;padding:0 4vw;background:#080b0bd9;border-top:1px solid #ffffff35;display:flex;align-items:center;justify-content:space-between;pointer-events:auto}
.bar button,.modal button{background:#c9f45b;border:0;padding:13px 22px;font-weight:bold;text-transform:uppercase;letter-spacing:.12em;cursor:pointer}
.overlay{position:fixed;inset:0;background:#080b0bc9;display:grid;place-items:center;z-index:3}
.overlay.hide{display:none}
.modal{width:min(500px,90vw);padding:38px;text-align:center;background:#121816;border:1px solid #ffffff45}
.modal h1{font-size:clamp(42px,9vw,70px);line-height:.9;margin:12px 0}
.modal p{color:#c4c9bf;line-height:1.7;font-size:14px}
.modal .eyebrow{color:#c9f45b;font-size:11px;letter-spacing:.2em}
.progress{position:absolute;top:0;left:0;height:4px;background:#c9f45b;width:0}
.touch{display:none;position:fixed;bottom:80px;left:50%;transform:translateX(-50%);gap:10px;pointer-events:auto}
.touch button{width:54px;height:48px;background:#111c;color:white;border:1px solid #fff8;border-radius:8px}
@media(max-width:650px){
  .hud{padding:16px}
  .title{left:18px;top:17%;font-size:56px}
  .stats{left:18px;bottom:86px;gap:14px}
  .stats b{font-size:20px}
  .help{display:none}
  .bar{height:60px;padding:0 16px;font-size:10px}
  .touch{display:flex}
}
</style>

<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js"}}
</script>
</head>
<body>
<div id="game"></div>
<div class="progress" id="progress"></div>

<div class="hud">
  <div class="brand">RIDE<span> / THREE</span></div>
  <div class="stage">
    <span id="level">LEVEL 01 / 03</span><br>
    <b id="bikeName">FROSTBITE 900</b>
  </div>
  <div class="title">
    <small id="environment">SNOW HIGHWAY</small>
    <span id="headline">FULL<br>THROTTLE</span>
  </div>
  <div class="stats">
    <div>DISTANCE<b><span id="distance">0</span><small> m</small></b></div>
    <div>SCORE<b id="score">0</b></div>
    <div>SPEED<b><span id="speed">0</span><small> km/h</small></b></div>
  </div>
  <div class="help">
    A / D or ← / → STEER<br>
    W / ↑ ACCELERATE · S / ↓ BRAKE
  </div>
</div>

<div class="touch">
  <button data-k="left">◀</button>
  <button data-k="up">▲</button>
  <button data-k="right">▶</button>
</div>

<div class="bar">
  <div>THREE ROADS. THREE SUPERBIKES.</div>
  <button id="pause">PAUSE</button>
</div>

<div class="overlay" id="overlay">
  <section class="modal">
    <div class="eyebrow">ARCADE SUPERBIKE RUN</div>
    <h1 id="modalTitle">RIDE<br>THE <span class="accent">EDGE</span></h1>
    <p id="modalCopy">
      Race three changing environments. Avoid traffic and unlock a faster
      superbike at every level. Reach each finish line to complete the run.
    </p>
    <button id="go">START RIDE</button>
    <p style="font-size:11px">
      Use WASD or arrow keys. On mobile, use the on-screen controls.
    </p>
  </section>
</div>

<script type="module">
import * as THREE from 'three';
import { GLTFLoader } from
  'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js';

const host=document.querySelector('#game');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0xaed2e3);
scene.fog=new THREE.Fog(0xaed2e3,35,145);

const camera=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,.1,220);
camera.position.set(0,5.4,10);
camera.lookAt(0,1,-5);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.1;
host.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xeaf6ff,0x47504a,2.1));
const sun=new THREE.DirectionalLight(0xffedce,3);
sun.position.set(-8,15,8);
sun.castShadow=true;
scene.add(sun);

const levels=[
  {
    env:'SNOW HIGHWAY',
    name:'FROSTBITE 900',
    color:0x76eaff,
    sky:0xaed2e3,
    ground:0xe7eef0,
    road:0x343b40,
    length:1000,
    bikeModel:'/static/models/bike-rider-level-1.glb'
  },
  {
    env:'GHAT ROAD',
    name:'VIPER X-12',
    color:0xff7048,
    sky:0x9dc8ba,
    ground:0x506653,
    road:0x303535,
    length:1500,
    bikeModel:'/static/models/bike-rider-level-2.glb'
  },
  {
    env:'SCENIC COAST HIGHWAY',
    name:'APEX RR TURBO',
    color:0xc9f45b,
    sky:0x77c3dc,
    ground:0x698c58,
    road:0x343b40,
    length:2000,
    bikeModel:'/static/models/bike-rider-level-3.glb'
  }
];

let level=0;
let playing=false;
let dist=0;
let score=0;
let speed=0;
let lane=0;
let targetLane=0;
let last=performance.now();
let spawn=0;
let objects=[];
let roadBits=[];
let bike;

const mat=(color,roughness=.7,metalness=0)=>
  new THREE.MeshStandardMaterial({color,roughness,metalness});

const bikeMat=mat(levels[0].color,.3,.5);
const dark=mat(0x15191b,.35,.6);
const rubber=mat(0x101214,.9);
const chrome=mat(0xb8c2c4,.25,.8);

const loader=new GLTFLoader();
let carModel=null;

loader.load(
  '/static/models/traffic-car.glb',
  gltf=>{carModel=gltf.scene},
  undefined,
  ()=>{}
);

function cylinder(parent,r1,r2,length,x,y,z,material,rotZ=0) {
  const mesh=new THREE.Mesh(
    new THREE.CylinderGeometry(r1,r2,length,16),
    material
  );
  mesh.rotation.z=rotZ;
  mesh.position.set(x,y,z);
  mesh.castShadow=true;
  parent.add(mesh);
  return mesh;
}

function makeBike() {
  const group=new THREE.Group();

  for (const z of [-.78,.75]) {
    const wheel=new THREE.Mesh(
      new THREE.TorusGeometry(.43,.09,10,20),
      rubber
    );
    wheel.rotation.y=Math.PI/2;
    wheel.position.set(0,.5,z);
    wheel.castShadow=true;
    group.add(wheel);
    cylinder(group,.07,.07,.17,0,.5,z,chrome,Math.PI/2);
  }

  const frame=cylinder(group,.12,.13,1.2,0,.92,0,dark);
  frame.rotation.x=Math.PI/2;

  const tank=new THREE.Mesh(
    new THREE.SphereGeometry(.38,20,12),
    bikeMat
  );
  tank.scale.set(.78,.65,1.3);
  tank.position.set(0,1.23,-.18);
  group.add(tank);

  const nose=new THREE.Mesh(new THREE.BoxGeometry(.62,.56,.55),bikeMat);
  nose.position.set(0,1.16,-.79);
  group.add(nose);

  const lamp=new THREE.Mesh(
    new THREE.SphereGeometry(.16,16,12),
    new THREE.MeshBasicMaterial({color:0xfff3c1})
  );
  lamp.position.set(0,1.25,-1.07);
  group.add(lamp);

  const seat=new THREE.Mesh(new THREE.BoxGeometry(.42,.13,.7),dark);
  seat.position.set(0,1.48,.38);
  group.add(seat);

  const rider=new THREE.Mesh(
    new THREE.CapsuleGeometry(.19,.52,5,10),
    mat(0x252b30)
  );
  rider.position.set(0,1.82,.14);
  rider.rotation.x=.78;
  group.add(rider);

  const helmet=new THREE.Mesh(
    new THREE.SphereGeometry(.24,16,12),
    mat(0x222b30,.25,.4)
  );
  helmet.position.set(0,2.17,-.06);
  group.add(helmet);

  const visor=new THREE.Mesh(
    new THREE.BoxGeometry(.3,.11,.08),
    mat(0x71dbea,.2,.4)
  );
  visor.position.set(0,2.17,-.25);
  group.add(visor);

  cylinder(group,.045,.045,.95,0,1.58,-.75,chrome,Math.PI/2);
  return group;
}

bike=makeBike();
bike.position.set(0,0,2.8);
scene.add(bike);

let activeBikeLevel=-1;
let bikeRequest=0;

function fitAsset(root,targetLength,targetHeight) {
  root.rotation.y=0;

  let bounds=new THREE.Box3().setFromObject(root);
  const size=bounds.getSize(new THREE.Vector3());

  const factor=Math.min(
    targetLength/Math.max(size.x,size.z),
    targetHeight/Math.max(size.y,.001)
  );

  root.scale.setScalar(factor);
  root.updateMatrixWorld(true);

  bounds.setFromObject(root);
  const center=bounds.getCenter(new THREE.Vector3());

  root.position.x-=center.x;
  root.position.y-=bounds.min.y;
  root.position.z-=center.z;

  root.traverse(object=>{
    if (object.isMesh) {
      object.castShadow=true;
      object.receiveShadow=true;
    }
  });

  return root;
}

function loadBikeForLevel() {
  const request=++bikeRequest;
  activeBikeLevel=level;

  const placeholder=makeBike();
  placeholder.position.set(lane,0,2.8);
  scene.remove(bike);
  bike=placeholder;
  scene.add(bike);

  loader.load(
    levels[level].bikeModel,
    gltf=>{
      if (request!==bikeRequest) return;

      const model=fitAsset(gltf.scene,2.3,2.4);
      model.position.set(lane,0,2.8);
      scene.remove(bike);
      bike=model;
      scene.add(bike);
    },
    undefined,
    ()=>{
      // Keep the built-in bike if the Blender GLB is not present.
    }
  );
}

function clearWorld() {
  for (const object of objects) {
    scene.remove(object);
    object.traverse?.(mesh=>mesh.geometry?.dispose());
  }
  objects=[];

  for (const dash of roadBits) scene.remove(dash);
  roadBits=[];
}

function addTree(x,z,scale=1) {
  const group=new THREE.Group();

  const trunk=new THREE.Mesh(
    new THREE.CylinderGeometry(.12*scale,.2*scale,1.7*scale,7),
    mat(0x564839)
  );
  trunk.position.y=.85*scale;
  group.add(trunk);

  for (let j=0;j<3;j++) {
    const tree=new THREE.Mesh(
      new THREE.ConeGeometry((1.05-j*.2)*scale,1.6*scale,7),
      mat(level===0 ? 0x607878 : 0x315343)
    );
    tree.position.y=(1.8+j*.58)*scale;
    group.add(tree);
  }

  group.position.set(x,0,z);
  scene.add(group);
  objects.push(group);
}

function setup() {
  clearWorld();

  const stage=levels[level];
  bikeMat.color.setHex(stage.color);
  if (activeBikeLevel!==level) loadBikeForLevel();

  scene.background.setHex(stage.sky);
  scene.fog.color.setHex(stage.sky);

  const floor=new THREE.Mesh(
    new THREE.PlaneGeometry(180,260),
    mat(stage.ground)
  );
  floor.rotation.x=-Math.PI/2;
  floor.position.set(0,-.08,-90);
  scene.add(floor);
  objects.push(floor);

  const road=new THREE.Mesh(
    new THREE.PlaneGeometry(12,260),
    mat(stage.road,.95)
  );
  road.rotation.x=-Math.PI/2;
  road.position.set(0,0,-90);
  scene.add(road);
  objects.push(road);

  for (const side of [-1,1]) {
    const rail=new THREE.Mesh(
      new THREE.BoxGeometry(.16,.6,260),
      mat(level===0 ? 0xe5eff2 : 0x8b9691,.4,.5)
    );
    rail.position.set(side*6,.35,-90);
    scene.add(rail);
    objects.push(rail);
  }

  for (let i=0;i<24;i++) {
    const dash=new THREE.Mesh(
      new THREE.BoxGeometry(.12,.035,2.5),
      mat(0xf3f0dc)
    );
    dash.position.set(0,.025,-i*10);
    scene.add(dash);
    roadBits.push(dash);
  }

  for (let i=0;i<32;i++) {
    const z=-i*8-4;
    addTree((level===1 ? 9 : 11)+Math.random()*5,z);
    addTree(-(level===1 ? 9 : 11)-Math.random()*5,z-3);
  }

  if (level===1) {
    for (let i=0;i<13;i++) {
      const rock=new THREE.Mesh(
        new THREE.DodecahedronGeometry(1+Math.random()*2,0),
        mat(0x697366)
      );
      rock.position.set((i%2 ? 1 : -1)*(9+Math.random()*4),1,-i*13);
      scene.add(rock);
      objects.push(rock);
    }
  }
}

function obstacle() {
  let car;

  if (carModel) {
    car=fitAsset(carModel.clone(),4.2,2.2);
  } else {
    car=new THREE.Group();

    const body=new THREE.Mesh(
      new THREE.BoxGeometry(1.3,.65,2.2),
      mat([0xc54e39,0x485a70,0xe0c34d][Math.floor(Math.random()*3)],.35,.4)
    );
    body.position.y=.75;
    car.add(body);

    const cabin=new THREE.Mesh(
      new THREE.BoxGeometry(.95,.55,.9),
      mat(0x9ccbd0,.2,.35)
    );
    cabin.position.set(0,1.3,-.1);
    car.add(cabin);

    for (const x of [-.51,.51]) {
      for (const z of [-.68,.68]) {
        const wheel=new THREE.Mesh(
          new THREE.CylinderGeometry(.19,.19,.12,12),
          rubber
        );
        wheel.rotation.z=Math.PI/2;
        wheel.position.set(x,.38,z);
        car.add(wheel);
      }
    }
  }

  car.position.set([-3,0,3][Math.floor(Math.random()*3)],0,-75);
  car.userData.car=true;
  scene.add(car);
  objects.push(car);
}

function hud() {
  document.querySelector('#level').textContent =
    `LEVEL ${String(level+1).padStart(2,'0')} / 03 · ${levels[level].length} M`;
  document.querySelector('#bikeName').textContent=levels[level].name;
  document.querySelector('#environment').textContent=levels[level].env;
  document.querySelector('#distance').textContent=Math.floor(dist);
  document.querySelector('#score').textContent=score;
  document.querySelector('#speed').textContent=Math.floor(speed);
  document.querySelector('#progress').style.width =
    Math.min(100,dist/levels[level].length*100)+'%';
}

function begin() {
  document.querySelector('#overlay').classList.add('hide');

  const headline=document.querySelector('#headline');
  headline.classList.add('headline-hidden');
  headline.style.display='none';

  document.body.classList.add('playing');
  playing=true;
  last=performance.now();
}

function endRun(win) {
  playing=false;
  document.body.classList.remove('playing');

  const headline=document.querySelector('#headline');
  headline.classList.remove('headline-hidden');
  headline.style.display='';

  document.querySelector('#modalTitle').innerHTML=win
    ? 'RUN<br><span class="accent">COMPLETE</span>'
    : 'CRASH<br><span class="accent">RUN OVER</span>';

  document.querySelector('#modalCopy').textContent=win
    ? `All three superbikes unlocked. Final score: ${score}.`
    : `You crashed at ${Math.floor(dist)} m in level ${level+1}. Score: ${score}.`;

  document.querySelector('#go').textContent='RIDE AGAIN';
  document.querySelector('#overlay').classList.remove('hide');

  document.querySelector('#go').onclick=()=>{
    level=0;
    dist=0;
    score=0;
    speed=0;
    lane=0;
    targetLane=0;
    spawn=0;
    setup();
    hud();
    begin();
  };
}

document.querySelector('#go').onclick=begin;

document.querySelector('#pause').onclick=()=>{
  if (playing) {
    playing=false;
    document.body.classList.remove('playing');

    const headline=document.querySelector('#headline');
    headline.classList.remove('headline-hidden');
    headline.style.display='';

    document.querySelector('#modalTitle').textContent='PAUSED';
    document.querySelector('#modalCopy').textContent=
      'Take a breather. Your run is ready when you are.';
    document.querySelector('#go').textContent='RESUME';
    document.querySelector('#overlay').classList.remove('hide');

    document.querySelector('#go').onclick=()=>{
      document.querySelector('#overlay').classList.add('hide');
      document.body.classList.add('playing');
      headline.classList.add('headline-hidden');
      headline.style.display='none';
      playing=true;
      last=performance.now();
    };
  } else {
    begin();
  }
};

const keys={};

addEventListener('keydown',event=>{
  keys[event.key.toLowerCase()]=true;
  if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(event.key)) {
    event.preventDefault();
  }
});

addEventListener('keyup',event=>keys[event.key.toLowerCase()]=false);

document.querySelectorAll('.touch button').forEach(button=>{
  const key=button.dataset.k;

  button.onpointerdown=event=>{
    event.preventDefault();
    keys[key]=true;
  };

  button.onpointerup=button.onpointerleave=()=>keys[key]=false;
});

function frame(now) {
  requestAnimationFrame(frame);
  const dt=Math.min((now-last)/1000,.04);
  last=now;

  if (playing) {
    const accelerating=keys.w||keys.arrowup||keys.up;
    const braking=keys.s||keys.arrowdown;

    speed=THREE.MathUtils.clamp(
      speed+(accelerating ? 30 : -10)*dt-(braking ? 45*dt : 0),
      0,
      level===0 ? 150 : level===1 ? 190 : 235
    );

    if (keys.a||keys.arrowleft||keys.left) targetLane-=dt*5;
    if (keys.d||keys.arrowright||keys.right) targetLane+=dt*5;

    targetLane=THREE.MathUtils.clamp(targetLane,-4.4,4.4);
    lane=THREE.MathUtils.damp(lane,targetLane,6,dt);

    bike.position.x=lane;
    bike.rotation.z=-(targetLane-lane)*.08;
    bike.rotation.x=.015*Math.sin(now/90);

    const travel=speed*dt*.12;
    dist+=travel;
    score+=Math.floor(travel*2);
    spawn+=dt;

    if (spawn>Math.max(.7,1.9-speed/150)) {
      spawn=0;
      obstacle();
    }

    for (const dash of roadBits) {
      dash.position.z+=travel*3;
      if (dash.position.z>5) dash.position.z-=240;
    }

    for (const object of objects) {
      if (object.userData.car) {
        object.position.z+=travel*3;

        if (Math.abs(object.position.z-bike.position.z)<2.1 &&
            Math.abs(object.position.x-lane)<1.45) {
          endRun(false);
          break;
        } else if (object.position.z>5) {
          score+=100;
          object.position.z=-110-Math.random()*40;
        }
      } else if (Math.abs(object.position.x)>8) {
        object.position.z+=travel*3;
        if (object.position.z>8) object.position.z-=256;
      }
    }

    if (playing && dist>=levels[level].length) {
      dist=0;
      level++;

      if (level>=3) {
        endRun(true);
      } else {
        speed=Math.max(80,speed);
        setup();

        document.querySelector('#modalTitle').innerHTML=
          'LEVEL COMPLETE<br><span class="accent">BIKE UPGRADED</span>';
        document.querySelector('#modalCopy').textContent=
          `Finish line crossed! Level ${level+1} is ${levels[level].env} (${levels[level].length} m). Your upgraded ${levels[level].name} is ready.`;
        document.querySelector('#go').textContent='CONTINUE';
        document.querySelector('#go').onclick=begin;
        playing=false;
        document.body.classList.remove('playing');
        document.querySelector('#overlay').classList.remove('hide');
      }
    }

    camera.position.x=THREE.MathUtils.damp(camera.position.x,lane*.32,3,dt);
    camera.lookAt(lane*.3,1,-5);
    hud();
  }

  renderer.render(scene,camera);
}

setup();
requestAnimationFrame(frame);

addEventListener('resize',()=>{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>'''


@app.get('/')
def home():
    return render_template_string(PAGE)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)