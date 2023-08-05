/*! For license information please see chunk.70dac66a555d119d666d.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[3122],{63207:(e,t,i)=>{"use strict";i(65660),i(15112);var s=i(9672),n=i(87156),o=i(50856),r=i(65233);(0,s.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:r.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{"use strict";i.d(t,{P:()=>n});i(65233);var s=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var o=n.types;(0,s.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var s=new n({type:e,key:t});return void 0!==i&&i!==s.value?s.value=i:this.value!==s.value&&(this.value=s.value),s},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},58993:(e,t,i)=>{"use strict";i.d(t,{yh:()=>s,U2:()=>r,t8:()=>a,ZH:()=>h});class s{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((i,s)=>{const n=indexedDB.open(e,1);n.onerror=()=>s(n.error),n.onsuccess=()=>i(n.result),n.onupgradeneeded=()=>{n.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((i=>new Promise(((s,n)=>{const o=i.transaction(this.storeName,e);o.oncomplete=()=>s(),o.onabort=o.onerror=()=>n(o.error),t(o.objectStore(this.storeName))}))))}}let n;function o(){return n||(n=new s),n}function r(e,t=o()){let i;return t._withIDBStore("readonly",(t=>{i=t.get(e)})).then((()=>i.result))}function a(e,t,i=o()){return i._withIDBStore("readwrite",(i=>{i.put(t,e)}))}function h(e=o()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}}}]);
//# sourceMappingURL=chunk.70dac66a555d119d666d.js.map