const $=id=>document.getElementById(id);
const fmtPT=d=>d.toLocaleString('en-US',{timeZone:'America/Los_Angeles',dateStyle:'medium',timeStyle:'short'})+' PT';
function ago(ms){const s=ms/1e3,m=s/60,h=m/60,d=h/24;
 if(d>=1)return `${Math.floor(d)}d ${Math.floor(h%24)}h ago`;if(h>=1)return `${Math.floor(h)}h ${Math.floor(m%60)}m ago`;return `${Math.max(1,Math.floor(m))}m ago`;}
fetch('data/resets.json').then(r=>r.json()).then(({resets,generated_utc})=>{
 const L=resets[0],t=new Date(L.utc);
 const tick=()=>{const ms=Date.now()-t;$('ago').textContent=ago(ms);$('days').textContent=(ms/864e5).toFixed(1)};tick();setInterval(tick,30000);
 $('when').textContent=fmtPT(t)+' · '+t.toISOString().slice(0,16).replace('T',' ')+' UTC';
 $('quote').textContent='“'+L.quote+'” — @thsottiaux';$('postlink').href=L.url;
 $('share').href='https://x.com/intent/post?text='+encodeURIComponent(`Last global Codex usage reset: ${ago(Date.now()-t)}. Track them all:`)+'&url='+encodeURIComponent(location.href);
 $('count').textContent=resets.length;
 const ts=resets.map(r=>+new Date(r.utc));$('gap').textContent=ts.length>1?((ts[0]-ts.at(-1))/864e5/(ts.length-1)).toFixed(1):'–';
 $('timeline').innerHTML=resets.map(r=>`<li><time>${fmtPT(new Date(r.utc))}</time><span class="tag ${r.status=='announced'?'ann':''}">${r.status}</span>
 <p>${r.announcement&&r.announcement.root_text?r.announcement.root_text+' — ':''}${r.quote.replace(/[<>&]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}</p><a href="${r.url}" target="_blank" rel="noopener">Source post ↗</a></li>`).join('');
 $('updated').textContent='Data updated '+fmtPT(new Date(generated_utc));
}).catch(()=>{$('ago').textContent='Data unavailable'});
function pace(){const p=+$('pct').value,h=+$('hrs').value;
 $('paceout').innerHTML=(p>=0&&h>0)?`Budget about <b>${(p/h).toFixed(2)}% per hour</b> (${(p/h*24).toFixed(1)}%/day) to last until your reset.`:'Enter valid numbers.';}
$('pct').oninput=$('hrs').oninput=pace;pace();
