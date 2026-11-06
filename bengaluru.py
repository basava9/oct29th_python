from flask import Flask, render_template_string

app = Flask(__name__)

# Bengaluru road-map driving prototype. Start with: python app.py
PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101513"><title>Bengaluru Drive</title>
<link href="https://unpkg.com/maplibre-gl@5.6.2/dist/maplibre-gl.css" rel="stylesheet">
<style>
*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;background:#1d2925;color:#eff5ed;font:14px Inter,system-ui,Arial,sans-serif}#map{position:absolute;inset:0}.shade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,#08120dcc,transparent 24%,transparent 65%,#07100dc9)}.top{position:absolute;z-index:3;top:0;left:0;right:0;padding:20px 28px;display:flex;align-items:center;justify-content:space-between}.brand{display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.13em}.logo{width:38px;height:38px;border:1px solid #d6f88a;border-radius:50%;display:grid;place-items:center;color:#d6f88a;font-size:20px}.brand small{display:block;color:#acb8ae;font:9px ui-monospace,monospace;letter-spacing:.15em;margin-top:4px}.open{font:10px ui-monospace,monospace;letter-spacing:.12em;color:#d5f88c}.glass{position:absolute;z-index:3;background:#0e1714d9;border:1px solid #ffffff28;border-radius:12px;backdrop-filter:blur(13px);box-shadow:0 14px 50px #0003}.left{left:24px;top:92px;width:236px;padding:17px}.kicker{color:#a9b6a9;font:9px ui-monospace,monospace;letter-spacing:.16em}.district{font-size:20px;font-weight:800;margin:8px 0 3px}.small{color:#aab7ac;font-size:11px}.weather{display:flex;gap:10px;align-items:center;padding:13px 0;border-bottom:1px solid #ffffff24;margin-bottom:9px}.weather span{font-size:24px}.weather b{font-size:13px}.weather small{display:block;color:#aab7ac;font-size:10px;margin-top:3px}.row{display:flex;justify-content:space-between;padding:7px 0;color:#c4cec5;font-size:11px}.row b{font:11px ui-monospace,monospace;color:#fff}.right{right:24px;top:92px;width:205px;padding:15px}.right h2{font-size:10px;letter-spacing:.13em;margin:0 0 10px;text-transform:uppercase}.route{width:100%;display:flex;justify-content:space-between;padding:10px;border:1px solid transparent;border-radius:8px;background:#ffffff09;color:#d6dfd7;font-size:11px;cursor:pointer;margin:5px 0;text-align:left}.route.active,.route:hover{border-color:#d6f88870;background:#d6f88814}.route small{color:#9aa89c;font:9px ui-monospace,monospace}.mapnote{position:absolute;z-index:3;top:72px;left:50%;transform:translateX(-50%);color:#eef5edaa;font:9px ui-monospace,monospace;letter-spacing:.14em;white-space:nowrap}.carview{position:absolute;z-index:2;left:50%;bottom:55px;transform:translateX(-50%);width:min(620px,80vw);height:330px;pointer-events:none}.carview canvas{width:100%;height:100%}.speed{position:absolute;z-index:3;bottom:27px;left:50%;transform:translateX(-50%);text-align:center;text-shadow:0 2px 12px #000}.speed strong{font:38px ui-monospace,monospace}.speed small{font-size:10px;color:#c6d0c6}.speed label{display:block;font:9px ui-monospace,monospace;letter-spacing:.12em;color:#aeb9ad;margin-top:2px}.help{position:absolute;z-index:3;bottom:25px;left:24px;color:#d0d9d1;font:10px ui-monospace,monospace;line-height:1.8}.help kbd{padding:2px 5px;border:1px solid #ffffff50;border-radius:4px;background:#ffffff10}.status{position:absolute;z-index:3;right:24px;bottom:25px;color:#d5f88c;font:9px ui-monospace,monospace;letter-spacing:.08em}.toast{position:absolute;z-index:5;top:75px;left:50%;transform:translate(-50%,-8px);opacity:0;transition:.2s;background:#0e1714ed;border:1px solid #d6f88880;border-radius:8px;padding:10px 14px;font-size:12px}.toast.show{opacity:1;transform:translate(-50%,0)}.touch{display:none}.warning{position:absolute;z-index:4;left:50%;top:50%;transform:translate(-50%,-50%);display:none;max-width:440px;padding:22px;border:1px solid #ffffff40;border-radius:14px;background:#101714ed;line-height:1.6}.warning.show{display:block}.warning h2{font-size:17px;margin:0 0 8px}.warning p{font-size:12px;color:#bec9bf;margin:5px 0}.warning button{margin-top:12px;border:1px solid #ffffff40;border-radius:7px;background:#ffffff12;color:#fff;padding:8px 12px;cursor:pointer}.maplibregl-ctrl-bottom-right{bottom:8px!important}.maplibregl-ctrl-attrib{font-size:9px!important;opacity:.8}
@media(max-width:720px){.top{padding:14px}.left{top:75px;left:10px;width:168px;padding:12px}.right{top:auto;right:10px;bottom:125px;width:158px;padding:10px}.district{font-size:16px}.weather{padding:8px 0}.route{padding:8px}.help{display:none}.status{right:12px;bottom:12px;font-size:8px}.carview{bottom:62px;width:94vw;height:250px}.speed{bottom:19px}.speed strong{font-size:30px}.mapnote{top:59px}.touch{display:grid;position:absolute;z-index:5;left:12px;bottom:18px;grid-template-columns:43px 43px 43px;grid-template-rows:40px 40px;gap:5px}.touch button{border:1px solid #ffffff50;border-radius:8px;background:#0e1714c9;color:#fff;font-size:16px;touch-action:none}.touch .up{grid-column:2}.touch .down{grid-column:2;grid-row:2}}
</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/"}}</script>
</head>
<body>
<div id="map"></div><div class="shade"></div>
<header class="top"><div class="brand"><div class="logo">↗</div><div>BENGALURU DRIVE<small>OPEN CITY · KARNATAKA, INDIA</small></div></div><div class="open">● OPENSTREETMAP CITY DATA</div></header>
<div class="mapnote" id="mapnote">CHURCH STREET · BENGALURU</div>
<aside class="glass left"><div class="kicker">LIVE LOCATION</div><div class="district" id="district">Church Street</div><div class="small">Central Bengaluru · Karnataka</div><div class="weather"><span>🌧</span><div><b>Monsoon showers</b><small>24°C · wet roads</small></div></div><div class="row"><span>Speed</span><b><span id="speed">0</span> km/h</b></div><div class="row"><span>Distance driven</span><b id="distance">0.00 km</b></div><div class="row"><span>Road surface</span><b>City streets</b></div></aside>
<aside class="glass right"><h2>Drive to an area</h2><button class="route active" data-name="Church Street" data-lat="12.9756" data-lng="77.6050"><span>Church Street</span><small>CENTRAL</small></button><button class="route" data-name="MG Road" data-lat="12.9752" data-lng="77.6068"><span>MG Road</span><small>CBD</small></button><button class="route" data-name="Cubbon Park" data-lat="12.9763" data-lng="77.5929"><span>Cubbon Park</span><small>PARK</small></button><button class="route" data-name="Outer Ring Road" data-lat="12.9592" data-lng="77.6974"><span>Outer Ring Road</span><small>HIGHWAY</small></button></aside>
<section class="carview"><canvas id="carCanvas"></canvas></section><div class="speed"><strong id="speedBig">0</strong> <small>km/h</small><label>SUPERCAR · THIRD-PERSON DRIVE</label></div>
<div class="help"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> DRIVE · <kbd>SPACE</kbd> BRAKE<br>Mouse: orbit map · R: reset car</div><div class="status">REAL MAP ROADS · MAP DATA © OPENSTREETMAP</div>
<div class="touch"><button class="up" style="grid-column:2;width:43px;height:40px;padding:0" data-key="w">▲</button><button class="leftkey" style="grid-column:1;grid-row:2;width:43px;height:40px;padding:0" data-key="a">◀</button><button class="down" style="grid-column:2;grid-row:2;width:43px;height:40px;padding:0" data-key="s">▼</button><button class="rightkey" style="grid-column:3;grid-row:2;width:43px;height:40px;padding:0" data-key="d">▶</button></div><div class="toast" id="toast"></div>
<div class="warning" id="carWarning"><h2>3D car model did not load</h2><p>The Bengaluru map is still live. Check your internet connection to load the CC0 sports-car asset.</p><button onclick="this.parentElement.classList.remove('show')">Continue</button></div>
<script src="https://unpkg.com/maplibre-gl@5.6.2/dist/maplibre-gl.js"></script>
<script type="module">
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const start={lat:12.9756,lng:77.6050};
const map=new maplibregl.Map({container:'map',style:'https://tiles.openfreemap.org/styles/liberty',center:[start.lng,start.lat],zoom:16.7,pitch:64,bearing:0,antialias:true,attributionControl:true,cooperativeGestures:true});
map.addControl(new maplibregl.NavigationControl({showCompass:false}), 'bottom-right');
let lat=start.lat,lng=start.lng,heading=0,velocity=0,distance=0,steer=0,last=performance.now();
const keys={};const mPerLat=111320;
function toast(msg){const t=document.querySelector('#toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)}
function reset(){lat=start.lat;lng=start.lng;heading=0;velocity=0;distance=0;toast('Back to Church Street')}
window.addEventListener('keydown',e=>{keys[e.key.toLowerCase()]=true;if(e.code==='Space')keys.brake=true;if(e.key.toLowerCase()==='r')reset()});
window.addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false;if(e.code==='Space')keys.brake=false});
document.querySelectorAll('.touch button').forEach(b=>{const k=b.dataset.key;b.onpointerdown=e=>{e.preventDefault();keys[k]=true};b.onpointerup=b.onpointerleave=()=>keys[k]=false});
document.querySelectorAll('.route').forEach(b=>b.onclick=()=>{lat=Number(b.dataset.lat);lng=Number(b.dataset.lng);velocity=0;heading=0;document.querySelector('#district').textContent=b.dataset.name;document.querySelector('#mapnote').textContent=b.dataset.name.toUpperCase()+' · BENGALURU';document.querySelectorAll('.route').forEach(x=>x.classList.toggle('active',x===b));map.easeTo({center:[lng,lat],zoom:16.7,pitch:64,bearing:0,duration:1800});toast('Driving to '+b.dataset.name)});
map.on('load',()=>{
 map.setLight({anchor:'viewport',color:'#fff2d9',intensity:.48});
 // Some OpenFreeMap styles already include 3D buildings. Add the layer only if needed.
 const style=map.getStyle(), buildingSource=(style.layers||[]).find(l=>l['source-layer']==='building');
 const already3d=(style.layers||[]).some(l=>l.type==='fill-extrusion'&&l['source-layer']==='building');
 if(buildingSource&&!already3d){map.addLayer({id:'bengaluru-osm-3d-buildings',type:'fill-extrusion',source:buildingSource.source,'source-layer':'building',minzoom:14,paint:{'fill-extrusion-color':['interpolate',['linear'],['coalesce',['get','render_height'],['get','height'],8],0,'#a7a69b',25,'#878c84',80,'#747d78'],'fill-extrusion-height':['coalesce',['get','render_height'],['get','height'],8],'fill-extrusion-base':['coalesce',['get','render_min_height'],['get','min_height'],0],'fill-extrusion-opacity':.94}},buildingSource.id)}
 toast('Real Bengaluru streets loaded');
});

// Detailed game-ready sports car model, displayed in the chase-camera foreground.
const canvas=document.querySelector('#carCanvas');
const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(canvas.clientWidth,canvas.clientHeight,false);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
const scene=new THREE.Scene();
scene.add(new THREE.HemisphereLight(0xe6f3f1,0x28302b,2.2));
const keyLight=new THREE.DirectionalLight(0xffe7c2,3.4);keyLight.position.set(-4,8,5);scene.add(keyLight);
const fill=new THREE.DirectionalLight(0x83b5ce,1.3);fill.position.set(5,3,-5);scene.add(fill);
const camera=new THREE.PerspectiveCamera(34,1,.1,100);camera.position.set(5.2,3.1,7.8);camera.lookAt(0,.65,0);
let player=null;
const loader=new GLTFLoader();
loader.load('https://raw.githubusercontent.com/JaronKBragg7337/spectral-gt-rs/main/spectral_gt_rs_game_ready.glb',
 gltf=>{player=gltf.scene;player.scale.setScalar(.95);player.rotation.y=Math.PI/2;player.position.y=.04;scene.add(player)},
 undefined,
 ()=>document.querySelector('#carWarning').classList.add('show')
);
function resize(){const w=canvas.clientWidth,h=canvas.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()}
new ResizeObserver(resize).observe(canvas);

function frame(now){
 requestAnimationFrame(frame);
 const dt=Math.min((now-last)/1000,.04);last=now;
 const forward=keys.w||keys.arrowup,back=keys.s||keys.arrowdown;
 const left=keys.a||keys.arrowleft,right=keys.d||keys.arrowright;
 if(forward)velocity=Math.min(velocity+28*dt,25);
 else if(back)velocity=Math.max(velocity-36*dt,-8);
 else velocity*=keys.brake?.84:.992;
 if(left)steer=Math.min(steer+2.2*dt,.9);
 else if(right)steer=Math.max(steer-2.2*dt,-.9);
 else steer*=.88;
 heading+=steer*(velocity/12)*dt;
 const meters=velocity*dt;
 lat+=Math.cos(heading)*meters/mPerLat;
 lng+=Math.sin(heading)*meters/(mPerLat*Math.cos(lat*Math.PI/180));
 distance+=Math.abs(meters)/1000;
 document.querySelector('#speed').textContent=Math.round(Math.abs(velocity)*3.6);
 document.querySelector('#speedBig').textContent=Math.round(Math.abs(velocity)*3.6);
 document.querySelector('#distance').textContent=distance.toFixed(2)+' km';
 if(Math.abs(meters)>.002)map.jumpTo({center:[lng,lat],bearing:heading*180/Math.PI,pitch:64,zoom:17});
 if(player){player.rotation.y=Math.PI/2-heading;player.position.y=.04+Math.sin(now*.012)*Math.min(Math.abs(velocity)*.002,.025)}
 renderer.render(scene,camera);
}
requestAnimationFrame(frame);
</script>
</body></html>'''


@app.get('/')
def home():
    return render_template_string(PAGE)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)