(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[8317],{96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>n});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{i(e)}))},22814:(e,t,r)=>{"use strict";r.d(t,{_r:()=>i,iI:()=>n,W2:()=>o,TZ:()=>s});const i=`${location.protocol}//${location.host}`,n=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),o=async(e,t,r,i)=>e.callWS({type:"config/auth_provider/openpeerpower/create",user_id:t,username:r,password:i}),s=async(e,t,r)=>e.callWS({type:"config/auth_provider/openpeerpower/admin_change_password",user_id:t,password:r})},41500:(e,t,r)=>{"use strict";r.r(t);var i=r(15652),n=r(81471),o=r(49629),s=r(62877),a=r(58831),c=r(29171),l=r(91741),d=(r(22098),r(56007)),p=r(93491),f=r(15688),h=r(22503),u=r(22193),m=r(53658),y=(r(97282),r(75502));function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!b(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return P(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?P(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=E(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=_(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function v(e){var t,r=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function E(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function P(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function C(e,t,r){return(C="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=x(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function x(e){return(x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=g();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(k(o.descriptor)||k(n.descriptor)){if(b(o)||b(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(b(o)){if(b(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}w(o,n)}else t.push(o)}return t}(s.d.map(v)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hui-picture-entity-card")],(function(e,t){class g extends t{constructor(...t){super(...t),e(this)}}return{F:g,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(5009),r.e(2955),r.e(8161),r.e(9543),r.e(8374),r.e(9494),r.e(6051),r.e(3098),r.e(4618),r.e(9033),r.e(3300),r.e(3304),r.e(6087),r.e(6133),r.e(1456),r.e(4507),r.e(6966),r.e(4535),r.e(8101),r.e(6902),r.e(8331),r.e(7580),r.e(167),r.e(6693)]).then(r.bind(r,13930)),document.createElement("hui-picture-entity-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,r){return{type:"picture-entity",entity:(0,f.j)(e,1,t,r,["light","switch"])[0]||"",image:"https://demo.openpeerpower.io/stub_config/bedroom.png"}}},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e||!e.entity)throw new Error("Entity must be specified");if("camera"!==(0,a.M)(e.entity)&&!e.image&&!e.state_image&&!e.camera_image)throw new Error("No image source configured");this._config={show_name:!0,show_state:!0,...e}}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,m.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(C(x(g.prototype),"updated",this).call(this,e),!this._config||!this.opp)return;const t=e.get("opp"),r=e.get("_config");t&&r&&t.themes===this.opp.themes&&r.theme===this._config.theme||(0,s.R)(this,this.opp.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.opp)return i.dy``;const e=this.opp.states[this._config.entity];if(!e)return i.dy`
        <hui-warning>
          ${(0,y.i)(this.opp,this._config.entity)}
        </hui-warning>
      `;const t=this._config.name||(0,l.C)(e),r=(0,c.D)(this.opp.localize,e,this.opp.locale);let s="";return this._config.show_name&&this._config.show_state?s=i.dy`
        <div class="footer both">
          <div>${t}</div>
          <div>${r}</div>
        </div>
      `:this._config.show_name?s=i.dy`<div class="footer">${t}</div>`:this._config.show_state&&(s=i.dy`<div class="footer state">${r}</div>`),i.dy`
      <ha-card>
        <hui-image
          .opp=${this.opp}
          .image=${this._config.image}
          .stateImage=${this._config.state_image}
          .stateFilter=${this._config.state_filter}
          .cameraImage=${"camera"===(0,a.M)(this._config.entity)?this._config.entity:this._config.camera_image}
          .cameraView=${this._config.camera_view}
          .entity=${this._config.entity}
          .aspectRatio=${this._config.aspect_ratio}
          @action=${this._handleAction}
          .actionHandler=${(0,p.K)({hasHold:(0,u._)(this._config.hold_action),hasDoubleClick:(0,u._)(this._config.double_tap_action)})}
          tabindex=${(0,o.o)((0,u._)(this._config.tap_action)||this._config.entity?"0":void 0)}
          class=${(0,n.$)({clickable:!d.V_.includes(e.state)})}
        ></hui-image>
        ${s}
      </ha-card>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-card {
        min-height: 75px;
        overflow: hidden;
        position: relative;
        height: 100%;
        box-sizing: border-box;
      }

      hui-image.clickable {
        cursor: pointer;
      }

      .footer {
        /* start paper-font-common-nowrap style */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        /* end paper-font-common-nowrap style */

        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: var(
          --op-picture-card-background-color,
          rgba(0, 0, 0, 0.3)
        );
        padding: 16px;
        font-size: 16px;
        line-height: 16px;
        color: var(--op-picture-card-text-color, white);
      }

      .both {
        display: flex;
        justify-content: space-between;
      }

      .state {
        text-align: right;
      }
    `}},{kind:"method",key:"_handleAction",value:function(e){(0,h.G)(this,this.opp,this._config,e.detail.action)}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.f52e4e42ac1c51a5ab76.js.map