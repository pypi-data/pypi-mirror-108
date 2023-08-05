(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1038],{349:(e,t,i)=>{"use strict";function r(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}i.d(t,{m:()=>o});const n=new class{constructor(){r(this,"_storage",{}),r(this,"_listeners",{}),window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const i=this._listeners[e].indexOf(t);-1!==i&&this._listeners[e].splice(i,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}},o=(e,t,i)=>r=>{const o=String(r.key);e=e||String(r.key);const s=r.initializer?r.initializer():void 0;n.addFromStorage(e);const a=()=>n.hasKey(e)?n.getValue(e):s;return{kind:"method",placement:"prototype",key:r.key,descriptor:{set(i){((i,o)=>{let s;t&&(s=a()),n.setValue(e,o),t&&i.requestUpdate(r.key,s)})(this,i)},get:()=>a(),enumerable:!0,configurable:!0},finisher(s){if(t){const t=s.prototype.connectedCallback,a=s.prototype.disconnectedCallback;s.prototype.connectedCallback=function(){var i;t.call(this),this[`__unbsubLocalStorage${o}`]=(i=this,n.subscribeChanges(e,(e=>{i.requestUpdate(r.key,e)})))},s.prototype.disconnectedCallback=function(){a.call(this),this[`__unbsubLocalStorage${o}`]()},s.createProperty(r.key,{noAccessor:!0,...i})}}}}},22311:(e,t,i)=>{"use strict";i.d(t,{N:()=>n});var r=i(58831);const n=e=>(0,r.M)(e.entity_id)},85415:(e,t,i)=>{"use strict";i.d(t,{q:()=>r,w:()=>n});const r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},91038:(e,t,i)=>{"use strict";i.r(t);i(53918),i(25230);var r=i(55317),n=(i(25782),i(53973),i(51095),i(50424)),o=i(55358),s=i(76666),a=i(40417),l=i(14516),d=i(349),c=i(47181),h=i(70518),p=i(58831),u=i(85415),f=i(87744),m=i(6936),v=i(1600),y=i(93491),b=i(11654);i(16509),i(48932),i(52039),i(10174);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!_(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return $(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?$(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=P(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:E(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=E(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function k(e){var t,i=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function _(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function E(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function P(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function $(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function T(e,t,i){return(T="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const S=["config","developer-tools","hassio","aishelp","aisdocs"],O="scrollIntoViewIfNeeded"in document.body,A={aisaudio:1,"media-browser":2,aiszigbee:3,map:4,logbook:5,history:6,"developer-tools":9,hassio:10,config:11,aishelp:12,aisdocs:13},D=(e,t,i,r)=>{const n=e.indexOf(i.url_path),o=e.indexOf(r.url_path);return n!==o?n<o?1:-1:z(t,i,r)},z=(e,t,i)=>{const r="lovelace"===t.component_name,n="lovelace"===i.component_name;if(t.url_path===e)return-1;if(i.url_path===e)return 1;if(r&&n)return(0,u.q)(t.title,i.title);if(r&&!n)return-1;if(n)return 1;const o=t.url_path in A,s=i.url_path in A;return o&&s?A[t.url_path]-A[i.url_path]:o?-1:s?1:(0,u.q)(t.title,i.title)},M=(0,l.Z)(((e,t,i,r)=>{if(!e)return[[],[]];const n=[],o=[];Object.values(e).forEach((e=>{r.includes(e.url_path)||!e.title&&e.url_path!==t||(S.includes(e.url_path)?o:n).push(e)}));const s=[...i].reverse();return n.sort(((e,i)=>D(s,t,e,i))),o.sort(((e,i)=>D(s,t,e,i))),[n,o]}));let H;!function(e,t,i,r){var n=g();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(x(o.descriptor)||x(n.descriptor)){if(_(o)||_(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(_(o)){if(_(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}w(o,n)}else t.push(o)}return t}(s.d.map(k)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-sidebar")],(function(e,t){class l extends t{constructor(...t){super(...t),e(this)}}return{F:l,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"alwaysExpand",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"editMode",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_externalConfig",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_notifications",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_mouseLeaveTimeout",value:void 0},{kind:"field",key:"_tooltipHideTimeout",value:void 0},{kind:"field",key:"_recentKeydownActiveUntil",value:()=>0},{kind:"field",decorators:[(0,d.m)("sidebarPanelOrder",!0,{attribute:!1})],key:"_panelOrder",value:()=>[]},{kind:"field",decorators:[(0,d.m)("sidebarHiddenPanels",!0,{attribute:!1})],key:"_hiddenPanels",value:()=>[]},{kind:"field",key:"_sortable",value:void 0},{kind:"method",key:"render",value:function(){return this.hass?n.dy`
      ${this._renderHeader()}
      ${this._renderAllPanels()}
      ${this._renderDivider()}
      ${this._renderNotifications()}
      ${this._renderUserItem()}
      <div disabled class="bottom-spacer"></div>
      <div class="tooltip"></div>
    `:n.dy``}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("expanded")||e.has("narrow")||e.has("alwaysExpand")||e.has("_externalConfig")||e.has("_notifications")||e.has("editMode")||e.has("_renderEmptySortable")||e.has("_hiddenPanels")||e.has("_panelOrder")&&!this.editMode)return!0;if(!this.hass||!e.has("hass"))return!1;const t=e.get("hass");if(!t)return!0;const i=this.hass;return i.panels!==t.panels||i.panelUrl!==t.panelUrl||i.user!==t.user||i.localize!==t.localize||i.locale!==t.locale||i.states!==t.states||i.defaultPanel!==t.defaultPanel}},{kind:"method",key:"firstUpdated",value:function(e){T(C(l.prototype),"firstUpdated",this).call(this,e),this.hass&&this.hass.auth.external&&(0,v.e)(this.hass.auth.external).then((e=>{this._externalConfig=e})),(0,m.r)(this.hass.connection,(e=>{this._notifications=e}))}},{kind:"method",key:"updated",value:function(e){if(T(C(l.prototype),"updated",this).call(this,e),e.has("alwaysExpand")&&(0,h.X)(this,"expanded",this.alwaysExpand),e.has("editMode")&&(this.editMode?this._activateEditMode():this._deactivateEditMode()),!e.has("hass"))return;const t=e.get("hass");if(t&&t.locale===this.hass.locale||(0,h.X)(this,"rtl",(0,f.HE)(this.hass)),O&&(!t||t.panelUrl!==this.hass.panelUrl)){const e=this.shadowRoot.querySelector(".iron-selected");e&&e.scrollIntoViewIfNeeded()}}},{kind:"method",key:"_renderHeader",value:function(){return n.dy`<div
      class="menu"
      @action=${this._handleAction}
      .actionHandler=${(0,y.K)({hasHold:!this.editMode,disabled:this.editMode})}
    >
      ${this.narrow?"":n.dy`
            <mwc-icon-button
              .label=${this.hass.localize("ui.sidebar.sidebar_toggle")}
              @action=${this._toggleSidebar}
            >
              <ha-svg-icon
                .path=${"docked"===this.hass.dockedSidebar?r.XIn:r.$Qi}
              ></ha-svg-icon>
            </mwc-icon-button>
          `}
      ${this.editMode?n.dy`<mwc-button outlined @click=${this._closeEditMode}>
            ${this.hass.localize("ui.sidebar.done")}
          </mwc-button>`:n.dy`<div class="title">AI-Speaker</div>`}
    </div>`}},{kind:"method",key:"_renderAllPanels",value:function(){const[e,t]=M(this.hass.panels,this.hass.defaultPanel,this._panelOrder,this._hiddenPanels);return n.dy`
      <paper-listbox
        attr-for-selected="data-panel"
        class="ha-scrollbar"
        .selected=${this.hass.panelUrl}
        @focusin=${this._listboxFocusIn}
        @focusout=${this._listboxFocusOut}
        @scroll=${this._listboxScroll}
        @keydown=${this._listboxKeydown}
      >
        ${this.editMode?this._renderPanelsEdit(e):this._renderPanels(e)}
        ${this._renderSpacer()}
        ${this._renderPanels(t)}
        ${this._renderExternalConfiguration()}
      </paper-listbox>
    `}},{kind:"method",key:"_renderPanelsEdit",value:function(e){return n.dy`<div id="sortable">
        ${(0,a.l)([this._hiddenPanels,this._renderEmptySortable],(()=>this._renderEmptySortable?"":this._renderPanels(e)))}
      </div>
      ${this._renderSpacer()}
      ${this._renderHiddenPanels()} `}},{kind:"method",key:"_renderHiddenPanels",value:function(){return n.dy` ${this._hiddenPanels.length?n.dy`${this._hiddenPanels.map((e=>{const t=this.hass.panels[e];return t?n.dy`<paper-icon-item
            @click=${this._unhidePanel}
            class="hidden-panel"
            .panel=${e}
          >
            <ha-icon
              slot="item-icon"
              .icon=${t.url_path===this.hass.defaultPanel?"mdi:view-dashboard":t.icon}
            ></ha-icon>
            <span class="item-text"
              >${t.url_path===this.hass.defaultPanel?this.hass.localize("panel.states"):this.hass.localize(`panel.${t.title}`)||t.title}</span
            >
            <mwc-icon-button class="show-panel">
              <ha-svg-icon .path=${r.qX5}></ha-svg-icon>
            </mwc-icon-button>
          </paper-icon-item>`:""}))}
        ${this._renderSpacer()}`:""}`}},{kind:"method",key:"_renderDivider",value:function(){return n.dy`<div class="divider"></div>`}},{kind:"method",key:"_renderSpacer",value:function(){return n.dy`<div class="spacer" disabled></div>`}},{kind:"method",key:"_renderNotifications",value:function(){let e=this._notifications?this._notifications.length:0;for(const t in this.hass.states)"configurator"===(0,p.M)(t)&&e++;return n.dy` <div
      class="notifications-container"
      @mouseenter=${this._itemMouseEnter}
      @mouseleave=${this._itemMouseLeave}
    >
      <paper-icon-item
        class="notifications"
        aria-role="option"
        @click=${this._handleShowNotificationDrawer}
      >
        <ha-svg-icon slot="item-icon" .path=${r.Kox}></ha-svg-icon>
        ${!this.alwaysExpand&&e>0?n.dy`
              <span class="notification-badge" slot="item-icon">
                ${e}
              </span>
            `:""}
        <span class="item-text">
          ${this.hass.localize("ui.notification_drawer.title")}
        </span>
        ${this.alwaysExpand&&e>0?n.dy` <span class="notification-badge">${e}</span> `:""}
      </paper-icon-item>
    </div>`}},{kind:"method",key:"_renderUserItem",value:function(){return n.dy`<a
      class=${(0,s.$)({profile:!0,"iron-selected":"profile"===this.hass.panelUrl})}
      href="/profile"
      data-panel="panel"
      tabindex="-1"
      aria-role="option"
      aria-label=${this.hass.localize("panel.profile")}
      @mouseenter=${this._itemMouseEnter}
      @mouseleave=${this._itemMouseLeave}
    >
      <paper-icon-item>
        <ha-user-badge
          slot="item-icon"
          .user=${this.hass.user}
          .hass=${this.hass}
        ></ha-user-badge>

        <span class="item-text">
          ${this.hass.user?this.hass.user.name:""}
        </span>
      </paper-icon-item>
    </a>`}},{kind:"method",key:"_renderExternalConfiguration",value:function(){return n.dy`${this._externalConfig&&this._externalConfig.hasSettingsScreen?n.dy`
          <a
            aria-role="option"
            aria-label=${this.hass.localize("ui.sidebar.external_app_configuration")}
            href="#external-app-configuration"
            tabindex="-1"
            @click=${this._handleExternalAppConfiguration}
            @mouseenter=${this._itemMouseEnter}
            @mouseleave=${this._itemMouseLeave}
          >
            <paper-icon-item>
              <ha-svg-icon
                slot="item-icon"
                .path=${r.SPQ}
              ></ha-svg-icon>
              <span class="item-text">
                ${this.hass.localize("ui.sidebar.external_app_configuration")}
              </span>
            </paper-icon-item>
          </a>
        `:""}`}},{kind:"get",key:"_tooltip",value:function(){return this.shadowRoot.querySelector(".tooltip")}},{kind:"method",key:"_handleAction",value:function(e){"hold"===e.detail.action&&(0,c.B)(this,"hass-edit-sidebar",{editMode:!0})}},{kind:"method",key:"_activateEditMode",value:async function(){if(!H){const[e,t]=await Promise.all([i.e(6087).then(i.bind(i,56087)),i.e(651).then(i.bind(i,70651))]),r=document.createElement("style");r.innerHTML=t.sortableStyles.cssText,this.shadowRoot.appendChild(r),H=e.Sortable,H.mount(e.OnSpill),H.mount(e.AutoScroll())}await this.updateComplete,this._createSortable()}},{kind:"method",key:"_createSortable",value:function(){this._sortable=new H(this.shadowRoot.getElementById("sortable"),{animation:150,fallbackClass:"sortable-fallback",dataIdAttr:"data-panel",handle:"paper-icon-item",onSort:async()=>{this._panelOrder=this._sortable.toArray()}})}},{kind:"method",key:"_deactivateEditMode",value:function(){var e;null===(e=this._sortable)||void 0===e||e.destroy(),this._sortable=void 0}},{kind:"method",key:"_closeEditMode",value:function(){(0,c.B)(this,"hass-edit-sidebar",{editMode:!1})}},{kind:"method",key:"_hidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;if(this._hiddenPanels.includes(t))return;this._hiddenPanels=[...this._hiddenPanels,t],this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_unhidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;this._hiddenPanels=this._hiddenPanels.filter((e=>e!==t)),this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_itemMouseEnter",value:function(e){this.alwaysExpand||(new Date).getTime()<this._recentKeydownActiveUntil||(this._mouseLeaveTimeout&&(clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=void 0),this._showTooltip(e.currentTarget))}},{kind:"method",key:"_itemMouseLeave",value:function(){this._mouseLeaveTimeout&&clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=window.setTimeout((()=>{this._hideTooltip()}),500)}},{kind:"method",key:"_listboxFocusIn",value:function(e){this.alwaysExpand||"A"!==e.target.nodeName||this._showTooltip(e.target.querySelector("paper-icon-item"))}},{kind:"method",key:"_listboxFocusOut",value:function(){this._hideTooltip()}},{kind:"method",decorators:[(0,o.hO)({passive:!0})],key:"_listboxScroll",value:function(){(new Date).getTime()<this._recentKeydownActiveUntil||this._hideTooltip()}},{kind:"method",key:"_listboxKeydown",value:function(){this._recentKeydownActiveUntil=(new Date).getTime()+100}},{kind:"method",key:"_showTooltip",value:function(e){this._tooltipHideTimeout&&(clearTimeout(this._tooltipHideTimeout),this._tooltipHideTimeout=void 0);const t=this._tooltip,i=this.shadowRoot.querySelector("paper-listbox");let r=e.offsetTop+11;i.contains(e)&&(r-=i.scrollTop),t.innerHTML=e.querySelector(".item-text").innerHTML,t.style.display="block",t.style.top=`${r}px`,t.style.left=`${e.offsetLeft+e.clientWidth+4}px`}},{kind:"method",key:"_hideTooltip",value:function(){this._tooltipHideTimeout||(this._tooltipHideTimeout=window.setTimeout((()=>{this._tooltipHideTimeout=void 0,this._tooltip.style.display="none"}),10))}},{kind:"method",key:"_handleShowNotificationDrawer",value:function(){(0,c.B)(this,"hass-show-notifications")}},{kind:"method",key:"_handleExternalAppConfiguration",value:function(e){e.preventDefault(),this.hass.auth.external.fireMessage({type:"config_screen/show"})}},{kind:"method",key:"_toggleSidebar",value:function(e){"tap"===e.detail.action&&(0,c.B)(this,"hass-toggle-menu")}},{kind:"method",key:"_renderPanels",value:function(e){return e.map((e=>this._renderPanel(e.url_path,e.url_path===this.hass.defaultPanel?e.title||this.hass.localize("panel.states"):this.hass.localize(`panel.${e.title}`)||e.title,e.icon,e.url_path!==this.hass.defaultPanel||e.icon?void 0:r.Ccq)))}},{kind:"method",key:"_renderPanel",value:function(e,t,i,o){return n.dy`
      <a
        aria-role="option"
        href=${`/${e}`}
        data-panel=${e}
        tabindex="-1"
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item>
          ${o?n.dy`<ha-svg-icon
                slot="item-icon"
                .path=${o}
              ></ha-svg-icon>`:n.dy`<ha-icon slot="item-icon" .icon=${i}></ha-icon>`}
          <span class="item-text">${t}</span>
        </paper-icon-item>
        ${this.editMode?n.dy`<mwc-icon-button
              class="hide-panel"
              .panel=${e}
              @click=${this._hidePanel}
            >
              <ha-svg-icon .path=${r.r5M}></ha-svg-icon>
            </mwc-icon-button>`:""}
      </a>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[b.$c,n.iv`
        :host {
          height: 100%;
          display: block;
          overflow: hidden;
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          border-right: 1px solid var(--divider-color);
          background-color: var(--sidebar-background-color);
          width: 56px;
        }
        :host([expanded]) {
          width: 256px;
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl]) {
          border-right: 0;
          border-left: 1px solid var(--divider-color);
        }
        .menu {
          height: var(--header-height);
          box-sizing: border-box;
          display: flex;
          padding: 0 4px;
          border-bottom: 1px solid transparent;
          white-space: nowrap;
          font-weight: 400;
          color: var(--sidebar-menu-button-text-color, --primary-text-color);
          border-bottom: 1px solid var(--divider-color);
          background-color: var(
            --sidebar-menu-button-background-color,
            --primary-background-color
          );
          font-size: 20px;
          align-items: center;
          padding-left: calc(4px + env(safe-area-inset-left));
        }
        :host([rtl]) .menu {
          padding-left: 4px;
          padding-right: calc(4px + env(safe-area-inset-right));
        }
        :host([expanded]) .menu {
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl][expanded]) .menu {
          width: calc(256px + env(safe-area-inset-right));
        }
        .menu mwc-icon-button {
          color: var(--sidebar-icon-color);
        }
        .title {
          margin-left: 19px;
          width: 100%;
          display: none;
        }
        :host([rtl]) .title {
          margin-left: 0;
          margin-right: 19px;
        }
        :host([narrow]) .title {
          margin: 0;
          padding: 0 16px;
        }
        :host([expanded]) .title {
          display: initial;
        }
        :host([expanded]) .menu mwc-button {
          margin: 0 8px;
        }
        .menu mwc-button {
          width: 100%;
        }
        #sortable,
        .hidden-panel {
          display: none;
        }

        paper-listbox {
          padding: 4px 0;
          display: flex;
          flex-direction: column;
          box-sizing: border-box;
          height: calc(100% - var(--header-height) - 132px);
          height: calc(
            100% - var(--header-height) - 132px - env(safe-area-inset-bottom)
          );
          overflow-x: hidden;
          background: none;
          margin-left: env(safe-area-inset-left);
        }

        :host([rtl]) paper-listbox {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }

        a {
          text-decoration: none;
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          position: relative;
          display: block;
          outline: 0;
        }

        paper-icon-item {
          box-sizing: border-box;
          margin: 4px;
          padding-left: 12px;
          border-radius: 4px;
          --paper-item-min-height: 40px;
          width: 48px;
        }
        :host([expanded]) paper-icon-item {
          width: 248px;
        }
        :host([rtl]) paper-icon-item {
          padding-left: auto;
          padding-right: 12px;
        }

        ha-icon[slot="item-icon"],
        ha-svg-icon[slot="item-icon"] {
          color: var(--sidebar-icon-color);
        }

        .iron-selected paper-icon-item::before,
        a:not(.iron-selected):focus::before {
          border-radius: 4px;
          position: absolute;
          top: 0;
          right: 2px;
          bottom: 0;
          left: 2px;
          pointer-events: none;
          content: "";
          transition: opacity 15ms linear;
          will-change: opacity;
        }
        .iron-selected paper-icon-item::before {
          background-color: var(--sidebar-selected-icon-color);
          opacity: 0.12;
        }
        a:not(.iron-selected):focus::before {
          background-color: currentColor;
          opacity: var(--dark-divider-opacity);
          margin: 4px 8px;
        }
        .iron-selected paper-icon-item:focus::before,
        .iron-selected:focus paper-icon-item::before {
          opacity: 0.2;
        }

        .iron-selected paper-icon-item[pressed]:before {
          opacity: 0.37;
        }

        paper-icon-item span {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
        }

        a.iron-selected paper-icon-item ha-icon,
        a.iron-selected paper-icon-item ha-svg-icon {
          color: var(--sidebar-selected-icon-color);
        }

        a.iron-selected .item-text {
          color: var(--sidebar-selected-text-color);
        }

        paper-icon-item .item-text {
          display: none;
          max-width: calc(100% - 56px);
        }
        :host([expanded]) paper-icon-item .item-text {
          display: block;
        }

        .divider {
          bottom: 112px;
          padding: 10px 0;
        }
        .divider::before {
          content: " ";
          display: block;
          height: 1px;
          background-color: var(--divider-color);
        }
        .notifications-container {
          display: flex;
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .notifications-container {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .notifications {
          cursor: pointer;
        }
        .notifications .item-text {
          flex: 1;
        }
        .profile {
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .profile {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .profile paper-icon-item {
          padding-left: 4px;
        }
        :host([rtl]) .profile paper-icon-item {
          padding-left: auto;
          padding-right: 4px;
        }
        .profile .item-text {
          margin-left: 8px;
        }
        :host([rtl]) .profile .item-text {
          margin-right: 8px;
        }

        .notification-badge {
          min-width: 20px;
          box-sizing: border-box;
          border-radius: 50%;
          font-weight: 400;
          background-color: var(--accent-color);
          line-height: 20px;
          text-align: center;
          padding: 0px 6px;
          color: var(--text-accent-color, var(--text-primary-color));
        }
        ha-svg-icon + .notification-badge {
          position: absolute;
          bottom: 14px;
          left: 26px;
          font-size: 0.65em;
        }

        .spacer {
          flex: 1;
          pointer-events: none;
        }

        .subheader {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          padding: 16px;
          white-space: nowrap;
        }

        .dev-tools {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          padding: 0 8px;
          width: 256px;
          box-sizing: border-box;
        }

        .dev-tools a {
          color: var(--sidebar-icon-color);
        }

        .tooltip {
          display: none;
          position: absolute;
          opacity: 0.9;
          border-radius: 2px;
          white-space: nowrap;
          color: var(--sidebar-background-color);
          background-color: var(--sidebar-text-color);
          padding: 4px;
          font-weight: 500;
        }

        :host([rtl]) .menu mwc-icon-button {
          -webkit-transform: scaleX(-1);
          transform: scaleX(-1);
        }
      `]}}]}}),n.oi)},10174:(e,t,i)=>{"use strict";i.d(t,{f:()=>b});var r=i(50424),n=i(55358),o=i(76666),s=i(92483),a=i(22311);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(e,t,i){return(v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const b=e=>e?e.trim().split(" ").slice(0,3).map((e=>e.substr(0,1))).join(""):"?";!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(p(o.descriptor)||p(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(s.d.map(d)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("ha-user-badge")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"user",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_personPicture",value:void 0},{kind:"field",key:"_personEntityId",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(v(y(i.prototype),"willUpdate",this).call(this,e),e.has("user"))return void this._getPersonPicture();const t=e.get("hass");if(this._personEntityId&&t&&this.hass.states[this._personEntityId]!==t.states[this._personEntityId]){const e=this.hass.states[this._personEntityId];e?this._personPicture=e.attributes.entity_picture:this._getPersonPicture()}else!this._personEntityId&&t&&this._getPersonPicture()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.user)return r.dy``;const e=this._personPicture;if(e)return r.dy`<div
        style=${(0,s.V)({backgroundImage:`url(${e})`})}
        class="picture"
      ></div>`;const t=b(this.user.name);return r.dy`<div
      class="initials ${(0,o.$)({long:t.length>2})}"
    >
      ${t}
    </div>`}},{kind:"method",key:"_getPersonPicture",value:function(){if(this._personEntityId=void 0,this._personPicture=void 0,this.hass&&this.user)for(const e of Object.values(this.hass.states))if(e.attributes.user_id===this.user.id&&"person"===(0,a.N)(e)){this._personEntityId=e.entity_id,this._personPicture=e.attributes.entity_picture;break}}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: contents;
      }
      .picture {
        width: 40px;
        height: 40px;
        background-size: cover;
        border-radius: 50%;
      }
      .initials {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }
      .initials.long {
        font-size: 80%;
      }
    `}}]}}),r.oi)},1600:(e,t,i)=>{"use strict";i.d(t,{e:()=>r});const r=e=>(e.cache.cfg||(e.cache.cfg=e.sendMessage({type:"config/get"})),e.cache.cfg)},93491:(e,t,i)=>{"use strict";i.d(t,{K:()=>h});i(66702);var r=i(50424),n=i(19967),o=i(47181),s=i(36639);function a(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}const l="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0;class d extends HTMLElement{constructor(){super(),a(this,"holdTime",500),a(this,"ripple",void 0),a(this,"timer",void 0),a(this,"held",!1),a(this,"cancelled",!1),a(this,"dblClickTimeout",void 0),this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:l?"100px":"50px",height:l?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((e=>{document.addEventListener(e,(()=>{this.cancelled=!0,this.timer&&(this.stopAnimation(),clearTimeout(this.timer),this.timer=void 0)}),{passive:!0})}))}bind(e,t={}){e.actionHandler&&(0,s.v)(t,e.actionHandler.options)||(e.actionHandler?(e.removeEventListener("touchstart",e.actionHandler.start),e.removeEventListener("touchend",e.actionHandler.end),e.removeEventListener("touchcancel",e.actionHandler.end),e.removeEventListener("mousedown",e.actionHandler.start),e.removeEventListener("click",e.actionHandler.end),e.removeEventListener("keyup",e.actionHandler.handleEnter)):e.addEventListener("contextmenu",(e=>{const t=e||window.event;return t.preventDefault&&t.preventDefault(),t.stopPropagation&&t.stopPropagation(),t.cancelBubble=!0,t.returnValue=!1,!1})),e.actionHandler={options:t},t.disabled||(e.actionHandler.start=e=>{let i,r;this.cancelled=!1,e.touches?(i=e.touches[0].pageX,r=e.touches[0].pageY):(i=e.pageX,r=e.pageY),t.hasHold&&(this.held=!1,this.timer=window.setTimeout((()=>{this.startAnimation(i,r),this.held=!0}),this.holdTime))},e.actionHandler.end=e=>{if(["touchend","touchcancel"].includes(e.type)&&this.cancelled)return;const i=e.target;e.cancelable&&e.preventDefault(),t.hasHold&&(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0),t.hasHold&&this.held?(0,o.B)(i,"action",{action:"hold"}):t.hasDoubleClick?"click"===e.type&&e.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"double_tap"})):(0,o.B)(i,"action",{action:"tap"})},e.actionHandler.handleEnter=e=>{13===e.keyCode&&e.currentTarget.actionHandler.end(e)},e.addEventListener("touchstart",e.actionHandler.start,{passive:!0}),e.addEventListener("touchend",e.actionHandler.end),e.addEventListener("touchcancel",e.actionHandler.end),e.addEventListener("mousedown",e.actionHandler.start,{passive:!0}),e.addEventListener("click",e.actionHandler.end),e.addEventListener("keyup",e.actionHandler.handleEnter)))}startAnimation(e,t){Object.assign(this.style,{left:`${e}px`,top:`${t}px`,display:null}),this.ripple.disabled=!1,this.ripple.startPress(),this.ripple.unbounded=!0}stopAnimation(){this.ripple.endPress(),this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler",d);const c=(e,t)=>{const i=(()=>{const e=document.body;if(e.querySelector("action-handler"))return e.querySelector("action-handler");const t=document.createElement("action-handler");return e.appendChild(t),t})();i&&i.bind(e,t)},h=(0,n.XM)(class extends n.Xe{update(e,[t]){return c(e.element,t),r.Jb}render(e){}})}}]);
//# sourceMappingURL=chunk.5281c6e6ab02fac38afb.js.map