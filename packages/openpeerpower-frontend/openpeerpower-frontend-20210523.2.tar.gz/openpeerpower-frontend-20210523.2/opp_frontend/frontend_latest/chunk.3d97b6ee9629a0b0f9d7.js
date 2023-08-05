/*! For license information please see chunk.3d97b6ee9629a0b0f9d7.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[2862],{83278:(e,t,r)=>{"use strict";r.d(t,{r:()=>p});var i=r(94707);const n=(e,t)=>{const r=e.startNode.parentNode,n=void 0===t?e.endNode:t.startNode,o=r.insertBefore((0,i.IW)(),n);r.insertBefore((0,i.IW)(),n);const s=new i.nt(e.options);return s.insertAfterNode(o),s},o=(e,t)=>(e.setValue(t),e.commit(),e),s=(e,t,r)=>{const n=e.startNode.parentNode,o=r?r.startNode:e.endNode,s=t.endNode.nextSibling;s!==o&&(0,i.V)(n,t.startNode,s,o)},a=e=>{(0,i.r4)(e.startNode.parentNode,e.startNode,e.endNode.nextSibling)},c=(e,t,r)=>{const i=new Map;for(let n=t;n<=r;n++)i.set(e[n],n);return i},l=new WeakMap,d=new WeakMap,p=(0,i.XM)(((e,t,r)=>{let p;return void 0===r?r=t:void 0!==t&&(p=t),t=>{if(!(t instanceof i.nt))throw new Error("repeat can only be used in text bindings");const u=l.get(t)||[],h=d.get(t)||[],f=[],m=[],v=[];let y,b,g=0;for(const t of e)v[g]=p?p(t,g):g,m[g]=r(t,g),g++;let k=0,w=u.length-1,E=0,P=m.length-1;for(;k<=w&&E<=P;)if(null===u[k])k++;else if(null===u[w])w--;else if(h[k]===v[E])f[E]=o(u[k],m[E]),k++,E++;else if(h[w]===v[P])f[P]=o(u[w],m[P]),w--,P--;else if(h[k]===v[P])f[P]=o(u[k],m[P]),s(t,u[k],f[P+1]),k++,P--;else if(h[w]===v[E])f[E]=o(u[w],m[E]),s(t,u[w],u[k]),w--,E++;else if(void 0===y&&(y=c(v,E,P),b=c(h,k,w)),y.has(h[k]))if(y.has(h[w])){const e=b.get(v[E]),r=void 0!==e?u[e]:null;if(null===r){const e=n(t,u[k]);o(e,m[E]),f[E]=e}else f[E]=o(r,m[E]),s(t,r,u[k]),u[e]=null;E++}else a(u[w]),w--;else a(u[k]),k++;for(;E<=P;){const e=n(t,f[P+1]);o(e,m[E]),f[E++]=e}for(;k<=w;){const e=u[k++];null!==e&&a(e)}l.set(t,f),d.set(t,v)}}))},12198:(e,t,r)=>{"use strict";r.d(t,{p:()=>o,D:()=>s});var i=r(68928),n=r(43274);const o=n.Sb?(e,t)=>e.toLocaleDateString(t.language,{year:"numeric",month:"long",day:"numeric"}):e=>(0,i.WU)(e,"longDate"),s=n.Sb?(e,t)=>e.toLocaleDateString(t.language,{weekday:"long",month:"short",day:"numeric"}):e=>(0,i.WU)(e,"dddd, MMM D")},49684:(e,t,r)=>{"use strict";r.d(t,{mr:()=>o,Vu:()=>s,xO:()=>a});var i=r(68928),n=r(43274);const o=n.BF?(e,t)=>e.toLocaleTimeString(t.language,{hour:"numeric",minute:"2-digit"}):e=>(0,i.WU)(e,"shortTime"),s=n.BF?(e,t)=>e.toLocaleTimeString(t.language,{hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>(0,i.WU)(e,"mediumTime"),a=n.BF?(e,t)=>e.toLocaleTimeString(t.language,{weekday:"long",hour:"numeric",minute:"2-digit"}):e=>(0,i.WU)(e,"dddd, HH:mm")},5435:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});const i=[60,60,24,7],n=["second","minute","hour","day"];function o(e,t,r={}){let o=((r.compareTime||new Date).getTime()-e.getTime())/1e3;const s=o>=0?"past":"future";o=Math.abs(o);let a=Math.round(o);if(0===a)return t("ui.components.relative_time.just_now");let c="week";for(let e=0;e<i.length;e++){if(a<i[e]){c=n[e];break}o/=i[e],a=Math.round(o)}return t(!1===r.includeTense?`ui.components.relative_time.duration.${c}`:`ui.components.relative_time.${s}_duration.${c}`,"count",a)}},91168:(e,t,r)=>{"use strict";r.d(t,{Z:()=>n});const i=e=>e<10?`0${e}`:e;function n(e){const t=Math.floor(e/3600),r=Math.floor(e%3600/60),n=Math.floor(e%3600%60);return t>0?`${t}:${i(r)}:${i(n)}`:r>0?`${r}:${i(n)}`:n>0?""+n:null}},29171:(e,t,r)=>{"use strict";r.d(t,{D:()=>l});var i=r(56007),n=r(12198),o=r(44583),s=r(49684),a=r(45524),c=r(22311);const l=(e,t,r,l)=>{const d=void 0!==l?l:t.state;if(d===i.lz||d===i.nZ)return e(`state.default.${d}`);if(t.attributes.unit_of_measurement)return`${(0,a.u)(d,r)} ${t.attributes.unit_of_measurement}`;const p=(0,c.N)(t);if("input_datetime"===p){let e;if(!t.attributes.has_time)return e=new Date(t.attributes.year,t.attributes.month-1,t.attributes.day),(0,n.p)(e,r);if(!t.attributes.has_date){const i=new Date;return e=new Date(i.getFullYear(),i.getMonth(),i.getDay(),t.attributes.hour,t.attributes.minute),(0,s.mr)(e,r)}return e=new Date(t.attributes.year,t.attributes.month-1,t.attributes.day,t.attributes.hour,t.attributes.minute),(0,o.o)(e,r)}return"humidifier"===p&&"on"===d&&t.attributes.humidity?`${t.attributes.humidity} %`:"counter"===p||"number"===p||"input_number"===p?(0,a.u)(d,r):t.attributes.device_class&&e(`component.${p}.state.${t.attributes.device_class}.${d}`)||e(`component.${p}.state._.${d}`)||d}},45524:(e,t,r)=>{"use strict";r.d(t,{u:()=>n});var i=r(66477);const n=(e,t,r)=>{let n;switch(null==t?void 0:t.number_format){case i.y4.comma_decimal:n=["en-US","en"];break;case i.y4.decimal_comma:n=["de","es","it"];break;case i.y4.space_comma:n=["fr","sv","cs"];break;case i.y4.system:n=void 0;break;default:n=null==t?void 0:t.language}if(Number.isNaN=Number.isNaN||function e(t){return"number"==typeof t&&e(t)},!Number.isNaN(Number(e))&&Intl&&(null==t?void 0:t.number_format)!==i.y4.none)try{return new Intl.NumberFormat(n,o(e,r)).format(Number(e))}catch(t){return console.error(t),new Intl.NumberFormat(void 0,o(e,r)).format(Number(e))}return e?e.toString():""},o=(e,t)=>{const r=t||{};if("string"!=typeof e)return r;if(!t||!t.minimumFractionDigits&&!t.maximumFractionDigits){const t=e.indexOf(".")>-1?e.split(".")[1].length:0;r.minimumFractionDigits=t,r.maximumFractionDigits=t}return r}},43793:(e,t,r)=>{"use strict";r.d(t,{x:()=>i});const i=(e,t)=>e.substring(0,t.length)===t},42952:(e,t,r)=>{"use strict";var i=r(15652),n=r(5435);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function s(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function h(e,t,r){return(h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=o();if(i)for(var d=0;d<i.length;d++)n=i[d](n);var p=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(p.d.map(s)),e);n.initializeClassElements(p.F,u.elements),n.runClassFinishers(p.F,u.finishers)}([(0,i.Mo)("ha-relative-time")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"datetime",value:void 0},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){h(f(r.prototype),"disconnectedCallback",this).call(this),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){h(f(r.prototype),"connectedCallback",this).call(this),this.datetime&&this._startInterval()}},{kind:"method",key:"firstUpdated",value:function(e){h(f(r.prototype),"firstUpdated",this).call(this,e),this._updateRelative()}},{kind:"method",key:"update",value:function(e){h(f(r.prototype),"update",this).call(this,e),this._updateRelative()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}},{kind:"method",key:"_updateRelative",value:function(){this.datetime?this.innerHTML=(0,n.Z)(new Date(this.datetime),this.opp.localize):this.innerHTML=this.opp.localize("ui.components.relative_time.never")}}]}}),i.f4)},97389:(e,t,r)=>{"use strict";r.d(t,{mA:()=>n,lj:()=>o,U_:()=>s,nV:()=>a,Zm:()=>c});var i=r(43793);const n=(e,t,r,i)=>e.callWS({type:"trace/get",domain:t,item_id:r,run_id:i}),o=(e,t,r)=>e.callWS({type:"trace/list",domain:t,item_id:r}),s=(e,t,r)=>e.callWS({type:"trace/contexts",domain:t,item_id:r}),a=(e,t)=>{const r=t.split("/").reverse();let i=e;for(;r.length;){const e=r.pop(),t=Number(e);if(isNaN(t))i=i[e];else if(Array.isArray(i))i=i[t];else if(0!==t)throw new Error("If config is not an array, can only return index 0")}return i},c=e=>"trigger"===e||(0,i.x)(e,"trigger/")},45578:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HaAutomationTrace:()=>Ft});var i=r(15652),n=r(97389),o=(r(25230),r(47181)),s=(r(52039),r(55317)),a=r(81471);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const v=10,y=30,b={fromAttribute:e=>e.split(",").map((e=>parseInt(e))),toAttribute:e=>e instanceof Array?e.join(","):`${e}`};!function(e,t,r,i){var n=c();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(u(o.descriptor)||u(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(s.d.map(l)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-graph")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({type:Number})],key:"_num_items",value:()=>0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"branching",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,converter:b})],key:"track_start",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,converter:b})],key:"track_end",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"selected",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"short",value:()=>!1},{kind:"method",key:"updateChildren",value:async function(){this._num_items=this.children.length}},{kind:"method",key:"render",value:function(){const e=[];let t=0,r=0,n=Number.POSITIVE_INFINITY;if(this.branching)for(const i of Array.from(this.children)){if("head"===i.slot)continue;const o=i.getBoundingClientRect();e.push({x:o.width/2+t,height:o.height,start:null!=i.getAttribute("graphStart"),end:null!=i.getAttribute("graphEnd")}),t+=o.width,r=Math.max(r,o.height),n=Math.min(n,o.height)}return i.dy`
      <slot name="head" @slotchange=${this.updateChildren}> </slot>
      ${this.branching?i.YP`
            <svg
              id="top"
              width="${t}"
              height="${20}"
            >
              ${e.map(((e,r)=>{var n,o,s;return e.start?"":i.YP`
                  <path
                    class="${(0,a.$)({line:!0,track:null!==(n=null===(o=this.track_start)||void 0===o?void 0:o.includes(r))&&void 0!==n&&n})}"
                    id="${(null===(s=this.track_start)||void 0===s?void 0:s.includes(r))?"track-start":""}"
                    index=${r}
                    d="
                      M ${t/2} 0
                      L ${e.x} ${20}
                      "/>
                `}))}
              <use xlink:href="#track-start" />
            </svg>
          `:""}
      <div id="branches">
        ${this.branching?i.YP`
              <svg
                id="lines"
                width="${t}"
                height="${r}"
              >
                ${e.map(((e,t)=>{var n,o;return e.end?"":i.YP`
                    <path
                      class="${(0,a.$)({line:!0,track:null!==(n=null===(o=this.track_end)||void 0===o?void 0:o.includes(t))&&void 0!==n&&n})}"
                      index=${t}
                      d="
                        M ${e.x} ${e.height}
                        l 0 ${r-e.height}
                        "/>
                  `}))}
              </svg>
            `:""}
        <slot @slotchange=${this.updateChildren}></slot>
      </div>

      ${this.branching&&!this.short?i.YP`
            <svg
              id="bottom"
              width="${t}"
              height="${30}"
            >
              ${e.map(((e,r)=>{var n,o,s;return e.end?"":i.YP`
                  <path
                    class="${(0,a.$)({line:!0,track:null!==(n=null===(o=this.track_end)||void 0===o?void 0:o.includes(r))&&void 0!==n&&n})}"
                    id="${(null===(s=this.track_end)||void 0===s?void 0:s.includes(r))?"track-end":""}"
                    index=${r}
                    d="
                      M ${e.x} 0
                      L ${e.x} ${v}
                      L ${t/2} ${30}
                      "/>
                `}))}
              <use xlink:href="#track-end" />
            </svg>
          `:""}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        --stroke-clr: var(--stroke-color, var(--secondary-text-color));
        --active-clr: var(--active-color, var(--primary-color));
        --track-clr: var(--track-color, var(--accent-color));
        --hover-clr: var(--hover-color, var(--primary-color));
        --disabled-clr: var(--disabled-color, var(--disabled-text-color));
        --default-trigger-color: 3, 169, 244;
        --rgb-trigger-color: var(--trigger-color, var(--default-trigger-color));
        --background-clr: var(--background-color, white);
        --default-icon-clr: var(--icon-color, black);
        --icon-clr: var(--stroke-clr);
      }
      :host(:focus) {
        outline: none;
      }
      #branches {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      :host([branching]) #branches {
        flex-direction: row;
        align-items: start;
      }
      :host([branching]) ::slotted(*) {
        z-index: 1;
      }
      :host([branching]) ::slotted([slot="head"]) {
        margin-bottom: ${-10}px;
      }

      #lines {
        position: absolute;
      }

      path.line {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      path.line.track {
        stroke: var(--track-clr);
      }
      :host([disabled]) path.line {
        stroke: var(--disabled-clr);
      }
    `}}]}}),i.oi);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!E(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=x(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:$(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=$(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function k(e){var t,r=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function P(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function $(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function D(e,t,r){return(D="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=g();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(P(o.descriptor)||P(n.descriptor)){if(E(o)||E(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(E(o)){if(E(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}w(o,n)}else t.push(o)}return t}(s.d.map(k)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-graph-node")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)()],key:"iconPath",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"graphstart",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"nofocus",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Number})],key:"badge",value:void 0},{kind:"method",key:"connectedCallback",value:function(){D(C(r.prototype),"connectedCallback",this).call(this),this.hasAttribute("tabindex")||this.nofocus||this.setAttribute("tabindex","0")}},{kind:"method",key:"render",value:function(){const e=y+(this.graphstart?2:11);return i.YP`
    <svg
    width="${40}px"
    height="${e}px"
    viewBox="-${Math.ceil(20)} -${this.graphstart?Math.ceil(e/2):Math.ceil(25)} ${40} ${e}"
    >
      ${this.graphstart?"":i.YP`
          <path
            class="connector"
            d="
              M 0 ${-25}
              L 0 0
            "
            line-caps="round"
          />
          `}
    <g class="node">
      <circle
        cx="0"
        cy="0"
        r="${15}"
      />
      }
      ${this.badge?i.YP`
        <g class="number">
          <circle
            cx="8"
            cy="${-15}"
            r="8"
          ></circle>
          <text
            x="8"
            y="${-15}"
            text-anchor="middle"
            alignment-baseline="middle"
          >${this.badge>9?"9+":this.badge}</text>
        </g>
      `:""}
      <g
        style="pointer-events: none"
        transform="translate(${-12} ${-12})"
      >
        ${this.iconPath?i.YP`<path class="icon" d="${this.iconPath}"/>`:""}
      </g>
    </g>
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: flex;
        flex-direction: column;
      }
      :host(.track) {
        --stroke-clr: var(--track-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host(.active) circle {
        --stroke-clr: var(--active-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host(:focus) {
        outline: none;
      }
      :host(:hover) circle {
        --stroke-clr: var(--hover-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host([disabled]) circle {
        stroke: var(--disabled-clr);
      }
      :host-context([disabled]) {
        --stroke-clr: var(--disabled-clr);
      }
      :host([nofocus]):host-context(.active),
      :host([nofocus]):host-context(:focus) {
        --circle-clr: var(--active-clr);
        --icon-clr: var(--default-icon-clr);
      }
      circle,
      path.connector {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      circle {
        fill: var(--background-clr);
        stroke: var(--circle-clr, var(--stroke-clr));
      }
      .number circle {
        fill: var(--track-clr);
        stroke: none;
        stroke-width: 0;
      }
      .number text {
        font-size: smaller;
      }
      path.icon {
        fill: var(--icon-clr);
      }

      :host(.triggered) svg {
        overflow: visible;
      }
      :host(.triggered) circle {
        animation: glow 10s;
      }
      @keyframes glow {
        0% {
          filter: drop-shadow(0px 0px 5px rgba(var(--rgb-trigger-color), 0));
        }
        10% {
          filter: drop-shadow(0px 0px 10px rgba(var(--rgb-trigger-color), 1));
        }
        100% {
          filter: drop-shadow(0px 0px 5px rgba(var(--rgb-trigger-color), 0));
        }
      }
    `}}]}}),i.oi);var T=r(42141);function A(){A=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!j(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return N(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?N(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=F(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:z(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=z(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function S(e){var t,r=F(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function O(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function I(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function z(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function F(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function N(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=A();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(I(o.descriptor)||I(n.descriptor)){if(j(o)||j(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(j(o)){if(j(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}O(o,n)}else t.push(o)}return t}(s.d.map(S)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-graph-spacer")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"method",key:"render",value:function(){return i.YP`
    <svg
    width="${v}px"
    height="${41}px"
    viewBox="-${5} 0 10 ${41}"
    >
          <path
            class="connector"
            d="
              M 0 ${41}
              L 0 0
            "
            line-caps="round"
          />
      }
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: flex;
        flex-direction: column;
      }
      :host(.track) {
        --stroke-clr: var(--track-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host-context([disabled]) {
        --stroke-clr: var(--disabled-clr);
      }
      path.connector {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
    `}}]}}),i.oi);function R(){R=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!B(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?Y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=q(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:W(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=W(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function M(e){var t,r=q(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function L(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function B(e){return e.decorators&&e.decorators.length}function U(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function W(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function q(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function V(e,t,r){return(V="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=H(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function H(e){return(H=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=R();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(U(o.descriptor)||U(n.descriptor)){if(B(o)||B(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(B(o)){if(B(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}L(o,n)}else t.push(o)}return t}(s.d.map(M)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-script-graph")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"selected",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"trackedNodes",value:()=>({})},{kind:"method",key:"selectNode",value:function(e,t){return()=>{(0,o.B)(this,"graph-node-selected",{config:e,path:t})}}},{kind:"method",key:"render_trigger",value:function(e,t){const r=`trigger/${t}`,n=this.trace&&r in this.trace.trace;return n&&(this.trackedNodes[r]={config:e,path:r}),i.dy`
      <hat-graph-node
        graphStart
        @focus=${this.selectNode(e,r)}
        class=${(0,a.$)({track:n,active:this.selected===r})}
        .iconPath=${s.AD$}
        tabindex=${n?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_condition",value:function(e,t){const r=`condition/${t}`,n=this.trace.trace[r],o=void 0===(null==n?void 0:n[0].result)?0:n[0].result.result?1:2;return n&&(this.trackedNodes[r]={config:e,path:r}),i.dy`
      <hat-graph
        branching
        @focus=${this.selectNode(e,r)}
        class=${(0,a.$)({track:o,active:this.selected===r})}
        .track_start=${[o]}
        .track_end=${[o]}
        tabindex=${n?"-1":"0"}
        short
      >
        <hat-graph-node
          slot="head"
          class=${(0,a.$)({track:void 0!==n})}
          .iconPath=${s._wd}
          nofocus
          graphEnd
        ></hat-graph-node>
        <div
          style=${"width: 40px;"}
          graphStart
          graphEnd
        ></div>
        <div></div>
        <hat-graph-node
          .iconPath=${s.r5M}
          graphEnd
          nofocus
          class=${(0,a.$)({track:2===o})}
        ></hat-graph-node>
      </hat-graph>
    `}},{kind:"method",key:"render_choose_node",value:function(e,t){var r,n,o,c;const l=this.trace.trace[t],d=(null==l?void 0:l[0].result)?"default"===l[0].result.choice?[(null===(r=e.choose)||void 0===r?void 0:r.length)||0]:[l[0].result.choice]:[];return i.dy`
      <hat-graph
        tabindex=${void 0===l?"-1":"0"}
        branching
        .track_start=${d}
        .track_end=${d}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:void 0!==l,active:this.selected===t})}
      >
        <hat-graph-node
          .iconPath=${s.g$R}
          class=${(0,a.$)({track:void 0!==l})}
          slot="head"
          nofocus
        ></hat-graph-node>

        ${null===(n=e.choose)||void 0===n?void 0:n.map(((r,n)=>{var o;const c=`${t}/choose/${n}`,d=void 0!==l&&(null===(o=l[0].result)||void 0===o?void 0:o.choice)===n;return d&&(this.trackedNodes[c]={config:e,path:c}),i.dy`
            <hat-graph>
              <hat-graph-node
                .iconPath=${!l||d?s.Eut:s.Ii0}
                @focus=${this.selectNode(e,c)}
                class=${(0,a.$)({active:this.selected===c,track:d})}
              ></hat-graph-node>
              ${(0,T.r)(r.sequence).map(((e,t)=>this.render_node(e,`${c}/sequence/${t}`)))}
            </hat-graph>
          `}))}
        <hat-graph>
          <hat-graph-spacer
            class=${(0,a.$)({track:void 0!==l&&"default"===(null===(o=l[0].result)||void 0===o?void 0:o.choice)})}
          ></hat-graph-spacer>
          ${null===(c=(0,T.r)(e.default))||void 0===c?void 0:c.map(((e,r)=>this.render_node(e,`${t}/default/${r}`)))}
        </hat-graph>
      </hat-graph>
    `}},{kind:"method",key:"render_condition_node",value:function(e,t){const r=this.trace.trace[t]||void 0,n=void 0===(null==r?void 0:r[0].result)?0:r[0].result.result?1:2;return i.dy`
      <hat-graph
        branching
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:n,active:this.selected===t})}
        .track_start=${[n]}
        .track_end=${[n]}
        tabindex=${void 0===r?"-1":"0"}
        short
      >
        <hat-graph-node
          slot="head"
          class=${(0,a.$)({track:Boolean(r)})}
          .iconPath=${s._wd}
          nofocus
          graphEnd
        ></hat-graph-node>
        <div
          style=${"width: 40px;"}
          graphStart
          graphEnd
        ></div>
        <div></div>
        <hat-graph-node
          .iconPath=${s.r5M}
          graphEnd
          nofocus
          class=${(0,a.$)({track:2===n})}
        ></hat-graph-node>
      </hat-graph>
    `}},{kind:"method",key:"render_delay_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.clR}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_device_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.p0g}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_event_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.XW6}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_repeat_node",value:function(e,t){var r,n;const o=this.trace.trace[t],c=o?[0,1]:[],l=null===(r=this.trace)||void 0===r||null===(n=r.trace[`${t}/repeat/sequence/0`])||void 0===n?void 0:n.length;return i.dy`
      <hat-graph
        .track_start=${c}
        .track_end=${c}
        tabindex=${void 0===o?"-1":"0"}
        branching
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
      >
        <hat-graph-node
          .iconPath=${s.jcD}
          class=${(0,a.$)({track:o})}
          slot="head"
          nofocus
        ></hat-graph-node>
        <hat-graph-node
          .iconPath=${s.XHH}
          nofocus
          class=${(0,a.$)({track:c.includes(1)})}
          .badge=${l}
        ></hat-graph-node>
        <hat-graph>
          ${(0,T.r)(e.repeat.sequence).map(((e,r)=>this.render_node(e,`${t}/repeat/sequence/${r}`)))}
        </hat-graph>
      </hat-graph>
    `}},{kind:"method",key:"render_scene_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.XW6}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_service_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.zrb}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_wait_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s._yq}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
        tabindex=${this.trace&&t in this.trace.trace?"0":"-1"}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_other_node",value:function(e,t){return i.dy`
      <hat-graph-node
        .iconPath=${s.Nqu}
        @focus=${this.selectNode(e,t)}
        class=${(0,a.$)({track:t in this.trace.trace,active:this.selected===t})}
      ></hat-graph-node>
    `}},{kind:"method",key:"render_node",value:function(e,t){const r={choose:this.render_choose_node,condition:this.render_condition_node,delay:this.render_delay_node,device_id:this.render_device_node,event:this.render_event_node,repeat:this.render_repeat_node,scene:this.render_scene_node,service:this.render_service_node,wait_template:this.render_wait_node,wait_for_trigger:this.render_wait_node,other:this.render_other_node},i=r[Object.keys(r).find((t=>t in e))||"other"].bind(this)(e,t);return this.trace&&t in this.trace.trace&&(this.trackedNodes[t]={config:e,path:t}),i}},{kind:"method",key:"render",value:function(){const e=Object.keys(this.trackedNodes);let t=this.trace&&"trigger"in this.trace.trace?void 0:[0];const r=(0,T.r)(this.trace.config.trigger).map(((e,r)=>(this.trace&&`trigger/${r}`in this.trace.trace&&(t=[r]),this.render_trigger(e,r))));try{var n;return i.dy`
        <hat-graph class="parent">
          <div></div>
          <hat-graph
            branching
            id="trigger"
            .short=${r.length<2}
            .track_start=${t}
            .track_end=${t}
          >
            ${r}
          </hat-graph>
          <hat-graph id="condition">
            ${null===(n=(0,T.r)(this.trace.config.condition))||void 0===n?void 0:n.map(((e,t)=>this.render_condition(e,t)))}
          </hat-graph>
          ${(0,T.r)(this.trace.config.action).map(((e,t)=>this.render_node(e,`action/${t}`)))}
        </hat-graph>
        <div class="actions">
          <mwc-icon-button
            .disabled=${0===e.length||e[0]===this.selected}
            @click=${this.previousTrackedNode}
          >
            <ha-svg-icon .path=${s.Waq}></ha-svg-icon>
          </mwc-icon-button>
          <mwc-icon-button
            .disabled=${0===e.length||e[e.length-1]===this.selected}
            @click=${this.nextTrackedNode}
          >
            <ha-svg-icon .path=${s.CW}></ha-svg-icon>
          </mwc-icon-button>
        </div>
      `}catch(e){return i.dy`
        <div class="error">
          Error rendering graph. Please download trace and share with the
          developers.
        </div>
      `}}},{kind:"method",key:"update",value:function(e){e.has("trace")&&(this.trackedNodes={}),V(H(r.prototype),"update",this).call(this,e)}},{kind:"method",key:"updated",value:function(e){if(V(H(r.prototype),"updated",this).call(this,e),e.has("trace")){const e=this.getTrackedNodes(),t=Object.keys(e);if(""===this.selected||!(this.selected in t))for(const r of t)if(e[r]){(0,o.B)(this,"graph-node-selected",e[r]);break}if(this.trace){const e=Object.keys(this.trace.trace),t=Object.keys(this.trackedNodes).sort(((t,r)=>e.indexOf(t)-e.indexOf(r))).reduce(((e,t)=>(e[t]=this.trackedNodes[t],e)),{});this.trackedNodes=t}}}},{kind:"method",key:"getTrackedNodes",value:function(){return this.trackedNodes}},{kind:"method",key:"previousTrackedNode",value:function(){const e=this.getTrackedNodes(),t=Object.keys(e);for(let r=t.indexOf(this.selected)-1;r>=0;r--)if(e[t[r]]){(0,o.B)(this,"graph-node-selected",e[t[r]]);break}}},{kind:"method",key:"nextTrackedNode",value:function(){const e=this.getTrackedNodes(),t=Object.keys(e);for(let r=t.indexOf(this.selected)+1;r<t.length;r++)if(e[t[r]]){(0,o.B)(this,"graph-node-selected",e[t[r]]);break}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: flex;
      }
      .actions {
        display: flex;
        flex-direction: column;
      }
      .parent {
        margin-left: 8px;
      }
      .error {
        padding: 16px;
        max-width: 300px;
      }
    `}}]}}),i.oi);var J=r(11654),Z=r(29311),X=r(55422),K=r(44583),G=r(83278),Q=r(26765),ee=r(50947);r(10983),r(53822);function te(){te=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ne(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ce(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?ce(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=ae(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:se(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=se(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function re(e){var t,r=ae(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function ie(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ne(e){return e.decorators&&e.decorators.length}function oe(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function se(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function ae(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function ce(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=te();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(oe(o.descriptor)||oe(n.descriptor)){if(ne(o)||ne(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ne(o)){if(ne(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ie(o,n)}else t.push(o)}return t}(s.d.map(re)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-logbook-note")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return i.dy`
      Not all shown logbook entries might be related to this automation.
    `}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
    :host {
      display: block;
      text-align: center;
      font-style: italic;
      padding: 16px;
      margin-top: 8px;
    }
  `}]}}),i.oi);const le=i.iv`
  .tabs {
    background-color: var(--primary-background-color);
    border-top: 1px solid var(--divider-color);
    border-bottom: 1px solid var(--divider-color);
    display: flex;
    padding-left: 4px;
  }

  .tabs.top {
    border-top: none;
  }

  .tabs > * {
    padding: 2px 16px;
    cursor: pointer;
    position: relative;
    bottom: -1px;
    border: none;
    border-bottom: 2px solid transparent;
    user-select: none;
    background: none;
    color: var(--primary-text-color);
    outline: none;
    transition: background 15ms linear;
  }

  .tabs > *.active {
    border-bottom-color: var(--accent-color);
  }

  .tabs > *:focus,
  .tabs > *:hover {
    background: var(--secondary-background-color);
  }
`;r(97740);function de(){de=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!he(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ye(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?ye(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=ve(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:me(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=me(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function pe(e){var t,r=ve(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function ue(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function he(e){return e.decorators&&e.decorators.length}function fe(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function me(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function ve(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function ye(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=de();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(fe(o.descriptor)||fe(n.descriptor)){if(he(o)||he(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(he(o)){if(he(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ue(o,n)}else t.push(o)}return t}(s.d.map(pe)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace-path-details")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"selected",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"trace",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"logbookEntries",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"trackedNodes",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_view",value:()=>"config"},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="padded-box trace-info">
        ${this._renderSelectedTraceInfo()}
      </div>

      <div class="tabs top">
        ${[["config","Step Config"],["changed_variables","Changed Variables"],["logbook","Related logbook entries"]].map((([e,t])=>i.dy`
            <button
              .view=${e}
              class=${(0,a.$)({active:this._view===e})}
              @click=${this._showTab}
            >
              ${t}
            </button>
          `))}
      </div>
      ${"config"===this._view?this._renderSelectedConfig():"changed_variables"===this._view?this._renderChangedVars():this._renderLogbook()}
    `}},{kind:"method",key:"_renderSelectedTraceInfo",value:function(){var e;const t=this.trace.trace;if(!(null===(e=this.selected)||void 0===e?void 0:e.path))return"Select a node on the left for more information.";const r=this.selected.path.split("/");if("default"===r[r.length-1]){var n,o;const e=t[r.slice(0,r.length-1).join("/")];if(e&&"default"===(null===(n=e[0])||void 0===n||null===(o=n.result)||void 0===o?void 0:o.choice))return"The default node was executed because no choices matched."}if(!(this.selected.path in t))return"This node was not executed and so no further trace information is available.";const s=t[this.selected.path];return s.map(((e,t)=>{const{path:r,timestamp:n,result:o,error:a,changed_variables:c,...l}=e;return i.dy`
        ${1===s.length?"":i.dy`<h3>Iteration ${t+1}</h3>`}
        Executed:
        ${(0,K.E)(new Date(n),this.opp.locale)}<br />
        ${o?i.dy`Result:
              <pre>${(0,ee.safeDump)(o)}</pre>`:a?i.dy`<div class="error">Error: ${a}</div>`:""}
        ${0===Object.keys(l).length?"":i.dy`<pre>${(0,ee.safeDump)(l)}</pre>`}
      `}))}},{kind:"method",key:"_renderSelectedConfig",value:function(){var e;if(!(null===(e=this.selected)||void 0===e?void 0:e.path))return"";const t=(0,n.nV)(this.trace.config,this.selected.path);return t?i.dy`<ha-code-editor
          .value=${(0,ee.safeDump)(t).trimRight()}
          readOnly
        ></ha-code-editor>`:"Unable to find config"}},{kind:"method",key:"_renderChangedVars",value:function(){const e=this.trace.trace[this.selected.path];return i.dy`
      <div class="padded-box">
        ${e.map(((e,t)=>i.dy`
            ${t>0?i.dy`<p>Iteration ${t+1}</p>`:""}
            ${0===Object.keys(e.changed_variables||{}).length?"No variables changed":i.dy`<pre>
${(0,ee.safeDump)(e.changed_variables).trimRight()}</pre
                >`}
          `))}
      </div>
    `}},{kind:"method",key:"_renderLogbook",value:function(){const e=this.trace.trace,t=e[this.selected.path],r=Object.keys(this.trackedNodes),n=r.indexOf(this.selected.path);if(-1===n)return i.dy`<div class="padded-box">Node not tracked.</div>`;let o;if(n===r.length-1){const e=new Date(t[0].timestamp),r=this.logbookEntries.findIndex((t=>new Date(t.when)>=e));o=-1===r?[]:this.logbookEntries.slice(r)}else{const i=e[r[n+1]],s=new Date(t[0].timestamp),a=new Date(i[0].timestamp);o=[];for(const e of this.logbookEntries||[]){const t=new Date(e.when);if(t>=s){if(!(t<a))break;o.push(e)}}}return o.length?i.dy`
          <ha-logbook
            relative-time
            .opp=${this.opp}
            .entries=${o}
            .narrow=${this.narrow}
          ></ha-logbook>
          <hat-logbook-note></hat-logbook-note>
        `:i.dy`<div class="padded-box">
          No Logbook entries found for this step.
        </div>`}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"get",static:!0,key:"styles",value:function(){return[le,i.iv`
        .padded-box {
          margin: 16px;
        }

        :host(:not([narrow])) .trace-info {
          min-height: 250px;
        }

        pre {
          margin: 0;
        }

        .error {
          color: var(--error-color);
        }
      `]}}]}}),i.oi);function be(){be=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!we(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return xe(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?xe(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=$e(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Pe(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=Pe(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function ge(e){var t,r=$e(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function ke(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function we(e){return e.decorators&&e.decorators.length}function Ee(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Pe(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function $e(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function xe(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=be();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(Ee(o.descriptor)||Ee(n.descriptor)){if(we(o)||we(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(we(o)){if(we(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ke(o,n)}else t.push(o)}return t}(s.d.map(ge)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-timeline")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"label",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"raised",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"lastItem",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:String})],key:"icon",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"moreItems",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_showMore",value:()=>!1},{kind:"method",key:"render",value:function(){return i.dy`
      <div class="timeline-start">
        ${this.label?"":i.dy`
              <ha-svg-icon .path=${this.icon||s.KS$}></ha-svg-icon>
            `}
        ${this.lastItem?"":i.dy`<div class="line"></div>`}
      </div>
      <div class="content">
        <slot></slot>
        ${this.moreItems?i.dy`
              <div>
                ${this._showMore||1===this.moreItems.length?this.moreItems:i.dy`
                      <button class="link" @click=${this._handleShowMore}>
                        Show ${this.moreItems.length} more items
                      </button>
                    `}
              </div>
            `:""}
      </div>
    `}},{kind:"method",key:"_handleShowMore",value:function(){this._showMore=!0}},{kind:"get",static:!0,key:"styles",value:function(){return[i.iv`
        :host {
          display: flex;
          flex-direction: row;
        }
        :host(:not([lastItem])) {
          min-height: 50px;
        }
        :host([label]) {
          margin-top: -8px;
          font-style: italic;
          color: var(--timeline-label-color, var(--secondary-text-color));
        }
        .timeline-start {
          display: flex;
          flex-direction: column;
          align-items: center;
          margin-right: 8px;
          width: 24px;
        }
        ha-svg-icon {
          color: var(
            --timeline-ball-color,
            var(--timeline-color, var(--secondary-text-color))
          );
          border-radius: 50%;
        }
        :host([raised]) ha-svg-icon {
          transform: scale(1.3);
        }
        .line {
          flex: 1;
          width: 2px;
          background-color: var(
            --timeline-line-color,
            var(--timeline-color, var(--secondary-text-color))
          );
          margin: 4px 0;
        }
        .content {
          margin-top: 2px;
        }
        :host(:not([lastItem])) .content {
          padding-bottom: 16px;
        }
        :host([label]) .content {
          margin-top: 0;
          padding-top: 6px;
        }
      `,J.k1]}}]}}),i.oi);var _e=r(44547),De=r(5435),Ce=r(91168),Te=r(91741),Ae=r(61761);var Se=r(49629);function Oe(){Oe=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ze(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Me(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?Me(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Re(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Ne(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=Ne(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function je(e){var t,r=Re(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function Ie(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ze(e){return e.decorators&&e.decorators.length}function Fe(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Ne(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Re(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Me(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function Le(e,t,r){return(Le="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Be(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function Be(e){return(Be=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function Ue(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}const We=(e,t)=>Math.abs(t.getTime()-e.getTime())>1e3;class qe{constructor(e,t,r){this.opp=e,this.entries=t,Ue(this,"lastReportedTime",void 0),this.lastReportedTime=new Date(r.timestamp.start)}setLastReportedTime(e){this.lastReportedTime=e}renderTime(e,t){this.entries.push(i.dy`
      <ha-timeline label>
        ${(0,De.Z)(e,this.opp.localize,{compareTime:t,includeTense:!1})}
        later
      </ha-timeline>
    `),this.lastReportedTime=t}maybeRenderTime(e){return We(e,this.lastReportedTime)?(this.renderTime(this.lastReportedTime,e),!0):(this.lastReportedTime=e,!1)}}class Ye{constructor(e,t,r){this.entries=e,this.timeTracker=t,this.logbookEntries=r,Ue(this,"curIndex",void 0),Ue(this,"pendingItems",[]),this.curIndex=r.length>0&&"automation"===r[0].domain?1:0}get curItem(){return this.logbookEntries[this.curIndex]}get hasNext(){return this.curIndex!==this.logbookEntries.length}maybeRenderItem(){const e=this.curItem;this.curIndex++;const t=new Date(e.when);if(0===this.pendingItems.length)return void this.pendingItems.push([t,e]);const r=this.pendingItems[this.pendingItems.length-1][0];We(r,t)&&(this._renderLogbookEntries(),this.timeTracker.renderTime(r,t)),this.pendingItems.push([t,e])}flush(){this.pendingItems.length>0&&this._renderLogbookEntries()}_renderLogbookEntries(){this.timeTracker.maybeRenderTime(this.pendingItems[0][0]);const e=[];let t,r;for(t=0;t<Math.min(this.pendingItems.length,2);t++)e.push(this._renderLogbookEntryHelper(this.pendingItems[t][1]));if(t<this.pendingItems.length)for(r=[];t<this.pendingItems.length;t++)r.push(this._renderLogbookEntryHelper(this.pendingItems[t][1]));this.entries.push(i.dy`
      <ha-timeline .icon=${s.KS$} .moreItems=${r}>
        ${e}
      </ha-timeline>
    `),this.timeTracker.setLastReportedTime(this.pendingItems[this.pendingItems.length-1][0]),this.pendingItems=[]}_renderLogbookEntryHelper(e){return i.dy`${e.name} (${e.entity_id})
      ${e.message||`turned ${e.state}`}<br />`}}class Ve{constructor(e,t,r,i,n){this.opp=e,this.entries=t,this.trace=r,this.logbookRenderer=i,this.timeTracker=n,Ue(this,"curIndex",0),Ue(this,"keys",void 0),this.keys=Object.keys(r.trace)}get curItem(){return this._getItem(this.curIndex)}get hasNext(){return this.curIndex!==this.keys.length}renderItem(){this.curIndex=this._renderItem(this.curIndex)}_getItem(e){return this.trace.trace[this.keys[e]]}_renderItem(e,t){const r=this._getItem(e);if((0,n.Zm)(r[0].path))return this._handleTrigger(e,r[0]);const o=new Date(r[0].timestamp);for(;this.logbookRenderer.hasNext&&new Date(this.logbookRenderer.curItem.when)<o;)this.logbookRenderer.maybeRenderItem();this.logbookRenderer.flush(),this.timeTracker.maybeRenderTime(o);const s=r[0].path;let a;try{a=(0,n.nV)(this.trace.config,s)}catch(t){return this.entries.push(i.dy`Unable to extract path ${s}. Download trace and report as bug`),e+1}return 2===s.split("/").length||t?(t||(t=(0,_e.Pw)(a)),"choose"===t?this._handleChoose(e):(this._renderEntry(s,((e,t,r)=>{if(t.alias)return t.alias;if(r||(r=(0,_e.Pw)(t)),"service"===r){const e=t;let i;if(e.service_template||e.service&&(0,Ae.J)(e.service))i="Call a service based on a template";else{if(!e.service)return r;i=`Call service ${e.service}`}if(e.target){const t=[];for(const[r,i]of Object.entries({area_id:"areas",device_id:"devices",entity_id:"entities"})){if(!(r in e.target))continue;const n=Array.isArray(e.target[r])?e.target[r]:[e.target[r]],o=[];let s=!0;for(const e of n){if((0,Ae.J)(e)){t.push(`templated ${i}`),s=!1;break}o.push(e)}s&&t.push(`${i} ${o.join(", ")}`)}t.length>0&&(i+=` on ${t.join(", ")}`)}return i}if("delay"===r){const e=t;let r;return r="number"==typeof e.delay?`for ${(0,Ce.Z)(e.delay)}`:"string"==typeof e.delay?(0,Ae.J)(e.delay)?"based on a template":`for ${e.delay}`:`for ${JSON.stringify(e.delay)}`,`Delay ${r}`}if("activate_scene"===r){const r=t,i=e.states[r.scene];return`Activate scene ${i?(0,Te.C)(i):r.scene}`}if("wait_for_trigger"===r){const e=t;return`Wait for ${(0,T.r)(e.wait_for_trigger).map((e=>(e=>`${e.platform} trigger`)(e))).join(", ")}`}if("variables"===r){const e=t;return`Define variables ${Object.keys(e.variables).join(", ")}`}if("fire_event"===r){const e=t;return(0,Ae.J)(e.event)?"Fire event based on a template":`Fire event ${e.event}`}return"wait_template"===r?"Wait for a template to render true":"check_condition"===r?`Test ${i=t,i.alias?i.alias:"template"===i.condition?"Test a template":`${i.condition} condition`}`:r;var i})(this.opp,a,t)),e+1)):(this._renderEntry(s,s.replace(/\//g," ")),e+1)}_handleTrigger(e,t){return this._renderEntry(t.path,`Triggered ${"trigger"===t.path?"manually":`by the ${this.trace.trigger}`} at\n    ${(0,K.E)(new Date(t.timestamp),this.opp.locale)}`,s.mdD),e+1}_handleChoose(e){var t;const r=this.keys[e],i=r.split("/").length-1,n=this._getItem(e)[0],o="default"===(null===(t=n.result)||void 0===t?void 0:t.choice),s=this._getDataFromPath(this.keys[e]).alias||"Choose";if(o)this._renderEntry(r,`${s}: Default action executed`);else{var a,c;const t=this._getDataFromPath(`${this.keys[e]}/choose/${null===(a=n.result)||void 0===a?void 0:a.choice}`),i=t?`${t.alias||`Choice ${null===(c=n.result)||void 0===c?void 0:c.choice}`} executed`:`Error: ${n.error}`;this._renderEntry(r,`${s}: ${i}`)}let l;for(l=e+1;l<this.keys.length;l++){const e=this.keys[l].split("/");if(e.length<=i)return l;if(o&&"default"===e[i+1]||!o&&"sequence"===e[i+3])break}for(;l<this.keys.length;){const e=this.keys[l];if(e.split("/").length<=i)return l;l=this._renderItem(l,(0,_e.Pw)(this._getDataFromPath(e)))}return l}_renderEntry(e,t,r=s.U3w){this.entries.push(i.dy`
      <ha-timeline .icon=${r} data-path=${e}>
        ${t}
      </ha-timeline>
    `)}_getDataFromPath(e){return(0,n.nV)(this.trace.config,e)}}!function(e,t,r,i){var n=Oe();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(Fe(o.descriptor)||Fe(n.descriptor)){if(ze(o)||ze(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ze(o)){if(ze(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}Ie(o,n)}else t.push(o)}return t}(s.d.map(je)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("hat-trace-timeline")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"logbookEntries",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"selectedPath",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"allowPick",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.trace)return i.dy``;const e=[],t=new qe(this.opp,e,this.trace),r=new Ye(e,t,this.logbookEntries||[]),n=new Ve(this.opp,e,this.trace,r,t);for(;n.hasNext;)n.renderItem();for(;r.hasNext;)r.maybeRenderItem();r.flush();const o=()=>(0,K.E)(new Date(this.trace.timestamp.finish),this.opp.locale),a=()=>`(runtime:\n      ${((new Date(this.trace.timestamp.finish).getTime()-new Date(this.trace.timestamp.start).getTime())/1e3).toFixed(2)}\n      seconds)`;let c;if("running"===this.trace.state)c={description:"Still running",icon:s.plV};else if("debugged"===this.trace.state)c={description:"Debugged",icon:s.Oy8};else if("finished"===this.trace.script_execution)c={description:`Finished at ${o()} ${a()}`,icon:s.mdD};else if("aborted"===this.trace.script_execution)c={description:`Aborted at ${o()} ${a()}`,icon:s.fr4};else if("cancelled"===this.trace.script_execution)c={description:`Cancelled at ${o()} ${a()}`,icon:s.fr4};else{let e,t,r=!1;switch(this.trace.script_execution){case"failed_conditions":e="a condition failed";break;case"failed_single":e="only a single execution is allowed";break;case"failed_max_runs":e="maximum number of parallel runs reached";break;case"error":e="an error was encountered",r=!0,t=i.dy`<br /><br />${this.trace.error}`;break;default:e=`of unknown reason "${this.trace.script_execution}"`,r=!0}c={description:i.dy`Stopped because ${e} at ${o()}
        ${a()}${t||""}`,icon:s.fr4,className:r?"error":void 0}}return c&&e.push(i.dy`
        <ha-timeline
          lastItem
          .icon=${c.icon}
          class=${(0,Se.o)(c.className)}
        >
          ${c.description}
        </ha-timeline>
      `),i.dy`${e}`}},{kind:"method",key:"updated",value:function(e){if(Le(Be(r.prototype),"updated",this).call(this,e),this.allowPick&&e.has("trace")&&this.trace&&this.selectedPath&&!(this.selectedPath in this.trace.trace)){const e=this.shadowRoot.querySelector("ha-timeline[data-path]");e&&((0,o.B)(this,"value-changed",{value:e.dataset.path}),this.selectedPath=e.dataset.path)}(e.has("trace")||e.has("selectedPath"))&&this.shadowRoot.querySelectorAll("ha-timeline[data-path]").forEach((e=>{if(e.toggleAttribute("selected",this.selectedPath===e.dataset.path),!this.allowPick||0===e.tabIndex)return;e.tabIndex=0;const t=()=>{this.selectedPath=e.dataset.path,(0,o.B)(this,"value-changed",{value:e.dataset.path})};e.addEventListener("click",t),e.addEventListener("keydown",(e=>{"Enter"!==e.key&&" "!==e.key||t()})),e.addEventListener("mouseover",(()=>{e.raised=!0})),e.addEventListener("mouseout",(()=>{e.raised=!1}))}))}},{kind:"get",static:!0,key:"styles",value:function(){return[i.iv`
        ha-timeline[lastItem].condition {
          --timeline-ball-color: var(--error-color);
        }
        ha-timeline[data-path] {
          cursor: pointer;
        }
        ha-timeline[selected] {
          --timeline-ball-color: var(--primary-color);
        }
        ha-timeline:focus {
          outline: none;
          --timeline-ball-color: var(--accent-color);
        }
        .error {
          --timeline-ball-color: var(--error-color);
          color: var(--error-color);
        }
      `]}}]}}),i.oi);function He(){He=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!Xe(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return et(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?et(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Qe(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Ge(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=Ge(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function Je(e){var t,r=Qe(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function Ze(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Xe(e){return e.decorators&&e.decorators.length}function Ke(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Ge(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Qe(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function et(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=He();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(Ke(o.descriptor)||Ke(n.descriptor)){if(Xe(o)||Xe(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(Xe(o)){if(Xe(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}Ze(o,n)}else t.push(o)}return t}(s.d.map(Je)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace-timeline")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"logbookEntries",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"selected",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <hat-trace-timeline
        .opp=${this.opp}
        .trace=${this.trace}
        .logbookEntries=${this.logbookEntries}
        .selectedPath=${this.selected.path}
        allowPick
      >
      </hat-trace-timeline>
      <hat-logbook-note></hat-logbook-note>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[i.iv`
        :host {
          display: block;
          padding: 16px;
        }
      `]}}]}}),i.oi);function tt(){tt=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!nt(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ct(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?ct(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=at(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:st(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=st(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function rt(e){var t,r=at(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function it(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function nt(e){return e.decorators&&e.decorators.length}function ot(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function st(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function at(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function ct(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=tt();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(ot(o.descriptor)||ot(n.descriptor)){if(nt(o)||nt(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(nt(o)){if(nt(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}it(o,n)}else t.push(o)}return t}(s.d.map(rt)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace-config")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"trace",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-code-editor
        .value=${(0,ee.safeDump)(this.trace.config).trimRight()}
        readOnly
      ></ha-code-editor>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[i.iv``]}}]}}),i.oi);function lt(){lt=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ut(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return vt(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?vt(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=mt(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:ft(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=ft(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function dt(e){var t,r=mt(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function pt(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ut(e){return e.decorators&&e.decorators.length}function ht(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function ft(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function mt(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function vt(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=lt();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(ht(o.descriptor)||ht(n.descriptor)){if(ut(o)||ut(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ut(o)){if(ut(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}pt(o,n)}else t.push(o)}return t}(s.d.map(dt)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace-logbook")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"logbookEntries",value:void 0},{kind:"method",key:"render",value:function(){return this.logbookEntries.length?i.dy`
          <ha-logbook
            relative-time
            .opp=${this.opp}
            .entries=${this.logbookEntries}
            .narrow=${this.narrow}
          ></ha-logbook>
          <hat-logbook-note></hat-logbook-note>
        `:i.dy`<div class="padded-box">
          No Logbook entries found for this step.
        </div>`}},{kind:"get",static:!0,key:"styles",value:function(){return[i.iv`
        .padded-box {
          padding: 16px;
        }
      `]}}]}}),i.oi);function yt(){yt=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!kt(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return $t(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?$t(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Pt(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Et(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=Et(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function bt(e){var t,r=Pt(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function gt(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function kt(e){return e.decorators&&e.decorators.length}function wt(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Et(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Pt(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function $t(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=yt();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(wt(o.descriptor)||wt(n.descriptor)){if(kt(o)||kt(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(kt(o)){if(kt(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}gt(o,n)}else t.push(o)}return t}(s.d.map(bt)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace-blueprint-config")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"trace",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-code-editor
        .value=${(0,ee.safeDump)(this.trace.blueprint_inputs||"").trimRight()}
        readOnly
      ></ha-code-editor>
    `}}]}}),i.oi);var xt=r(7323);function _t(){_t=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!Tt(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return jt(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?jt(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Ot(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:St(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=St(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function Dt(e){var t,r=Ot(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function Ct(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Tt(e){return e.decorators&&e.decorators.length}function At(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function St(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Ot(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function jt(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function It(e,t,r){return(It="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=zt(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function zt(e){return(zt=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let Ft=function(e,t,r,i){var n=_t();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(At(o.descriptor)||At(n.descriptor)){if(Tt(o)||Tt(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(Tt(o)){if(Tt(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}Ct(o,n)}else t.push(o)}return t}(s.d.map(Dt)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-automation-trace")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"opp",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"automationId",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"automations",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_entityId",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_traces",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_runId",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_selected",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_trace",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_view",value:()=>"details"},{kind:"method",key:"render",value:function(){var e,t;const r=this._entityId?this.opp.states[this._entityId]:void 0,n=null===(e=this.shadowRoot.querySelector("hat-script-graph"))||void 0===e?void 0:e.getTrackedNodes(),o=(null==r?void 0:r.attributes.friendly_name)||this._entityId;const c=i.dy`
      <mwc-icon-button label="Refresh" @click=${()=>this._loadTraces()}>
        <ha-svg-icon .path=${s.jcD}></ha-svg-icon>
      </mwc-icon-button>
      <mwc-icon-button
        .disabled=${!this._trace}
        label="Download Trace"
        @click=${this._downloadTrace}
      >
        <ha-svg-icon .path=${s.OGU}></ha-svg-icon>
      </mwc-icon-button>
    `;return i.dy`
      ${""}
      <opp-tabs-subpage
        .opp=${this.opp}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${Z.configSections.automation}
      >
        ${this.narrow?i.dy`<span slot="header">
                ${o}
              </span>
              <div slot="toolbar-icon">
                ${c}
              </div>`:""}
        <div class="toolbar">
          ${this.narrow?"":i.dy`<div>
                ${o}
                <a
                  class="linkButton"
                  href="/config/automation/edit/${this.automationId}"
                >
                  <mwc-icon-button label="Edit Automation" tabindex="-1">
                    <ha-svg-icon .path=${s.r9}></ha-svg-icon>
                  </mwc-icon-button>
                </a>
              </div>`}
          ${this._traces&&this._traces.length>0?i.dy`
                <div>
                  <mwc-icon-button
                    .disabled=${this._traces[this._traces.length-1].run_id===this._runId}
                    label="Older trace"
                    @click=${this._pickOlderTrace}
                  >
                    <ha-svg-icon .path=${s.JXK}></ha-svg-icon>
                  </mwc-icon-button>
                  <select .value=${this._runId} @change=${this._pickTrace}>
                    ${(0,G.r)(this._traces,(e=>e.run_id),(e=>i.dy`<option value=${e.run_id}
                          >${(0,K.E)(new Date(e.timestamp.start),this.opp.locale)}</option
                        >`))}
                  </select>
                  <mwc-icon-button
                    .disabled=${this._traces[0].run_id===this._runId}
                    label="Newer trace"
                    @click=${this._pickNewerTrace}
                  >
                    <ha-svg-icon .path=${s.RWP}></ha-svg-icon>
                  </mwc-icon-button>
                </div>
              `:""}
          ${this.narrow?"":i.dy`<div>${c}</div>`}
        </div>

        ${void 0===this._traces?i.dy`<div class="container">Loading…</div>`:0===this._traces.length?i.dy`<div class="container">No traces found</div>`:void 0===this._trace?"":i.dy`
              <div class="main">
                <div class="graph">
                  <hat-script-graph
                    .trace=${this._trace}
                    .selected=${null===(t=this._selected)||void 0===t?void 0:t.path}
                    @graph-node-selected=${this._pickNode}
                  ></hat-script-graph>
                </div>

                <div class="info">
                  <div class="tabs top">
                    ${[["details","Step Details"],["timeline","Trace Timeline"],["logbook","Related logbook entries"],["config","Automation Config"]].map((([e,t])=>i.dy`
                        <button
                          tabindex="0"
                          .view=${e}
                          class=${(0,a.$)({active:this._view===e})}
                          @click=${this._showTab}
                        >
                          ${t}
                        </button>
                      `))}
                    ${this._trace.blueprint_inputs?i.dy`
                          <button
                            tabindex="0"
                            .view=${"blueprint"}
                            class=${(0,a.$)({active:"blueprint"===this._view})}
                            @click=${this._showTab}
                          >
                            Blueprint Config
                          </div>
                        `:""}
                  </div>
                  ${void 0===this._selected||void 0===this._logbookEntries||void 0===n?"":"details"===this._view?i.dy`
                        <ha-automation-trace-path-details
                          .opp=${this.opp}
                          .narrow=${this.narrow}
                          .trace=${this._trace}
                          .selected=${this._selected}
                          .logbookEntries=${this._logbookEntries}
                          .trackedNodes=${n}
                        ></ha-automation-trace-path-details>
                      `:"config"===this._view?i.dy`
                        <ha-automation-trace-config
                          .opp=${this.opp}
                          .trace=${this._trace}
                        ></ha-automation-trace-config>
                      `:"logbook"===this._view?i.dy`
                        <ha-automation-trace-logbook
                          .opp=${this.opp}
                          .narrow=${this.narrow}
                          .logbookEntries=${this._logbookEntries}
                        ></ha-automation-trace-logbook>
                      `:"blueprint"===this._view?i.dy`
                        <ha-automation-trace-blueprint-config
                          .opp=${this.opp}
                          .trace=${this._trace}
                        ></ha-automation-trace-blueprint-config>
                      `:i.dy`
                        <ha-automation-trace-timeline
                          .opp=${this.opp}
                          .trace=${this._trace}
                          .logbookEntries=${this._logbookEntries}
                          .selected=${this._selected}
                          @value-changed=${this._timelinePathPicked}
                        ></ha-automation-trace-timeline>
                      `}
                </div>
              </div>
            `}
      </opp-tabs-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){if(It(zt(r.prototype),"firstUpdated",this).call(this,e),!this.automationId)return;const t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}},{kind:"method",key:"updated",value:function(e){if(It(zt(r.prototype),"updated",this).call(this,e),e.get("automationId")&&(this._traces=void 0,this._entityId=void 0,this._runId=void 0,this._trace=void 0,this._logbookEntries=void 0,this.automationId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._logbookEntries=void 0,this.shadowRoot.querySelector("select").value=this._runId,this._loadTrace()),e.has("automations")&&this.automationId&&!this._entityId){const e=this.automations.find((e=>e.attributes.id===this.automationId));this._entityId=null==e?void 0:e.entity_id}}},{kind:"method",key:"_pickOlderTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_loadTraces",value:async function(e){if(this._traces=await(0,n.lj)(this.opp,"automation",this.automationId),this._traces.reverse(),e&&(this._runId=e),this._runId&&!this._traces.some((e=>e.run_id===this._runId))){if(this._runId=void 0,this._selected=void 0,e){const e=new URLSearchParams(location.search);e.delete("run_id"),history.replaceState(null,"",`${location.pathname}?${e.toString()}`)}await(0,Q.Ys)(this,{text:"Chosen trace is no longer available"})}!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id)}},{kind:"method",key:"_loadTrace",value:async function(){const e=await(0,n.mA)(this.opp,"automation",this.automationId,this._runId);this._logbookEntries=(0,xt.p)(this.opp,"logbook")?await(0,X.sS)(this.opp,e.timestamp.start,e.context.id):[],this._trace=e}},{kind:"method",key:"_downloadTrace",value:function(){const e=document.createElement("a");e.download=`trace ${this._entityId} ${this._trace.timestamp.start}.json`,e.href=`data:application/json;charset=utf-8,${encodeURI(JSON.stringify({trace:this._trace,logbookEntries:this._logbookEntries},void 0,2))}`,e.click()}},{kind:"method",key:"_importTrace",value:function(){const e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){const t=JSON.parse(e);this._trace=t.trace,this._logbookEntries=t.logbookEntries}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"method",key:"_timelinePathPicked",value:function(e){const t=e.detail.value,r=this.shadowRoot.querySelector("hat-script-graph").getTrackedNodes();r[t]&&(this._selected=r[t])}},{kind:"get",static:!0,key:"styles",value:function(){return[J.Qx,le,i.iv`
        .toolbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 20px;
          height: var(--header-height);
          padding: 0 16px;
          background-color: var(--primary-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }

        .toolbar > * {
          display: flex;
          align-items: center;
        }

        :host([narrow]) .toolbar > * {
          display: contents;
        }

        .main {
          height: calc(100% - 56px);
          display: flex;
          background-color: var(--card-background-color);
        }

        :host([narrow]) .main {
          height: auto;
          flex-direction: column;
        }

        .container {
          padding: 16px;
        }

        .graph {
          border-right: 1px solid var(--divider-color);
          overflow-x: auto;
          max-width: 50%;
        }
        :host([narrow]) .graph {
          max-width: 100%;
        }

        .info {
          flex: 1;
          background-color: var(--card-background-color);
        }

        .linkButton {
          color: var(--primary-text-color);
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.3d97b6ee9629a0b0f9d7.js.map