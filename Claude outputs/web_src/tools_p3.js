/* ================= Giai đoạn 3: Flashcard · Thi thử · Sổ lỗi · Tiến độ ================= */
const DAY = 86400000;
const CARDS = D.flashcards || [];
const monName = m => m==="MMT" ? "Mạng máy tính" : "Nền tảng TTNT";
function fcState(id){ S.fc = S.fc || {}; return S.fc[id]; }
function isDue(c){ const st=fcState(c.id); return !st || st.due <= Date.now(); }
function blockSel(mon, cur, base){
  return '<div class="flow">'+BLOCKS.filter(b=>b.mon===mon && !b.soon).map(b=>'<a class="chip'+(b.id===cur?' on':'')+'" href="#/'+base+'/'+b.id+'">'+b.id+(unlocked(b.id)?'':' 🔒')+'</a>').join("")+'</div>';
}
/* ---------- Flashcard ---------- */
let FC = null;
function renderFlash(r){
  const bid = r[1] || (FC && FC.bid) || "K1";
  const b = BMAP[bid] || BMAP.K1; setAcc(b.mon);
  if(FC && FC.bid!==b.id) FC=null;
  let h='<div class="kicker"><b>Luyện nhớ</b> · lặp lại ngắt quãng</div><h1>Flashcard</h1>';
  h+='<p class="small muted">Thẻ “Chưa nhớ” quay lại sau <b>1 ngày</b> (và xem lại cuối phiên); thẻ “Nhớ rồi” lùi dần <b>3 ngày</b>, rồi <b>7 ngày</b>. Phím: <kbd>Space</kbd> lật · <kbd>1</kbd> chưa nhớ · <kbd>2</kbd> nhớ rồi.</p>';
  ["TTNT","MMT"].forEach(m=>{ h+='<div class="small" style="margin-top:6px"><b style="color:var(--'+m.toLowerCase()+')">'+monName(m)+'</b></div>'+BLOCKS.filter(x=>x.mon===m&&!x.soon).map(x=>{ const cs=CARDS.filter(c=>c.khoi===x.id); const due=cs.filter(isDue).length; return '<a class="chip'+(x.id===b.id?' on':'')+'" href="#/flash/'+x.id+'">'+x.id+(unlocked(x.id)?' · '+due+' đến hạn':' 🔒')+'</a>'; }).join(""); });
  if(!unlocked(b.id)){
    h+='<div class="card lockbox"><div class="ic">🔒</div><p>Flashcard của '+b.id+' mở khi khối này đã “Đã ôn xong”.</p><p><a class="btn pri" href="#/on/'+b.id+'">Tới trang ôn '+b.id+'</a> <button class="btn" id="skipLock">Bỏ qua khóa</button></p></div>';
    $("#app").innerHTML=h; $("#skipLock").onclick=()=>{ S.skip[b.id]=true; save(); render(); }; return;
  }
  const cs=CARDS.filter(c=>c.khoi===b.id);
  if(!FC){
    const due=cs.filter(isDue);
    h+='<div class="card"><p><b>'+b.id+'. '+esc(b.title)+'</b> · '+cs.length+' thẻ · <b>'+due.length+'</b> thẻ đến hạn.</p><div class="donebar"><button class="btn pri" id="fcDue"'+(due.length?'':' disabled')+'>Học thẻ đến hạn ('+due.length+')</button><button class="btn" id="fcAll">Ôn cấp tốc cả '+cs.length+' thẻ (không đổi lịch)</button></div></div>';
    const learned=cs.filter(c=>{const st=fcState(c.id); return st && st.box>0;}).length;
    h+='<p class="small muted">Đã nhớ (ít nhất 1 lần “Nhớ rồi”): '+learned+'/'+cs.length+'.</p>';
    $("#app").innerHTML=h;
    $("#fcDue").onclick=()=>{ FC={bid:b.id, q:shuffle(cs.filter(isDue)), i:0, flip:false, cram:false, ok:0, n:0, again:{}}; renderFlash(["flash",b.id]); };
    $("#fcAll").onclick=()=>{ FC={bid:b.id, q:shuffle(cs), i:0, flip:false, cram:true, ok:0, n:0, again:{}}; renderFlash(["flash",b.id]); };
    return;
  }
  if(FC.i>=FC.q.length){
    h+='<div class="card"><p class="big">'+FC.ok+'/'+FC.n+'</p><p>Hết phiên. '+(FC.cram?'Chế độ cấp tốc không đổi lịch ôn.':'Lịch ôn đã được cập nhật.')+'</p><div class="donebar"><button class="btn pri" id="fcBack">Về danh sách thẻ</button><a class="btn" href="#/quiz/'+b.id+'">Làm quiz '+b.id+'</a></div></div>';
    $("#app").innerHTML=h; $("#fcBack").onclick=()=>{ FC=null; renderFlash(["flash",b.id]); }; return;
  }
  const c=FC.q[FC.i];
  h+='<div class="prog"><i style="width:'+Math.round(FC.i/FC.q.length*100)+'%"></i></div><div class="small muted">Thẻ '+(FC.i+1)+'/'+FC.q.length+(FC.cram?' · cấp tốc':'')+'</div>';
  h+='<div class="card" id="fcCard" style="min-height:180px;cursor:pointer;display:flex;flex-direction:column;justify-content:center;text-align:center;font-size:19px"><div>'+c.f+'</div>'+(FC.flip?'<hr style="border:0;border-top:1px dashed var(--line);margin:14px 0"><div style="color:var(--acc);font-weight:600">'+c.b+'</div>':'<div class="small muted" style="margin-top:12px">bấm thẻ hoặc Space để lật</div>')+'</div>';
  h+='<div class="donebar" style="justify-content:center">'+(FC.flip?'<button class="btn" id="fcNo">1 · Chưa nhớ</button><button class="btn pri" id="fcYes">2 · Nhớ rồi</button>':'<button class="btn pri" id="fcFlip">Lật thẻ</button>')+'</div>';
  h+='<p class="small" style="text-align:center"><a href="javascript:void 0" id="fcStop">Dừng phiên</a></p>';
  $("#app").innerHTML=h;
  $("#fcCard").onclick=()=>{ if(!FC.flip){ FC.flip=true; renderFlash(["flash",b.id]); } };
  const fl=$("#fcFlip"); if(fl) fl.onclick=()=>{ FC.flip=true; renderFlash(["flash",b.id]); };
  const y=$("#fcYes"); if(y) y.onclick=()=>fcAnswer(true);
  const n=$("#fcNo"); if(n) n.onclick=()=>fcAnswer(false);
  $("#fcStop").onclick=()=>{ FC=null; renderFlash(["flash",b.id]); };
}
function fcAnswer(ok){
  const c=FC.q[FC.i]; FC.n++; if(ok) FC.ok++;
  if(!FC.cram && !FC.again[c.id]){
    S.fc=S.fc||{}; const st=S.fc[c.id]||{box:0,due:0};
    if(ok){ st.due = Date.now() + (st.box>=1 ? 7 : 3)*DAY; st.box = Math.min(2, st.box+1); }
    else { st.box=0; st.due=Date.now()+1*DAY; }
    S.fc[c.id]=st; save();
  }
  if(!ok && !FC.again[c.id]){ FC.again[c.id]=1; FC.q.push(c); }
  FC.i++; FC.flip=false; renderFlash(["flash",FC.bid]);
}
document.addEventListener("keydown", e=>{
  if(!FC || !$("#fcCard") || (e.target && /INPUT|TEXTAREA/.test(e.target.tagName))) return;
  if(e.key===" "||e.key==="Enter"){ e.preventDefault(); if(!FC.flip){ FC.flip=true; renderFlash(["flash",FC.bid]); } }
  else if(FC.flip && e.key==="1"){ e.preventDefault(); fcAnswer(false); }
  else if(FC.flip && e.key==="2"){ e.preventDefault(); fcAnswer(true); }
});
TOOLS.flash = renderFlash;

