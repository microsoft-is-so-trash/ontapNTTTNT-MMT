/* ================= Bài tính MMT (random) ================= */
const ri = (a,b)=>a+Math.floor(Math.random()*(b-a+1));
const pick = arr=>arr[Math.floor(Math.random()*arr.length)];
const fmt = (x,d)=>{ if(!isFinite(x)) return "∞"; const v=+x.toFixed(d===undefined?4:d); return String(v).replace(".",","); };
const bin16 = n=>(n>>>0).toString(2).padStart(16,"0");
const ip2n = s=>s.split(".").reduce((a,o)=>a*256+(+o),0);
const n2ip = n=>[24,16,8,0].map(k=>Math.floor(n/2**k)%256).join(".");
const CALC = [
 {id:"tre", ch:"C1", name:"Trễ truyền & lan truyền", gen(){
   const Lb=pick([500,1000,1250,1500,2000,4000]), R=pick([1,2,5,10,100]), dkm=pick([100,500,1000,2500,4000]), s=2e8;
   const L=Lb*8, dt=L/(R*1e6)*1000, dp=dkm*1000/s*1000;
   return {de:`Gói tin dài <b>${Lb} byte</b> được gửi trên một liên kết <b>${R} Mbps</b> dài <b>${dkm} km</b>, tốc độ lan truyền 2×10<sup>8</sup> m/s. Bỏ qua trễ xử lý và hàng đợi.`,
     ans:[{k:"d_trans (ms)",v:dt},{k:"d_prop (ms)",v:dp},{k:"Tổng d_trans + d_prop (ms)",v:dt+dp}],
     sol:`L = ${Lb} × 8 = ${L} bit.<br>d<sub>trans</sub> = L/R = ${L} / ${R}×10<sup>6</sup> = <b>${fmt(dt)} ms</b>.<br>d<sub>prop</sub> = d/s = ${dkm}×10<sup>3</sup> / 2×10<sup>8</sup> = <b>${fmt(dp)} ms</b>.<br>Tổng = <b>${fmt(dt+dp)} ms</b>. (chuong 1 tr.55)`};
 }},
 {id:"thl", ch:"C1", name:"Thông lượng & nút cổ chai", gen(){
   const r=[pick([1,2,5,10,20]),pick([1,2,5,10,20,50]),pick([2,5,10,100])]; const F=pick([4,8,16,32,40]);
   const T=Math.min(...r);
   return {de:`Server gửi file <b>${F} MB</b> (1 MB = 8×10<sup>6</sup> bit) tới client qua 3 liên kết nối tiếp có tốc độ R<sub>1</sub> = ${r[0]} Mbps, R<sub>2</sub> = ${r[1]} Mbps, R<sub>3</sub> = ${r[2]} Mbps. Không có lưu lượng khác.`,
     ans:[{k:"Thông lượng (Mbps)",v:T},{k:"Thời gian truyền file (s)",v:F*8/T}],
     sol:`Thông lượng = min(R<sub>1</sub>, R<sub>2</sub>, R<sub>3</sub>) = <b>${T} Mbps</b> (nút cổ chai).<br>Thời gian ≈ F / thông lượng = ${F}×8×10<sup>6</sup> / ${T}×10<sup>6</sup> = <b>${fmt(F*8/T)} s</b>. (chuong 1 tr.58–59)`};
 }},
 {id:"http", ch:"C2", name:"Thời gian tải trang HTTP", gen(){
   const N=ri(2,12), rtt=pick([10,20,30,50,100]);
   const np=2*rtt*(N+1), p=2*rtt+N*rtt;
   return {de:`Trang web gồm 1 tệp HTML gốc tham chiếu tới <b>${N}</b> đối tượng nhỏ trên cùng server. RTT = <b>${rtt} ms</b>, bỏ qua thời gian truyền. Các đối tượng được lấy <b>tuần tự</b> (không mở kết nối song song).`,
     ans:[{k:"HTTP không liên tục (ms)",v:np},{k:"HTTP liên tục, mỗi đối tượng 1 RTT (ms)",v:p}],
     sol:`Không liên tục: mỗi đối tượng cần 2RTT (1 RTT mở TCP + 1 RTT yêu cầu/đáp ứng) → (N+1)·2RTT = ${N+1}·${2*rtt} = <b>${np} ms</b>.<br>Liên tục: 2RTT cho TCP + HTML gốc, sau đó mỗi đối tượng 1 RTT → 2·${rtt} + ${N}·${rtt} = <b>${p} ms</b>. (chuong 2 tr.25–26)`};
 }},
 {id:"p2p", ch:"C2", name:"Phân phối file client-server vs P2P", note:"Công thức theo bảng bài tính của kế hoạch (Kurose §2.5); slide chương 2 v1 không trình bày.", gen(){
   const F=pick([1,5,10,15]), us=pick([20,30,50]), dmin=pick([2,5,10]), u=pick([0.3,0.5,1,2]), N=pick([10,100,1000]);
   const Fb=F*1e3; // Gbit -> Mbit
   const dcs=Math.max(N*Fb/us, Fb/dmin), dp=Math.max(Fb/us, Fb/dmin, N*Fb/(us+N*u));
   return {de:`Phân phối file F = <b>${F} Gbit</b> tới <b>N = ${N}</b> peer. Tốc độ upload server u<sub>s</sub> = <b>${us} Mbps</b>, tốc độ download nhỏ nhất d<sub>min</sub> = <b>${dmin} Mbps</b>, mỗi peer upload u = <b>${u} Mbps</b>.`,
     ans:[{k:"D_cs tối thiểu (s)",v:dcs},{k:"D_P2P tối thiểu (s)",v:dp}],
     sol:`F = ${Fb} Mbit.<br>D<sub>cs</sub> ≥ max(NF/u<sub>s</sub>, F/d<sub>min</sub>) = max(${fmt(N*Fb/us)}, ${fmt(Fb/dmin)}) = <b>${fmt(dcs)} s</b>.<br>D<sub>P2P</sub> ≥ max(F/u<sub>s</sub>, F/d<sub>min</sub>, NF/(u<sub>s</sub> + N·u)) = max(${fmt(Fb/us)}, ${fmt(Fb/dmin)}, ${fmt(N*Fb/(us+N*u))}) = <b>${fmt(dp)} s</b>.`};
 }},
 {id:"csum", ch:"C3", name:"Checksum UDP (16 bit)", gen(){
   const a=ri(0x8000,0xffff), b=ri(0x4000,0xffff);
   const s=a+b, w=(s&0xffff)+(s>>>16), c=(~w)&0xffff;
   return {de:`Tính checksum UDP cho hai từ 16 bit:<br><code>${bin16(a)}</code><br><code>${bin16(b)}</code>`,
     ans:[{k:"Tổng sau wraparound (16 bit)",v:bin16(w),t:"bin"},{k:"Checksum",v:bin16(c),t:"bin"}],
     sol:`Cộng: ${s>0xffff?"<code>1 "+bin16(s&0xffff)+"</code> (tràn 1 bit)":"<code>"+bin16(s)+"</code> (không tràn)"}.<br>${s>0xffff?"Cộng bit tràn vào bit thấp nhất: ":"Tổng: "}<code><b>${bin16(w)}</b></code>.<br>Đảo mọi bit (bù 1): <code><b>${bin16(c)}</b></code>. (chuong 3 tr.18–19)`};
 }},
 {id:"util", ch:"C3", name:"Hiệu suất dừng-và-chờ & pipeline", gen(){
   const L=pick([1000,8000,12000]), R=pick([1e6,1e7,1e8,1e9]), rtt=pick([1,2,9,10,30]), N=pick([3,5,10]);
   const t=L/R*1000, u1=t/(rtt+t), uN=Math.min(1,N*t/(rtt+t));
   return {de:`Gói L = <b>${L} bit</b>, liên kết R = <b>${R/1e6} Mbps</b>, RTT = <b>${rtt} ms</b>. Tính độ khả dụng bên gửi U.`,
     ans:[{k:"L/R (ms)",v:t},{k:"U dừng-và-chờ",v:u1},{k:`U pipeline N = ${N}`,v:uN}],
     sol:`L/R = ${L}/${R} s = <b>${fmt(t,6)} ms</b>.<br>U = (L/R)/(RTT + L/R) = ${fmt(t,6)}/(${rtt} + ${fmt(t,6)}) = <b>${fmt(u1,6)}</b>.<br>Pipeline: U = N·(L/R)/(RTT + L/R) = <b>${fmt(uN,6)}</b>${N*t/(rtt+t)>1?" (tối đa 1)":""}. (chuong 3 tr.42–45)`};
 }},
 {id:"rtt", ch:"C3", name:"EstimatedRTT, DevRTT, Timeout", gen(){
   const e=ri(8,15)*10, d=ri(1,4)*5, smp=e+pick([-40,-20,20,30,50,80]);
   const e2=0.875*e+0.125*smp, d2=0.75*d+0.25*Math.abs(smp-e2), to=e2+4*d2;
   return {de:`EstimatedRTT = <b>${e} ms</b>, DevRTT = <b>${d} ms</b>. Đo được SampleRTT = <b>${smp} ms</b>. α = 0,125, β = 0,25. (Tính DevRTT bằng EstimatedRTT <b>vừa cập nhật</b>.)`,
     ans:[{k:"EstimatedRTT mới (ms)",v:e2},{k:"DevRTT mới (ms)",v:d2},{k:"TimeoutInterval (ms)",v:to}],
     sol:`EstimatedRTT = 0,875·${e} + 0,125·${smp} = <b>${fmt(e2)}</b>.<br>DevRTT = 0,75·${d} + 0,25·|${smp} − ${fmt(e2)}| = <b>${fmt(d2)}</b>.<br>TimeoutInterval = ${fmt(e2)} + 4·${fmt(d2)} = <b>${fmt(to)} ms</b>. (chuong 3 tr.62–63)`};
 }},
 {id:"seq", ch:"C3", name:"SEQ / ACK trong TCP", gen(){
   const s=ri(1,90)*10, a=ri(2,9)*10, b=ri(2,9)*10, c=ri(2,9)*10;
   return {de:`Host A gửi liên tiếp 3 segment cho B: segment 1 Seq = <b>${s}</b> mang <b>${a}</b> byte, segment 2 mang <b>${b}</b> byte, segment 3 mang <b>${c}</b> byte. Segment 2 bị mất; segment 1 và 3 tới B.`,
     ans:[{k:"Seq của segment 3",v:s+a+b},{k:"ACK B gửi khi nhận segment 1",v:s+a},{k:"ACK B gửi khi nhận segment 3",v:s+a},{k:"ACK sau khi segment 2 được gửi lại và tới B",v:s+a+b+c}],
     sol:`Seq = số thứ tự byte đầu tiên; ACK = byte tiếp theo mong đợi (tích luỹ).<br>Segment 2 Seq = ${s}+${a} = ${s+a}; segment 3 Seq = <b>${s+a+b}</b>.<br>Nhận segment 1 → ACK <b>${s+a}</b>. Segment 3 tới sai thứ tự → ACK trùng <b>${s+a}</b>.<br>Segment 2 lấp chỗ trống (segment 3 đã đệm) → ACK <b>${s+a+b+c}</b>. (chuong 3 tr.59, 68–70)`};
 }},
 {id:"cwnd", ch:"C3", name:"cwnd theo từng vòng (Tahoe/Reno)", gen(){
   const ss=pick([8,16]), variant=pick(["Reno","Tahoe"]), ev=pick(["3 ACK trùng","timeout"]);
   // simulate
   let cw=1, th=ss, rows=[], lossAt=null; const lossCw=ss+ri(2,4);
   for(let r=1;r<=16;r++){
     rows.push({r,cw,th});
     if(lossAt===null && cw>=lossCw){ lossAt=r; const nth=Math.floor(cw/2); th=nth; cw=(ev==="timeout"||variant==="Tahoe")?1:nth; continue; }
     if(cw<th) cw=Math.min(cw*2, th); else cw=cw+1;
   }
   const q=ri(lossAt+1, Math.min(16,lossAt+5));
   const at=rows.find(x=>x.r===q), lr=rows.find(x=>x.r===lossAt);
   return {de:`TCP <b>${variant}</b>, cwnd ban đầu 1 MSS, ssthresh ban đầu <b>${ss} MSS</b>. Không có mất mát cho tới vòng <b>${lossAt}</b> (khi cwnd = ${lr.cw} MSS) thì phát hiện <b>${ev}</b> ở cuối vòng đó. Quy ước: khởi động chậm gấp đôi mỗi vòng nhưng không vượt ssthresh; từ ssthresh trở lên tăng 1 MSS mỗi vòng.`,
     ans:[{k:"ssthresh sau sự kiện (MSS)",v:Math.floor(lr.cw/2)},{k:`cwnd ở vòng ${lossAt+1} (MSS)`,v:rows.find(x=>x.r===lossAt+1).cw},{k:`cwnd ở vòng ${q} (MSS)`,v:at.cw}],
     sol:`Diễn biến (vòng: cwnd): ${rows.map(x=>(x.r===lossAt?'<b>':'')+x.r+":"+x.cw+(x.r===lossAt?'</b>':'')).join(" · ")}.<br>Sự kiện ở cwnd = ${lr.cw} → ssthresh = ${lr.cw}/2 = <b>${Math.floor(lr.cw/2)}</b>; ${(ev==="timeout"||variant==="Tahoe")?"timeout hoặc Tahoe → cwnd = 1 MSS rồi khởi động chậm":"Reno + 3 ACK trùng → cwnd = ssthresh rồi tăng tuyến tính"}. (chuong 3 tr.99–102)`};
 }},
 {id:"subnet", ch:"C4", name:"Subnet / CIDR", gen(){
   const x=ri(20,30), base=[pick([10,172,192,200]),ri(0,255),ri(0,255),ri(0,255)];
   const n=ip2n(base.join(".")), size=2**(32-x), net=Math.floor(n/size)*size, bc=net+size-1;
   return {de:`Host có địa chỉ <b>${base.join(".")}/${x}</b>.`,
     ans:[{k:"Địa chỉ mạng",v:n2ip(net),t:"str"},{k:"Địa chỉ broadcast",v:n2ip(bc),t:"str"},{k:"Số host dùng được",v:size-2}],
     sol:`Phần host = 32 − ${x} = ${32-x} bit → khối ${size} địa chỉ.<br>Địa chỉ mạng: giữ ${x} bit đầu, bit host = 0 → <b>${n2ip(net)}</b>.<br>Broadcast: bit host = 1 → <b>${n2ip(bc)}</b>.<br>Số host = 2<sup>${32-x}</sup> − 2 = <b>${size-2}</b>. (chuong 4 tr.27)`};
 }},
 {id:"frag", ch:"C4", name:"Phân mảnh IPv4", note:"Cách tính theo giáo trình §4.3.2 (offset đơn vị 8 byte); slide chỉ nêu các trường identifier/flags/offset.", gen(){
   const tot=pick([2000,2400,3000,4000,4500,5000,6000]), mtu=pick([576,620,1000,1500]);
   const data=tot-20, per=Math.floor((mtu-20)/8)*8, k=Math.ceil(data/per), last=data-(k-1)*per;
   return {de:`Datagram IPv4 tổng chiều dài <b>${tot} byte</b> (header 20 byte, không options) đi qua liên kết có <b>MTU = ${mtu} byte</b>.`,
     ans:[{k:"Số mảnh",v:k},{k:"Số byte dữ liệu mỗi mảnh (trừ mảnh cuối)",v:per},{k:"Số byte dữ liệu mảnh cuối",v:last},{k:"Offset của mảnh cuối",v:(k-1)*per/8}],
     sol:`Dữ liệu = ${tot} − 20 = ${data} byte. Mỗi mảnh tối đa ${mtu} − 20 = ${mtu-20} byte dữ liệu, làm tròn xuống bội của 8 → <b>${per}</b>.<br>Số mảnh = ⌈${data}/${per}⌉ = <b>${k}</b>; mảnh cuối ${data} − ${k-1}·${per} = <b>${last}</b> byte.<br>Offset (đơn vị 8 byte): ${[...Array(k).keys()].map(i=>i*per/8).join(", ")} → mảnh cuối <b>${(k-1)*per/8}</b>. Cờ more-fragments = 1 trừ mảnh cuối; mọi mảnh cùng identifier.`};
 }},
 {id:"dij", ch:"C4", name:"Dijkstra (chạy bảng)", gen(){
   const nodes=["u","v","w","x","y","z"]; const E={};
   const add=(a,b,c)=>{E[a+b]=c;E[b+a]=c;};
   for(let i=1;i<nodes.length;i++){ add(nodes[i], nodes[ri(Math.max(0,i-2),i-1)], ri(1,9)); }
   let extra=ri(3,5), guard=0;
   while(extra>0 && guard++<50){ const a=pick(nodes), b=pick(nodes); if(a!==b && E[a+b]===undefined){ add(a,b,ri(1,9)); extra--; } }
   const D={}, Pp={}, Nn=["u"], steps=[]; nodes.forEach(n=>{D[n]=(n==="u")?0:(E["u"+n]!==undefined?E["u"+n]:Infinity); Pp[n]="u";});
   steps.push({N:"u",D:Object.assign({},D),P:Object.assign({},Pp)});
   while(Nn.length<nodes.length){
     let w=null; nodes.forEach(n=>{ if(!Nn.includes(n) && (w===null || D[n]<D[w])) w=n; });
     if(D[w]===Infinity) break;
     Nn.push(w);
     nodes.forEach(v=>{ if(!Nn.includes(v) && E[w+v]!==undefined && D[w]+E[w+v]<D[v]){ D[v]=D[w]+E[w+v]; Pp[v]=w; } });
     steps.push({N:Nn.join(""),D:Object.assign({},D),P:Object.assign({},Pp)});
   }
   const el=Object.keys(E).filter(k=>k[0]<k[1]).map(k=>k[0]+"–"+k[1]+" = "+E[k]).join(", ");
   const tbl='<div class="tw"><table><tr><th>Bước</th><th>N\'</th>'+nodes.slice(1).map(n=>'<th>D('+n+'),p</th>').join("")+'</tr>'+steps.map((s,i)=>'<tr><td>'+i+'</td><td>'+s.N+'</td>'+nodes.slice(1).map(n=>'<td>'+(s.N.includes(n)?"":(s.D[n]===Infinity?"∞":s.D[n]+","+s.P[n]))+'</td>').join("")+'</tr>').join("")+'</table></div>';
   const path=n=>{ let p=[n]; while(p[0]!=="u") p.unshift(Pp[p[0]]); return p.join("–"); };
   return {de:`Đồ thị vô hướng với chi phí: ${el}. Chạy Dijkstra từ <b>u</b>. Cho chi phí thấp nhất từ u tới mỗi nút.`,
     ans:nodes.slice(1).map(n=>({k:"D("+n+")",v:D[n]})),
     sol:tbl+'<p>Đường đi: '+nodes.slice(1).map(n=>n+": "+path(n)+" ("+D[n]+")").join(" · ")+'. Mỗi bước chọn nút ngoài N\' có D nhỏ nhất, rồi cập nhật D(v) = min(D(v), D(w) + c(w,v)) cho các nút kề. (chuong 4 tr.49–51)</p>'};
 }},
 {id:"bf", ch:"C4", name:"Bellman-Ford một bước", gen(){
   const nb=["v","w","x"].map(n=>({n,c:ri(1,9),d:ri(1,12)}));
   const vals=nb.map(o=>o.c+o.d), m=Math.min(...vals), hop=nb[vals.indexOf(m)].n;
   return {de:`Nút u có ba hàng xóm: ${nb.map(o=>`c(u,${o.n}) = ${o.c}`).join(", ")}. Các hàng xóm báo: ${nb.map(o=>`d<sub>${o.n}</sub>(z) = ${o.d}`).join(", ")}.`,
     ans:[{k:"d_u(z)",v:m},{k:"Hop kế tiếp (v, w hoặc x)",v:hop,t:"str"}],
     sol:`d<sub>u</sub>(z) = min{ ${nb.map(o=>o.c+"+"+o.d).join(", ")} } = min{ ${vals.join(", ")} } = <b>${m}</b>, đạt tại <b>${hop}</b>${vals.filter(v=>v===m).length>1?" (hoà — chọn tuỳ ý)":""}. (chuong 4 tr.53–54)`};
 }},
];
let CALC_CUR=null;
function renderCalc(r){
  setAcc("MMT");
  const sel = r[1] || (CALC_CUR&&CALC_CUR.id) || CALC[0].id;
  const t = CALC.find(x=>x.id===sel) || CALC[0];
  let h='<div class="kicker"><b>Mạng máy tính</b> · Luyện tay</div><h1>Bài tính MMT</h1><p class="small muted">Số liệu sinh ngẫu nhiên mỗi lần bấm “Đề mới”. Nhập đáp án (số thập phân dùng dấu phẩy hoặc chấm; sai số cho phép 1%), bấm Kiểm tra, rồi xem lời giải từng bước. Mỗi dạng mở khi chương tương ứng đã “Đã ôn xong”.</p>';
  h+='<div class="flow">'+CALC.map(c=>'<a class="chip'+(c.id===t.id?' on':'')+'" href="#/tinh/'+c.id+'">'+c.ch+' · '+esc(c.name)+(unlocked(c.ch)?'':' 🔒')+'</a>').join("")+'</div>';
  if(!unlocked(t.ch)){
    h+='<div class="card lockbox"><div class="ic">🔒</div><p>Dạng này thuộc '+t.ch+'. Ôn xong trang '+t.ch+' (bấm “Đã ôn xong”) để mở.</p><p><a class="btn pri" href="#/on/'+t.ch+'">Tới trang '+t.ch+'</a> <button class="btn" id="skipLock">Bỏ qua khóa</button></p></div>';
    $("#app").innerHTML=h; $("#skipLock").onclick=()=>{ S.skip[t.ch]=true; save(); render(); }; return;
  }
  if(!CALC_CUR || CALC_CUR.id!==t.id){ CALC_CUR={id:t.id, p:t.gen()}; }
  const p=CALC_CUR.p;
  h+='<div class="q"><div class="qh"><span>'+t.ch+' · '+esc(t.name)+'</span><span><button class="btn sm" id="newP">Đề mới ↻</button></span></div>';
  if(t.note) h+='<p class="small muted">'+esc(t.note)+'</p>';
  h+='<div class="de">'+p.de+'</div><div style="margin-top:10px">';
  p.ans.forEach((a,i)=>{ h+='<label style="display:flex;gap:10px;align-items:center;margin:6px 0;flex-wrap:wrap"><span style="min-width:220px">'+a.k+'</span><input data-i="'+i+'" style="flex:1;min-width:140px;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font-family:var(--mono)" autocomplete="off"><span class="res" data-r="'+i+'"></span></label>'; });
  h+='</div><div class="qbar"><span class="kbdhint"><kbd>Enter</kbd> để kiểm tra</span><span><button class="btn" id="showSol">Xem lời giải</button> <button class="btn pri" id="chk">Kiểm tra</button></span></div><div id="sol" class="verdict hide"><span class="vt">Lời giải</span><div class="gt">'+p.sol+'</div></div></div>';
  $("#app").innerHTML=h;
  $("#newP").onclick=()=>{ CALC_CUR={id:t.id,p:t.gen()}; renderCalc(["tinh",t.id]); };
  $("#showSol").onclick=()=>$("#sol").classList.remove("hide");
  const check=()=>{ let all=true; p.ans.forEach((a,i)=>{ const inp=$('input[data-i="'+i+'"]'); const raw=(inp.value||"").trim(); let ok=false;
      if(a.t==="bin") ok = raw.replace(/\s/g,"")===a.v;
      else if(a.t==="str") ok = raw.replace(/\s/g,"").toLowerCase()===String(a.v).toLowerCase();
      else { const x=parseFloat(raw.replace(",",".")); ok = isFinite(x) && (a.v===0 ? Math.abs(x)<1e-9 : Math.abs(x-a.v)/Math.abs(a.v) <= 0.01); }
      all = all && ok; const r=$('[data-r="'+i+'"]'); r.innerHTML = ok?'<b class="right">✓</b>':'<b class="wrongc">✗</b> <span class="small muted">'+(a.t?a.v:fmt(a.v,6))+'</span>'; });
    $("#sol").classList.remove("hide");
    S.calc = S.calc||{}; const st=S.calc[t.id]||{n:0,ok:0}; st.n++; if(all) st.ok++; S.calc[t.id]=st; save(); };
  $("#chk").onclick=check;
  $("#app").querySelectorAll("input").forEach(i=>i.addEventListener("keydown",e=>{ if(e.key==="Enter"){ e.preventDefault(); check(); } }));
}
TOOLS.tinh = renderCalc;
window.__CALC = ()=>CALC_CUR; window.__CALCLIST = CALC;
