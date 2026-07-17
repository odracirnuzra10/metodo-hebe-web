/* ═══════════════════ ACTIVACIÓN · tabla 957 ═══════════════════
   Panel de activación de clientes nuevos (Vortex/Atlas/Summit).
   /onboarding sigue intacto para los 52 legacy de la tabla 327.

   Los 17 checks automáticos, las 4 etapas, 🚦 Estado, Progreso y SLA son campos
   FÓRMULA en Baserow → read-only por construcción. El humano no edita el check;
   edita los CRUDOS de los que depende (cantidades) desde el drawer de etapa, y
   adjunta foto/video como evidencia. Cuando exista ACT-3, el job pisa los crudos.
   ═════════════════════════════════════════════════════════════ */
const ACT_STAGES=[
  {f:'Etapa 1 · Conexión',  label:'Conexión',   checks:['C1 · Datos base','C2 · WhatsApp','C3 · Sucursales','C4 · Horarios','C5 · Usuarios y permisos']},
  {f:'Etapa 2 · Migración', label:'Migración',  checks:['M1 · Profesionales','M2 · Tratamientos','M3 · Pacientes','M4 · Citas futuras','M5 · Ficha y consentimientos']},
  {f:'Etapa 3 · Activación',label:'Activación', checks:['A1 · Agente texto','A2 · Agente voz · CAMILA','A3 · Plantillas','A4 · Automatizaciones','A5 · Difusiones','A6 · Embed','A7 · Cobros y pagos']},
  {f:'Etapa 4 · Entrega',   label:'Entrega',    checks:['E1 · Check','E2 · Check','E3 · Check']}
];
const ACT_DENOM=['Sucursales declaradas','Profesionales declarados','Tratamientos declarados','Pacientes declarados'];
const ACT_PLANS={Vortex:{price:279,impl:450,credits:'28.000',camila:false,users:10,sedes:1},
                 Atlas:{price:379,impl:450,credits:'37.000',camila:true,users:15,sedes:2},
                 Summit:{price:479,impl:450,credits:'46.000',camila:true,users:25,sedes:'∞'}};

/* qué crudos alimentan cada check, para el drawer de etapa.
   t: num | tri | text · denom: campo declarado para mostrar X/Y */
const ACT_CHECK_INPUTS={
 'C1 · Datos base':{rule:'slug · logo · color · timezone == país · moneda == país',fields:[
   {f:'Logo cargado',t:'tri'},{f:'Color personalizado',t:'tri'},{f:'Timezone consistente',t:'tri'},{f:'Moneda consistente',t:'tri'},{f:'Timezone leída',t:'text'}]},
 'C2 · WhatsApp':{rule:'WhatsApp status == CONNECTED',fields:[
   {f:'WhatsApp status',t:'text',hint:'CONNECTED'},{f:'WhatsApp número',t:'text'}]},
 'C3 · Sucursales':{rule:'cargadas >= declaradas',fields:[{f:'Sucursales cargadas',t:'num',denom:'Sucursales declaradas'}]},
 'C4 · Horarios':{rule:'toda sucursal con horario',fields:[{f:'Sucursales con horarios',t:'num',denom:'Sucursales cargadas'}]},
 'C5 · Usuarios y permisos':{rule:'>=2 usuarios con rol',fields:[{f:'Usuarios con rol',t:'num',need:'>=2'},{f:'Usuarios cargados',t:'num'}]},
 'M1 · Profesionales':{rule:'activos >= declarados',fields:[{f:'Profesionales activos',t:'num',denom:'Profesionales declarados'},{f:'Profesionales cargados',t:'num'}]},
 'M2 · Tratamientos':{rule:'cargados >= declarados · todos con precio Y duración',fields:[
   {f:'Tratamientos cargados',t:'num',denom:'Tratamientos declarados'},{f:'Tratamientos con precio',t:'num'},{f:'Tratamientos con duración',t:'num'}]},
 'M3 · Pacientes':{rule:'cargados >= declarados × 0.95',fields:[{f:'Pacientes cargados',t:'num',denom:'Pacientes declarados'}]},
 'M4 · Citas futuras':{rule:'citas del sistema anterior trasladadas ( > 0 )',fields:[{f:'Citas futuras',t:'num',need:'>0'}]},
 'M5 · Ficha y consentimientos':{rule:'plantilla de ficha + consentimiento',fields:[{f:'Ficha plantilla configurada',t:'tri'},{f:'Consentimiento cargado',t:'tri'}]},
 'A1 · Agente texto':{rule:'activo · 3/3 bloques · modo · mensaje de respaldo',fields:[
   {f:'Agente texto activo',t:'tri'},{f:'Agente texto bloques',t:'num',need:'=3'},{f:'Agente texto modo',t:'text'},{f:'Agente texto respaldo',t:'text'}]},
 'A2 · Agente voz · CAMILA':{rule:'solo Atlas/Summit — N/A en Vortex',fields:[{f:'CAMILA disponible',t:'tri'},{f:'CAMILA activa',t:'tri'}]},
 'A3 · Plantillas':{rule:'>=3 aprobadas por Meta',fields:[{f:'Plantillas aprobadas Meta',t:'num',need:'>=3'},{f:'Plantillas cargadas',t:'num'}]},
 'A4 · Automatizaciones':{key:true,rule:'>=2 activas · enviados>0 · error<5% — CLAVE: "activa" no es "funcionando"',fields:[
   {f:'Automatizaciones activas',t:'num',need:'>=2'},{f:'Enviados 24h',t:'num'},{f:'Errores 24h',t:'num'}]},
 'A5 · Difusiones':{rule:'>=1 audiencia · >=1 enviada',fields:[{f:'Difusiones audiencias',t:'num',need:'>=1'},{f:'Difusiones enviadas',t:'num',need:'>=1'},{f:'Difusiones 30d',t:'num'}]},
 'A6 · Embed':{rule:'hits_30d > 0',fields:[{f:'Embed hits 30d',t:'num',need:'>0'}]},
 'A7 · Cobros y pagos':{rule:'medio de pago configurado',fields:[{f:'Cobros medio configurado',t:'tri'}]}
};
const ACT_HARD_LOCK=['📅 Entrega formal','Última sync','Precio plan USD','Implementación USD','Créditos/mes','Stripe Subscription ID'];

