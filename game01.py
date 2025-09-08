import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mouse Dodge Hell Mode", layout="wide")
st.title("💀 滑鼠閃避 - 彈幕地獄版")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { margin:0; overflow:hidden; background:#000; }
  #game { position:relative; width:100vw; height:80vh; background:#111; overflow:hidden; }
  #player {
    position:absolute; width:25px; height:25px; text-align:center; line-height:25px;
    font-size:1.3rem; user-select:none;
  }
  .obstacle {
    position:absolute; width:60px; height:60px; text-align:center; line-height:60px;
    font-size:2.2rem;
  }
  #score {
    position:absolute; top:10px; left:10px; color:white; font-size:1.2rem;
  }
  #game-over {
    display:none; position:absolute; top:40%; left:50%; transform:translate(-50%,-50%);
    background:rgba(255,255,255,0.9); padding:20px 40px; border-radius:12px; text-align:center;
  }
</style>
</head>
<body>
<div id="game">
  <div id="player">🟢</div>
  <div id="score">Score: 0</div>
  <div id="game-over">
    Game Over!<br>
    Score: <span id="final-score"></span><br>
    <button onclick="location.reload()">Restart</button>
  </div>
</div>

<script>
const game=document.getElementById("game");
const player=document.getElementById("player");
const scoreEl=document.getElementById("score");
const go=document.getElementById("game-over");
const fs=document.getElementById("final-score");

let score=0, run=true, difficulty=5;

// 滑鼠控制
game.addEventListener("mousemove",e=>{
  const rect=game.getBoundingClientRect();
  let x=e.clientX-rect.left-12;
  let y=e.clientY-rect.top-12;
  player.style.left=x+"px";
  player.style.top=y+"px";
});

// 生成障礙物
function spawnObstacle(){
  if(!run) return;

  // 一次生成 3~6 個
  let count = 3 + Math.floor(Math.random()*4) + Math.floor(difficulty/5);
  for(let i=0;i<count;i++){
    const o=document.createElement("div");
    o.className="obstacle";
    o.textContent="⬛";

    const side=Math.floor(Math.random()*4);
    let x,y,vx,vy;
    const w=game.clientWidth, h=game.clientHeight;
    const baseSpeed=4+difficulty*1.0; // 更快初速

    if(side===0){ x=Math.random()*w; y=-70; vx=(Math.random()-0.5)*6; vy=baseSpeed+Math.random()*4; }
    else if(side===1){ x=Math.random()*w; y=h+70; vx=(Math.random()-0.5)*6; vy=-(baseSpeed+Math.random()*4); }
    else if(side===2){ x=-70; y=Math.random()*h; vx=baseSpeed+Math.random()*4; vy=(Math.random()-0.5)*6; }
    else { x=w+70; y=Math.random()*h; vx=-(baseSpeed+Math.random()*4); vy=(Math.random()-0.5)*6; }

    game.appendChild(o);

    let interval=setInterval(()=>{
      if(!run){clearInterval(interval); return;}
      x+=vx; y+=vy;
      o.style.left=x+"px"; o.style.top=y+"px";

      const p=player.getBoundingClientRect(), ob=o.getBoundingClientRect();
      if(!(p.right<ob.left||p.left>ob.right||p.bottom<ob.top||p.top>ob.bottom)){
        gameOver();
        clearInterval(interval);
      }

      if(x<-120||x>w+120||y<-120||y>h+120){
        o.remove();
        clearInterval(interval);
      }
    },16);
  }

  setTimeout(spawnObstacle, 200+Math.random()*300); // 幾乎每 0.2s 就出現
}

// 分數 & 難度
setInterval(()=>{
  if(run){ 
    score++; 
    scoreEl.textContent="Score: "+score;
    if(score%10===0) difficulty+=2; // 每 10 秒，難度爆升
  }
},1000);

// 遊戲結束
function gameOver(){
  run=false;
  fs.textContent=score;
  go.style.display="block";
}

spawnObstacle();
</script>
</body>
</html>
"""

components.html(game_html, height=500, scrolling=False)
