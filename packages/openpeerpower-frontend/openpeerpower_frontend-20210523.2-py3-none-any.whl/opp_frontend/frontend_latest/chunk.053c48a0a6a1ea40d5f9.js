(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[3775],{53775:(e,t,i)=>{"use strict";i.r(t);i(81689);var o=i(55317),n=i(15652),r=i(81471),s=i(14516),a=i(47181),l=i(58831),d=i(91741),c=i(45485),p=i(85415),u=i(87744),h=(i(65992),i(81545),i(22098),i(83927),i(10983),i(43709),i(83270));var f=i(90363),m=(i(13076),i(20482),i(11654)),y=i(81796);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(o){t.forEach((function(t){var n=t.placement;if(t.kind===o&&("static"===n||"prototype"===n)){var r="static"===n?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var o=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],o=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!k(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),o.push.apply(o,t.finishers)}),this),!t)return{elements:i,finishers:o};var r=this.decorateConstructor(i,t);return o.push.apply(o,r.finishers),r.finishers=o,r},addElementPlacement:function(e,t,i){var o=t[e.placement];if(!i&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,t){for(var i=[],o=[],n=e.decorators,r=n.length-1;r>=0;r--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[r])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&o.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:o,extras:i}},decorateConstructor:function(e,t){for(var i=[],o=t.length-1;o>=0;o--){var n=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[o])(n)||n);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return E(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?E(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=x(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:o,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var o=(0,t[i])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function v(e){var t,i=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var o=i.call(e,t||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function E(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,o=new Array(t);i<t;i++)o[i]=e[i];return o}function $(e,t,i){return($="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(o){var n=Object.getOwnPropertyDescriptor(o,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,o){var n=g();if(o)for(var r=0;r<o.length;r++)n=o[r](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},o=0;o<e.length;o++){var n,r=e[o];if("method"===r.kind&&(n=t.find(i)))if(b(r.descriptor)||b(n.descriptor)){if(k(r)||k(n))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");n.descriptor=r.descriptor}else{if(k(r)){if(k(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");n.decorators=r.decorators}_(r,n)}else t.push(r)}return t}(s.d.map(v)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("cloud-google-assistant")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_entities",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_entityConfigs",value:()=>({})},{kind:"field",key:"_popstateSyncAttached",value:()=>!1},{kind:"field",key:"_popstateReloadStatusAttached",value:()=>!1},{kind:"field",key:"_isInitialExposed",value:void 0},{kind:"field",key:"_getEntityFilterFunc",value:()=>(0,s.Z)((e=>(0,c.h)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities)))},{kind:"method",key:"render",value:function(){if(void 0===this._entities)return n.dy` <opp-loading-screen></opp-loading-screen> `;const e=(0,c.E)(this.cloudStatus.google_entities),t=this._getEntityFilterFunc(this.cloudStatus.google_entities),i=(0,u.Zu)(this.opp),s=this._isInitialExposed||new Set,a=void 0===this._isInitialExposed;let l=0;const d=[],p=[];return this._entities.forEach((c=>{const u=this.opp.states[c.entity_id],h=this._entityConfigs[c.entity_id]||{should_expose:null},f=e?this._configIsExposed(c.entity_id,h):t(c.entity_id),m=e?this._configIsDomainExposed(c.entity_id):t(c.entity_id);f&&(l++,a&&s.add(c.entity_id));const y=s.has(c.entity_id)?d:p,g=n.dy`<mwc-icon-button
        slot="trigger"
        class=${(0,r.$)({exposed:f,"not-exposed":!f})}
        .disabled=${!e}
        .title=${this.opp.localize("ui.panel.config.cloud.google.expose")}
      >
        <ha-svg-icon
          .path=${null!==h.should_expose?f?o.qtl:o.xaH:m?o.D4N:o.tyg}
        ></ha-svg-icon>
      </mwc-icon-button>`;y.push(n.dy`
        <ha-card>
          <div class="card-content">
            <div class="top-line">
              <state-info
                .opp=${this.opp}
                .stateObj=${u}
                secondary-line
                @click=${this._showMoreInfo}
              >
                ${c.traits.map((e=>e.substr(e.lastIndexOf(".")+1))).join(", ")}
              </state-info>
              ${e?n.dy`<ha-button-menu
                    corner="BOTTOM_START"
                    .entityId=${u.entity_id}
                    @action=${this._exposeChanged}
                  >
                    ${g}
                    <mwc-list-item hasMeta>
                      ${this.opp.localize("ui.panel.config.cloud.google.expose_entity")}
                      <ha-svg-icon
                        class="exposed"
                        slot="meta"
                        .path=${o.qtl}
                      ></ha-svg-icon>
                    </mwc-list-item>
                    <mwc-list-item hasMeta>
                      ${this.opp.localize("ui.panel.config.cloud.google.dont_expose_entity")}
                      <ha-svg-icon
                        class="not-exposed"
                        slot="meta"
                        .path=${o.xaH}
                      ></ha-svg-icon>
                    </mwc-list-item>
                    <mwc-list-item hasMeta>
                      ${this.opp.localize("ui.panel.config.cloud.google.follow_domain")}
                      <ha-svg-icon
                        class=${(0,r.$)({exposed:m,"not-exposed":!m})}
                        slot="meta"
                        .path=${m?o.D4N:o.tyg}
                      ></ha-svg-icon>
                    </mwc-list-item>
                  </ha-button-menu>`:n.dy`${g}`}
            </div>
            ${c.might_2fa?n.dy`
                  <div>
                    <ha-formfield
                      .label=${this.opp.localize("ui.panel.config.cloud.google.disable_2FA")}
                      .dir=${i}
                    >
                      <ha-switch
                        .entityId=${c.entity_id}
                        .checked=${Boolean(h.disable_2fa)}
                        @change=${this._disable2FAChanged}
                      ></ha-switch>
                    </ha-formfield>
                  </div>
                `:""}
          </div>
        </ha-card>
      `)})),a&&(this._isInitialExposed=s),n.dy`
      <opp-subpage
        .opp=${this.opp}
        .header=${this.opp.localize("ui.panel.config.cloud.google.title")}
        .narrow=${this.narrow}>
        ${e?n.dy`
                <mwc-button
                  slot="toolbar-icon"
                  @click=${this._openDomainToggler}
                  >${this.opp.localize("ui.panel.config.cloud.google.manage_domains")}</mwc-button
                >
              `:""}
        ${e?"":n.dy`
                <div class="banner">
                  ${this.opp.localize("ui.panel.config.cloud.google.banner")}
                </div>
              `}
          ${d.length>0?n.dy`
                  <div class="header">
                    <h3>
                      ${this.opp.localize("ui.panel.config.cloud.google.exposed_entities")}
                    </h3>
                    ${this.narrow?l:this.opp.localize("ui.panel.config.cloud.alexa.exposed","selected",l)}
                  </div>
                  <div class="content">${d}</div>
                `:""}
          ${p.length>0?n.dy`
                  <div class="header second">
                    <h3>
                      ${this.opp.localize("ui.panel.config.cloud.google.not_exposed_entities")}
                    </h3>
                    ${this.narrow?this._entities.length-l:this.opp.localize("ui.panel.config.cloud.alexa.not_exposed","selected",this._entities.length-l)}
                  </div>
                  <div class="content">${p}</div>
                `:""}
        </div>
      </opp-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){$(C(i.prototype),"firstUpdated",this).call(this,e),this._fetchData()}},{kind:"method",key:"updated",value:function(e){$(C(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.google_entity_configs)}},{kind:"method",key:"_configIsDomainExposed",value:function(e){const t=(0,l.M)(e);return!this.cloudStatus.prefs.google_default_expose||this.cloudStatus.prefs.google_default_expose.includes(t)}},{kind:"method",key:"_configIsExposed",value:function(e,t){var i;return null!==(i=t.should_expose)&&void 0!==i?i:this._configIsDomainExposed(e)}},{kind:"method",key:"_fetchData",value:async function(){const e=await(t=this.opp,t.callWS({type:"cloud/google_assistant/entities"}));var t;e.sort(((e,t)=>{const i=this.opp.states[e.entity_id],o=this.opp.states[t.entity_id];return(0,p.q)(i?(0,d.C)(i):e.entity_id,o?(0,d.C)(o):t.entity_id)})),this._entities=e}},{kind:"method",key:"_showMoreInfo",value:function(e){const t=e.currentTarget.stateObj.entity_id;(0,a.B)(this,"opp-more-info",{entityId:t})}},{kind:"method",key:"_exposeChanged",value:async function(e){const t=e.currentTarget.entityId;let i=null;switch(e.detail.index){case 0:i=!0;break;case 1:i=!1;break;case 2:i=null}await this._updateExposed(t,i)}},{kind:"method",key:"_updateExposed",value:async function(e,t){await this._updateConfig(e,{should_expose:t}),this.cloudStatus.google_registered&&this._ensureEntitySync()}},{kind:"method",key:"_disable2FAChanged",value:async function(e){const t=e.currentTarget.entityId,i=e.target.checked;i!==Boolean((this._entityConfigs[t]||{}).disable_2fa)&&await this._updateConfig(t,{disable_2fa:i})}},{kind:"method",key:"_updateConfig",value:async function(e,t){const i=await(0,h.QD)(this.opp,e,t);this._entityConfigs={...this._entityConfigs,[e]:i},this._ensureStatusReload()}},{kind:"method",key:"_openDomainToggler",value:function(){(0,f._)(this,{domains:this._entities.map((e=>(0,l.M)(e.entity_id))).filter(((e,t,i)=>i.indexOf(e)===t)),exposedDomains:this.cloudStatus.prefs.google_default_expose,toggleDomain:(e,t)=>{this._updateDomainExposed(e,t)},resetDomain:e=>{this._entities.forEach((t=>{(0,l.M)(t.entity_id)===e&&this._updateExposed(t.entity_id,null)}))}})}},{kind:"method",key:"_updateDomainExposed",value:async function(e,t){const i=this.cloudStatus.prefs.google_default_expose||this._entities.map((e=>(0,l.M)(e.entity_id))).filter(((e,t,i)=>i.indexOf(e)===t));t&&i.includes(e)||!t&&!i.includes(e)||(t?i.push(e):i.splice(i.indexOf(e),1),await(0,h.LV)(this.opp,{google_default_expose:i}),(0,a.B)(this,"ha-refresh-cloud-status"))}},{kind:"method",key:"_ensureStatusReload",value:function(){if(this._popstateReloadStatusAttached)return;this._popstateReloadStatusAttached=!0;const e=this.parentElement;window.addEventListener("popstate",(()=>(0,a.B)(e,"ha-refresh-cloud-status")),{once:!0})}},{kind:"method",key:"_ensureEntitySync",value:function(){if(this._popstateSyncAttached)return;this._popstateSyncAttached=!0;const e=this.parentElement;window.addEventListener("popstate",(()=>{(0,y.C)(e,{message:this.opp.localize("ui.panel.config.cloud.google.sync_to_google")}),(0,h.A$)(this.opp)}),{once:!0})}},{kind:"get",static:!0,key:"styles",value:function(){return[m.Qx,n.iv`
        mwc-list-item > [slot="meta"] {
          margin-left: 4px;
        }
        .banner {
          color: var(--primary-text-color);
          background-color: var(
            --op-card-background,
            var(--card-background-color, white)
          );
          padding: 16px 8px;
          text-align: center;
        }
        .content {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          grid-gap: 8px 8px;
          padding: 8px;
        }
        .card-content {
          padding-bottom: 12px;
        }
        state-info {
          cursor: pointer;
        }
        ha-switch {
          padding: 8px 0;
        }
        .top-line {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--app-header-background-color);
        }
        .header.second {
          border-top: 1px solid var(--divider-color);
        }
        .exposed {
          color: var(--success-color);
        }
        .not-exposed {
          color: var(--error-color);
        }
        @media all and (max-width: 450px) {
          ha-card {
            max-width: 100%;
          }
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.053c48a0a6a1ea40d5f9.js.map