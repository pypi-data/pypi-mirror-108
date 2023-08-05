/*! For license information please see chunk.ca15ea29e7454c60e8f3.js.LICENSE.txt */
(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[2411],{52003:(t,e,i)=>{"use strict";i.d(e,{F:()=>a,C:()=>o});const a=async(t,e,a=!1)=>{if(!t.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const o=(await i.e(6085).then(i.t.bind(i,70208,23))).default;o.Icon.Default.imagePath="/static/images/leaflet/images/",a&&await i.e(7716).then(i.t.bind(i,27716,23));const s=o.map(t),r=document.createElement("link");r.setAttribute("href","/static/images/leaflet/leaflet.css"),r.setAttribute("rel","stylesheet"),t.parentNode.appendChild(r),s.setView([52.3731339,4.8903147],13);return[s,o,n(o,Boolean(e)).addTo(s)]},o=(t,e,i,a)=>(e.removeLayer(i),(i=n(t,a)).addTo(e),i),n=(t,e)=>t.tileLayer(`https://{s}.basemaps.cartocdn.com/${e?"dark_all":"light_all"}/{z}/{x}/{y}${t.Browser.retina?"@2x.png":".png"}`,{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},27269:(t,e,i)=>{"use strict";i.d(e,{p:()=>a});const a=t=>t.substr(t.indexOf(".")+1)},22311:(t,e,i)=>{"use strict";i.d(e,{N:()=>o});var a=i(58831);const o=t=>(0,a.M)(t.entity_id)},91741:(t,e,i)=>{"use strict";i.d(e,{C:()=>o});var a=i(27269);const o=t=>void 0===t.attributes.friendly_name?(0,a.p)(t.entity_id).replace(/_/g," "):t.attributes.friendly_name||""},45841:(t,e,i)=>{"use strict";i.d(e,{V3:()=>o,AD:()=>n,nq:()=>s,zt:()=>r,$H:()=>l,Bf:()=>p,vp:()=>c,fT:()=>h,Pc:()=>u});var a=i(83849);const o="#FF9800",n="#03a9f4",s="#9b9b9b",r=t=>t.callWS({type:"zone/list"}),l=(t,e)=>t.callWS({type:"zone/create",...e}),p=(t,e,i)=>t.callWS({type:"zone/update",zone_id:e,...i}),c=(t,e)=>t.callWS({type:"zone/delete",zone_id:e});let d;const h=(t,e)=>{d=e,(0,a.c)(t,"/config/zone/new")},u=()=>{const t=d;return d=void 0,t}},27849:(t,e,i)=>{"use strict";i(39841);var a=i(50856);i(28426);class o extends(customElements.get("app-header-layout")){static get template(){return a.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",o)},11052:(t,e,i)=>{"use strict";i.d(e,{I:()=>n});var a=i(76389),o=i(47181);const n=(0,a.o)((t=>class extends t{fire(t,e,i){return i=i||{},(0,o.B)(i.node||this,t,e,i)}}))},1265:(t,e,i)=>{"use strict";i.d(e,{Z:()=>a});const a=(0,i(76389).o)((t=>class extends t{static get properties(){return{opp:Object,localize:{type:Function,computed:"__computeLocalize(opp.localize)"}}}__computeLocalize(t){return t}}))},73085:(t,e,i)=>{"use strict";i(44285);var a=i(50856),o=i(28426),n=i(11052);class s extends((0,n.I)(o.H3)){static get template(){return a.d`
      <style include="iron-positioning"></style>
      <style>
        .marker {
          position: relative;
          display: block;
          margin: 0 auto;
          width: 2.5em;
          text-align: center;
          height: 2.5em;
          line-height: 2.5em;
          font-size: 1.5em;
          border-radius: 50%;
          border: 0.1em solid var(--op-marker-color, var(--primary-color));
          color: var(--primary-text-color);
          background-color: var(--card-background-color);
        }
        iron-image {
          border-radius: 50%;
        }
      </style>

      <div class="marker" style$="border-color:{{entityColor}}">
        <template is="dom-if" if="[[entityName]]">[[entityName]]</template>
        <template is="dom-if" if="[[entityPicture]]">
          <iron-image
            sizing="cover"
            class="fit"
            src="[[entityPicture]]"
          ></iron-image>
        </template>
      </div>
    `}static get properties(){return{opp:{type:Object},entityId:{type:String,value:""},entityName:{type:String,value:null},entityPicture:{type:String,value:null},entityColor:{type:String,value:null}}}ready(){super.ready(),this.addEventListener("click",(t=>this.badgeTap(t)))}badgeTap(t){t.stopPropagation(),this.entityId&&this.fire("opp-more-info",{entityId:this.entityId})}}customElements.define("ha-entity-marker",s)},2411:(t,e,i)=>{"use strict";i.r(e);i(12730);var a=i(50856),o=i(28426),n=i(52003),s=i(22311),r=i(91741),l=i(83849),p=(i(16509),i(48932),i(45841)),c=(i(27849),i(1265));i(25409),i(73085);class d extends((0,c.Z)(o.H3)){static get template(){return a.d`
      <style include="ha-style">
        #map {
          height: calc(100vh - var(--header-height));
          width: 100%;
          z-index: 0;
          background: inherit;
        }

        .icon {
          color: var(--primary-text-color);
        }
      </style>

      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              opp="[[opp]]"
              narrow="[[narrow]]"
            ></ha-menu-button>
            <div main-title>[[localize('panel.map')]]</div>
            <template is="dom-if" if="[[computeShowEditZone(opp)]]">
              <ha-icon-button
                icon="opp:pencil"
                on-click="openZonesEditor"
              ></ha-icon-button>
            </template>
          </app-toolbar>
        </app-header>
        <div id="map"></div>
      </ha-app-layout>
    `}static get properties(){return{opp:{type:Object,observer:"drawEntities"},narrow:Boolean}}connectedCallback(){super.connectedCallback(),this.loadMap()}async loadMap(){this._darkMode=this.opp.themes.darkMode,[this._map,this.Leaflet,this._tileLayer]=await(0,n.F)(this.$.map,this._darkMode),this.drawEntities(this.opp),this._map.invalidateSize(),this.fitMap()}disconnectedCallback(){this._map&&this._map.remove()}computeShowEditZone(t){return t.user.is_admin}openZonesEditor(){(0,l.c)(this,"/config/zone")}fitMap(){let t;0===this._mapItems.length?this._map.setView(new this.Leaflet.LatLng(this.opp.config.latitude,this.opp.config.longitude),14):(t=new this.Leaflet.latLngBounds(this._mapItems.map((t=>t.getLatLng()))),this._map.fitBounds(t.pad(.5)))}drawEntities(t){const e=this._map;if(!e)return;this._darkMode!==this.opp.themes.darkMode&&(this._darkMode=this.opp.themes.darkMode,this._tileLayer=(0,n.C)(this.Leaflet,e,this._tileLayer,this.opp.themes.darkMode)),this._mapItems&&this._mapItems.forEach((function(t){t.remove()}));const i=this._mapItems=[];this._mapZones&&this._mapZones.forEach((function(t){t.remove()}));const a=this._mapZones=[];Object.keys(t.states).forEach((o=>{const n=t.states[o];if("home"===n.state||!("latitude"in n.attributes)||!("longitude"in n.attributes))return;const l=(0,r.C)(n);let c;if("zone"===(0,s.N)(n)){if(n.attributes.passive)return;let t="";if(n.attributes.icon){const e=document.createElement("ha-icon");e.setAttribute("icon",n.attributes.icon),t=e.outerHTML}else{const e=document.createElement("span");e.innerHTML=l,t=e.outerHTML}return c=this.Leaflet.divIcon({html:t,iconSize:[24,24],className:"icon"}),a.push(this.Leaflet.marker([n.attributes.latitude,n.attributes.longitude],{icon:c,interactive:!1,title:l}).addTo(e)),void a.push(this.Leaflet.circle([n.attributes.latitude,n.attributes.longitude],{interactive:!1,color:p.V3,radius:n.attributes.radius}).addTo(e))}const d=n.attributes.entity_picture||"",h=l.split(" ").map((function(t){return t.substr(0,1)})).join("");c=this.Leaflet.divIcon({html:"<ha-entity-marker entity-id='"+n.entity_id+"' entity-name='"+h+"' entity-picture='"+d+"'></ha-entity-marker>",iconSize:[45,45],className:""}),i.push(this.Leaflet.marker([n.attributes.latitude,n.attributes.longitude],{icon:c,title:(0,r.C)(n)}).addTo(e)),n.attributes.gps_accuracy&&i.push(this.Leaflet.circle([n.attributes.latitude,n.attributes.longitude],{interactive:!1,color:"#0288D1",radius:n.attributes.gps_accuracy}).addTo(e))}))}}customElements.define("ha-panel-map",d)},25409:(t,e,i)=>{"use strict";i(21384);var a=i(11654);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${a.Qx.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(o.content)}}]);
//# sourceMappingURL=chunk.ca15ea29e7454c60e8f3.js.map