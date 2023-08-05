/*! For license information please see chunk.91080c39ec773c066902.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[6830,4507,1002,305,7523,2858,4325,875,7887,2982,7130],{99257:(e,t,r)=>{"use strict";r(65233);var o=r(15112),n=r(9672),i=r(87156);(0,n.k)({is:"iron-iconset-svg",properties:{name:{type:String,observer:"_nameChanged"},size:{type:Number,value:24},rtlMirroring:{type:Boolean,value:!1},useGlobalRtlAttribute:{type:Boolean,value:!1}},created:function(){this._meta=new o.P({type:"iconset",key:null,value:null})},attached:function(){this.style.display="none"},getIconNames:function(){return this._icons=this._createIconMap(),Object.keys(this._icons).map((function(e){return this.name+":"+e}),this)},applyIcon:function(e,t){this.removeIcon(e);var r=this._cloneIcon(t,this.rtlMirroring&&this._targetIsRTL(e));if(r){var o=(0,i.vz)(e.root||e);return o.insertBefore(r,o.childNodes[0]),e._svgIcon=r}return null},removeIcon:function(e){e._svgIcon&&((0,i.vz)(e.root||e).removeChild(e._svgIcon),e._svgIcon=null)},_targetIsRTL:function(e){if(null==this.__targetIsRTL)if(this.useGlobalRtlAttribute){var t=document.body&&document.body.hasAttribute("dir")?document.body:document.documentElement;this.__targetIsRTL="rtl"===t.getAttribute("dir")}else e&&e.nodeType!==Node.ELEMENT_NODE&&(e=e.host),this.__targetIsRTL=e&&"rtl"===window.getComputedStyle(e).direction;return this.__targetIsRTL},_nameChanged:function(){this._meta.value=null,this._meta.key=this.name,this._meta.value=this,this.async((function(){this.fire("iron-iconset-added",this,{node:window})}))},_createIconMap:function(){var e=Object.create(null);return(0,i.vz)(this).querySelectorAll("[id]").forEach((function(t){e[t.id]=t})),e},_cloneIcon:function(e,t){return this._icons=this._icons||this._createIconMap(),this._prepareSvgClone(this._icons[e],this.size,t)},_prepareSvgClone:function(e,t,r){if(e){var o=e.cloneNode(!0),n=document.createElementNS("http://www.w3.org/2000/svg","svg"),i=o.getAttribute("viewBox")||"0 0 "+t+" "+t,l="pointer-events: none; display: block; width: 100%; height: 100%;";return r&&o.hasAttribute("mirror-in-rtl")&&(l+="-webkit-transform:scale(-1,1);transform:scale(-1,1);transform-origin:center;"),n.setAttribute("viewBox",i),n.setAttribute("preserveAspectRatio","xMidYMid meet"),n.setAttribute("focusable","false"),n.style.cssText=l,n.appendChild(o).removeAttribute("id"),n}return null}})},67810:(e,t,r)=>{"use strict";r.d(t,{o:()=>n});r(65233);var o=r(87156);const n={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,t){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),t)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var r=this.domHost;this.scrollTarget=r&&r.$?r.$[e]:(0,o.vz)(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(e){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=e)},set _scrollLeft(e){this.scrollTarget===this._doc?window.scrollTo(e,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=e)},scroll:function(e,t){var r;"object"==typeof e?(r=e.left,t=e.top):r=e,r=r||0,t=t||0,this.scrollTarget===this._doc?window.scrollTo(r,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=r,this.scrollTarget.scrollTop=t)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(e,t){var r=t===this._doc?window:t;e?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),r.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(r.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(e){this._shouldHaveListener=e,this._toggleScrollListener(e,this.scrollTarget)}}},25782:(e,t,r)=>{"use strict";r(65233),r(65660),r(70019),r(97968);var o=r(9672),n=r(50856),i=r(33760);(0,o.k)({_template:n.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.U]})},89194:(e,t,r)=>{"use strict";r(65233),r(65660),r(70019);var o=r(9672),n=r(50856);(0,o.k)({_template:n.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},1275:(e,t,r)=>{"use strict";r.d(t,{l:()=>i});var o=r(94707);const n=new WeakMap,i=(0,o.XM)(((e,t)=>r=>{const o=n.get(r);if(Array.isArray(e)){if(Array.isArray(o)&&o.length===e.length&&e.every(((e,t)=>e===o[t])))return}else if(o===e&&(void 0!==e||n.has(r)))return;r.setValue(t()),n.set(r,Array.isArray(e)?Array.from(e):e)}))},4268:(e,t,r)=>{"use strict";function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function n(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?n(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):n(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function l(e,t){if(null==e)return{};var r,o,n=function(e,t){if(null==e)return{};var r,o,n={},i=Object.keys(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}function*s(e,t){!0===e||(!1===e?yield t.fail():yield*e)}function c(e){const{done:t,value:r}=e.next();return t?void 0:r}r.d(t,{DD:()=>u,Yj:()=>y,IX:()=>g,hu:()=>h,O7:()=>v,D8:()=>_,kE:()=>b,i0:()=>m,Rx:()=>T,Ry:()=>O,jt:()=>S,Z_:()=>j,n_:()=>k,dt:()=>A,G0:()=>L});class a{constructor(e){const{type:t,schema:r,coercer:o=(e=>e),validator:n=(()=>[]),refiner:i=(()=>[])}=e;this.type=t,this.schema=r,this.coercer=o,this.validator=n,this.refiner=i}}class u extends TypeError{constructor(e,t){const{path:r,value:o,type:n,branch:i}=e,s=l(e,["path","value","type","branch"]);let c;super(`Expected a value of type \`${n}\`${r.length?` for \`${r.join(".")}\``:""} but received \`${JSON.stringify(o)}\`.`),this.value=o,Object.assign(this,s),this.type=n,this.path=r,this.branch=i,this.failures=function(){return c||(c=[e,...t]),c},this.stack=(new Error).stack,this.__proto__=u.prototype}}function h(e,t){const r=p(e,t);if(r[0])throw r[0]}function d(e,t){const r=t.coercer(e);return h(r,t),r}function p(e,t,r=!1){r&&(e=t.coercer(e));const o=f(e,t),n=c(o);if(n){return[new u(n,o),void 0]}return[void 0,e]}function*f(e,t,r=[],o=[]){const{type:n}=t,l={value:e,type:n,branch:o,path:r,fail:(t={})=>i({value:e,type:n,path:r,branch:[...o,e]},t),check:(e,t,n,i)=>f(e,t,void 0!==n?[...r,i]:r,void 0!==n?[...o,n]:o)},a=s(t.validator(e,l),l),u=c(a);u?(yield u,yield*a):yield*s(t.refiner(e,l),l)}function y(){return k("any",(()=>!0))}function g(e){return new a({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map((t=>d(t,e))):t,*validator(t,r){if(Array.isArray(t)){if(e)for(const[o,n]of t.entries())yield*r.check(n,e,t,o)}else yield r.fail()}})}function v(){return k("boolean",(e=>"boolean"==typeof e))}function _(e){return k("Dynamic<...>",((t,r)=>r.check(t,e(t,r))))}function b(e){return k(`Enum<${e.map(I)}>`,(t=>e.includes(t)))}function m(e){return k(`Literal<${I(e)}>`,(t=>t===e))}function w(){return k("never",(()=>!1))}function T(){return k("number",(e=>"number"==typeof e&&!isNaN(e)))}function O(e){const t=e?Object.keys(e):[],r=w();return new a({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?E(e):e=>e,*validator(o,n){if("object"==typeof o&&null!=o){if(e){const i=new Set(Object.keys(o));for(const r of t){i.delete(r);const t=e[r],l=o[r];yield*n.check(l,t,o,r)}for(const e of i){const t=o[e];yield*n.check(t,r,o,e)}}}else yield n.fail()}})}function S(e){return new a({type:`${e.type}?`,schema:e.schema,validator:(t,r)=>void 0===t||r.check(t,e)})}function j(){return k("string",(e=>"string"==typeof e))}function k(e,t){return new a({type:e,validator:t,schema:null})}function A(e){const t=Object.keys(e);return k(`Type<{${t.join(",")}}>`,(function*(r,o){if("object"==typeof r&&null!=r)for(const n of t){const t=e[n],i=r[n];yield*o.check(i,t,r,n)}else yield o.fail()}))}function L(e){return k(`${e.map((e=>e.type)).join(" | ")}`,(function*(t,r){for(const o of e){const[...e]=r.check(t,o);if(0===e.length)return}yield r.fail()}))}function I(e){return"string"==typeof e?`"${e.replace(/"/g,'"')}"`:`${e}`}function E(e){const t=Object.keys(e);return r=>{if("object"!=typeof r||null==r)return r;const o={},n=new Set(Object.keys(r));for(const i of t){n.delete(i);const t=e[i],l=r[i];o[i]=d(l,t)}for(const e of n)o[e]=r[e];return o}}}}]);
//# sourceMappingURL=chunk.91080c39ec773c066902.js.map