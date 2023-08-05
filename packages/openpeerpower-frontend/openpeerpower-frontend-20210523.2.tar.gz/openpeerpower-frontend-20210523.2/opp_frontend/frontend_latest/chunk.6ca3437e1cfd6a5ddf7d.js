/*! For license information please see chunk.6ca3437e1cfd6a5ddf7d.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[4507],{67810:(e,t,r)=>{"use strict";r.d(t,{o:()=>n});r(65233);var o=r(87156);const n={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,t){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),t)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var r=this.domHost;this.scrollTarget=r&&r.$?r.$[e]:(0,o.vz)(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(e){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=e)},set _scrollLeft(e){this.scrollTarget===this._doc?window.scrollTo(e,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=e)},scroll:function(e,t){var r;"object"==typeof e?(r=e.left,t=e.top):r=e,r=r||0,t=t||0,this.scrollTarget===this._doc?window.scrollTo(r,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=r,this.scrollTarget.scrollTop=t)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(e,t){var r=t===this._doc?window:t;e?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),r.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(r.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(e){this._shouldHaveListener=e,this._toggleScrollListener(e,this.scrollTarget)}}},25782:(e,t,r)=>{"use strict";r(65233),r(65660),r(70019),r(97968);var o=r(9672),n=r(50856),l=r(33760);(0,o.k)({_template:n.d`
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
`,is:"paper-icon-item",behaviors:[l.U]})},89194:(e,t,r)=>{"use strict";r(65233),r(65660),r(70019);var o=r(9672),n=r(50856);(0,o.k)({_template:n.d`
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
`,is:"paper-item-body"})},4268:(e,t,r)=>{"use strict";function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function n(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function l(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?n(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):n(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function i(e,t){if(null==e)return{};var r,o,n=function(e,t){if(null==e)return{};var r,o,n={},l=Object.keys(e);for(o=0;o<l.length;o++)r=l[o],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(o=0;o<l.length;o++)r=l[o],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}function*s(e,t){!0===e||(!1===e?yield t.fail():yield*e)}function c(e){const{done:t,value:r}=e.next();return t?void 0:r}r.d(t,{DD:()=>u,Yj:()=>y,IX:()=>g,hu:()=>h,O7:()=>b,D8:()=>_,kE:()=>v,i0:()=>w,Rx:()=>m,Ry:()=>O,jt:()=>j,Z_:()=>S,n_:()=>k,dt:()=>L,G0:()=>H});class a{constructor(e){const{type:t,schema:r,coercer:o=(e=>e),validator:n=(()=>[]),refiner:l=(()=>[])}=e;this.type=t,this.schema=r,this.coercer=o,this.validator=n,this.refiner=l}}class u extends TypeError{constructor(e,t){const{path:r,value:o,type:n,branch:l}=e,s=i(e,["path","value","type","branch"]);let c;super(`Expected a value of type \`${n}\`${r.length?` for \`${r.join(".")}\``:""} but received \`${JSON.stringify(o)}\`.`),this.value=o,Object.assign(this,s),this.type=n,this.path=r,this.branch=l,this.failures=function(){return c||(c=[e,...t]),c},this.stack=(new Error).stack,this.__proto__=u.prototype}}function h(e,t){const r=f(e,t);if(r[0])throw r[0]}function p(e,t){const r=t.coercer(e);return h(r,t),r}function f(e,t,r=!1){r&&(e=t.coercer(e));const o=d(e,t),n=c(o);if(n){return[new u(n,o),void 0]}return[void 0,e]}function*d(e,t,r=[],o=[]){const{type:n}=t,i={value:e,type:n,branch:o,path:r,fail:(t={})=>l({value:e,type:n,path:r,branch:[...o,e]},t),check:(e,t,n,l)=>d(e,t,void 0!==n?[...r,l]:r,void 0!==n?[...o,n]:o)},a=s(t.validator(e,i),i),u=c(a);u?(yield u,yield*a):yield*s(t.refiner(e,i),i)}function y(){return k("any",(()=>!0))}function g(e){return new a({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map((t=>p(t,e))):t,*validator(t,r){if(Array.isArray(t)){if(e)for(const[o,n]of t.entries())yield*r.check(n,e,t,o)}else yield r.fail()}})}function b(){return k("boolean",(e=>"boolean"==typeof e))}function _(e){return k("Dynamic<...>",((t,r)=>r.check(t,e(t,r))))}function v(e){return k(`Enum<${e.map($)}>`,(t=>e.includes(t)))}function w(e){return k(`Literal<${$(e)}>`,(t=>t===e))}function T(){return k("never",(()=>!1))}function m(){return k("number",(e=>"number"==typeof e&&!isNaN(e)))}function O(e){const t=e?Object.keys(e):[],r=T();return new a({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?x(e):e=>e,*validator(o,n){if("object"==typeof o&&null!=o){if(e){const l=new Set(Object.keys(o));for(const r of t){l.delete(r);const t=e[r],i=o[r];yield*n.check(i,t,o,r)}for(const e of l){const t=o[e];yield*n.check(t,r,o,e)}}}else yield n.fail()}})}function j(e){return new a({type:`${e.type}?`,schema:e.schema,validator:(t,r)=>void 0===t||r.check(t,e)})}function S(){return k("string",(e=>"string"==typeof e))}function k(e,t){return new a({type:e,validator:t,schema:null})}function L(e){const t=Object.keys(e);return k(`Type<{${t.join(",")}}>`,(function*(r,o){if("object"==typeof r&&null!=r)for(const n of t){const t=e[n],l=r[n];yield*o.check(l,t,r,n)}else yield o.fail()}))}function H(e){return k(`${e.map((e=>e.type)).join(" | ")}`,(function*(t,r){for(const o of e){const[...e]=r.check(t,o);if(0===e.length)return}yield r.fail()}))}function $(e){return"string"==typeof e?`"${e.replace(/"/g,'"')}"`:`${e}`}function x(e){const t=Object.keys(e);return r=>{if("object"!=typeof r||null==r)return r;const o={},n=new Set(Object.keys(r));for(const l of t){n.delete(l);const t=e[l],i=r[l];o[l]=p(i,t)}for(const e of n)o[e]=r[e];return o}}}}]);
//# sourceMappingURL=chunk.6ca3437e1cfd6a5ddf7d.js.map