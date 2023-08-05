(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[4705],{4705:(e,t,l)=>{"use strict";l.r(t);l(12730);var o=l(50856),a=l(28426);l(48932),l(25409);class r extends a.H3{static get template(){return o.d`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          position: absolute;
          height: calc(100% - var(--header-height));
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button opp="[[opp]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts allow-modals"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{opp:Object,narrow:Boolean,panel:Object}}}customElements.define("ha-panel-iframe",r)},25409:(e,t,l)=>{"use strict";l(21384);var o=l(11654);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${o.Qx.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(a.content)}}]);
//# sourceMappingURL=chunk.45ad919898134640008e.js.map