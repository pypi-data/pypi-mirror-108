/*! For license information please see chunk.f93f86a43071d30ddd76.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[1428],{18601:(e,t,i)=>{"use strict";i.d(t,{qN:()=>r.q,Wg:()=>o});var r=i(78220);class o extends r.H{createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(e){this.formElement&&this.formElement.setAttribute("aria-label",e)}firstUpdated(){super.firstUpdated(),this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}},32333:(e,t,i)=>{"use strict";var r=i(15652);class o extends r.oi{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},readonly:{type:Boolean},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number},valueLabel:{type:String},lowLabel:{type:String},highLabel:{type:String}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.attachedListeners=!1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(e){let t=(this.startAngle+this.arcLength/2-e+180+360)%360-180;return t<this.arcLength/2&&t>-this.arcLength/2}_angle2xy(e){return this.rtl?{x:-Math.cos(e),y:Math.sin(e)}:{x:Math.cos(e),y:Math.sin(e)}}_xy2angle(e,t){return this.rtl&&(e=-e),(Math.atan2(t,e)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(e){const t=((e=Math.min(this.max,Math.max(this.min,e)))-this.min)/(this.max-this.min);return this._start+t*this._len}_angle2value(e){return Math.round((e/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const e=this._angle2xy(this._start),t=this._angle2xy(this._end);let i=1;this._angleInside(270)||(i=Math.max(-e.y,-t.y));let r=1;this._angleInside(90)||(r=Math.max(e.y,t.y));let o=1;this._angleInside(180)||(o=Math.max(-e.x,-t.x));let n=1;return this._angleInside(0)||(n=Math.max(e.x,t.x)),{up:i,down:r,left:o,right:n,height:i+r,width:o+n}}_mouse2value(e){const t=e.type.startsWith("touch")?e.touches[0].clientX:e.clientX,i=e.type.startsWith("touch")?e.touches[0].clientY:e.clientY,r=this.shadowRoot.querySelector("svg").getBoundingClientRect(),o=this._boundaries,n=t-(r.left+o.left*r.width/o.width),s=i-(r.top+o.up*r.height/o.height),a=this._xy2angle(n,s);return this._angle2value(a)}dragStart(e){if(!this._showHandle||this.disabled)return;let t,i=e.target;if(this._rotation&&"focus"!==this._rotation.type)return;if(i.classList.contains("shadowpath"))if("touchstart"===e.type&&(t=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)i=this.shadowRoot.querySelector("#value");else{const t=this._mouse2value(e);i=Math.abs(t-this.low)<Math.abs(t-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(i.classList.contains("overflow")&&(i=i.nextElementSibling),!i.classList.contains("handle"))return;i.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const r="high"===i.id?this.low:this.min,o="low"===i.id?this.high:this.max;this._rotation={handle:i,min:r,max:o,start:this[i.id],type:e.type,cooldown:t},this.dragging=!0}_cleanupRotation(){const e=this._rotation.handle;e.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,e.blur()}dragEnd(e){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const t=this._rotation.handle;this._cleanupRotation();let i=new CustomEvent("value-changed",{detail:{[t.id]:this[t.id]},bubbles:!0,composed:!0});this.dispatchEvent(i),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(e){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.coldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;e.preventDefault();const t=this._mouse2value(e);this._dragpos(t)}_dragpos(e){if(e<this._rotation.min||e>this._rotation.max)return;const t=this._rotation.handle;this[t.id]=e;let i=new CustomEvent("value-changing",{detail:{[t.id]:e},bubbles:!0,composed:!0});this.dispatchEvent(i)}_keyStep(e){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const t=this._rotation.handle;"ArrowLeft"!==e.key&&"ArrowDown"!==e.key||(e.preventDefault(),this.rtl?this._dragpos(this[t.id]+this.step):this._dragpos(this[t.id]-this.step)),"ArrowRight"!==e.key&&"ArrowUp"!==e.key||(e.preventDefault(),this.rtl?this._dragpos(this[t.id]-this.step):this._dragpos(this[t.id]+this.step)),"Home"===e.key&&(e.preventDefault(),this._dragpos(this.min)),"End"===e.key&&(e.preventDefault(),this._dragpos(this.max))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(e){if(this.shadowRoot.querySelector(".slider")){const e=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(e&&e.strokeWidth){const t=parseFloat(e.strokeWidth);if(t>this.handleSize*this.handleZoom){const e=this._boundaries,i=`\n          ${t/2*Math.abs(e.up)}px\n          ${t/2*Math.abs(e.right)}px\n          ${t/2*Math.abs(e.down)}px\n          ${t/2*Math.abs(e.left)}px`;this.shadowRoot.querySelector("svg").style.margin=i}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){e.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((e=>{if(e.getAttribute("stroke-width"))return;const t=parseFloat(getComputedStyle(e).getPropertyValue("stroke-width"));e.style.strokeWidth=t*this._scale+"px"}));const t=this.shadowRoot.querySelector("svg").getBoundingClientRect(),i=Math.max(t.width,t.height);this._scale=2/i}}_renderArc(e,t){const i=t-e;return e=this._angle2xy(e),t=this._angle2xy(t+.001),`\n      M ${e.x} ${e.y}\n      A 1 1,\n        0,\n        ${i>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${t.x} ${t.y}\n    `}_renderHandle(e){const t=this._value2angle(this[e]),i=this._angle2xy(t),o={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[e]||"";return r.YP`
      <g class="${e} handle">
        <path
          id=${e}
          class="overflow"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${e}
          class="handle"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[e]}
          aria-disabled=${this.disabled}
          aria-label=${o||""}
          />
        </g>
      `}render(){const e=this._boundaries;return r.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-e.left} ${-e.up} ${e.width} ${e.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />

        </g>

        <g class="handles">
        ${this._showHandle?null!=this.low?this._reverseOrder?r.dy`${this._renderHandle("high")} ${this._renderHandle("low")}`:r.dy`${this._renderHandle("low")} ${this._renderHandle("high")}`:r.dy`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return r.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}customElements.define("round-slider",o)},60461:e=>{e.exports=function e(t){return Object.freeze(t),Object.getOwnPropertyNames(t).forEach((function(i){!t.hasOwnProperty(i)||null===t[i]||"object"!=typeof t[i]&&"function"!=typeof t[i]||Object.isFrozen(t[i])||e(t[i])})),t}},58993:(e,t,i)=>{"use strict";i.d(t,{yh:()=>r,U2:()=>s,t8:()=>a,ZH:()=>l});class r{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((i,r)=>{const o=indexedDB.open(e,1);o.onerror=()=>r(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((i=>new Promise(((r,o)=>{const n=i.transaction(this.storeName,e);n.oncomplete=()=>r(),n.onabort=n.onerror=()=>o(n.error),t(n.objectStore(this.storeName))}))))}}let o;function n(){return o||(o=new r),o}function s(e,t=n()){let i;return t._withIDBStore("readonly",(t=>{i=t.get(e)})).then((()=>i.result))}function a(e,t,i=n()){return i._withIDBStore("readwrite",(i=>{i.put(t,e)}))}function l(e=n()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}},69470:(e,t,i)=>{"use strict";i.d(t,{j:()=>o,fs:()=>n,$y:()=>s});const r=(e,t,i)=>new Promise(((r,o)=>{const n=document.createElement(e);let s="src",a="body";switch(n.onload=()=>r(t),n.onerror=()=>o(t),e){case"script":n.async=!0,i&&(n.type=i);break;case"link":n.type="text/css",n.rel="stylesheet",s="href",a="head"}n[s]=t,document[a].appendChild(n)})),o=e=>r("link",e),n=e=>r("script",e),s=e=>r("script",e,"module")},86977:(e,t,i)=>{"use strict";i.d(t,{Q:()=>r});const r=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},85415:(e,t,i)=>{"use strict";i.d(t,{q:()=>r,w:()=>o});const r=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},15493:(e,t,i)=>{"use strict";i.d(t,{Q2:()=>r,io:()=>o,ou:()=>n,j4:()=>s,pc:()=>a});const r=()=>{const e={},t=new URLSearchParams(location.search);for(const[i,r]of t.entries())e[i]=r;return e},o=e=>new URLSearchParams(window.location.search).get(e),n=e=>{const t=new URLSearchParams;return Object.entries(e).forEach((([e,i])=>{t.append(e,i)})),t.toString()},s=e=>{const t=new URLSearchParams(window.location.search);return Object.entries(e).forEach((([e,i])=>{t.set(e,i)})),t.toString()},a=e=>{const t=new URLSearchParams(window.location.search);return t.delete(e),t.toString()}},81545:(e,t,i)=>{"use strict";i(33300);var r=i(15652);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,p.elements)}),i),p=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(a(n)||a(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(a(n)){if(a(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,p.elements),c.runClassFinishers(h.F,p.finishers)}([(0,r.Mo)("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return r.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),r.oi)},46167:(e,t,i)=>{"use strict";i(87482);var r=i(15652);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function p(e,t,i){return(p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=u(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function u(e){return(u=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const f=customElements.get("paper-tabs");let m;!function(e,t,i,r){var c=o();if(r)for(var d=0;d<r.length;d++)c=r[d](c);var h=t((function(e){c.initializeInstanceElements(e,p.elements)}),i),p=c.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(l(n.descriptor)||l(o.descriptor)){if(a(n)||a(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(a(n)){if(a(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(h.d.map(n)),e);c.initializeClassElements(h.F,p.elements),c.runClassFinishers(h.F,p.finishers)}([(0,r.Mo)("ha-tabs")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"_firstTabWidth",value:()=>0},{kind:"field",key:"_lastTabWidth",value:()=>0},{kind:"field",key:"_lastLeftHiddenState",value:()=>!1},{kind:"get",static:!0,key:"template",value:function(){if(!m){m=f.template.cloneNode(!0);const e=m.content.querySelector("style");m.content.querySelectorAll("paper-icon-button").forEach((e=>{e.setAttribute("noink","")})),e.appendChild(document.createTextNode("\n          #selectionBar {\n            box-sizing: border-box;\n          }\n          .not-visible {\n            display: none;\n          }\n          paper-icon-button {\n            width: 24px;\n            height: 48px;\n            padding: 0;\n            margin: 0;\n          }\n        "))}return m}},{kind:"method",key:"_tabChanged",value:function(e,t){p(u(i.prototype),"_tabChanged",this).call(this,e,t);const r=this.querySelectorAll("paper-tab:not(.hide-tab)");r.length>0&&(this._firstTabWidth=r[0].clientWidth,this._lastTabWidth=r[r.length-1].clientWidth);const o=this.querySelector(".iron-selected");o&&o.scrollIntoView()}},{kind:"method",key:"_affectScroll",value:function(e){if(0===this._firstTabWidth||0===this._lastTabWidth)return;this.$.tabsContainer.scrollLeft+=e;const t=this.$.tabsContainer.scrollLeft;this._leftHidden=t-this._firstTabWidth<0,this._rightHidden=t+this._lastTabWidth>this._tabContainerScrollSize,this._lastLeftHiddenState!==this._leftHidden&&(this._lastLeftHiddenState=this._leftHidden,this.$.tabsContainer.scrollLeft+=this._leftHidden?-23:23)}}]}}),f)},57066:(e,t,i)=>{"use strict";i.d(t,{Lo:()=>s,IO:()=>a,qv:()=>l,sG:()=>h});var r=i(31497),o=i(85415),n=i(38346);const s=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),a=(e,t,i)=>e.callWS({type:"config/area_registry/update",area_id:t,...i}),l=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),c=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,t)=>(0,o.q)(e.name,t.name))))),d=(e,t)=>e.subscribeEvents((0,n.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"area_registry_updated"),h=(e,t)=>(0,r.B)("_areaRegistry",c,d,e,t)},57292:(e,t,i)=>{"use strict";i.d(t,{jL:()=>s,y_:()=>a,t1:()=>l,q4:()=>h});var r=i(31497),o=i(91741),n=i(38346);const s=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,r=e.states[t];if(r)return(0,o.C)(r)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device"),a=(e,t)=>e.filter((e=>e.area_id===t)),l=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),c=e=>e.sendMessagePromise({type:"config/device_registry/list"}),d=(e,t)=>e.subscribeEvents((0,n.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),h=(e,t)=>(0,r.B)("_dr",c,d,e,t)},15327:(e,t,i)=>{"use strict";i.d(t,{eL:()=>r,SN:()=>o,id:()=>n,fg:()=>s,j2:()=>a,JR:()=>l,Y:()=>c,iM:()=>d,Q2:()=>h,Oh:()=>p,vj:()=>u,Gc:()=>f});const r=e=>e.sendMessagePromise({type:"lovelace/resources"}),o=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),n=(e,t,i)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...i}),s=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),a=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),c=(e,t,i)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...i}),d=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),h=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i}),p=(e,t,i)=>e.callWS({type:"lovelace/config/save",url_path:t,config:i}),u=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),f=(e,t,i)=>e.subscribeEvents((e=>{e.data.url_path===t&&i()}),"lovelace_updated")},77760:(e,t,i)=>{"use strict";i.d(t,{VG:()=>b,Gg:()=>x});var r=i(50674),o=i(7323),n=i(49706),s=i(58831),a=i(27269),l=i(22311),c=i(91741);var d=i(85415);const h=async(e,t)=>new Promise((i=>{const r=t(e,(e=>{r(),i(e)}))}));var p=i(57066),u=i(57292),f=i(74186),m=i(5986),v=i(41499);const y=new Set(["automation","configurator","device_tracker","geo_location","persistent_notification","zone"]),g=new Set(["mobile_app"]);let w=!1;const b=(e,t,i=!1)=>{const r=[],o=[],n=t.title?`${t.title} `:void 0;for(const[t,a]of e){const e=(0,s.M)(t);if("alarm_control_panel"===e){const e={type:"alarm-panel",entity:t};r.push(e)}else if("camera"===e){const e={type:"picture-entity",entity:t};r.push(e)}else if("climate"===e){const e={type:"thermostat",entity:t};r.push(e)}else if("humidifier"===e){const e={type:"humidifier",entity:t};r.push(e)}else if("light"===e&&i){const e={type:"light",entity:t};r.push(e)}else if("media_player"===e){const e={type:"media-control",entity:t};r.push(e)}else if("plant"===e){const e={type:"plant-status",entity:t};r.push(e)}else if("weather"===e){const e={type:"weather-forecast",entity:t,show_forecast:!1};r.push(e)}else if("sensor"===e&&(null==a?void 0:a.attributes.device_class)===v.A);else{let e;const i=n&&a&&(e=(0,c.C)(a))!==n&&e.startsWith(n)?{entity:t,name:k(e.substr(n.length))}:t;o.push(i)}}return o.length>0&&r.unshift({type:"entities",entities:o,...t}),r},k=e=>{return(t=e.substr(0,e.indexOf(" "))).toLowerCase()!==t?e:e[0].toUpperCase()+e.slice(1);var t},_=(e,t,i,r,o,n)=>{const a=(e=>{const t=[],i={};return Object.keys(e).forEach((r=>{const o=e[r];"group"===(0,s.M)(r)?t.push(o):i[r]=o})),t.forEach((e=>e.attributes.entity_id.forEach((e=>{delete i[e]})))),{groups:t,ungrouped:i}})(o);a.groups.sort(((e,t)=>n[e.entity_id]-n[t.entity_id]));const h={};Object.keys(a.ungrouped).forEach((e=>{const t=a.ungrouped[e],i=(0,l.N)(t);i in h||(h[i]=[]),h[i].push(t.entity_id)}));let p=[];a.groups.forEach((e=>{p=p.concat(b(e.attributes.entity_id.map((e=>[e,o[e]])),{title:(0,c.C)(e),show_header_toggle:"hidden"!==e.attributes.control}))})),Object.keys(h).sort().forEach((t=>{p=p.concat(b(h[t].sort(((e,t)=>(0,d.q)((0,c.C)(o[e]),(0,c.C)(o[t])))).map((e=>[e,o[e]])),{title:(0,m.Lh)(e,t)}))}));const u={path:t,title:i,cards:p};return r&&(u.icon=r),u},E=(e,t,i,r,o)=>{const n=((e,t)=>{const i={},r=new Set(t.filter((e=>g.has(e.platform))).map((e=>e.entity_id)));return Object.keys(e).forEach((t=>{const o=e[t];y.has((0,l.N)(o))||r.has(o.entity_id)||(i[t]=e[t])})),i})(r,i),s={};Object.keys(n).forEach((e=>{const t=n[e];t.attributes.order&&(s[e]=t.attributes.order)}));const a=((e,t,i,r)=>{const o={...r},n=[];for(const r of e){const e=[],s=new Set(t.filter((e=>e.area_id===r.area_id)).map((e=>e.id)));for(const t of i)(s.has(t.device_id)&&!t.area_id||t.area_id===r.area_id)&&t.entity_id in o&&(e.push(o[t.entity_id]),delete o[t.entity_id]);e.length>0&&n.push([r,e])}return{areasWithEntities:n,otherEntities:o}})(e,t,i,n),c=_(o,"default_view","Home",undefined,a.otherEntities,s),d=[];return a.areasWithEntities.forEach((([e,t])=>{d.push(...b(t.map((e=>[e.entity_id,e])),{title:e.name}))})),c.cards.unshift(...d),c},C=async(e,t,i,r,l,d)=>{if(e.config.safe_mode)return{title:e.config.location_name,views:[{cards:[{type:"safe-mode"}]}]};const h=(e=>{const t=[];return Object.keys(e).forEach((i=>{const r=e[i];r.attributes.view&&t.push(r)})),t.sort(((e,t)=>e.entity_id===n.a1?-1:t.entity_id===n.a1?1:e.attributes.order-t.attributes.order)),t})(l),p=h.map((e=>{const t=((e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const r=e[t];if(r&&(i[r.entity_id]=r,"group"===(0,s.M)(r.entity_id))){const t=((e,t)=>{const i={};return t.attributes.entity_id.forEach((t=>{const r=e[t];r&&(i[r.entity_id]=r)})),i})(e,r);Object.keys(t).forEach((e=>{const r=t[e];i[e]=r}))}})),i})(l,e),i={};return Object.keys(t).forEach(((e,t)=>{i[e]=t})),_(d,(0,a.p)(e.entity_id),(0,c.C)(e),e.attributes.icon,t,i)}));let u=e.config.location_name;return 0!==h.length&&h[0].entity_id===n.a1||(p.unshift(E(t,i,r,l,d)),(0,o.p)(e,"geo_location")&&p[0]&&p[0].cards&&p[0].cards.push({type:"map",geo_location_sources:["all"]}),p.length>1&&"Home"===u&&(u="Open Peer Power")),1===p.length&&0===p[0].cards.length&&p[0].cards.push({type:"empty-state"}),{title:u,views:p}},x=async(e,t)=>{if(e.config.state===r.UE)return{title:e.config.location_name,views:[{cards:[{type:"starting"}]}]};if(e.config.safe_mode)return{title:e.config.location_name,views:[{cards:[{type:"safe-mode"}]}]};w||(w=!0,(0,p.sG)(e.connection,(()=>{})),(0,u.q4)(e.connection,(()=>{})),(0,f.LM)(e.connection,(()=>{})));const[i,o,n]=await Promise.all([h(e.connection,p.sG),h(e.connection,u.q4),h(e.connection,f.LM)]);return C(e,i,o,n,e.states,t||e.localize)}},68500:(e,t,i)=>{"use strict";i.d(t,{k:()=>s});var r=i(69470);const o={},n={},s=(e,t)=>e.forEach((e=>{const i=new URL(e.url,t).toString();switch(e.type){case"css":if(i in o)break;o[i]=(0,r.j)(i);break;case"js":if(i in n)break;n[i]=(0,r.fs)(i);break;case"module":(0,r.$y)(i);break;default:console.warn(`Unknown resource type specified: ${e.type}`)}}))},73953:(e,t,i)=>{"use strict";i.d(t,{J:()=>s});i(71948);var r=i(7778);const o=new Set(["error","state-label"]),n={"entity-filter":()=>i.e(8045).then(i.bind(i,68045))},s=e=>(0,r.Tw)("badge",e,o,n,void 0,"state-label")},97504:(e,t,i)=>{"use strict";i.d(t,{L:()=>o,F:()=>n});var r=i(47181);const o=()=>Promise.all([i.e(5906),i.e(9494),i.e(1960),i.e(6133),i.e(1480),i.e(5796),i.e(7065),i.e(2979),i.e(4077),i.e(1687)]).then(i.bind(i,52408)),n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-create-card",dialogImport:o,dialogParams:t})}},62765:(e,t,i)=>{"use strict";i.d(t,{K:()=>o,k:()=>n});var r=i(47181);const o=()=>Promise.all([i.e(5009),i.e(6076),i.e(5050)]).then(i.bind(i,95050)),n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-delete-card",dialogImport:o,dialogParams:t})}},18678:(e,t,i)=>{"use strict";i.d(t,{I:()=>o,x:()=>n});var r=i(47181);const o=()=>Promise.all([i.e(5009),i.e(2955),i.e(8161),i.e(9543),i.e(8374),i.e(5906),i.e(9494),i.e(3098),i.e(9033),i.e(3304),i.e(6087),i.e(6133),i.e(1456),i.e(4507),i.e(6966),i.e(4535),i.e(8101),i.e(6902),i.e(8331),i.e(7580),i.e(167),i.e(2231),i.e(858)]).then(i.bind(i,90705)),n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-edit-card",dialogImport:o,dialogParams:t})}},54324:(e,t,i)=>{"use strict";i.d(t,{Z0:()=>r,BN:()=>o,LG:()=>n,f1:()=>s,qD:()=>a,Y7:()=>l,wI:()=>c,Uo:()=>d,YI:()=>h,mA:()=>p,PT:()=>u});const r=(e,t,i)=>{const[r]=t,o=[];return e.views.forEach(((t,n)=>{if(n!==r)return void o.push(e.views[n]);const s=t.cards?[...t.cards,i]:[i];o.push({...t,cards:s})})),{...e,views:o}},o=(e,t,i)=>{const[r]=t,o=[];return e.views.forEach(((t,n)=>{if(n!==r)return void o.push(e.views[n]);const s=t.cards?[...t.cards,...i]:[...i];o.push({...t,cards:s})})),{...e,views:o}},n=(e,t,i)=>{const[r,o]=t,n=[];return e.views.forEach(((t,s)=>{s===r?n.push({...t,cards:(t.cards||[]).map(((e,t)=>t===o?i:e))}):n.push(e.views[s])})),{...e,views:n}},s=(e,t)=>{const[i,r]=t,o=[];return e.views.forEach(((t,n)=>{n===i?o.push({...t,cards:(t.cards||[]).filter(((e,t)=>t!==r))}):o.push(e.views[n])})),{...e,views:o}},a=(e,t,i)=>{const[r,o]=t,n=[];return e.views.forEach(((t,s)=>{if(s!==r)return void n.push(e.views[s]);const a=t.cards?[...t.cards.slice(0,o),i,...t.cards.slice(o)]:[i];n.push({...t,cards:a})})),{...e,views:n}},l=(e,t,i)=>{const r=e.views[t[0]].cards[t[1]],o=e.views[i[0]].cards[i[1]],n=e.views[t[0]],s={...n,cards:n.cards.map(((e,i)=>i===t[1]?o:e))},a=t[0]===i[0]?s:e.views[i[0]],l={...a,cards:a.cards.map(((e,t)=>t===i[1]?r:e))};return{...e,views:e.views.map(((e,r)=>r===i[0]?l:r===t[0]?s:e))}},c=(e,t,i)=>{if(t[0]===i[0])throw new Error("You can not move a card to the view it is in.");const r=e.views[t[0]],o=r.cards[t[1]],n={...r,cards:(r.cards||[]).filter(((e,i)=>i!==t[1]))},s=e.views[i[0]],a=s.cards?[...s.cards,o]:[o],l={...s,cards:a};return{...e,views:e.views.map(((e,r)=>r===i[0]?l:r===t[0]?n:e))}},d=(e,t)=>({...e,views:e.views.concat(t)}),h=(e,t,i)=>({...e,views:e.views.map(((e,r)=>r===t?i:e))}),p=(e,t,i)=>{const r=e.views[t],o=e.views[i];return{...e,views:e.views.map(((e,n)=>n===i?r:n===t?o:e))}},u=(e,t)=>({...e,views:e.views.filter(((e,i)=>i!==t))})},3887:(e,t,i)=>{"use strict";i.r(t);i(53918);var r=i(60461),o=i.n(r),n=i(15652),s=i(5986),a=i(15327),l=(i(76816),i(13076),i(81796)),c=i(77760),d=i(68500),h=i(47181);const p="show-save-config";let u=!1;i(81689);var f=i(55317);i(53268),i(85530);(0,i(28393).VA)("waterfall",{run:function(){this.shadow=this.isOnScreen()&&this.isContentBelow()}});i(12730),i(91441),i(87482);var m=i(81471),v=i(14516),y=i(7323);var g=i(86977),w=i(83849),b=i(15493);const k=e=>{const t=window.location.pathname;return e?t+"?"+e:t};var _=i(87744),E=i(38346),C=i(96151);i(81545),i(16509),i(25230),i(52039);function x(){x=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!S(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return T(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?T(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=O(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:D(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=D(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function P(e){var t,i=O(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function $(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function S(e){return e.decorators&&e.decorators.length}function A(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function D(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function O(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function T(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function z(e,t,i){return(z="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=j(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function j(e){return(j=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var o=x();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(A(n.descriptor)||A(o.descriptor)){if(S(n)||S(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(S(n)){if(S(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}$(n,o)}else t.push(n)}return t}(s.d.map(P)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("ha-icon-button-arrow-next")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_icon",value:()=>f.aIO},{kind:"method",key:"connectedCallback",value:function(){z(j(i.prototype),"connectedCallback",this).call(this),setTimeout((()=>{this._icon="ltr"===window.getComputedStyle(this).direction?f.aIO:f.J3k}),100)}},{kind:"method",key:"render",value:function(){var e;return n.dy`<mwc-icon-button
      .disabled=${this.disabled}
      .label=${this.label||(null===(e=this.opp)||void 0===e?void 0:e.localize("ui.common.next"))||"Next"}
    >
      <ha-svg-icon .path=${this._icon}></ha-svg-icon>
    </mwc-icon-button> `}}]}}),n.oi);i(2315),i(48932),i(46167);var M=i(26765),R=i(27633),L=(i(27849),i(11654)),I=i(27322),F=i(54324);let B=!1;const V="show-edit-lovelace",U=(e,t)=>{B||(B=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:V,dialogTag:"hui-dialog-edit-lovelace",dialogImport:()=>Promise.all([i.e(5009),i.e(1199),i.e(4764)]).then(i.bind(i,74764))})})(e)),(0,h.B)(e,V,t)};let N=!1;const q="show-edit-view",W=(e,t)=>{N||(N=!0,(e=>{(0,h.B)(e,"register-dialog",{dialogShowEvent:q,dialogTag:"hui-dialog-edit-view",dialogImport:()=>Promise.all([i.e(5009),i.e(2955),i.e(9543),i.e(8374),i.e(5906),i.e(3098),i.e(6087),i.e(4535),i.e(6902),i.e(7979)]).then(i.bind(i,18632))})})(e)),(0,h.B)(e,q,t)};var H=i(62877),Q=(i(6315),i(90271)),G=i(73953),Z=i(51153),Y=i(50467);function X(){X=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!ee(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return oe(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?oe(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=re(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:ie(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=ie(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function J(e){var t,i=re(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function K(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ee(e){return e.decorators&&e.decorators.length}function te(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function ie(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function re(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function oe(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function ne(e,t,i){return(ne="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=se(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function se(e){return(se=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let ae=!1;const le=(e,t)=>{let i=0;for(let t=0;t<e.length;t++){if(e[t]<5){i=t;break}e[t]<e[i]&&(i=t)}return e[i]+=t,i};let ce=function(e,t,i,r){var o=X();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(te(n.descriptor)||te(o.descriptor)){if(ee(n)||ee(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(ee(n)){if(ee(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}K(n,o)}else t.push(n)}return t}(s.d.map(J)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this.addEventListener("iron-resize",(e=>e.stopPropagation()))}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"cards",value:()=>[]},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"badges",value:()=>[]},{kind:"field",decorators:[(0,n.sz)()],key:"_columns",value:void 0},{kind:"field",key:"_createColumnsIteration",value:()=>0},{kind:"field",key:"_mqls",value:void 0},{kind:"method",key:"setConfig",value:function(e){}},{kind:"method",key:"render",value:function(){var e;return n.dy`
      <div
        id="badges"
        style=${this.badges.length>0?"display: block":"display: none"}
      >
        ${this.badges.map((e=>n.dy`${e}`))}
      </div>
      <div id="columns"></div>
      ${(null===(e=this.lovelace)||void 0===e?void 0:e.editMode)?n.dy`
            <ha-fab
              .label=${this.opp.localize("ui.panel.lovelace.editor.edit_card.add")}
              extended
              @click=${this._addCard}
              class=${(0,m.$)({rtl:(0,_.HE)(this.opp)})}
            >
              <ha-svg-icon slot="icon" .path=${f.qX5}></ha-svg-icon>
            </ha-fab>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._mqls=[300,600,900,1200].map((e=>{const t=window.matchMedia(`(min-width: ${e}px)`);return t.addListener((()=>this._updateColumns())),t})),this._updateColumns()}},{kind:"method",key:"updated",value:function(e){var t,o,n;if(ne(se(r.prototype),"updated",this).call(this,e),(null===(t=this.lovelace)||void 0===t?void 0:t.editMode)&&!ae&&(ae=!0,Promise.all([i.e(9119),i.e(741)]).then(i.bind(i,70741))),e.has("opp")){const t=e.get("opp");if(t&&this.opp.dockedSidebar!==t.dockedSidebar&&this._updateColumns(),1===e.size)return}e.has("narrow")&&this._updateColumns();const s=e.get("lovelace");(e.has("lovelace")&&((null==s?void 0:s.config)!==(null===(o=this.lovelace)||void 0===o?void 0:o.config)||(null==s?void 0:s.editMode)!==(null===(n=this.lovelace)||void 0===n?void 0:n.editMode))||e.has("_columns"))&&this._createColumns()}},{kind:"method",key:"_addCard",value:function(){(0,h.B)(this,"ll-create-card")}},{kind:"method",key:"_createColumns",value:async function(){if(!this._columns)return;this._createColumnsIteration++;const e=this._createColumnsIteration,t=this.shadowRoot.getElementById("columns");for(;t.lastChild;)t.removeChild(t.lastChild);const i=[],r=[];for(let e=0;e<Math.min(this._columns,this.cards.length);e++){const e=document.createElement("div");e.classList.add("column"),t.appendChild(e),i.push(0),r.push(e)}let o,n;for(const[t,s]of this.cards.entries()){let a;void 0===o&&(o=(0,C.y)().then((()=>{o=void 0,n=void 0}))),void 0===n?n=new Date:(new Date).getTime()-n.getTime()>16&&(a=o);const l=(0,Y.N)(s),[c]=await Promise.all([l,a]);if(e!==this._createColumnsIteration)return;this._addCardToColumn(r[le(i,c)],t,this.lovelace.editMode)}r.forEach((e=>{e.lastChild||e.parentElement.removeChild(e)}))}},{kind:"method",key:"_addCardToColumn",value:function(e,t,i){const r=this.cards[t];if(i){const i=document.createElement("hui-card-options");i.opp=this.opp,i.lovelace=this.lovelace,i.path=[this.index,t],r.editMode=!0,i.appendChild(r),e.appendChild(i)}else r.editMode=!1,e.appendChild(r)}},{kind:"method",key:"_updateColumns",value:function(){if(!this._mqls)return;const e=this._mqls.reduce(((e,t)=>e+Number(t.matches)),0);this._columns=Math.max(1,e-Number(!this.narrow&&"docked"===this.opp.dockedSidebar))}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: block;
        padding-top: 4px;
        height: 100%;
        box-sizing: border-box;
      }

      #badges {
        margin: 8px 16px;
        font-size: 85%;
        text-align: center;
      }

      #columns {
        display: flex;
        flex-direction: row;
        justify-content: center;
        margin-left: 4px;
        margin-right: 4px;
      }

      .column {
        flex: 1 0 0;
        max-width: 500px;
        min-width: 0;
      }

      .column > * {
        display: block;
        margin: var(--masonry-view-card-margin, 4px 4px 8px);
      }

      ha-fab {
        position: sticky;
        float: right;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }

      ha-fab.rtl {
        float: left;
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }

      @media (max-width: 500px) {
        .column > * {
          margin-left: 0;
          margin-right: 0;
        }
      }

      @media (max-width: 599px) {
        .column {
          max-width: 600px;
        }
      }
    `}}]}}),n.oi);customElements.define("hui-masonry-view",ce);var de=i(7778);const he=new Set(["masonry"]),pe={panel:()=>i.e(8480).then(i.bind(i,48480))};var ue=i(97504),fe=i(18678);var me=i(62765);async function ve(e,t,i,r){const o=i.config.views[r[0]].cards[r[1]];(0,me.k)(e,{cardConfig:o,deleteCard:async()=>{try{const n=(0,F.f1)(i.config,r);await i.saveConfig(n);((e,t,i)=>{const r={message:t.localize("ui.common.successfully_deleted")};i&&(r.action={action:i,text:t.localize("ui.common.undo")}),(0,l.C)(e,r)})(e,t,(async()=>{await i.saveConfig((0,F.qD)(n,r,o))}))}catch(t){(0,M.Ys)(e,{text:`Deleting failed: ${t.message}`})}}})}function ye(){ye=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!be(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Ce(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?Ce(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=Ee(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_e(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_e(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function ge(e){var t,i=Ee(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function we(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function be(e){return e.decorators&&e.decorators.length}function ke(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _e(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function Ee(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Ce(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function xe(e,t,i){return(xe="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Pe(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function Pe(e){return(Pe=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var o=ye();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(ke(n.descriptor)||ke(o.descriptor)){if(be(n)||be(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(be(n)){if(be(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}we(n,o)}else t.push(n)}return t}(s.d.map(ge)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-view")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_cards",value:()=>[]},{kind:"field",decorators:[(0,n.sz)()],key:"_badges",value:()=>[]},{kind:"field",key:"_layoutElementType",value:void 0},{kind:"field",key:"_layoutElement",value:void 0},{kind:"method",key:"createCardElement",value:function(e){const t=(0,Z.Z6)(e);return t.opp=this.opp,t.addEventListener("ll-rebuild",(i=>{this.lovelace.editMode||(i.stopPropagation(),this._rebuildCard(t,e))}),{once:!0}),t}},{kind:"method",key:"createBadgeElement",value:function(e){const t=(0,G.J)(e);return t.opp=this.opp,t.addEventListener("ll-badge-rebuild",(()=>{this._rebuildBadge(t,e)}),{once:!0}),t}},{kind:"method",key:"updated",value:function(e){xe(Pe(i.prototype),"updated",this).call(this,e);const t=this.opp,r=this.lovelace,o=e.has("opp"),n=e.get("lovelace");let s,a=!1,l=!1;e.has("index")?l=!0:e.has("lovelace")&&(a=n&&r.editMode!==n.editMode,l=!n||r.config!==n.config),l&&(s=r.config.views[this.index],s={...s,type:s.panel?"panel":s.type||"masonry"});let c=!1;var d;!l||this._layoutElement&&this._layoutElementType===s.type||(c=!0,this._layoutElement=(d=s,(0,de.Tw)("view",d,he,pe)),this._layoutElementType=s.type,this._layoutElement.addEventListener("ll-create-card",(()=>{(0,ue.F)(this,{lovelaceConfig:this.lovelace.config,saveConfig:this.lovelace.saveConfig,path:[this.index]})})),this._layoutElement.addEventListener("ll-edit-card",(e=>{(0,fe.x)(this,{lovelaceConfig:this.lovelace.config,saveConfig:this.lovelace.saveConfig,path:e.detail.path})})),this._layoutElement.addEventListener("ll-delete-card",(e=>{ve(this,this.opp,this.lovelace,e.detail.path)}))),l&&(this._createBadges(s),this._createCards(s),this._layoutElement.opp=this.opp,this._layoutElement.narrow=this.narrow,this._layoutElement.lovelace=r,this._layoutElement.index=this.index),o&&(this._badges.forEach((e=>{e.opp=t})),this._cards.forEach((e=>{e.opp=t})),this._layoutElement.opp=this.opp),e.has("narrow")&&(this._layoutElement.narrow=this.narrow),a&&(this._layoutElement.lovelace=r),(l||o||a||e.has("_cards")||e.has("_badges"))&&(this._layoutElement.cards=this._cards,this._layoutElement.badges=this._badges);const h=e.get("opp");if((l||a||o&&h&&(t.themes!==h.themes||t.selectedTheme!==h.selectedTheme))&&(0,H.R)(this,t.themes,r.config.views[this.index].theme),this._layoutElement&&c){for(;this.lastChild;)this.removeChild(this.lastChild);this.appendChild(this._layoutElement)}}},{kind:"method",key:"_createBadges",value:function(e){if(!e||!e.badges||!Array.isArray(e.badges))return void(this._badges=[]);const t=(0,Q.A)(e.badges);this._badges=t.map((e=>{const t=(0,G.J)(e);return t.opp=this.opp,t}))}},{kind:"method",key:"_createCards",value:function(e){e&&e.cards&&Array.isArray(e.cards)?this._cards=e.cards.map((e=>{const t=this.createCardElement(e);return t.opp=this.opp,t})):this._cards=[]}},{kind:"method",key:"_rebuildCard",value:function(e,t){const i=this.createCardElement(t);i.opp=this.opp,e.parentElement&&e.parentElement.replaceChild(i,e),this._cards=this._cards.map((t=>t===e?i:t))}},{kind:"method",key:"_rebuildBadge",value:function(e,t){const i=this.createBadgeElement(t);i.opp=this.opp,e.parentElement&&e.parentElement.replaceChild(i,e),this._badges=this._badges.map((t=>t===e?i:t))}}]}}),n.f4);function $e(){$e=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!De(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return je(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?je(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=ze(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Te(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=Te(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function Se(e){var t,i=ze(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function Ae(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function De(e){return e.decorators&&e.decorators.length}function Oe(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Te(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function ze(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function je(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function Me(e,t,i){return(Me="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Re(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function Re(e){return(Re=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let Le=function(e,t,i,r){var o=$e();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(Oe(n.descriptor)||Oe(o.descriptor)){if(De(n)||De(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(De(n)){if(De(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}Ae(n,o)}else t.push(n)}return t}(s.d.map(Se)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._debouncedConfigChanged=(0,E.D)((()=>this._selectView(this._curView,!0)),100,!1)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_curView",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-app-layout",!0)],key:"_appLayout",value:void 0},{kind:"field",key:"_viewCache",value:void 0},{kind:"field",key:"_debouncedConfigChanged",value:void 0},{kind:"field",key:"_conversation",value(){return(0,v.Z)((e=>(0,y.p)(this.opp,"conversation")))}},{kind:"method",key:"render",value:function(){var e,t,i,r;return n.dy`
      <ha-app-layout
        class=${(0,m.$)({"edit-mode":this._editMode})}
        id="layout"
      >
        <app-header slot="header" effects="waterfall" fixed condenses>
          ${this._editMode?n.dy`
                <app-toolbar class="edit-mode">
                  <mwc-icon-button
                    .label="${this.opp.localize("ui.panel.lovelace.menu.exit_edit_mode")}"
                    title="${this.opp.localize("ui.panel.lovelace.menu.close")}"
                    @click="${this._editModeDisable}"
                  >
                    <ha-svg-icon .path=${f.r5M}></ha-svg-icon>
                  </mwc-icon-button>
                  <div main-title>
                    ${this.config.title||this.opp.localize("ui.panel.lovelace.editor.header")}
                    <mwc-icon-button
                      aria-label="${this.opp.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      title="${this.opp.localize("ui.panel.lovelace.editor.edit_lovelace.edit_title")}"
                      class="edit-icon"
                      @click="${this._editLovelace}"
                    >
                      <ha-svg-icon .path=${f.r9}></ha-svg-icon>
                    </mwc-icon-button>
                  </div>
                  <a
                    href="${(0,I.R)(this.opp,"/lovelace/")}"
                    rel="noreferrer"
                    class="menu-link"
                    target="_blank"
                  >
                    <mwc-icon-button
                      title="${this.opp.localize("ui.panel.lovelace.menu.help")}"
                    >
                      <ha-svg-icon .path=${f.Xc_}></ha-svg-icon>
                    </mwc-icon-button>
                  </a>
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .title="${this.opp.localize("ui.panel.lovelace.editor.menu.open")}"
                      .label=${this.opp.localize("ui.panel.lovelace.editor.menu.open")}
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.opp.localize("ui.panel.lovelace.unused_entities.title")}
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.lAj}
                            >
                            </ha-svg-icon>
                            ${this.opp.localize("ui.panel.lovelace.unused_entities.title")}
                          </mwc-list-item>
                        `}
                    <mwc-list-item
                      graphic="icon"
                      @request-selected="${this._handleRawEditor}"
                    >
                      <ha-svg-icon
                        slot="graphic"
                        .path=${f.bl5}
                      ></ha-svg-icon>
                      ${this.opp.localize("ui.panel.lovelace.editor.menu.raw_editor")}
                    </mwc-list-item>
                    ${n.dy`<mwc-list-item
                            graphic="icon"
                            @request-selected="${this._handleManageDashboards}"
                          >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.Ccq}
                            ></ha-svg-icon>
                            ${this.opp.localize("ui.panel.lovelace.editor.menu.manage_dashboards")}
                          </mwc-list-item>
                          ${(null===(e=this.opp.userData)||void 0===e?void 0:e.showAdvanced)?n.dy`<mwc-list-item
                                graphic="icon"
                                @request-selected="${this._handleManageResources}"
                              >
                                <ha-svg-icon
                                  slot="graphic"
                                  .path=${f.b82}
                                ></ha-svg-icon>
                                ${this.opp.localize("ui.panel.lovelace.editor.menu.manage_resources")}
                              </mwc-list-item>`:""} `}
                  </ha-button-menu>
                </app-toolbar>
              `:n.dy`
                <app-toolbar>
                  <ha-menu-button
                    .opp=${this.opp}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                  ${this.lovelace.config.views.length>1?n.dy`
                        <ha-tabs
                          scrollable
                          .selected="${this._curView}"
                          @iron-activate="${this._handleViewSelected}"
                          dir="${(0,_.Zu)(this.opp)}"
                        >
                          ${this.lovelace.config.views.map((e=>n.dy`
                              <paper-tab
                                aria-label="${e.title}"
                                class="${(0,m.$)({"hide-tab":Boolean(void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.opp.user.id))||!1===e.visible))})}"
                              >
                                ${e.icon?n.dy`
                                      <ha-icon
                                        title="${e.title}"
                                        .icon="${e.icon}"
                                      ></ha-icon>
                                    `:e.title||"Unnamed view"}
                              </paper-tab>
                            `))}
                        </ha-tabs>
                      `:n.dy`<div main-title>${this.config.title}</div>`}
                  ${!this.narrow&&this._conversation(this.opp.config.components)?n.dy`
                        <mwc-icon-button
                          .label=${this.opp.localize("ui.panel.lovelace.menu.start_conversation")}
                          @click=${this._showVoiceCommandDialog}
                        >
                          <ha-svg-icon .path=${f.N3O}></ha-svg-icon>
                        </mwc-icon-button>
                      `:""}
                  <ha-button-menu corner="BOTTOM_START">
                    <mwc-icon-button
                      slot="trigger"
                      .label=${this.opp.localize("ui.panel.lovelace.editor.menu.open")}
                      .title="${this.opp.localize("ui.panel.lovelace.editor.menu.open")}"
                    >
                      <ha-svg-icon .path=${f.SXi}></ha-svg-icon>
                    </mwc-icon-button>
                    ${this.narrow&&this._conversation(this.opp.config.components)?n.dy`
                          <mwc-list-item
                            .label=${this.opp.localize("ui.panel.lovelace.menu.start_conversation")}
                            graphic="icon"
                            @request-selected=${this._showVoiceCommandDialog}
                          >
                            <span
                              >${this.opp.localize("ui.panel.lovelace.menu.start_conversation")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.N3O}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${this._yamlMode?n.dy`
                          <mwc-list-item
                            aria-label=${this.opp.localize("ui.common.refresh")}
                            graphic="icon"
                            @request-selected="${this._handleRefresh}"
                          >
                            <span
                              >${this.opp.localize("ui.common.refresh")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                          <mwc-list-item
                            aria-label=${this.opp.localize("ui.panel.lovelace.unused_entities.title")}
                            graphic="icon"
                            @request-selected="${this._handleUnusedEntities}"
                          >
                            <span
                              >${this.opp.localize("ui.panel.lovelace.unused_entities.title")}</span
                            >
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.RIj}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${"yaml"===(null===(t=this.opp.panels.lovelace)||void 0===t||null===(i=t.config)||void 0===i?void 0:i.mode)?n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.opp.localize("ui.panel.lovelace.menu.reload_resources")}
                            @request-selected=${this._handleReloadResources}
                          >
                            ${this.opp.localize("ui.panel.lovelace.menu.reload_resources")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.jcD}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    ${(null===(r=this.opp.user)||void 0===r?void 0:r.is_admin)&&!this.opp.config.safe_mode?n.dy`
                          <mwc-list-item
                            graphic="icon"
                            aria-label=${this.opp.localize("ui.panel.lovelace.menu.configure_ui")}
                            @request-selected=${this._handleEnableEditMode}
                          >
                            ${this.opp.localize("ui.panel.lovelace.menu.configure_ui")}
                            <ha-svg-icon
                              slot="graphic"
                              .path=${f.Shd}
                            ></ha-svg-icon>
                          </mwc-list-item>
                        `:""}
                    <a
                      href="${(0,I.R)(this.opp,"/lovelace/")}"
                      rel="noreferrer"
                      class="menu-link"
                      target="_blank"
                    >
                      <mwc-list-item
                        graphic="icon"
                        aria-label=${this.opp.localize("ui.panel.lovelace.menu.help")}
                      >
                        ${this.opp.localize("ui.panel.lovelace.menu.help")}
                        <ha-svg-icon
                          slot="graphic"
                          .path=${f.HET}
                        ></ha-svg-icon>
                      </mwc-list-item>
                    </a>
                  </ha-button-menu>
                </app-toolbar>
              `}
          ${this._editMode?n.dy`
                <div sticky>
                  <paper-tabs
                    scrollable
                    .selected="${this._curView}"
                    @iron-activate="${this._handleViewSelected}"
                    dir="${(0,_.Zu)(this.opp)}"
                  >
                    ${this.lovelace.config.views.map((e=>n.dy`
                        <paper-tab
                          aria-label="${e.title}"
                          class="${(0,m.$)({"hide-tab":Boolean(!this._editMode&&void 0!==e.visible&&(Array.isArray(e.visible)&&!e.visible.some((e=>e.user===this.opp.user.id))||!1===e.visible))})}"
                        >
                          ${this._editMode?n.dy`
                                <ha-icon-button-arrow-prev
                                  .opp=${this.opp}
                                  .title="${this.opp.localize("ui.panel.lovelace.editor.edit_view.move_left")}"
                                  .label="${this.opp.localize("ui.panel.lovelace.editor.edit_view.move_left")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewLeft}"
                                  ?disabled="${0===this._curView}"
                                ></ha-icon-button-arrow-prev>
                              `:""}
                          ${e.icon?n.dy`
                                <ha-icon
                                  title="${e.title}"
                                  .icon="${e.icon}"
                                ></ha-icon>
                              `:e.title||"Unnamed view"}
                          ${this._editMode?n.dy`
                                <ha-svg-icon
                                  title="${this.opp.localize("ui.panel.lovelace.editor.edit_view.edit")}"
                                  class="edit-icon view"
                                  .path=${f.r9}
                                  @click="${this._editView}"
                                ></ha-svg-icon>
                                <ha-icon-button-arrow-next
                                  .opp=${this.opp}
                                  .title="${this.opp.localize("ui.panel.lovelace.editor.edit_view.move_right")}"
                                  .label="${this.opp.localize("ui.panel.lovelace.editor.edit_view.move_right")}"
                                  class="edit-icon view"
                                  @click="${this._moveViewRight}"
                                  ?disabled="${this._curView+1===this.lovelace.config.views.length}"
                                ></ha-icon-button-arrow-next>
                              `:""}
                        </paper-tab>
                      `))}
                    ${this._editMode?n.dy`
                          <mwc-icon-button
                            id="add-view"
                            @click="${this._addView}"
                            title="${this.opp.localize("ui.panel.lovelace.editor.edit_view.add")}"
                          >
                            <ha-svg-icon .path=${f.qX5}></ha-svg-icon>
                          </mwc-icon-button>
                        `:""}
                  </paper-tabs>
                </div>
              `:""}
        </app-header>
        <div id="view" @ll-rebuild="${this._debouncedConfigChanged}"></div>
      </ha-app-layout>
    `}},{kind:"field",key:"_isVisible",value(){return e=>Boolean(this._editMode||void 0===e.visible||!0===e.visible||Array.isArray(e.visible)&&e.visible.some((e=>{var t;return e.user===(null===(t=this.opp.user)||void 0===t?void 0:t.id)})))}},{kind:"method",key:"firstUpdated",value:function(){"1"===(0,b.io)("edit")&&this._enableEditMode()}},{kind:"method",key:"updated",value:function(e){Me(Re(r.prototype),"updated",this).call(this,e);const t=this._viewRoot.lastChild;let i;e.has("opp")&&t&&(t.opp=this.opp),e.has("narrow")&&t&&(t.narrow=this.narrow);let o=!1;const n=this.route.path.split("/")[1];if(e.has("route")){const e=this.config.views;if(!n&&e.length)i=e.findIndex(this._isVisible),this._navigateToView(e[i].path||i,!0);else if("opp-unused-entities"===n)i="opp-unused-entities";else if(n){const t=n,r=Number(t);let o=0;for(let i=0;i<e.length;i++)if(e[i].path===t||i===r){o=i;break}i=o}}if(e.has("lovelace")){const r=e.get("lovelace");if(r&&r.config===this.lovelace.config||(o=!0),!r||r.editMode!==this.lovelace.editMode){const e=this.config&&this.config.views;(0,h.B)(this,"iron-resize"),"storage"===this.lovelace.mode&&"opp-unused-entities"===n&&(i=e.findIndex(this._isVisible),this._navigateToView(e[i].path||i,!0))}!o&&t&&(t.lovelace=this.lovelace)}(void 0!==i||o)&&(o&&void 0===i&&(i=this._curView),(0,C.T)((()=>this._selectView(i,o))))}},{kind:"get",key:"config",value:function(){return this.lovelace.config}},{kind:"get",key:"_yamlMode",value:function(){return"yaml"===this.lovelace.mode}},{kind:"get",key:"_editMode",value:function(){return this.lovelace.editMode}},{kind:"get",key:"_layout",value:function(){return this.shadowRoot.getElementById("layout")}},{kind:"get",key:"_viewRoot",value:function(){return this.shadowRoot.getElementById("view")}},{kind:"method",key:"_handleRefresh",value:function(e){(0,g.Q)(e)&&(0,h.B)(this,"config-refresh")}},{kind:"method",key:"_handleReloadResources",value:function(e){(0,g.Q)(e)&&(this.opp.callService("lovelace","reload_resources"),(0,M.g7)(this,{title:this.opp.localize("ui.panel.lovelace.reload_resources.refresh_header"),text:this.opp.localize("ui.panel.lovelace.reload_resources.refresh_body"),confirmText:this.opp.localize("ui.common.refresh"),dismissText:this.opp.localize("ui.common.not_now"),confirm:()=>location.reload()}))}},{kind:"method",key:"_handleRawEditor",value:function(e){(0,g.Q)(e)&&this.lovelace.enableFullEditMode()}},{kind:"method",key:"_handleManageDashboards",value:function(e){(0,g.Q)(e)&&(0,w.c)(this,"/config/lovelace/dashboards")}},{kind:"method",key:"_handleManageResources",value:function(e){(0,g.Q)(e)&&(0,w.c)(this,"/config/lovelace/resources")}},{kind:"method",key:"_handleUnusedEntities",value:function(e){var t;(0,g.Q)(e)&&(0,w.c)(this,`${null===(t=this.route)||void 0===t?void 0:t.prefix}/opp-unused-entities`)}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,R._)(this)}},{kind:"method",key:"_handleEnableEditMode",value:function(e){(0,g.Q)(e)&&(this._yamlMode?(0,M.Ys)(this,{text:"The edit UI is not available when in YAML mode."}):this._enableEditMode())}},{kind:"method",key:"_enableEditMode",value:function(){this.lovelace.setEditMode(!0),window.history.replaceState(null,"",k((0,b.j4)({edit:"1"})))}},{kind:"method",key:"_editModeDisable",value:function(){this.lovelace.setEditMode(!1),window.history.replaceState(null,"",k((0,b.pc)("edit")))}},{kind:"method",key:"_editLovelace",value:function(){U(this,this.lovelace)}},{kind:"method",key:"_navigateToView",value:function(e,t){this.lovelace.editMode?(0,w.c)(this,`${this.route.prefix}/${e}?${(0,b.j4)({edit:"1"})}`,t):(0,w.c)(this,`${this.route.prefix}/${e}`,t)}},{kind:"method",key:"_editView",value:function(){W(this,{lovelace:this.lovelace,viewIndex:this._curView})}},{kind:"method",key:"_moveViewLeft",value:function(){if(0===this._curView)return;const e=this.lovelace,t=this._curView,i=this._curView-1;this._curView=i,e.saveConfig((0,F.mA)(e.config,t,i))}},{kind:"method",key:"_moveViewRight",value:function(){if(this._curView+1===this.lovelace.config.views.length)return;const e=this.lovelace,t=this._curView,i=this._curView+1;this._curView=i,e.saveConfig((0,F.mA)(e.config,t,i))}},{kind:"method",key:"_addView",value:function(){W(this,{lovelace:this.lovelace,saveCallback:(e,t)=>{const i=t.path||e;this._navigateToView(i)}})}},{kind:"method",key:"_handleViewSelected",value:function(e){const t=e.detail.selected;if(t!==this._curView){const e=this.config.views[t].path||t;this._navigateToView(e)}!function(e,t){const i=t,r=Math.random(),o=Date.now(),n=i.scrollTop,s=0-n;e._currentAnimationId=r,function t(){const a=Date.now()-o;var l;a>200?i.scrollTop=0:e._currentAnimationId===r&&(i.scrollTop=(l=a,-s*(l/=200)*(l-2)+n),requestAnimationFrame(t.bind(e)))}.call(e)}(this,this._layout.header.scrollTarget)}},{kind:"method",key:"_selectView",value:function(e,t){if(!t&&this._curView===e)return;e=void 0===e?0:e,this._curView=e,t&&(this._viewCache={});const r=this._viewRoot;if(r.lastChild&&r.removeChild(r.lastChild),"opp-unused-entities"===e){const e=document.createElement("hui-unused-entities");return Promise.all([i.e(9494),i.e(1960),i.e(9119),i.e(7065),i.e(9123)]).then(i.bind(i,28279)).then((()=>{e.opp=this.opp,e.lovelace=this.lovelace,e.narrow=this.narrow})),void r.appendChild(e)}let o;const n=this.config.views[e];if(!n)return void this._enableEditMode();!t&&this._viewCache[e]?o=this._viewCache[e]:(o=document.createElement("hui-view"),o.index=e,this._viewCache[e]=o),o.lovelace=this.lovelace,o.opp=this.opp,o.narrow=this.narrow;const s=n.background||this.config.background;s?this._appLayout.style.setProperty("--lovelace-background",s):this._appLayout.style.removeProperty("--lovelace-background"),r.appendChild(o),(0,h.B)(this,"iron-resize")}},{kind:"get",static:!0,key:"styles",value:function(){return[L.Qx,n.iv`
        :host {
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
        }

        ha-app-layout {
          min-height: 100%;
        }
        ha-tabs {
          width: 100%;
          height: 100%;
          margin-left: 4px;
        }
        paper-tabs {
          margin-left: 12px;
          margin-left: max(env(safe-area-inset-left), 12px);
          margin-right: env(safe-area-inset-right);
        }
        ha-tabs,
        paper-tabs {
          --paper-tabs-selection-bar-color: var(
            --app-header-selection-bar-color,
            var(--app-header-text-color, #fff)
          );
          text-transform: uppercase;
        }

        .edit-mode app-header,
        .edit-mode app-toolbar {
          background-color: var(--app-header-edit-background-color, #455a64);
          color: var(--app-header-edit-text-color, #fff);
        }
        .edit-mode div[main-title] {
          pointer-events: auto;
        }
        paper-tab.iron-selected .edit-icon {
          display: inline-flex;
        }
        .edit-icon {
          color: var(--accent-color);
          padding-left: 8px;
          vertical-align: middle;
          --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
        }
        .edit-icon.view {
          display: none;
        }
        #add-view {
          position: absolute;
          height: 44px;
        }
        #add-view ha-svg-icon {
          background-color: var(--accent-color);
          border-radius: 4px;
        }
        app-toolbar a {
          color: var(--text-primary-color, white);
        }
        mwc-button.warning:not([disabled]) {
          color: var(--error-color);
        }
        #view {
          min-height: calc(100vh - var(--header-height));
          /**
          * Since we only set min-height, if child nodes need percentage
          * heights they must use absolute positioning so we need relative
          * positioning here.
          *
          * https://www.w3.org/TR/CSS2/visudet.html#the-height-property
          */
          position: relative;
          display: flex;
        }
        /**
         * In edit mode we have the tab bar on a new line *
         */
        .edit-mode #view {
          min-height: calc(100vh - var(--header-height) - 48px);
        }
        #view > * {
          /**
          * The view could get larger than the window in Firefox
          * to prevent that we set the max-width to 100%
          * flex-grow: 1 and flex-basis: 100% should make sure the view
          * stays full width.
          *
          * https://github.com/openpeerpower/openpeerpower-polymer/pull/3806
          */
          flex: 1 1 100%;
          max-width: 100%;
        }
        .hide-tab {
          display: none;
        }
        .menu-link {
          text-decoration: none;
        }
        hui-view {
          background: var(
            --lovelace-background,
            var(--primary-background-color)
          );
        }
      `]}}]}}),n.oi);function Ie(){Ie=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!Ve(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return We(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?We(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=qe(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Ne(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=Ne(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function Fe(e){var t,i=qe(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function Be(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Ve(e){return e.decorators&&e.decorators.length}function Ue(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Ne(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function qe(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function We(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function He(e,t,i){return(He="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Qe(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function Qe(e){return(Qe=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}customElements.define("hui-root",Le),window.loadCardHelpers=()=>Promise.all([i.e(4909),i.e(319),i.e(7282),i.e(9810),i.e(5457)]).then(i.bind(i,49686));let Ge=!1,Ze=!1,Ye=function(e,t,i,r){var o=Ie();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(Ue(n.descriptor)||Ue(o.descriptor)){if(Ve(n)||Ve(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(Ve(n)){if(Ve(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}Be(n,o)}else t.push(n)}return t}(s.d.map(Fe)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this),this._closeEditor=this._closeEditor.bind(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"panel",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_state",value:()=>"loading"},{kind:"field",decorators:[(0,n.sz)()],key:"_errorMsg",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"lovelace",value:void 0},{kind:"field",key:"_ignoreNextUpdateEvent",value:()=>!1},{kind:"field",key:"_fetchConfigOnConnect",value:()=>!1},{kind:"field",key:"_unsubUpdates",value:void 0},{kind:"method",key:"connectedCallback",value:function(){He(Qe(r.prototype),"connectedCallback",this).call(this),this.lovelace&&this.opp&&this.lovelace.locale!==this.opp.locale?this._setLovelaceConfig(this.lovelace.config,this.lovelace.mode):this.lovelace&&"generated"===this.lovelace.mode?(this._state="loading",this._regenerateConfig()):this._fetchConfigOnConnect&&this._fetchConfig(!1)}},{kind:"method",key:"disconnectedCallback",value:function(){He(Qe(r.prototype),"disconnectedCallback",this).call(this),null!==this.urlPath&&this._unsubUpdates&&this._unsubUpdates()}},{kind:"method",key:"render",value:function(){const e=this._state;return"loaded"===e?n.dy`
        <hui-root
          .opp=${this.opp}
          .lovelace=${this.lovelace}
          .route=${this.route}
          .narrow=${this.narrow}
          @config-refresh=${this._forceFetchConfig}
        ></hui-root>
      `:"error"===e?n.dy`
        <opp-error-screen
          .opp=${this.opp}
          title="${(0,s.Lh)(this.opp.localize,"lovelace")}"
          .error="${this._errorMsg}"
        >
          <mwc-button raised @click=${this._forceFetchConfig}>
            ${this.opp.localize("ui.panel.lovelace.reload_lovelace")}
          </mwc-button>
        </opp-error-screen>
      `:"yaml-editor"===e?n.dy`
        <hui-editor
          .opp=${this.opp}
          .lovelace="${this.lovelace}"
          .closeEditor="${this._closeEditor}"
        ></hui-editor>
      `:n.dy`
      <opp-loading-screen
        rootnav
        .opp=${this.opp}
        .narrow=${this.narrow}
      ></opp-loading-screen>
    `}},{kind:"method",key:"firstUpdated",value:function(){this._fetchConfig(!1),this._unsubUpdates||this._subscribeUpdates(),window.addEventListener("connection-status",(e=>{"connected"===e.detail&&this._fetchConfig(!1)}))}},{kind:"method",key:"_regenerateConfig",value:async function(){const e=await(0,c.Gg)(this.opp);this._setLovelaceConfig(e,"generated"),this._state="loaded"}},{kind:"method",key:"_subscribeUpdates",value:async function(){this._unsubUpdates=await(0,a.Gc)(this.opp.connection,this.urlPath,(()=>this._lovelaceChanged()))}},{kind:"method",key:"_closeEditor",value:function(){this._state="loaded"}},{kind:"method",key:"_lovelaceChanged",value:function(){this._ignoreNextUpdateEvent?this._ignoreNextUpdateEvent=!1:this.isConnected?(0,l.C)(this,{message:this.opp.localize("ui.panel.lovelace.changed_toast.message"),action:{action:()=>this._fetchConfig(!1),text:this.opp.localize("ui.common.refresh")},duration:0,dismissable:!1}):this._fetchConfigOnConnect=!0}},{kind:"get",key:"urlPath",value:function(){return"lovelace"===this.panel.url_path?null:this.panel.url_path}},{kind:"method",key:"_forceFetchConfig",value:function(){this._fetchConfig(!0)}},{kind:"method",key:"_fetchConfig",value:async function(e){let t,i,r=this.panel.config.mode;const o=window;o.llConfProm&&(i=o.llConfProm,o.llConfProm=void 0),Ze||(Ze=!0,(o.llConfProm||(0,a.eL)(this.opp.connection)).then((e=>(0,d.k)(e,this.opp.auth.data.oppUrl)))),null===this.urlPath&&i||(this.lovelace&&"yaml"===this.lovelace.mode&&(this._ignoreNextUpdateEvent=!0),i=(0,a.Q2)(this.opp.connection,this.urlPath,e));try{t=await i}catch(e){if("config_not_found"!==e.code)return console.log(e),this._state="error",void(this._errorMsg=e.message);const i=await this.opp.loadBackendTranslation("title");t=await(0,c.Gg)(this.opp,i),r="generated"}finally{this.lovelace&&"yaml"===this.lovelace.mode&&setTimeout((()=>{this._ignoreNextUpdateEvent=!1}),2e3)}this._state="yaml-editor"===this._state?this._state:"loaded",this._setLovelaceConfig(t,r)}},{kind:"method",key:"_checkLovelaceConfig",value:function(e){let t=Object.isFrozen(e)?void 0:e;return e.views.forEach(((i,r)=>{i.badges&&!i.badges.every(Boolean)&&(t=t||{...e,views:[...e.views]},t.views[r]={...i},t.views[r].badges=i.badges.filter(Boolean))})),t?o()(t):e}},{kind:"method",key:"_setLovelaceConfig",value:function(e,t){e=this._checkLovelaceConfig(e);const r=this.urlPath;this.lovelace={config:e,mode:t,urlPath:this.urlPath,editMode:!!this.lovelace&&this.lovelace.editMode,locale:this.opp.locale,enableFullEditMode:()=>{Ge||(Ge=!0,Promise.all([i.e(9033),i.e(3304),i.e(2118),i.e(5912)]).then(i.bind(i,95912))),this._state="yaml-editor"},setEditMode:e=>{var t,r;e&&"generated"===this.lovelace.mode?(t=this,r={lovelace:this.lovelace,mode:this.panel.config.mode},u||(u=!0,(0,h.B)(t,"register-dialog",{dialogShowEvent:p,dialogTag:"hui-dialog-save-config",dialogImport:()=>Promise.all([i.e(5906),i.e(9033),i.e(3304),i.e(8082)]).then(i.bind(i,78082))})),(0,h.B)(t,p,r)):this._updateLovelace({editMode:e})},saveConfig:async e=>{const{config:t,mode:i}=this.lovelace;e=this._checkLovelaceConfig(e);try{this._updateLovelace({config:e,mode:"storage"}),this._ignoreNextUpdateEvent=!0,await(0,a.Oh)(this.opp,r,e)}catch(e){throw console.error(e),this._updateLovelace({config:t,mode:i}),e}},deleteConfig:async()=>{const{config:e,mode:t}=this.lovelace;try{const e=await this.opp.loadBackendTranslation("title");this._updateLovelace({config:await(0,c.Gg)(this.opp,e),mode:"generated",editMode:!1}),this._ignoreNextUpdateEvent=!0,await(0,a.vj)(this.opp,r)}catch(i){throw console.error(i),this._updateLovelace({config:e,mode:t}),i}}}}},{kind:"method",key:"_updateLovelace",value:function(e){this.lovelace={...this.lovelace,...e}}}]}}),n.oi);customElements.define("ha-panel-lovelace",Ye)},27322:(e,t,i)=>{"use strict";i.d(t,{R:()=>r});const r=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.openpeerpower.io${t}`}}]);
//# sourceMappingURL=chunk.f93f86a43071d30ddd76.js.map