const actV=(r,f)=>{const v=r[f];return (v&&typeof v==='object'&&v.value!=null)?v.value:(v==null?'':v);};
const actNum=(r,f)=>{const v=r[f];return (v===''||v==null)?null:Number(v);};
const actStageDone=(r,s)=>actV(r,s.f)==='✅ Completada';
const actEntregado=r=>!!actV(r,'📅 Entrega formal');
const actSinDenom=r=>ACT_DENOM.some(f=>actNum(r,f)===null);
const actRegresion=r=>actEntregado(r)&&actV(r,'🚦 Estado')!=='✅ ENTREGADO';
const actEsperaMitzi=r=>actV(r,'AHA detectado')==='✅ Detectado'&&actV(r,'E3 · Verificación Mitzi')!=='✅ Conforme';
const actVencido=r=>!actEntregado(r)&&actV(r,'SLA')==='🔴 Vencido';
/* A4 CLAVE: automatización activa pero fallando (>5% error en 24h) */
const actA4Falla=r=>{const en=actNum(r,'Enviados 24h'),er=actNum(r,'Errores 24h');return en!=null&&er!=null&&en>0&&(er/en)>=0.05;};
function actStageIdx(r){for(let i=0;i<ACT_STAGES.length;i++)if(!actStageDone(r,ACT_STAGES[i]))return i;return 4;}
/* Mitzi solo puede aprobar si el sistema detectó el dato duro (spec: no verifica un AHA
   que el sistema no detectó), las 3 etapas automáticas están completas y E1 tiene grabación. */
function actMitziBloqueo(r){const falta=[];
  if(!actStageDone(r,ACT_STAGES[0])||!actStageDone(r,ACT_STAGES[1])||!actStageDone(r,ACT_STAGES[2]))falta.push('faltan checks de etapas 1-3');
  if(actNum(r,'ok_E1')!==1)falta.push('E1 sin completar o sin grabación');
  if(actV(r,'AHA detectado')!=='✅ Detectado')falta.push('el sistema no detectó cita creada por IA (AHA)');
  return falta;}
function actDaysSince(iso){if(!iso)return null;const d=new Date(iso+'T00:00:00');const now=new Date();return Math.floor((now-d)/864e5);}

const GACT=makeGrid({self:'GACT',px:'act',tid:957,el:'mod-act',title:'Activación',noRowOps:true,
  orderBy:'Fecha Ingreso (D0)',sort:'-Fecha Ingreso (D0)',dateField:'Fecha Ingreso (D0)',group:'',
  order:['Name','Slug Clinera','Nombre cliente','Cliente activo','Plan','Plan · detalle','🚦 Estado','Progreso','SLA',
         'Etapa 1 · Conexión','Etapa 2 · Migración','Etapa 3 · Activación','Etapa 4 · Entrega',
         'Encargado','País','Fecha Ingreso (D0)','📅 Entrega formal','Días desde D0','D+60 adopción',
         ...ACT_DENOM,'Denominadores congelados',
         'E1 · Capacitación','E1 · Grabación','E2 · Video ¡Eureka!','E3 · Verificación Mitzi','Nota Mitzi',
         'AHA detectado','AHA verificado Mitzi','Citas por IA (total)','Fecha primera cita IA',
         'Gate tramo 2','Gate tramo 3','Tramo 1 · Venta US$30','Tramo 2 · Config US$40','Tramo 3 · Adopción US$50','Comisión total US$',
         'Última sync'],
  search:['Name','Slug Clinera','Nombre cliente'],
  subtitle:['Plan · detalle'],
  kpis:()=>[]
});

/* Candado: los crudos del job son read-only en el drawer genérico. La entrada manual
   va SOLO por el drawer de etapa (setRaw). `📅 Entrega formal` no se escribe ni por ahí. */
