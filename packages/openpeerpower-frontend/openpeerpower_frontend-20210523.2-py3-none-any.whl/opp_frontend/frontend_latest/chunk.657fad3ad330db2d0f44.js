/*! For license information please see chunk.657fad3ad330db2d0f44.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[8267,3122],{63207:(e,t,i)=>{"use strict";i(65660),i(15112);var r=i(9672),o=i(87156),n=i(50856),s=i(65233);(0,r.k)({_template:n.d`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{"use strict";i.d(t,{P:()=>o});i(65233);var r=i(9672);class o{constructor(e){o[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return o.types[e]&&o.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=o.types[t]=o.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=o.types[this.type];return e?Object.keys(e).map((function(e){return n[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}o[" "]=function(){},o.types={};var n=o.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new o({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new o({type:this.type,key:e}).value}})},58993:(e,t,i)=>{"use strict";i.d(t,{yh:()=>r,U2:()=>s,t8:()=>a,ZH:()=>c});class r{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise(((i,r)=>{const o=indexedDB.open(e,1);o.onerror=()=>r(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}}))}_withIDBStore(e,t){return this._dbp.then((i=>new Promise(((r,o)=>{const n=i.transaction(this.storeName,e);n.oncomplete=()=>r(),n.onabort=n.onerror=()=>o(n.error),t(n.objectStore(this.storeName))}))))}}let o;function n(){return o||(o=new r),o}function s(e,t=n()){let i;return t._withIDBStore("readonly",(t=>{i=t.get(e)})).then((()=>i.result))}function a(e,t,i=n()){return i._withIDBStore("readwrite",(i=>{i.put(t,e)}))}function c(e=n()){return e._withIDBStore("readwrite",(e=>{e.clear()}))}},96305:(e,t,i)=>{"use strict";i.d(t,{v:()=>r});const r=(e,t)=>e&&Object.keys(e.services).filter((i=>t in e.services[i]))},77980:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HaConfigServerControl:()=>y});i(53918),i(53268),i(12730),i(30879);var r=i(15652),o=i(96305),n=(i(54909),i(22098),i(41886)),s=i(5986),a=(i(13491),i(11654)),c=(i(88165),i(29311));function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let y=function(e,t,i,r){var o=l();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(u(n.descriptor)||u(o.descriptor)){if(h(n)||h(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(h(n)){if(h(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}p(n,o)}else t.push(n)}return t}(s.d.map(d)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-config-server-control")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"_validating",value:()=>!1},{kind:"field",decorators:[(0,r.sz)()],key:"_reloadableDomains",value:()=>[]},{kind:"field",key:"_validateLog",value:()=>""},{kind:"field",key:"_isValid",value:()=>null},{kind:"method",key:"updated",value:function(e){const t=e.get("opp");!e.has("opp")||t&&t.config.components===this.opp.config.components||(this._reloadableDomains=(0,o.v)(this.opp,"reload").sort())}},{kind:"method",key:"render",value:function(){return r.dy`
      <opp-tabs-subpage
        .opp=${this.opp}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/config"
        .tabs=${c.configSections.general}
        .showAdvanced=${this.showAdvanced}
      >
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header"
            >${this.opp.localize("ui.panel.config.server_control.caption")}</span
          >
          <span slot="introduction"
            >${this.opp.localize("ui.panel.config.server_control.description")}</span
          >

          ${this.showAdvanced?r.dy` <ha-card
                header=${this.opp.localize("ui.panel.config.server_control.section.validation.heading")}
              >
                <div class="card-content">
                  ${this.opp.localize("ui.panel.config.server_control.section.validation.introduction")}
                  ${this._validateLog?r.dy`
                        <div class="config-invalid">
                          <span class="text">
                            ${this.opp.localize("ui.panel.config.server_control.section.validation.invalid")}
                          </span>
                          <mwc-button raised @click=${this._validateConfig}>
                            ${this.opp.localize("ui.panel.config.server_control.section.validation.check_config")}
                          </mwc-button>
                        </div>
                        <div id="configLog" class="validate-log">
                          ${this._validateLog}
                        </div>
                      `:r.dy`
                        <div
                          class="validate-container layout vertical center-center"
                        >
                          ${this._validating?r.dy`
                                <ha-circular-progress
                                  active
                                ></ha-circular-progress>
                              `:r.dy`
                                ${this._isValid?r.dy` <div
                                      class="validate-result"
                                      id="result"
                                    >
                                      ${this.opp.localize("ui.panel.config.server_control.section.validation.valid")}
                                    </div>`:""}
                                <mwc-button
                                  raised
                                  @click=${this._validateConfig}
                                >
                                  ${this.opp.localize("ui.panel.config.server_control.section.validation.check_config")}
                                </mwc-button>
                              `}
                        </div>
                      `}
                </div>
              </ha-card>`:""}

          <ha-card
            header=${this.opp.localize("ui.panel.config.server_control.section.server_management.heading")}
          >
            <div class="card-content">
              ${this.opp.localize("ui.panel.config.server_control.section.server_management.introduction")}
            </div>
            <div class="card-actions warning">
              <ha-call-service-button
                class="warning"
                .opp=${this.opp}
                domain="openpeerpower"
                service="restart"
                .confirmation=${this.opp.localize("ui.panel.config.server_control.section.server_management.confirm_restart")}
                >${this.opp.localize("ui.panel.config.server_control.section.server_management.restart")}
              </ha-call-service-button>
              <ha-call-service-button
                class="warning"
                .opp=${this.opp}
                domain="openpeerpower"
                service="stop"
                confirmation=${this.opp.localize("ui.panel.config.server_control.section.server_management.confirm_stop")}
                >${this.opp.localize("ui.panel.config.server_control.section.server_management.stop")}
              </ha-call-service-button>
            </div>
          </ha-card>

          ${this.showAdvanced?r.dy`
                <ha-card
                  header=${this.opp.localize("ui.panel.config.server_control.section.reloading.heading")}
                >
                  <div class="card-content">
                    ${this.opp.localize("ui.panel.config.server_control.section.reloading.introduction")}
                  </div>
                  <div class="card-actions">
                    <ha-call-service-button
                      .opp=${this.opp}
                      domain="openpeerpower"
                      service="reload_core_config"
                      >${this.opp.localize("ui.panel.config.server_control.section.reloading.core")}
                    </ha-call-service-button>
                  </div>
                  ${this._reloadableDomains.map((e=>r.dy`<div class="card-actions">
                        <ha-call-service-button
                          .opp=${this.opp}
                          .domain=${e}
                          service="reload"
                          >${this.opp.localize(`ui.panel.config.server_control.section.reloading.${e}`)||this.opp.localize("ui.panel.config.server_control.section.reloading.reload","domain",(0,s.Lh)(this.opp.localize,e))}
                        </ha-call-service-button>
                      </div>`))}
                </ha-card>
              `:""}
        </ha-config-section>
      </opp-tabs-subpage>
    `}},{kind:"method",key:"_validateConfig",value:async function(){this._validating=!0,this._validateLog="",this._isValid=null;const e=await(0,n.Ij)(this.opp);this._validating=!1,this._isValid="valid"===e.result,e.errors&&(this._validateLog=e.errors)}},{kind:"get",static:!0,key:"styles",value:function(){return[a.Qx,r.iv`
        .validate-container {
          height: 140px;
        }

        .validate-result {
          color: var(--success-color);
          font-weight: 500;
          margin-bottom: 1em;
        }

        .config-invalid {
          margin: 1em 0;
        }

        .config-invalid .text {
          color: var(--error-color);
          font-weight: 500;
        }

        .config-invalid mwc-button {
          float: right;
        }

        .validate-log {
          white-space: pre-line;
          direction: ltr;
        }

        ha-config-section {
          padding-bottom: 24px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.657fad3ad330db2d0f44.js.map