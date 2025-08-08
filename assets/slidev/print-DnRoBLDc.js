import{d as _,$ as u,y as f,f as i,o as r,g as e,t as a,F as g,Z as h,i as v,e as b,a0 as x}from"../modules/vue-CUp9nEH8.js";import{u as y,j as N,c as m,b as k}from"../index-BKBeeQfK.js";import{N as D}from"./NoteDisplay-doutZjVl.js";import"../modules/shiki-hMOtOMJt.js";const w=_({__name:"print",setup(p,{expose:n}){n();const{slides:l,total:o}=y();u(`
@page {
  size: A4;
  margin-top: 1.5cm;
  margin-bottom: 1cm;
}
* {
  -webkit-print-color-adjust: exact;
}
html,
html body,
html #app,
html #page-root {
  height: auto;
  overflow: auto !important;
}
`),N({title:`Notes - ${m.title}`});const d=f(()=>l.value.map(t=>{var s;return(s=t.meta)==null?void 0:s.slide}).filter(t=>t!==void 0&&t.noteHTML!=="")),c={slides:l,total:o,slidesWithNote:d,get configs(){return m},NoteDisplay:D};return Object.defineProperty(c,"__isScriptSetup",{enumerable:!1,value:!0}),c}}),B={id:"page-root"},L={class:"m-4"},S={class:"mb-10"},T={class:"text-4xl font-bold mt-2"},C={class:"opacity-50"},H={class:"text-lg"},V={class:"font-bold flex gap-2"},W={class:"opacity-50"},j={key:0,class:"border-main mb-8"};function z(p,n,l,o,d,c){return r(),i("div",B,[e("div",L,[e("div",S,[e("h1",T,a(o.configs.title),1),e("div",C,a(new Date().toLocaleString()),1)]),(r(!0),i(g,null,h(o.slidesWithNote,(t,s)=>(r(),i("div",{key:s,class:"flex flex-col gap-4 break-inside-avoid-page"},[e("div",null,[e("h2",H,[e("div",V,[e("div",W,a(t==null?void 0:t.no)+"/"+a(o.total),1),x(" "+a(t==null?void 0:t.title)+" ",1),n[0]||(n[0]=e("div",{class:"flex-auto"},null,-1))])]),b(o.NoteDisplay,{"note-html":t.noteHTML,class:"max-w-full"},null,8,["note-html"])]),s<o.slidesWithNote.length-1?(r(),i("hr",j)):v("v-if",!0)]))),128))])])}const P=k(w,[["render",z],["__file","/Users/supabowl/Library/Mobile Documents/com~apple~CloudDocs/BHT Promo iCloud/Organized AI/Windsurf/Organized Bootcamp/node_modules/@slidev/client/pages/presenter/print.vue"]]);export{P as default};