const ACT_JOB_FIELDS=['Logo cargado','Color personalizado','Timezone consistente','Moneda consistente','Timezone leída',
 'WhatsApp status','WhatsApp número','Sucursales cargadas','Sucursales con horarios','Usuarios cargados','Usuarios con rol',
 'Profesionales cargados','Profesionales activos','Tratamientos cargados','Tratamientos con precio','Tratamientos con duración',
 'Pacientes cargados','Citas futuras','Ficha plantilla configurada','Consentimiento cargado',
 'Agente texto activo','Agente texto bloques','Agente texto modo','Agente texto respaldo','CAMILA disponible','CAMILA activa',
 'Plantillas cargadas','Plantillas aprobadas Meta','Automatizaciones activas','Enviados 24h','Errores 24h',
 'Difusiones audiencias','Difusiones enviadas','Difusiones 30d','Embed hits 30d','Cobros medio configurado',
 'Citas por IA (total)','Citas IA últimas 4 sem','Fecha primera cita IA','Uso IA 30d US$',
 '📅 Entrega formal','Última sync','Denominadores congelados',
 'C1 📸','C2 📸','C3 📸','C4 📸','C5 📸','M1 📸','M2 📸','M3 📸','M4 📸','M5 📸',
 'A1 📸','A2 📸','A3 📸','A4 📸','A5 📸','A6 📸','A7 📸'];
const GACT_REFRESH=GACT.refreshSchema;
GACT.refreshSchema=async function(){
  const okS=await GACT_REFRESH.call(this);
  if(okS&&this.SCHEMA)this.SCHEMA.forEach(f=>{if(ACT_JOB_FIELDS.includes(f.name))f.ro=true;});
  this.buildCols();
  return okS;
};

const GACT_TABLE_RENDER=GACT.render;
GACT._view=localStorage.getItem('work.act.view')||'pipeline';
GACT._filt=null;
GACT.setView=function(v){this._view=v;localStorage.setItem('work.act.view',v);this.render();};
GACT.setFilt=function(f){this._filt=(this._filt===f?null:f)||null;this.render();};
GACT.actTag=function(){const el=document.getElementById('actTotales');
  if(el&&!el.dataset.esp){el.dataset.esp='1';
    el.insertAdjacentHTML('afterend',' <span class="mono text-[11px]" title="Etapas, 🚦 Estado, progreso y los 17 checks automáticos son fórmula: los calcula el sistema. Se editan los crudos desde el drawer de cada etapa." style="color:#8A8984">· etapas derivadas</span>');}};
GACT.ensureViewToggle=function(){
  if(!document.getElementById('actViewSeg')){
    const q=document.getElementById('actQ');if(!q)return;
    const seg=document.createElement('div');seg.id='actViewSeg';
    seg.className='inline-flex items-center rounded-lg border overflow-hidden mr-1';seg.style.borderColor='var(--line)';
    seg.innerHTML=`<button id="actViewPipe" onclick="GACT.setView('pipeline')" class="px-3 py-1.5 text-sm font-medium">Pipeline</button>`
      +`<button id="actViewTab" onclick="GACT.setView('tabla')" class="px-3 py-1.5 text-sm font-medium">Tabla</button>`;
    q.parentNode.insertBefore(seg,q);}
  const p=document.getElementById('actViewPipe'),t=document.getElementById('actViewTab');if(!p||!t)return;
  const on='background:#141413;color:#fff',off='background:#fff;color:var(--sub)';
  p.style.cssText=this._view==='pipeline'?on:off;
  t.style.cssText=this._view==='tabla'?on:off;
};

/* ── entrada manual sancionada de un crudo (drawer de etapa) ── */
GACT.setRaw=async function(id,field,val){
  if(ACT_HARD_LOCK.includes(field)){toast('Campo bloqueado — no se edita a mano');return;}
  try{
    const body={};body[field]=val;
    const upd=await api('/api/database/rows/table/957/'+id+'/?user_field_names=true',{method:'PATCH',body:JSON.stringify(body)});
    const i=this.DATA.findIndex(x=>x.id===id);if(i>=0)this.DATA[i]=upd;if(this.sel&&this.sel.id===id)this.sel=upd;
    this.render();
    if(this._stageOpen&&this._stageOpen.id===id)this.openStage(id,this._stageOpen.idx);
  }catch(e){toast('Error: '+e.message);}
};
GACT.stageFile=function(id,chk,idx){const inp=document.createElement('input');inp.type='file';inp.accept='image/*,video/*';
  inp.onchange=async()=>{const file=inp.files&&inp.files[0];if(!file)return;toast('Subiendo…');
    try{const up=await brUpload(file);const r=this.DATA.find(x=>x.id===id);const F=chk+' 📸';const cur=Array.isArray(r&&r[F])?r[F]:[];
      const upd=await api('/api/database/rows/table/957/'+id+'/?user_field_names=true',{method:'PATCH',body:JSON.stringify({[F]:[...cur.map(x=>({name:x.name})),{name:up.name}]})});
      const i=this.DATA.findIndex(x=>x.id===id);if(i>=0)this.DATA[i]=upd;this.sel=upd;this.render();this.openStage(id,idx);toast('Evidencia subida');
    }catch(e){toast('Error: '+e.message);}};
  inp.click();};
