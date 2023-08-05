(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[1855],{55422:(e,t,r)=>{"use strict";r.d(t,{jV:()=>l,sS:()=>d,rM:()=>p,tf:()=>m});var i=r(49706),o=r(58831),n=r(29171),a=r(56007);const s="ui.components.logbook.messages",l=["proximity","sensor"],c={},d=async(e,t,r)=>u(e,await h(e,t,void 0,void 0,void 0,r)),p=async(e,t,r,i,o)=>u(e,await f(e,t,r,i,o)),u=(e,t)=>{for(const r of t){const t=e.states[r.entity_id];r.state&&t&&(r.message=y(e,r.state,t,(0,o.M)(r.entity_id)))}return t},f=async(e,t,r,i,o)=>{const n="*";i||(i=n);const a=`${t}${r}`;if(c[a]||(c[a]={}),c[a][i])return c[a][i];if(i!==n&&c[a]["*"]){return(await c[a]["*"]).filter((e=>e.entity_id===i))}return c[a][i]=h(e,t,r,i!==n?i:void 0,o).then((e=>e.reverse())),c[a][i]},h=async(e,t,r,i,o,n)=>{const a=new URLSearchParams;return r&&a.append("end_time",r),i&&a.append("entity",i),o&&a.append("entity_matches_only",""),n&&a.append("context_id",n),e.callApi("GET",`logbook/${t}?${a.toString()}`)},m=(e,t)=>{c[`${e}${t}`]={}},y=(e,t,r,o)=>{switch(o){case"device_tracker":case"person":return"not_home"===t?e.localize(`${s}.was_away`):"home"===t?e.localize(`${s}.was_at_home`):e.localize(`${s}.was_at_state`,"state",t);case"sun":return"above_horizon"===t?e.localize(`${s}.rose`):e.localize(`${s}.set`);case"binary_sensor":{const o=t===i.uo,n=t===i.lC,a=r.attributes.device_class;switch(a){case"battery":if(o)return e.localize(`${s}.was_low`);if(n)return e.localize(`${s}.was_normal`);break;case"connectivity":if(o)return e.localize(`${s}.was_connected`);if(n)return e.localize(`${s}.was_disconnected`);break;case"door":case"garage_door":case"opening":case"window":if(o)return e.localize(`${s}.was_opened`);if(n)return e.localize(`${s}.was_closed`);break;case"lock":if(o)return e.localize(`${s}.was_unlocked`);if(n)return e.localize(`${s}.was_locked`);break;case"plug":if(o)return e.localize(`${s}.was_plugged_in`);if(n)return e.localize(`${s}.was_unplugged`);break;case"presence":if(o)return e.localize(`${s}.was_at_home`);if(n)return e.localize(`${s}.was_away`);break;case"safety":if(o)return e.localize(`${s}.was_unsafe`);if(n)return e.localize(`${s}.was_safe`);break;case"cold":case"gas":case"heat":case"moisture":case"motion":case"occupancy":case"power":case"problem":case"smoke":case"sound":case"vibration":if(o)return e.localize(`${s}.detected_device_class`,"device_class",a);if(n)return e.localize(`${s}.cleared_device_class`,"device_class",a)}break}case"cover":switch(t){case"open":return e.localize(`${s}.was_opened`);case"opening":return e.localize(`${s}.is_opening`);case"closing":return e.localize(`${s}.is_closing`);case"closed":return e.localize(`${s}.was_closed`)}break;case"lock":if("unlocked"===t)return e.localize(`${s}.was_unlocked`);if("locked"===t)return e.localize(`${s}.was_locked`)}return t===i.uo?e.localize(`${s}.turned_on`):t===i.lC?e.localize(`${s}.turned_off`):a.V_.includes(t)?e.localize(`${s}.became_unavailable`):e.localize(`${s}.changed_to_state`,"state",r?(0,n.D)(e.localize,r,e.locale,t):t)}},97740:(e,t,r)=>{"use strict";var i=r(15652),o=r(81471),n=r(51960),a=r(49706),s=r(12198),l=r(49684),c=r(25516),d=r(47181),p=r(58831),u=r(16023),f=r(87744),h=(r(3143),r(31206),r(42952),r(11654));function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!b(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=w(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function y(e){var t,r=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=m();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(k(n.descriptor)||k(o.descriptor)){if(b(n)||b(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(b(n)){if(b(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}v(n,o)}else t.push(n)}return t}(a.d.map(y)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,i.Mo)("ha-logbook")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"userIdToName",value:()=>({})},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"traceContexts",value:()=>({})},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"entries",value:()=>[]},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"narrow"})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({attribute:"rtl",type:Boolean})],key:"_rtl",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"no-name"})],key:"noName",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:()=>!1},{kind:"field",decorators:[(0,c.i)(".container")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("opp"),r=void 0===t||t.locale!==this.opp.locale;return e.has("entries")||e.has("traceContexts")||r}},{kind:"method",key:"updated",value:function(e){const t=e.get("opp");void 0!==t&&t.language===this.opp.language||(this._rtl=(0,f.HE)(this.opp))}},{kind:"method",key:"render",value:function(){var e;return(null===(e=this.entries)||void 0===e?void 0:e.length)?i.dy`
      <div
        class="container ha-scrollbar ${(0,o.$)({narrow:this.narrow,rtl:this._rtl,"no-name":this.noName,"no-icon":this.noIcon})}"
        @scroll=${this._saveScrollPos}
      >
        ${this.virtualize?(0,n.AR)({items:this.entries,renderItem:(e,t)=>this._renderLogbookItem(e,t)}):this.entries.map(((e,t)=>this._renderLogbookItem(e,t)))}
      </div>
    `:i.dy`
        <div class="container no-entries" .dir=${(0,f.$3)(this._rtl)}>
          ${this.opp.localize("ui.components.logbook.entries_not_found")}
        </div>
      `}},{kind:"method",key:"_renderLogbookItem",value:function(e,t){var r;if(void 0===t)return i.dy``;const n=this.entries[t-1],c=e.entity_id?this.opp.states[e.entity_id]:void 0,d=e.context_user_id&&this.userIdToName[e.context_user_id],f=e.entity_id?(0,p.M)(e.entity_id):e.domain;return i.dy`
      <div class="entry-container">
        ${0===t||(null==e?void 0:e.when)&&(null==n?void 0:n.when)&&new Date(e.when).toDateString()!==new Date(n.when).toDateString()?i.dy`
              <h4 class="date">
                ${(0,s.p)(new Date(e.when),this.opp.locale)}
              </h4>
            `:i.dy``}

        <div class="entry ${(0,o.$)({"no-entity":!e.entity_id})}">
          <div class="icon-message">
            ${this.noIcon?"":i.dy`
                  <state-badge
                    .opp=${this.opp}
                    .overrideIcon=${null!==(r=e.icon)&&void 0!==r?r:(0,u.K)(f,c,e.state)}
                    .overrideImage=${a.iY.has(f)?"":(null==c?void 0:c.attributes.entity_picture_local)||(null==c?void 0:c.attributes.entity_picture)}
                  ></state-badge>
                `}
            <div class="message-relative_time">
              <div class="message">
                ${this.noName?"":i.dy`<a
                      href="#"
                      @click=${this._entityClicked}
                      .entityId=${e.entity_id}
                      ><span class="name">${e.name}</span></a
                    >`}
                ${e.message}
                ${d?` ${this.opp.localize("ui.components.logbook.by")} ${d}`:e.context_event_type?"call_service"===e.context_event_type?` ${this.opp.localize("ui.components.logbook.by_service")}\n                  ${e.context_domain}.${e.context_service}`:e.context_entity_id===e.entity_id?` ${this.opp.localize("ui.components.logbook.by")}\n                  ${e.context_name?e.context_name:e.context_event_type}`:i.dy` ${this.opp.localize("ui.components.logbook.by")}
                      <a
                        href="#"
                        @click=${this._entityClicked}
                        .entityId=${e.context_entity_id}
                        class="name"
                        >${e.context_entity_id_name}</a
                      >`:""}
              </div>
              <div class="secondary">
                <span
                  >${(0,l.Vu)(new Date(e.when),this.opp.locale)}</span
                >
                -
                <ha-relative-time
                  .opp=${this.opp}
                  .datetime=${e.when}
                ></ha-relative-time>
                ${"automation"===e.domain&&e.context_id in this.traceContexts?i.dy`
                      -
                      <a
                        href=${`/config/automation/trace/${this.traceContexts[e.context_id].item_id}?run_id=${this.traceContexts[e.context_id].run_id}`}
                        >${this.opp.localize("ui.components.logbook.show_trace")}</a
                      >
                    `:""}
              </div>
            </div>
          </div>
        </div>
      </div>
    `}},{kind:"method",decorators:[(0,i.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_entityClicked",value:function(e){const t=e.currentTarget.entityId;t&&(e.preventDefault(),e.stopPropagation(),(0,d.B)(this,"opp-more-info",{entityId:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return[h.Qx,h.$c,i.iv`
        :host([virtualize]) {
          display: block;
          height: 100%;
        }

        .rtl {
          direction: ltr;
        }

        .entry-container {
          width: 100%;
        }

        .entry {
          display: flex;
          width: 100%;
          line-height: 2em;
          padding: 8px 16px;
          box-sizing: border-box;
          border-top: 1px solid var(--divider-color);
        }

        .entry.no-entity,
        .no-name .entry {
          cursor: default;
        }

        .entry:hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .narrow:not(.no-icon) .time {
          margin-left: 32px;
        }

        .message-relative_time {
          display: flex;
          flex-direction: column;
        }

        .secondary {
          font-size: 12px;
          line-height: 1.7;
        }

        .secondary a {
          color: var(--secondary-text-color);
        }

        .date {
          margin: 8px 0;
          padding: 0 16px;
        }

        .narrow .date {
          padding: 0 8px;
        }

        .rtl .date {
          direction: rtl;
        }

        .icon-message {
          display: flex;
          align-items: center;
        }

        .no-entries {
          text-align: center;
          color: var(--secondary-text-color);
        }

        state-badge {
          margin-right: 16px;
          flex-shrink: 0;
          color: var(--state-icon-color);
        }

        .message {
          color: var(--primary-text-color);
        }

        .no-name .message:first-letter {
          text-transform: capitalize;
        }

        a {
          color: var(--primary-color);
        }

        .uni-virtualizer-host {
          display: block;
          position: relative;
          contain: strict;
          height: 100%;
          overflow: auto;
        }

        .uni-virtualizer-host > * {
          box-sizing: border-box;
        }

        .narrow .entry {
          line-height: 1.5;
          padding: 8px;
        }

        .narrow .icon-message state-badge {
          margin-left: 0;
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.76190e8093ff5ea57c4a.js.map