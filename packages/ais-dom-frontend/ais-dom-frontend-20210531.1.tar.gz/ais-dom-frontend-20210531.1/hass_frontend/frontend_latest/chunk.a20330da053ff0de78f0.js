(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[5341],{91107:(e,t,r)=>{"use strict";r.d(t,{Ud:()=>u});const i=Symbol("Comlink.proxy"),n=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),o=Symbol("Comlink.thrown"),s=e=>"object"==typeof e&&null!==e||"function"==typeof e,l=new Map([["proxy",{canHandle:e=>s(e)&&e[i],serialize(e){const{port1:t,port2:r}=new MessageChannel;return c(e,t),[r,[r]]},deserialize:e=>(e.start(),u(e))}],["throw",{canHandle:e=>s(e)&&o in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function c(e,t=self){t.addEventListener("message",(function r(n){if(!n||!n.data)return;const{id:a,type:s,path:l}=Object.assign({path:[]},n.data),u=(n.data.argumentList||[]).map(v);let p;try{const t=l.slice(0,-1).reduce(((e,t)=>e[t]),e),r=l.reduce(((e,t)=>e[t]),e);switch(s){case"GET":p=r;break;case"SET":t[l.slice(-1)[0]]=v(n.data.value),p=!0;break;case"APPLY":p=r.apply(t,u);break;case"CONSTRUCT":p=function(e){return Object.assign(e,{[i]:!0})}(new r(...u));break;case"ENDPOINT":{const{port1:t,port2:r}=new MessageChannel;c(e,r),p=function(e,t){return m.set(e,t),e}(t,[t])}break;case"RELEASE":p=void 0;break;default:return}}catch(e){p={value:e,[o]:0}}Promise.resolve(p).catch((e=>({value:e,[o]:0}))).then((e=>{const[i,n]=y(e);t.postMessage(Object.assign(Object.assign({},i),{id:a}),n),"RELEASE"===s&&(t.removeEventListener("message",r),d(t))}))})),t.start&&t.start()}function d(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function u(e,t){return h(e,[],t)}function p(e){if(e)throw new Error("Proxy has been released and is not useable")}function h(e,t=[],r=function(){}){let i=!1;const o=new Proxy(r,{get(r,n){if(p(i),n===a)return()=>b(e,{type:"RELEASE",path:t.map((e=>e.toString()))}).then((()=>{d(e),i=!0}));if("then"===n){if(0===t.length)return{then:()=>o};const r=b(e,{type:"GET",path:t.map((e=>e.toString()))}).then(v);return r.then.bind(r)}return h(e,[...t,n])},set(r,n,a){p(i);const[o,s]=y(a);return b(e,{type:"SET",path:[...t,n].map((e=>e.toString())),value:o},s).then(v)},apply(r,a,o){p(i);const s=t[t.length-1];if(s===n)return b(e,{type:"ENDPOINT"}).then(v);if("bind"===s)return h(e,t.slice(0,-1));const[l,c]=f(o);return b(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:l},c).then(v)},construct(r,n){p(i);const[a,o]=f(n);return b(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:a},o).then(v)}});return o}function f(e){const t=e.map(y);return[t.map((e=>e[0])),(r=t.map((e=>e[1])),Array.prototype.concat.apply([],r))];var r}const m=new WeakMap;function y(e){for(const[t,r]of l)if(r.canHandle(e)){const[i,n]=r.serialize(e);return[{type:"HANDLER",name:t,value:i},n]}return[{type:"RAW",value:e},m.get(e)||[]]}function v(e){switch(e.type){case"HANDLER":return l.get(e.name).deserialize(e.value);case"RAW":return e.value}}function b(e,t,r){return new Promise((i=>{const n=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(r){r.data&&r.data.id&&r.data.id===n&&(e.removeEventListener("message",t),i(r.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:n},t),r)}))}},3239:(e,t,r)=>{"use strict";function i(e){if(!e||"object"!=typeof e)return e;if("[object Date]"==Object.prototype.toString.call(e))return new Date(e.getTime());if(Array.isArray(e))return e.map(i);var t={};return Object.keys(e).forEach((function(r){t[r]=i(e[r])})),t}r.d(t,{Z:()=>i})},25516:(e,t,r)=>{"use strict";r.d(t,{i:()=>i});const i=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]},enumerable:!0,configurable:!0},finisher(r){const i=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){if(i.call(this),this[t.key]){const r=this.renderRoot.querySelector(e);if(!r)return;r.scrollTop=this[t.key]}}}})},59110:(e,t,r)=>{"use strict";var i=r(50424),n=r(55358),a=r(14516),o=r(47181),s=r(87744);r(67065),r(3143),r(42952);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=l();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(p(a.descriptor)||p(n.descriptor)){if(u(a)||u(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(u(a)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}d(a,n)}else t.push(a)}return t}(o.d.map(c)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,n.Mo)("hui-entity-picker-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"entities",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-data-table
        selectable
        .id=${"entity_id"}
        .columns=${this._columns(this.narrow)}
        .data=${this.entities}
        .dir=${(0,s.Zu)(this.hass)}
        .searchLabel=${this.hass.localize("ui.panel.lovelace.unused_entities.search")}
        .noLabelFloat=${this.noLabelFloat}
        .noDataText=${this.hass.localize("ui.panel.lovelace.unused_entities.no_data")}
        @selection-changed=${this._handleSelectionChanged}
      ></ha-data-table>
    `}},{kind:"field",key:"_columns",value(){return(0,a.Z)((e=>{const t={icon:{title:"",type:"icon",template:(e,t)=>i.dy`
          <state-badge
            @click=${this._handleEntityClicked}
            .hass=${this.hass}
            .stateObj=${t.stateObj}
          ></state-badge>
        `},name:{title:this.hass.localize("ui.panel.lovelace.unused_entities.entity"),sortable:!0,filterable:!0,grows:!0,direction:"asc",template:(t,r)=>i.dy`
          <div @click=${this._handleEntityClicked} style="cursor: pointer;">
            ${t}
            ${e?i.dy`
                  <div class="secondary">${r.stateObj.entity_id}</div>
                `:""}
          </div>
        `}};return t.entity_id={title:this.hass.localize("ui.panel.lovelace.unused_entities.entity_id"),sortable:!0,filterable:!0,width:"30%",hidden:e},t.domain={title:this.hass.localize("ui.panel.lovelace.unused_entities.domain"),sortable:!0,filterable:!0,width:"15%",hidden:e},t.last_changed={title:this.hass.localize("ui.panel.lovelace.unused_entities.last_changed"),type:"numeric",sortable:!0,width:"15%",hidden:e,template:e=>i.dy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${e}
        ></ha-relative-time>
      `},t}))}},{kind:"method",key:"_handleSelectionChanged",value:function(e){const t=e.detail.value;(0,o.B)(this,"selected-changed",{selectedEntities:t})}},{kind:"method",key:"_handleEntityClicked",value:function(e){const t=e.target.closest(".mdc-data-table__row").rowId;(0,o.B)(this,"hass-more-info",{entityId:t})}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-data-table {
        --data-table-border-width: 0;
        height: 100%;
      }
    `}}]}}),i.oi)},47512:(e,t,r)=>{"use strict";r.d(t,{f:()=>a});var i=r(47181);const n=()=>Promise.all([r.e(5009),r.e(7895),r.e(5386),r.e(8595),r.e(5829),r.e(4302),r.e(4953),r.e(1859),r.e(1251),r.e(3918),r.e(1434),r.e(7209),r.e(7150),r.e(7407),r.e(3340),r.e(4608),r.e(7529),r.e(8534),r.e(7757),r.e(6857)]).then(r.bind(r,9444)),a=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:n,dialogParams:t})}}}]);
//# sourceMappingURL=chunk.a20330da053ff0de78f0.js.map