GACT.stageFileDel=async function(id,chk,fi,idx){const r=this.DATA.find(x=>x.id===id);if(!r)return;const F=chk+' 📸';
  const nx=(Array.isArray(r[F])?r[F]:[]).filter((_,i)=>i!==fi).map(x=>({name:x.name}));
  try{const upd=await api('/api/database/rows/table/957/'+id+'/?user_field_names=true',{method:'PATCH',body:JSON.stringify({[F]:nx})});
    const i=this.DATA.findIndex(x=>x.id===id);if(i>=0)this.DATA[i]=upd;this.sel=upd;this.render();this.openStage(id,idx);}catch(e){toast('Error: '+e.message);}};

/* ══════════ DRAWER DE ETAPA (clic en la flecha) ══════════ */
GACT.openStage=function(id,idx){const r=this.DATA.find(x=>x.id===id);if(!r)return;this.sel=r;this._stageOpen={id,idx};
  const st=ACT_STAGES[idx];
  const pill=v=>{const c=(v==='✅ Listo'||v==='✅ Completada'||v==='✅ Detectado')?['#DFF2E4','#116329']:v==='🚫 N/A'?['#EFEEEA','#8A8984']:['#FDF2E9','#9A5B1E'];
    return `<span class="badge" style="background:${c[0]};color:${c[1]}">${esc(v||'—')}</span>`;};
  const shots=(chk)=>{const short=chk.split(' ·')[0];const F=short+' 📸';const fa=Array.isArray(r[F])?r[F]:[];
    const thumbs=fa.map((x,i)=>`<span class="actshot">${x.is_image&&x.thumbnails&&x.thumbnails.small?`<a href="${esc(x.url)}" target="_blank"><img src="${esc(x.thumbnails.small.url)}" class="w-9 h-9 rounded object-cover border" style="border-color:var(--line)"></a>`:`<a href="${esc(x.url)}" target="_blank" class="badge" style="background:#F3F4F6;color:#374151">🎞 ${esc((x.visible_name||'archivo').slice(0,12))}</a>`}<span class="actshotdel" onclick="GACT.stageFileDel(${id},'${short}',${i},${idx})">✕</span></span>`).join('');
    return `<div class="actshots">${thumbs}<button class="actshotbtn" onclick="GACT.stageFile(${id},'${short}',${idx})">📎 Foto/video</button></div>`;};

  let body='';
  if(idx<3){
    body=st.checks.map(chk=>{const st2=actV(r,chk);const cfg=ACT_CHECK_INPUTS[chk]||{fields:[]};
      const inputs=cfg.fields.map(fd=>{const cur=r[fd.f];
        if(fd.t==='tri'){const cv=actV(r,fd.f);
          const b=(lbl,val)=>`<button class="actseg3 ${cv===val||(val===''&&!cv)?'on':''}" onclick="GACT.setRaw(${id},'${esc(fd.f)}',${val===''?'null':`'${val}'`})">${lbl}</button>`;
          return `<div class="actfield"><label>${esc(fd.f)}</label><div class="inline-flex rounded-lg border overflow-hidden" style="border-color:var(--line)">${b('—','')}${b('✅ Sí','✅ Sí')}${b('❌ No','❌ No')}</div></div>`;}
        if(fd.t==='num'){const dv=fd.denom?actNum(r,fd.denom):null;
          return `<div class="actfield"><label>${esc(fd.f)}${fd.need?` <span style="color:#8A8984">(${fd.need})</span>`:''}${fd.denom?` <span style="color:#8A8984">/ ${dv==null?'sin declarar':dv.toLocaleString('es')} declarados</span>`:''}</label>`
            +`<input type="number" value="${cur==null?'':esc(cur)}" class="actinp" onchange="GACT.setRaw(${id},'${esc(fd.f)}',this.value===''?null:Number(this.value))"></div>`;}
        return `<div class="actfield"><label>${esc(fd.f)}${fd.hint?` <span style="color:#8A8984">(esperado: ${fd.hint})</span>`:''}</label>`
          +`<input type="text" value="${esc(cur==null?'':cur)}" class="actinp" onchange="GACT.setRaw(${id},'${esc(fd.f)}',this.value===''?null:this.value)"></div>`;}).join('');
      let extra='';
      if(chk.indexOf('A4')===0){const en=actNum(r,'Enviados 24h'),er=actNum(r,'Errores 24h');
        if(en!=null&&er!=null&&en>0){const p=er/en*100;const bad=p>=5;
          extra=`<div class="acterr ${bad?'bad':'ok'}">Tasa de error 24h: <b>${p.toFixed(1)}%</b> (${er}/${en}) — máx 5%${bad?' · ⚠️ el cliente pierde citas y no lo sabe':''}</div>`;}
        else extra=`<div class="acterr na">Sin datos de envíos aún — hay que testear que las automatizaciones lleguen sin errores.</div>`;}
      return `<div class="actcard ${cfg.key?'actcard-key':''}"><div class="actcard-h"><b>${esc(chk)}</b><span class="flex items-center gap-1.5">${cfg.key?'<span class="actclave">⚠️ CLAVE</span>':''}${pill(st2)}</span></div>
        <div class="actrule">${esc(cfg.rule||'')}</div>${extra}${inputs}${shots(chk)}</div>`;}).join('');
  }else{
    const capOpts=['🕐 Pendiente','📅 Agendada','✅ Completada'];const capCur=actV(r,'E1 · Capacitación');
    const fileBlock=(F,lbl)=>{const fa=Array.isArray(r[F])?r[F]:[];
      const thumbs=fa.map((x,i)=>`<span class="actshot">${x.is_image&&x.thumbnails&&x.thumbnails.small?`<a href="${esc(x.url)}" target="_blank"><img src="${esc(x.thumbnails.small.url)}" class="w-9 h-9 rounded object-cover border" style="border-color:var(--line)"></a>`:`<a href="${esc(x.url)}" target="_blank" class="badge" style="background:#F3F4F6;color:#374151">🎞 ${esc((x.visible_name||'archivo').slice(0,14))}</a>`}<span class="actshotdel" onclick="GACT.fileDel(${id},'${esc(F)}',${i});setTimeout(()=>GACT.openStage(${id},3),500)">✕</span></span>`).join('');
      return `<div class="actshots">${thumbs}<button class="actshotbtn" onclick="GACT.fileAdd(${id},'${esc(F)}')">📎 Subir ${lbl}</button></div>`;};
    const bloqueo=actMitziBloqueo(r);
    body=`
     <div class="actcard"><div class="actcard-h"><b>E1 · Capacitación por rol</b>${pill(capCur)}</div>
       <div class="actrule">dueño · administración · recepción — grabación obligatoria</div>
       <div class="actfield"><label>Estado de la capacitación</label>
         <div class="inline-flex rounded-lg border overflow-hidden" style="border-color:var(--line)">${capOpts.map(o=>`<button class="actseg3 ${capCur===o?'on':''}" onclick="GACT.setRaw(${id},'E1 · Capacitación','${o}')">${o}</button>`).join('')}</div></div>
       <div class="actfield"><label>Grabación (obligatoria)</label>${fileBlock('E1 · Grabación','grabación')}</div></div>
     <div class="actcard"><div class="actcard-h"><b>E2 · Video ¡Eureka!</b>${pill(actNum(r,'ok_E2')===1?'✅ Listo':'⏳ Pendiente')}</div>
       <div class="actrule">link/archivo del cliente contando qué le cambió</div>${fileBlock('E2 · Video ¡Eureka!','video')}</div>
     <div class="actcard"><div class="actcard-h"><b>AHA — cita creada por la IA</b>${pill(actV(r,'AHA detectado'))}</div>
       <div class="actrule">dato duro: al menos 1 cita creada por la IA a un paciente real</div>
       <div class="actfield"><label>Citas por IA (total)</label><input type="number" value="${actNum(r,'Citas por IA (total)')??''}" class="actinp" onchange="GACT.setRaw(${id},'Citas por IA (total)',this.value===''?null:Number(this.value))"></div>
       <div class="actfield"><label>Fecha primera cita IA</label><input type="date" value="${esc(actV(r,'Fecha primera cita IA'))}" class="actinp" onchange="GACT.setRaw(${id},'Fecha primera cita IA',this.value||null)"></div></div>
     <div class="actcard"><div class="actcard-h"><b>E3 · Verificación Mitzi</b>${pill(actV(r,'E3 · Verificación Mitzi')||'⏳ Pendiente')}</div>
       <div class="actrule">llamada de cierre — gate final. Se aprueba desde la columna <b>Mitzi</b> de la tabla.</div>
       ${bloqueo.length?`<div class="actlock">🔒 Aún no se puede aprobar: ${esc(bloqueo.join(' · '))}</div>`:`<div class="actready">✅ Listo para que Mitzi apruebe.</div>`}</div>`;
  }

  showDrawer(`
  <div class="p-6 border-b" style="border-color:var(--line)">
    <div class="flex items-start justify-between gap-3">
      <div><div class="text-[11px] uppercase tracking-wide font-semibold" style="color:var(--violet)">Etapa ${idx+1} · ${esc(st.label)}</div>
        <h2 class="text-lg font-bold leading-tight mt-0.5">${esc(actV(r,'Name')||'—')}</h2>
        <p class="text-[12px] mt-0.5" style="color:var(--sub)">${esc(actV(r,'Plan · detalle')||'')}</p></div>
      <button onclick="closeDrawer()" class="border bg-white rounded-lg px-2.5 py-1.5 text-sm" style="border-color:var(--line)">✕</button>
    </div>
    <div class="flex gap-1.5 mt-3">${ACT_STAGES.map((s,i)=>`<button class="actstagetab ${i===idx?'on':''}" onclick="GACT.openStage(${id},${i})">${esc(s.label)}</button>`).join('')}</div>
    <div class="text-[11.5px] mt-2" style="color:var(--sub)">Entrada manual mientras no exista el endpoint (ACT-3). Cuando exista, el sistema pisa estos valores en cada sync.</div>
  </div>
  <div class="p-6 space-y-3">${body}</div>`);
};

