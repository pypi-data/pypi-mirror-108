(self.webpackChunkopenpeerpower_frontend=self.webpackChunkopenpeerpower_frontend||[]).push([[6169],{6169:(e,r,t)=>{"use strict";t.r(r);var s=t(15652),i=t(50467),o=t(99476);class n extends o.p{static async getConfigElement(){return await Promise.all([t.e(5009),t.e(2955),t.e(8161),t.e(9543),t.e(8374),t.e(9494),t.e(6051),t.e(3098),t.e(4618),t.e(9033),t.e(3300),t.e(3304),t.e(6087),t.e(6133),t.e(1456),t.e(4507),t.e(6966),t.e(1480),t.e(7482),t.e(4535),t.e(8101),t.e(6902),t.e(8331),t.e(7580),t.e(167),t.e(2231),t.e(2979),t.e(9737),t.e(2382)]).then(t.bind(t,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square)return this._cards.length/this.columns*2;const e=[];for(const r of this._cards)e.push((0,i.N)(r));const r=await Promise.all(e);return Math.max(...r)*(this._cards.length/this.columns)}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.toggleAttribute("square",this.square)}static get styles(){return[super.sharedStyles,s.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:first-child {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
      `]}}customElements.define("hui-grid-card",n)}}]);
//# sourceMappingURL=chunk.3fe0fb1bf87fa6cf2d1f.js.map