/* ---------- Thi thử ---------- */
let EX = null, EXT = null;
function mockUnlocked(mon){ return S.skip["THI_"+mon] || BLOCKS.filter(b=>b.mon===mon&&!b.soon).every(b=>S.quiz[b.id]); }
function renderMock(r){
  if(EXT){ clearInterval(EXT); EXT=null; }
  const mon = (r[1]==="MMT") ? "MMT" : "TTNT"; setAcc(mon);
  if(EX && EX.mon===mon && !EX.done){ renderExam(); return; }
  let h='<div class="kicker"><b>'+monName(mon)+'</b> · Thi thử</div><h1>Thi thử</h1><div class="flow"><a class="chip'+(mon==="TTNT"?' on':'')+'" href="#/thithu/TTNT">Nền tảng TTNT</a><a class="chip'+(mon==="MMT"?' on':'')+'" href="#/thithu/MMT">Mạng máy tính</a></div>';
  if(!mockUnlocked(mon)){
    const miss=BLOCKS.filter(b=>b.mon===mon&&!b.soon&&!S.quiz[b.id]).map(b=>b.id);
    h+='<div class="card lockbox"><div class="ic">🔒</div><p>Thi thử mở sau khi đã làm quiz của tất cả các khối. Còn thiếu: <b>'+miss.join(", ")+'</b>.</p><p><button class="btn" id="skipLock">Bỏ qua khóa</button></p></div>';
    $("#app").innerHTML=h; $("#skipLock").onclick=()=>{ S.skip["THI_"+mon]=true; save(); render(); }; return;
  }
  const blocks=BLOCKS.filter(b=>b.mon===mon&&!b.soon); const pool=QS.filter(q=>q.mon===mon);
  const last=(S.mock||[]).filter(x=>x.mon===mon).slice(-3).reverse();
  h+='<div class="card"><div style="display:grid;grid-template-columns:auto 1fr;gap:8px 12px;align-items:center">';
  h+='<span>Số câu</span><span><input id="exN" type="number" min="5" max="'+pool.length+'" value="'+Math.min(mon==="MMT"?40:30,pool.length)+'" style="width:90px;padding:5px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)"> / '+pool.length+'</span>';
  h+='<span>Thời gian (phút)</span><span><input id="exT" type="number" min="1" max="180" value="'+(mon==="MMT"?50:40)+'" style="width:90px;padding:5px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)"> <span class="small muted">(chưa rõ số câu/thời gian đề thật — tự chỉnh)</span></span>';
  h+='<span>Khối</span><span>'+blocks.map(b=>'<label class="chip" style="cursor:pointer"><input type="checkbox" class="exB" value="'+b.id+'" checked> '+b.id+'</label>').join("")+'</span></div>';
  if(mon==="TTNT") h+='<label class="small" style="display:flex;gap:8px;margin-top:10px"><input type="checkbox" id="exHide"'+(S.settings.hideType?' checked':'')+'> Không báo trước câu chọn nhiều (mọi câu dùng ô vuông)</label>';
  h+='<p class="small muted">Câu trộn ngẫu nhiên, chấm sau khi nộp; câu sai vào sổ lỗi. Hết giờ tự nộp.</p><div class="donebar"><button class="btn pri" id="exGo">Bắt đầu thi</button></div></div>';
  if(last.length) h+='<h2>Lần thi gần đây</h2><div class="tw"><table><tr><th>Thời điểm</th><th>Số câu</th><th>Điểm</th><th>Thời gian làm</th></tr>'+last.map(x=>'<tr><td>'+new Date(x.at).toLocaleString("vi-VN")+'</td><td>'+x.n+'</td><td><b class="'+(x.k/x.n>=.85?'right':'wrongc')+'">'+x.k+'/'+x.n+' ('+Math.round(x.k/x.n*100)+'%)</b></td><td>'+Math.round(x.sec/60)+' phút</td></tr>').join("")+'</table></div><p class="small muted">Mục tiêu trước ngày thi: thi thử từ 85% trở lên.</p>';
  $("#app").innerHTML=h;
  const hd=$("#exHide"); if(hd) hd.onchange=()=>{ S.settings.hideType=hd.checked; save(); };
  $("#exGo").onclick=()=>{
    const sel=[...document.querySelectorAll(".exB:checked")].map(x=>x.value);
    let qs=pool.filter(q=>sel.includes(q.khoi)); const n=Math.max(1,Math.min(qs.length, +$("#exN").value||20));
    // stratified: round-robin across blocks
    const byB={}; shuffle(qs).forEach(q=>{ (byB[q.khoi]=byB[q.khoi]||[]).push(q); });
    const pickd=[]; let added=true; while(pickd.length<n && added){ added=false; for(const k of sel){ if(byB[k]&&byB[k].length&&pickd.length<n){ pickd.push(byB[k].pop()); added=true; } } }
    EX={mon, items:buildItems(shuffle(pickd)), end:Date.now()+Math.max(1,+$("#exT").value||30)*60000, start:Date.now(), done:false};
    renderExam();
  };
}
function renderExam(){
  const mon=EX.mon; setAcc(mon);
  let h='<div style="position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap"><b>Thi thử '+monName(mon)+'</b><span id="exClock" class="mono" style="font-size:18px"></span><span class="small" id="exCount"></span><button class="btn pri sm" id="exSubmit">Nộp bài</button></div>';
  EX.items.forEach((it,qi)=>{
    const q=it.q, multi=isMultiUI(q);
    h+='<div class="q" id="exq'+qi+'"><div class="qh"><span>Câu '+(qi+1)+'</span><span>'+(multi?'<span class="tag multi">'+(q.loai==="multi"||!S.settings.hideType?'chọn nhiều':'ô vuông')+'</span>':'')+'</span></div><div class="de">'+q.de+'</div>'+(q.code?codeBlock(q.code,q.lang):'')+(q.hoi?'<div class="de">'+q.hoi+'</div>':'')+'<div class="opts">';
    it.order.forEach((oi,pos)=>{ h+='<button class="opt'+(multi?' multi':'')+(it.sel.includes(oi)?' sel':'')+'" data-q="'+qi+'" data-oi="'+oi+'"><span class="k">'+String.fromCharCode(97+pos)+'</span><span class="tx">'+q.dap_an[oi]+'</span></button>'; });
    h+='</div></div>';
  });
  h+='<div class="donebar"><button class="btn pri" id="exSubmit2">Nộp bài</button></div>';
  $("#app").innerHTML=h;
  $("#app").querySelectorAll(".opt").forEach(btn=>btn.onclick=()=>{ const it=EX.items[+btn.dataset.q], oi=+btn.dataset.oi; if(isMultiUI(it.q)){ const k=it.sel.indexOf(oi); if(k>=0) it.sel.splice(k,1); else it.sel.push(oi); } else it.sel=[oi];
    const card=$("#exq"+btn.dataset.q); card.querySelectorAll(".opt").forEach(b=>b.classList.toggle("sel", it.sel.includes(+b.dataset.oi))); tick(); });
  const sub=()=>{ const un=EX.items.filter(x=>!x.sel.length).length; if(un && !confirm("Còn "+un+" câu chưa trả lời. Nộp bài?")) return; submitExam(); };
  $("#exSubmit").onclick=sub; $("#exSubmit2").onclick=sub;
  const tick=()=>{ const left=Math.max(0,EX.end-Date.now()); const el=$("#exClock"); if(!el){ clearInterval(EXT); EXT=null; return; }
    el.textContent=String(Math.floor(left/60000)).padStart(2,"0")+":"+String(Math.floor(left/1000)%60).padStart(2,"0"); el.style.color = left<60000?"var(--bad)":"";
    $("#exCount").textContent="Đã làm "+EX.items.filter(x=>x.sel.length).length+"/"+EX.items.length;
    if(left<=0){ clearInterval(EXT); EXT=null; submitExam(); } };
  tick(); if(EXT) clearInterval(EXT); EXT=setInterval(tick, 1000);
  window.scrollTo(0,0);
}
function submitExam(){
  if(EXT){ clearInterval(EXT); EXT=null; }
  EX.done=true; let k=0;
  EX.items.forEach(it=>{ const a=it.sel.slice().sort().join(","), b=it.q.dung.slice().sort().join(","); it.ok = a===b; if(it.ok) k++; logResult(it.q, it.ok); });
  const n=EX.items.length, sec=Math.round((Date.now()-EX.start)/1000);
  S.mock=S.mock||[]; S.mock.push({mon:EX.mon, n, k, at:Date.now(), sec}); save(); renderSide(currentRoute());
  const byB={}; EX.items.forEach(it=>{ const t=byB[it.q.khoi]=byB[it.q.khoi]||{n:0,k:0}; t.n++; if(it.ok) t.k++; });
  let h='<div class="kicker"><b>Thi thử '+monName(EX.mon)+'</b></div><h1>Kết quả: '+k+'/'+n+' ('+Math.round(k/n*100)+'%)</h1>';
  h+='<div class="note '+(k/n>=.85?'ok':'bad')+'">'+(k/n>=.85?'Đạt mục tiêu ≥ 85%.':'Chưa đạt mục tiêu 85%: xem câu sai bên dưới và làm lại sổ lỗi.')+' Thời gian làm: '+Math.round(sec/60)+' phút.</div>';
  h+='<div class="tw"><table><tr><th>Khối</th><th>Đúng</th></tr>'+Object.keys(byB).sort().map(b=>'<tr><td>'+b+'</td><td>'+byB[b].k+'/'+byB[b].n+'</td></tr>').join("")+'</table></div>';
  h+='<h2>Chi tiết</h2>';
  EX.items.forEach((it,qi)=>{ const q=it.q;
    h+='<details'+(it.ok?'':' open')+'><summary><span class="'+(it.ok?'right':'wrongc')+'">'+(it.ok?'✓':'✗')+'</span> Câu '+(qi+1)+' · '+q.khoi+(q.demo?' · Demo Q'+q.demo:'')+'</summary><div class="de" style="margin-top:6px">'+q.de+'</div>'+(q.code?codeBlock(q.code,q.lang):'')+(q.hoi?'<div class="de">'+q.hoi+'</div>':'')+'<div class="opts">';
    it.order.forEach((oi,pos)=>{ const corr=q.dung.includes(oi), s=it.sel.includes(oi); h+='<div class="opt'+(corr?' right':(s?' wrong':''))+(corr&&!s?' miss':'')+'"><span class="k">'+String.fromCharCode(97+pos)+'</span><span class="tx">'+q.dap_an[oi]+'</span></div>'; });
    h+='</div><div class="small" style="margin-top:6px;white-space:pre-line">'+q.giai_thich+'</div><div class="src">'+esc(q.nguon||"")+(q.muc?' · <a href="#/on/'+q.khoi+'/'+q.muc+'">Ôn lại mục này →</a>':'')+'</div></details>'; });
  h+='<div class="donebar"><a class="btn pri" href="#/solo">Mở sổ lỗi</a><button class="btn" id="exAgain">Thi lại</button></div>';
  $("#app").innerHTML=h; enhance($("#app"));
  const mon=EX.mon; $("#exAgain").onclick=()=>{ EX=null; renderMock(["thithu",mon]); };
  window.scrollTo(0,0);
}
TOOLS.thithu = renderMock;