/* ══════════ MITZI: aprobar / observar ══════════ */
GACT.mitziModal=function(id,tipo){const r=this.DATA.find(x=>x.id===id);if(!r)return;
  if(tipo==='ok'){const b=actMitziBloqueo(r);if(b.length){toast('No se puede aprobar: '+b.join(' · '));return;}}
  const prev=actV(r,'Nota Mitzi');
  const box=document.createElement('div');box.className='actmodal';
  box.innerHTML=`<div class="actmodal-bg" onclick="this.parentNode.remove()"></div>
   <div class="actmodal-card">
     <div class="text-[15px] font-bold">${tipo==='ok'?'✅ Aprobar onboarding':'⚠️ Marcar con observaciones'}</div>
     <div class="text-[12.5px] mt-1" style="color:var(--sub)">${esc(actV(r,'Name'))} · ${esc(actV(r,'Slug Clinera'))}</div>
     ${tipo==='ok'?`<div class="text-[12px] mt-2 rounded-lg px-3 py-2" style="background:#FDF2E9;color:#9A5B1E">Al aprobar se fija <b>hoy</b> como 📅 Entrega formal (arranca el reloj de 60 días del tramo 3), se marca el AHA como verificado y se avisa por correo a ricardo@oacg.cl.</div>`:''}
     <label class="block text-[11px] uppercase tracking-wide font-medium mt-3 mb-1" style="color:var(--sub)">Nota del proceso</label>
     <textarea id="actNota" rows="4" class="w-full bg-white border rounded-lg px-3 py-2 text-sm" style="border-color:var(--line);resize:vertical" placeholder="Qué se revisó en la llamada de cierre…">${esc(prev)}</textarea>
     <div class="flex justify-end gap-2 mt-4">
       <button onclick="this.closest('.actmodal').remove()" class="border bg-white rounded-lg px-3.5 py-2 text-sm" style="border-color:var(--line)">Cancelar</button>
       <button onclick="GACT.mitziCommit(${id},'${tipo}')" class="rounded-lg px-3.5 py-2 text-sm font-semibold text-white" style="background:${tipo==='ok'?'#116329':'#9A5B1E'}">${tipo==='ok'?'Aprobar y avisar':'Guardar observación'}</button>
     </div>
   </div>`;
  document.body.appendChild(box);setTimeout(()=>{const t=document.getElementById('actNota');if(t)t.focus();},50);
};
GACT.mitziCommit=async function(id,tipo){const r=this.DATA.find(x=>x.id===id);if(!r)return;
  const nota=(document.getElementById('actNota')||{}).value||'';
  const modal=document.querySelector('.actmodal');if(modal)modal.remove();
  try{
    let body;
    if(tipo==='ok'){
      const b=actMitziBloqueo(r);if(b.length){toast('No se puede aprobar: '+b.join(' · '));return;}
      const hoy=new Date().toISOString().slice(0,10);
      body={'E3 · Verificación Mitzi':'✅ Conforme','AHA verificado Mitzi':'✅ Verificado','Nota Mitzi':nota};
      if(!actEntregado(r))body['📅 Entrega formal']=hoy;
    }else{
      body={'E3 · Verificación Mitzi':'⚠️ Con observaciones','Nota Mitzi':nota};
    }
    const upd=await api('/api/database/rows/table/957/'+id+'/?user_field_names=true',{method:'PATCH',body:JSON.stringify(body)});
    const i=this.DATA.findIndex(x=>x.id===id);if(i>=0)this.DATA[i]=upd;if(this.sel&&this.sel.id===id)this.sel=upd;this.render();
    if(tipo==='ok'){
      toast('Aprobado · '+(actV(upd,'Name')||''));
      fetch('/work-api/notify-complete',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({slug:actV(upd,'Slug Clinera'),name:actV(upd,'Name'),fecha:actV(upd,'📅 Entrega formal'),encargado:actV(upd,'Encargado'),nota})})
        .then(x=>x.json()).then(d=>{if(!d||d.ok!==true)toast('Aprobado. ⚠️ Correo no enviado: '+((d&&d.reason)||'sin SMTP')+' (ver HALLAZGOS §I)');})
        .catch(()=>toast('Aprobado. ⚠️ Correo no enviado (endpoint no disponible).'));
    }else toast('Observación guardada');
  }catch(e){toast('Error: '+e.message);}
};

