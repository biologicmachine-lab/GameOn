const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");

const pieces = {
  r:"♜", n:"♞", b:"♝", q:"♛", k:"♚", p:"♟",
  R:"♖", N:"♘", B:"♗", Q:"♕", K:"♔", P:"♙"
};

let board, selected, turn, mode, difficulty;

const initialBoard = [
  "rnbqkbnr",
  "pppppppp",
  "........",
  "........",
  "........",
  "........",
  "PPPPPPPP",
  "RNBQKBNR"
];

function resetGame() {
  board = initialBoard.map(r => r.split(""));
  selected = null;
  turn = "white";
  draw();
  statusEl.textContent = "White to move";
}

function draw() {
  boardEl.innerHTML = "";
  board.forEach((row,y)=>{
    row.forEach((cell,x)=>{
      const sq = document.createElement("div");
      sq.className = `square ${(x+y)%2?"dark":"light"}`;
      sq.dataset.x=x; sq.dataset.y=y;
      if(cell!==".") sq.textContent = pieces[cell];
      sq.onclick = ()=>clickSquare(x,y);
      boardEl.appendChild(sq);
    });
  });
}

function clickSquare(x,y){
  const piece = board[y][x];
  if(selected){
    move(selected.x,selected.y,x,y);
    selected=null;
    draw();
    if(mode==="ai" && turn==="black"){
      setTimeout(aiMove,300);
    }
  } else if(piece!=="." && isOwn(piece)){
    selected={x,y};
  }
}

function isOwn(p){
  return turn==="white" ? p===p.toUpperCase() : p===p.toLowerCase();
}

function move(x1,y1,x2,y2){
  const p = board[y1][x1];
  board[y1][x1]=".";
  board[y2][x2]=p;
  turn = turn==="white"?"black":"white";
  statusEl.textContent = `${turn[0].toUpperCase()+turn.slice(1)} to move`;
}

function aiMove(){
  let best = minimax(board,difficulty,true)[1];
  if(best){
    move(best.x1,best.y1,best.x2,best.y2);
    draw();
  }
}

function minimax(b,depth,max){
  if(depth===0) return [evaluate(b),null];
  let best = max?-Infinity:Infinity;
  let bestMove=null;

  for(let y=0;y<8;y++){
    for(let x=0;x<8;x++){
      let p=b[y][x];
      if(p==="."|| (max && p!==p.toLowerCase()) || (!max && p!==p.toUpperCase())) continue;
      for(let ty=0;ty<8;ty++){
        for(let tx=0;tx<8;tx++){
          let copy=b.map(r=>r.slice());
          copy[y][x]=".";
          copy[ty][tx]=p;
          let score=minimax(copy,depth-1,!max)[0];
          if(max && score>best){best=score;bestMove={x1:x,y1:y,x2:tx,y2:ty};}
          if(!max && score<best){best=score;bestMove={x1:x,y1:y,x2:tx,y2:ty};}
        }
      }
    }
  }
  return [best,bestMove];
}

function evaluate(b){
  const values={p:1,n:3,b:3,r:5,q:9,k:100};
  let score=0;
  b.flat().forEach(p=>{
    if(p!=="."){
      let v=values[p.toLowerCase()];
      score+=p===p.toLowerCase()?v:-v;
    }
  });
  return score;
}

document.getElementById("reset").onclick=resetGame;
document.getElementById("mode").onchange=e=>mode=e.target.value;
document.getElementById("difficulty").onchange=e=>difficulty=parseInt(e.target.value);

mode="2p";
difficulty=1;
resetGame();