/* ---------- Sổ lỗi ---------- */
function renderErrors(r){
  setAcc("TTNT");
  const ids=Object.keys(S.errors).filter(id=>QMAP[id]);
  let h='<div class="kicker"><b>Sổ lỗi</b></div><h1>Sổ lỗi ('+ids.length+' câu)</h1><p class="small muted">Mọi câu từng làm sai (quiz, đề mẫu, thi thử). Một câu rời sổ khi trả lời đúng <b>2 lần liên tiếp</b>. Mục tiêu trước ngày thi: còn dưới 10 câu.</p>';
  if(!ids.length){ h+='<div class="card">Sổ lỗi đang trống. 🎉</div>'; $("#app").innerHTML=h; return; }
  ["TTNT","MMT"].forEach(mon=>{
    const ms=ids.filter(id=>QMAP[id].mon===mon); if(!ms.length) return;
    h+='<h2 style="color:var(--'+mon.toLowerCase()+')">'+monName(mon)+' ('+ms.length+')</h2><div class="donebar"><button class="btn pri errGo" data-mon="'+mon+'">Làm lại '+ms.length+' câu '+mon+'</button></div>';
    BLOCKS.filter(b=>b.mon===mon).forEach(b=>{
      const bs=ms.filter(id=>QMAP[id].khoi===b.id); if(!bs.length) return;
      h+='<h3>'+b.id+'. '+esc(b.title)+' · '+bs.length+' câu <button class="btn sm errGo" data-b="'+b.id+'">Làm lại khối này</button></h3>';
      bs.forEach(id=>{ const q=QMAP[id], e=S.errors[id]; const plain=(q.de+" "+(q.hoi||"")).replace(/<[^>]+>/g,""); h+='<div class="card small"><b>'+id+'</b>'+(q.demo?' · Demo Q'+q.demo:'')+' · sai '+e.wrong+' lần · đúng liên tiếp '+(e.streak||0)+'/2<div>'+esc(plain.slice(0,160))+(plain.length>160?'…':'')+'</div>'+(q.muc?'<a href="#/on/'+q.khoi+'/'+q.muc+'">Ôn lại mục này →</a>':'')+'</div>'; });
    });
  });
  $("#app").innerHTML=h;
  $("#app").querySelectorAll(".errGo").forEach(bt=>bt.onclick=()=>{
    const qs=ids.map(id=>QMAP[id]).filter(q=> bt.dataset.b ? q.khoi===bt.dataset.b : q.mon===bt.dataset.mon);
    startQuiz("ERR", qs, "Sổ lỗi"+(bt.dataset.b?" "+bt.dataset.b:" "+bt.dataset.mon), {});
  });
}
TOOLS.solo = renderErrors;