GACT.render=function(){
  this.ensureViewToggle();this.actTag();
  if(this._view==='tabla'){GACT_TABLE_RENDER.call(this);return;}
  const all=this.filtered();

  const conSync=all.filter(r=>actV(r,'Última sync')).length;
  const banner=conSync===0&&all.length>0
    ? `<div class="actbanner">⏳ Esperando endpoint de Clinera (ACT-3) — sin datos sincronizados. Se llena a mano desde cada etapa; cuando exista el endpoint, el sistema lo pisa solo.</div>`
    : (conSync<all.length?`<div class="actbanner">⏳ ${all.length-conSync} de ${all.length} sin sincronizar — esperando el endpoint de Clinera (ACT-3).</div>`:'');

  const nTot=all.length;
  const nProc=all.filter(r=>actV(r,'🚦 Estado')==='🟡 EN PROCESO').length;
  const nDone=all.filter(r=>actV(r,'🚦 Estado')==='✅ ENTREGADO').length;
  const nVenc=all.filter(actVencido).length,nDen=all.filter(actSinDenom).length,
        nMit=all.filter(actEsperaMitzi).length,nReg=all.filter(actRegresion).length;
  let rows=all;
  if(this._filt==='proc') rows=rows.filter(r=>actV(r,'🚦 Estado')==='🟡 EN PROCESO');
  if(this._filt==='done') rows=rows.filter(r=>actV(r,'🚦 Estado')==='✅ ENTREGADO');
  if(this._filt==='venc') rows=rows.filter(actVencido);
  if(this._filt==='den')  rows=rows.filter(actSinDenom);
  if(this._filt==='mitzi')rows=rows.filter(actEsperaMitzi);
  if(this._filt==='reg')  rows=rows.filter(actRegresion);

  const k=document.getElementById('actKpis');
  if(k){k.style.maxWidth='860px';
    const card=(lbl,val,f,col)=>`<div class="onbkpi bg-white border rounded-xl px-5 py-4 ${this._filt===f&&f?'on':''}" style="border-color:var(--line)" onclick="GACT.setFilt('${f}')">
      <div class="k-lbl text-[11px] uppercase tracking-wide font-medium" style="color:var(--sub)">${lbl}</div>
      <div class="k-val mono text-[24px] font-semibold mt-1" ${col?`style="color:${col}"`:''}>${val}</div></div>`;
    k.innerHTML=`<div class="grid grid-cols-3 gap-3">${card('Total',nTot,'')}${card('En proceso',nProc,'proc','#9A5B1E')}${card('Completado',nDone,'done','#116329')}</div>
      <div class="flex flex-wrap gap-1.5 mt-2.5">
        ${[['🔴 Vencidos',nVenc,'venc'],['Sin denominador',nDen,'den'],['Esperando Mitzi',nMit,'mitzi'],['↩ Regresión',nReg,'reg']].map(([l,v,f])=>
          `<button class="actchip ${this._filt===f?'on':''}" onclick="GACT.setFilt('${f}')">${l} <b>${v}</b></button>`).join('')}</div>`;}

  const hn=document.getElementById('actHidN');if(hn)hn.textContent=this.prefs.hidden.length;
  document.getElementById('actCount').textContent=`${rows.length} de ${this.DATA.length} cargados`;
  document.getElementById('actTotales').textContent=`${this.total??'…'} elementos totales`;
  document.getElementById('actInfo').textContent=`${this.DATA.length} cargados`;
  document.getElementById('actMore').classList.toggle('hidden',!this.next);

  const seg=(r,s,i)=>{const done=actStageDone(r,s);const cur=actStageIdx(r)===i;
    const cls=done?'st-done':cur?'st-proc':'st-pend';
    return `<div class="onbseg actclick ${cls}" title="Abrir etapa ${i+1} · ${esc(s.label)}" onclick="event.stopPropagation();GACT.openStage(${r.id},${i})">
      <span class="t">${esc(s.label)}</span><span class="s">${done?'Completada':cur?'En proceso':'Pendiente'}</span></div>`;};

  const cnt=(r,got,den,lbl)=>{const g=actNum(r,got),d=actNum(r,den);
    if(d===null)return `<span class="actcnt actcnt-na" title="Sin denominador declarado">— /— ${lbl}</span>`;
    if(g===null)return `<span class="actcnt actcnt-na" title="Sin dato — cargar en la etapa">?/${d.toLocaleString('es')} ${lbl}</span>`;
    const ok=lbl==='pacientes'?g>=d*0.95:g>=d;
    return `<span class="actcnt ${ok?'actcnt-ok':'actcnt-bad'}" title="${lbl}: ${g.toLocaleString('es')} de ${d.toLocaleString('es')}">${g.toLocaleString('es')}/${d.toLocaleString('es')} ${lbl}</span>`;};

  const planCell=r=>{const p=String(actV(r,'Plan')||'').trim();const P=ACT_PLANS[p];const det=actV(r,'Plan · detalle');
    if(!P)return `<span class="text-[11.5px]" style="color:var(--sub)">${esc(det||p||'—')}</span>`;
    return `<span class="text-[11.5px]" style="color:var(--sub)" title="${esc(det)} · precio de Stripe">${esc(p)} · US$${P.price}/mes + US$${P.impl}</span>`;};

  const estadoChip=r=>{const e=actV(r,'🚦 Estado');
    const c=e==='✅ ENTREGADO'?['#DFF2E4','#116329']:e==='⛔ CANCELADO'?['#FBE9E7','#B3261E']:['#FDF2E9','#9A5B1E'];
    return `<span class="onbchip" style="background:${c[0]};color:${c[1]};cursor:default" title="Derivado de las 4 etapas, sin override manual.">${esc(e||'—')}</span>`;};

  const slaChip=r=>{const s=actV(r,'SLA');const d=actV(r,'Días desde D0');
    const c=s==='🔴 Vencido'?['#FBE9E7','#B3261E']:s==='🟡 En riesgo'?['#FDF2E9','#9A5B1E']:['#DFF2E4','#116329'];
    return `<span class="onbchip" style="background:${c[0]};color:${c[1]};cursor:default" title="${esc(s)} · D+${esc(d)}">D+${esc(d)}</span>`;};

  const mitziCell=r=>{const e=actV(r,'E3 · Verificación Mitzi');
    if(e==='✅ Conforme')return `<span class="onbchip" style="background:#DFF2E4;color:#116329;cursor:pointer" title="${esc(actV(r,'Nota Mitzi')||'aprobado')}" onclick="event.stopPropagation();GACT.mitziModal(${r.id},'ok')">✅ Conforme ✎</span>`;
    if(e==='⚠️ Con observaciones')return `<div class="flex flex-col gap-1"><span class="onbchip" style="background:#FDF2E9;color:#9A5B1E;cursor:pointer" title="${esc(actV(r,'Nota Mitzi')||'')}" onclick="event.stopPropagation();GACT.mitziModal(${r.id},'obs')">⚠️ Observado ✎</span><button class="actapprove" onclick="event.stopPropagation();GACT.mitziModal(${r.id},'ok')">Aprobar</button></div>`;
    const bloq=actMitziBloqueo(r).length>0;
    return `<div class="flex flex-col gap-1">
      <button class="actapprove ${bloq?'off':''}" title="${bloq?'Bloqueado: '+esc(actMitziBloqueo(r).join(' · ')):'Aprobar el onboarding'}" onclick="event.stopPropagation();GACT.mitziModal(${r.id},'ok')">✓ Aprobar</button>
      <button class="actobs" onclick="event.stopPropagation();GACT.mitziModal(${r.id},'obs')">Observar</button></div>`;};

  const comisionCell=r=>{const ef=actV(r,'📅 Entrega formal');
    if(!ef)return `<span style="color:var(--sub)" class="text-xs">—</span>`;
    const n=actDaysSince(ef);const faltan=60-n;
    const l2=faltan>0?`<span style="color:#9A5B1E">comisión en ${faltan}d</span>`:`<span style="color:#116329;font-weight:600">✅ comisión lista</span>`;
    return `<div class="text-xs leading-snug"><div class="mono" title="📅 Entrega formal: ${esc(ef)} — desde acá corren los 60 días">D+${n} <span style="color:var(--sub)">desde entrega</span></div><div class="mt-0.5">${l2}</div></div>`;};

  const head=`<div class="acthead"><div>Cliente</div><div>Estado</div><div>Etapas</div><div>Prog.</div><div>Contadores</div><div>SLA</div><div>Encargado</div><div>Mitzi</div><div>Comisión</div></div>`;
  const body=rows.map(r=>{const pais=String(actV(r,'País')||'').trim();const sync=actV(r,'Última sync');const inact=actV(r,'Cliente activo')==='❌ Inactivo';
    return `<div class="actrow ${actEntregado(r)?'onbrow-on':''} ${inact?'onbrow-off':''}" onclick="GACT.open(${r.id})">
      <div class="min-w-0">
        <div class="font-medium text-[13.5px] leading-tight truncate">${esc(actV(r,'Name')||'—')}
          ${actA4Falla(r)?'<span class="actflag" title="Automatizaciones activas pero con >5% de error en 24h — el cliente pierde citas. Check CLAVE.">⚠️ automatiz.</span>':''}
          ${actRegresion(r)?'<span class="actflag" title="REGRESIÓN: entregado y un check volvió a rojo.">↩ regresión</span>':''}
          ${!sync?'<span class="actflag actflag-wait" title="Nunca sincronizado — datos manuales">manual</span>':''}</div>
        <div class="text-[11.5px] mt-0.5 flex items-center gap-1.5">${planCell(r)}${pais?`<span style="color:var(--sub)">· ${esc(pais)}</span>`:''}</div>
      </div>
      <div>${estadoChip(r)}</div>
      <div class="onbflow">${ACT_STAGES.map((s,i)=>seg(r,s,i)).join('')}</div>
      <div class="mono text-[12.5px]" title="checks verdes / aplicables (N/A fuera)">${esc(actV(r,'Progreso')||'—')}</div>
      <div class="actcnts">
        ${cnt(r,'Sucursales cargadas','Sucursales declaradas','sucursales')}
        ${cnt(r,'Profesionales activos','Profesionales declarados','profesionales')}
        ${cnt(r,'Tratamientos cargados','Tratamientos declarados','tratamientos')}
        ${cnt(r,'Pacientes cargados','Pacientes declarados','pacientes')}
      </div>
      <div>${slaChip(r)}</div>
      <div>${(()=>{const v=r['Encargado'];
        if(v&&typeof v==='object'&&v.value){const cc=brCol(v.color);return `<span class="onbchip" style="background:${cc[0]};color:${cc[1]}" onclick="event.stopPropagation();GACT.pickOpt(event,${r.id},'Encargado')">${esc(v.value)}</span>`;}
        return `<span class="onbchip" style="background:#EFEEEA;color:#8A8984" onclick="event.stopPropagation();GACT.pickOpt(event,${r.id},'Encargado')">Asignar</span>`;})()}</div>
      <div onclick="event.stopPropagation()">${mitziCell(r)}</div>
      <div onclick="event.stopPropagation()">${comisionCell(r)}</div>
    </div>`;}).join('');

  document.getElementById('actGrid').innerHTML=banner+`<div class="bg-white border rounded-xl" style="border-color:var(--line);overflow:auto;max-height:calc(100vh - 140px)"><div style="min-width:1760px">${head}${body||'<div class="text-sm py-16 text-center" style="color:var(--sub)">Sin clientes con estos filtros. Los clientes nuevos entran solos desde Stripe vía n8n.</div>'}</div></div>`;
};
