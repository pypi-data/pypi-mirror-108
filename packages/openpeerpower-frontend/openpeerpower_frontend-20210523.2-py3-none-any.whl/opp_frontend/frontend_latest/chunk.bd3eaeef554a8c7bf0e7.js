(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[1927],{44634:(e,t,r)=>{"use strict";r.d(t,{M:()=>o});const o=(e,t)=>{const r=Number(e.state),o=t&&"on"===t.state;let a="opp:battery";if(isNaN(r))return"off"===e.state?a+="-full":"on"===e.state?a+="-alert":a+="-unknown",a;const i=10*Math.round(r/10);return o&&r>10?a+=`-charging-${i}`:o?a+="-outline":r<=5?a+="-alert":r>5&&r<95&&(a+=`-${i}`),a}},56949:(e,t,r)=>{"use strict";r.d(t,{q:()=>o});const o=e=>{const t=e.entity_id.split(".")[0];let r=e.state;return"climate"===t&&(r=e.attributes.hvac_action),r}},27269:(e,t,r)=>{"use strict";r.d(t,{p:()=>o});const o=e=>e.substr(e.indexOf(".")+1)},91741:(e,t,r)=>{"use strict";r.d(t,{C:()=>a});var o=r(27269);const a=e=>void 0===e.attributes.friendly_name?(0,o.p)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},82943:(e,t,r)=>{"use strict";r.d(t,{m2:()=>o,q_:()=>a,ow:()=>i});const o=(e,t)=>{const r="closed"!==e;switch(null==t?void 0:t.attributes.device_class){case"garage":switch(e){case"opening":return"opp:arrow-up-box";case"closing":return"opp:arrow-down-box";case"closed":return"opp:garage";default:return"opp:garage-open"}case"gate":switch(e){case"opening":case"closing":return"opp:gate-arrow-right";case"closed":return"opp:gate";default:return"opp:gate-open"}case"door":return r?"opp:door-open":"opp:door-closed";case"damper":return r?"opp:circle":"opp:circle-slice-8";case"shutter":switch(e){case"opening":return"opp:arrow-up-box";case"closing":return"opp:arrow-down-box";case"closed":return"opp:window-shutter";default:return"opp:window-shutter-open"}case"blind":case"curtain":case"shade":switch(e){case"opening":return"opp:arrow-up-box";case"closing":return"opp:arrow-down-box";case"closed":return"opp:blinds";default:return"opp:blinds-open"}case"window":switch(e){case"opening":return"opp:arrow-up-box";case"closing":return"opp:arrow-down-box";case"closed":return"opp:window-closed";default:return"opp:window-open"}}switch(e){case"opening":return"opp:arrow-up-box";case"closing":return"opp:arrow-down-box";case"closed":return"opp:window-closed";default:return"opp:window-open"}},a=e=>{switch(e.attributes.device_class){case"awning":case"door":case"gate":return"opp:arrow-expand-horizontal";default:return"opp:arrow-up"}},i=e=>{switch(e.attributes.device_class){case"awning":case"door":case"gate":return"opp:arrow-collapse-horizontal";default:return"opp:arrow-down"}}},16023:(e,t,r)=>{"use strict";r.d(t,{K:()=>n});var o=r(49706);var a=r(82943),i=r(44634);const n=(e,t,r)=>{const n=void 0!==r?r:null==t?void 0:t.state;switch(e){case"alarm_control_panel":switch(n){case"armed_home":return"opp:bell-plus";case"armed_night":return"opp:bell-sleep";case"disarmed":return"opp:bell-outline";case"triggered":return"opp:bell-ring";default:return"opp:bell"}case"binary_sensor":return((e,t)=>{const r="off"===e;switch(null==t?void 0:t.attributes.device_class){case"battery":return r?"opp:battery":"opp:battery-outline";case"battery_charging":return r?"opp:battery":"opp:battery-charging";case"cold":return r?"opp:thermometer":"opp:snowflake";case"connectivity":return r?"opp:server-network-off":"opp:server-network";case"door":return r?"opp:door-closed":"opp:door-open";case"garage_door":return r?"opp:garage":"opp:garage-open";case"power":return r?"opp:power-plug-off":"opp:power-plug";case"gas":case"problem":case"safety":case"smoke":return r?"opp:check-circle":"opp:alert-circle";case"heat":return r?"opp:thermometer":"opp:fire";case"light":return r?"opp:brightness-5":"opp:brightness-7";case"lock":return r?"opp:lock":"opp:lock-open";case"moisture":return r?"opp:water-off":"opp:water";case"motion":return r?"opp:walk":"opp:run";case"occupancy":return r?"opp:home-outline":"opp:home";case"opening":return r?"opp:square":"opp:square-outline";case"plug":return r?"opp:power-plug-off":"opp:power-plug";case"presence":return r?"opp:home-outline":"opp:home";case"sound":return r?"opp:music-note-off":"opp:music-note";case"vibration":return r?"opp:crop-portrait":"opp:vibrate";case"window":return r?"opp:window-closed":"opp:window-open";default:return r?"opp:radiobox-blank":"opp:checkbox-marked-circle"}})(n,t);case"cover":return(0,a.m2)(n,t);case"humidifier":return r&&"off"===r?"opp:air-humidifier-off":"opp:air-humidifier";case"lock":return"unlocked"===n?"opp:lock-open":"opp:lock";case"media_player":return"playing"===n?"opp:cast-connected":"opp:cast";case"zwave":switch(n){case"dead":return"opp:emoticon-dead";case"sleeping":return"opp:sleep";case"initializing":return"opp:timer-sand";default:return"opp:z-wave"}case"sensor":{const e=(e=>{const t=null==e?void 0:e.attributes.device_class;if(t&&t in o.h2)return o.h2[t];if("battery"===t)return e?(0,i.M)(e):"opp:battery";const r=null==e?void 0:e.attributes.unit_of_measurement;return r===o.ot||r===o.gD?"opp:thermometer":void 0})(t);if(e)return e;break}case"input_datetime":if(!(null==t?void 0:t.attributes.has_date))return"opp:clock";if(!t.attributes.has_time)return"opp:calendar";break;case"sun":return"above_horizon"===(null==t?void 0:t.state)?o.Zy[e]:"opp:weather-night"}return e in o.Zy?o.Zy[e]:(console.warn("Unable to find icon for domain "+e+" ("+t+")"),o.Rb)}},36145:(e,t,r)=>{"use strict";r.d(t,{M:()=>n});var o=r(49706),a=r(58831),i=r(16023);const n=e=>e?e.attributes.icon?e.attributes.icon:(0,i.K)((0,a.M)(e.entity_id),e):o.Rb},52797:(e,t,r)=>{"use strict";r.d(t,{N:()=>o});const o=r(15652).iv`
  ha-icon[data-domain="alert"][data-state="on"],
  ha-icon[data-domain="automation"][data-state="on"],
  ha-icon[data-domain="binary_sensor"][data-state="on"],
  ha-icon[data-domain="calendar"][data-state="on"],
  ha-icon[data-domain="camera"][data-state="streaming"],
  ha-icon[data-domain="cover"][data-state="open"],
  ha-icon[data-domain="fan"][data-state="on"],
  ha-icon[data-domain="humidifier"][data-state="on"],
  ha-icon[data-domain="light"][data-state="on"],
  ha-icon[data-domain="input_boolean"][data-state="on"],
  ha-icon[data-domain="lock"][data-state="unlocked"],
  ha-icon[data-domain="media_player"][data-state="on"],
  ha-icon[data-domain="media_player"][data-state="paused"],
  ha-icon[data-domain="media_player"][data-state="playing"],
  ha-icon[data-domain="script"][data-state="on"],
  ha-icon[data-domain="sun"][data-state="above_horizon"],
  ha-icon[data-domain="switch"][data-state="on"],
  ha-icon[data-domain="timer"][data-state="active"],
  ha-icon[data-domain="vacuum"][data-state="cleaning"],
  ha-icon[data-domain="group"][data-state="on"],
  ha-icon[data-domain="group"][data-state="home"],
  ha-icon[data-domain="group"][data-state="open"],
  ha-icon[data-domain="group"][data-state="locked"],
  ha-icon[data-domain="group"][data-state="problem"] {
    color: var(--paper-item-icon-active-color, #fdd835);
  }

  ha-icon[data-domain="climate"][data-state="cooling"] {
    color: var(--cool-color, #2b9af9);
  }

  ha-icon[data-domain="climate"][data-state="heating"] {
    color: var(--heat-color, #ff8100);
  }

  ha-icon[data-domain="climate"][data-state="drying"] {
    color: var(--dry-color, #efbd07);
  }

  ha-icon[data-domain="alarm_control_panel"] {
    color: var(--alarm-color-armed, var(--label-badge-red));
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="disarmed"] {
    color: var(--alarm-color-disarmed, var(--label-badge-green));
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="pending"],
  ha-icon[data-domain="alarm_control_panel"][data-state="arming"] {
    color: var(--alarm-color-pending, var(--label-badge-yellow));
    animation: pulse 1s infinite;
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="triggered"] {
    color: var(--alarm-color-triggered, var(--label-badge-red));
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  ha-icon[data-domain="plant"][data-state="problem"],
  ha-icon[data-domain="zwave"][data-state="dead"] {
    color: var(--error-state-color, #db4437);
  }

  /* Color the icon if unavailable */
  ha-icon[data-state="unavailable"] {
    color: var(--state-icon-unavailable-color);
  }
`},3143:(e,t,r)=>{"use strict";var o=r(15652),a=r(49629),i=r(79865),n=r(56949),s=r(22311),c=r(36145),l=r(52797);r(16509);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(o){t.forEach((function(t){var a=t.placement;if(t.kind===o&&("static"===a||"prototype"===a)){var i="static"===a?e:r;this.defineClassElement(i,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var o=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],o=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),o.push.apply(o,t.finishers)}),this),!t)return{elements:r,finishers:o};var i=this.decorateConstructor(r,t);return o.push.apply(o,i.finishers),i.finishers=o,i},addElementPlacement:function(e,t,r){var o=t[e.placement];if(!r&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,t){for(var r=[],o=[],a=e.decorators,i=a.length-1;i>=0;i--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,a[i])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&o.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:o,extras:r}},decorateConstructor:function(e,t){for(var r=[],o=t.length-1;o>=0;o--){var a=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[o])(a)||a);if(void 0!==i.finisher&&r.push(i.finisher),void 0!==i.elements){e=i.elements;for(var n=0;n<e.length-1;n++)for(var s=n+1;s<e.length;s++)if(e[n].key===e[s].key&&e[n].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:r,placement:o,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var o=(0,t[r])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var o=r.call(e,t||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,o=new Array(t);r<t;r++)o[r]=e[r];return o}let g=function(e,t,r,o){var a=d();if(o)for(var i=0;i<o.length;i++)a=o[i](a);var n=t((function(e){a.initializeInstanceElements(e,s.elements)}),r),s=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},o=0;o<e.length;o++){var a,i=e[o];if("method"===i.kind&&(a=t.find(r)))if(f(i.descriptor)||f(a.descriptor)){if(h(i)||h(a))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");a.descriptor=i.descriptor}else{if(h(i)){if(h(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");a.decorators=i.decorators}u(i,a)}else t.push(i)}return t}(n.d.map(p)),e);return a.initializeClassElements(n.F,s.elements),a.runClassFinishers(n.F,s.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",key:"opp",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"overrideImage",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"stateColor",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0,attribute:"icon"})],key:"_showIcon",value:()=>!0},{kind:"field",decorators:[(0,o.sz)()],key:"_iconStyle",value:()=>({})},{kind:"method",key:"render",value:function(){const e=this.stateObj;if(!e&&!this.overrideIcon&&!this.overrideImage)return o.dy`<div class="missing">
        <ha-icon icon="opp:alert"></ha-icon>
      </div>`;if(!this._showIcon)return o.dy``;const t=e?(0,s.N)(e):void 0;return o.dy`
      <ha-icon
        style=${(0,i.V)(this._iconStyle)}
        data-domain=${(0,a.o)(this.stateColor||"light"===t&&!1!==this.stateColor?t:void 0)}
        data-state=${e?(0,n.q)(e):""}
        .icon=${this.overrideIcon||(e?(0,c.M)(e):"")}
      ></ha-icon>
    `}},{kind:"method",key:"updated",value:function(e){if(!e.has("stateObj")&&!e.has("overrideImage")&&!e.has("overrideIcon"))return;const t=this.stateObj,r={},o={backgroundImage:""};if(this._showIcon=!0,t){if((t.attributes.entity_picture_local||t.attributes.entity_picture)&&!this.overrideIcon||this.overrideImage){let e=this.overrideImage||t.attributes.entity_picture_local||t.attributes.entity_picture;this.opp&&(e=this.opp.oppUrl(e)),o.backgroundImage=`url(${e})`,this._showIcon=!1}else if("on"===t.state){if(t.attributes.hs_color&&!1!==this.stateColor){const e=t.attributes.hs_color[0],o=t.attributes.hs_color[1];o>10&&(r.color=`hsl(${e}, 100%, ${100-o/2}%)`)}if(t.attributes.brightness&&!1!==this.stateColor){const e=t.attributes.brightness;if("number"!=typeof e){const r=`Type error: state-badge expected number, but type of ${t.entity_id}.attributes.brightness is ${typeof e} (${e})`;console.warn(r)}r.filter=`brightness(${(e+245)/5}%)`}}}else if(this.overrideImage){let e=this.overrideImage;this.opp&&(e=this.opp.oppUrl(e)),o.backgroundImage=`url(${e})`,this._showIcon=!1}this._iconStyle=r,Object.assign(this.style,o)}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
      :host {
        position: relative;
        display: inline-block;
        width: 40px;
        color: var(--paper-item-icon-color, #44739e);
        border-radius: 50%;
        height: 40px;
        text-align: center;
        background-size: cover;
        line-height: 40px;
        vertical-align: middle;
        box-sizing: border-box;
      }
      :host(:focus) {
        outline: none;
      }
      :host(:not([icon]):focus) {
        border: 2px solid var(--divider-color);
      }
      :host([icon]:focus) {
        background: var(--divider-color);
      }
      ha-icon {
        transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
      }
      .missing {
        color: #fce588;
      }

      ${l.N}
    `}}]}}),o.oi);customElements.define("state-badge",g)}}]);
//# sourceMappingURL=chunk.bd3eaeef554a8c7bf0e7.js.map