/* ---------- Tiến độ ---------- */
function renderProgress(r){
  setAcc("TTNT");
  let h='<div class="kicker"><b>Tổng quan</b></div><h1>Tiến độ</h1>';
  const errN=Object.keys(S.errors).filter(id=>QMAP[id]).length;
  ["TTNT","MMT"].forEach(mon=>{
    const bl=BLOCKS.filter(b=>b.mon===mon&&!b.soon); const done=bl.filter(b=>S.done[b.id]).length;
    const tried=bl.filter(b=>S.quiz[b.id]); const avg=tried.length?tried.reduce((a,b)=>a+S.quiz[b.id].last,0)/tried.length:0;
    const mocks=(S.mock||[]).filter(x=>x.mon===mon); const lastMock=mocks.length?mocks[mocks.length-1]:null;
    const weak=bl.slice().sort((a,b)=>{ const sa=S.quiz[a.id]?S.quiz[a.id].last:(S.done[a.id]?0:-1), sb=S.quiz[b.id]?S.quiz[b.id].last:(S.done[b.id]?0:-1); return sa-sb; })[0];
    h+='<h2 style="color:var(--'+mon.toLowerCase()+')">'+monName(mon)+'</h2><div class="grid2">';
    h+='<div class="tile"><div class="ds">Ôn xong</div><div class="big">'+done+'/'+bl.length+'</div><div class="prog"><i style="width:'+Math.round(done/bl.length*100)+'%;background:var(--'+mon.toLowerCase()+')"></i></div></div>';
    h+='<div class="tile"><div class="ds">Điểm quiz TB (lần gần nhất)</div><div class="big">'+(tried.length?Math.round(avg*100)+'%':'—')+'</div><div class="ds">'+tried.length+'/'+bl.length+' khối đã làm quiz</div></div>';
    h+='<div class="tile"><div class="ds">Thi thử gần nhất</div><div class="big">'+(lastMock?Math.round(lastMock.k/lastMock.n*100)+'%':'—')+'</div><div class="ds">mục tiêu ≥ 85%</div></div>';
    h+='<a class="tile" href="#/on/'+weak.id+'"><div class="ds">Khối cần ôn lại nhất</div><div class="big">'+weak.id+'</div><div class="ds">'+esc(weak.title)+' · '+(S.quiz[weak.id]?Math.round(S.quiz[weak.id].last*100)+'%':(S.done[weak.id]?'chưa làm quiz':'chưa ôn'))+'</div></a></div>';
    h+='<div class="tw"><table><tr><th>Khối</th><th>Ôn</th><th>Checklist</th><th>Quiz (gần nhất / tốt nhất)</th><th>Sổ lỗi</th><th>Flashcard nhớ</th></tr>';
    bl.forEach(b=>{ const ck=(S.checklist[b.id]||[]).filter(Boolean).length, ckN=(b.page.checklist||[]).length; const qz=S.quiz[b.id];
      const er=Object.keys(S.errors).filter(id=>QMAP[id]&&QMAP[id].khoi===b.id).length; const cs=CARDS.filter(c=>c.khoi===b.id); const lr=cs.filter(c=>{const st=fcState(c.id); return st&&st.box>0;}).length;
      const p=qz?Math.round(qz.last*100):null;
      h+='<tr><td><a href="#/on/'+b.id+'">'+b.id+'</a></td><td>'+(S.done[b.id]?'✓':'—')+'</td><td>'+ck+'/'+ckN+'</td><td>'+(qz?'<span class="'+(p>=80?'right':'wrongc')+'">'+p+'%</span> / '+Math.round(qz.best*100)+'% ('+qz.attempts+' lần)':'—')+'</td><td>'+(er||'')+'</td><td>'+lr+'/'+cs.length+'</td></tr>'; });
    h+='</table></div>';
  });
  h+='<h2>Sổ lỗi &amp; bài tính</h2><div class="grid2"><a class="tile" href="#/solo"><div class="ds">Câu trong sổ lỗi</div><div class="big '+(errN<10?'right':'wrongc')+'">'+errN+'</div><div class="ds">mục tiêu &lt; 10 trước ngày thi</div></a>';
  const cst=S.calc||{}; const cn=Object.values(cst).reduce((a,b)=>a+b.n,0), co=Object.values(cst).reduce((a,b)=>a+b.ok,0);
  h+='<a class="tile" href="#/tinh"><div class="ds">Bài tính MMT đã làm</div><div class="big">'+co+'/'+cn+'</div><div class="ds">số lần đúng hết / số lần kiểm tra</div></a>';
  if(S.quiz.DEMO) h+='<a class="tile" href="#/quiz/DEMO"><div class="ds">Đề mẫu Demo_MidTerm</div><div class="big">'+Math.round(S.quiz.DEMO.last*100)+'%</div><div class="ds">tốt nhất '+Math.round(S.quiz.DEMO.best*100)+'%</div></a>';
  h+='</div>';
  $("#app").innerHTML=h;
}
TOOLS.tiendo = renderProgress;
window.__P3 = {get FC(){return FC;}, get EX(){return EX;}, submitExam};
