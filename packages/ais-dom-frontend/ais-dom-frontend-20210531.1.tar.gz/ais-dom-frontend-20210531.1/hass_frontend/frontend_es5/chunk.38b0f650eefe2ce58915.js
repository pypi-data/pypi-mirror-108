(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[68558],{68558:function(e,t,n){"use strict";n.r(t),n.d(t,{HuiHumidifierCard:function(){return M}});n(32333);var r,i,o,s,a,c,l,d,u,f=n(50424),h=n(55358),p=n(62877),m=n(47181),y=n(91741),v=n(87744),g=(n(22098),n(10983),n(56007)),b=n(15688),w=n(53658),k=n(75502);function x(e){return(x="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function _(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function E(e,t,n,r,i,o,s){try{var a=e[o](s),c=a.value}catch(l){return void n(l)}a.done?t(c):Promise.resolve(c).then(r,i)}function P(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function S(e,t){return(S=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function z(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=q(e);if(t){var i=q(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return C(this,n)}}function C(e,t){return!t||"object"!==x(t)&&"function"!=typeof t?O(e):t}function O(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function j(){j=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!R(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return B(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?B(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=F(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:H(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=H(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function A(e){var t,n=F(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function D(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function R(e){return e.decorators&&e.decorators.length}function T(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function H(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function F(e){var t=function(e,t){if("object"!==x(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==x(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===x(t)?t:String(t)}function B(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function I(e,t,n){return(I="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=q(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function q(e){return(q=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var M=function(e,t,n,r){var i=j();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var s=t((function(e){i.initializeInstanceElements(e,a.elements)}),n),a=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(T(o.descriptor)||T(i.descriptor)){if(R(o)||R(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(R(o)){if(R(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}D(o,i)}else t.push(o)}return t}(s.d.map(A)),e);return i.initializeClassElements(s.F,a.elements),i.runClassFinishers(s.F,a.finishers)}([(0,h.Mo)("hui-humidifier-card")],(function(e,t){var x,C,j=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&S(e,t)}(r,t);var n=z(r);function r(){var t;P(this,r);for(var i=arguments.length,o=new Array(i),s=0;s<i;s++)o[s]=arguments[s];return t=n.call.apply(n,[this].concat(o)),e(O(t)),t}return r}(t);return{F:j,d:[{kind:"method",static:!0,key:"getConfigElement",value:(x=regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([n.e(75009),n.e(78161),n.e(42955),n.e(1041),n.e(91657),n.e(4268),n.e(93098),n.e(51422),n.e(74535),n.e(57210)]).then(n.bind(n,57210));case 2:return e.abrupt("return",document.createElement("hui-humidifier-card-editor"));case 3:case"end":return e.stop()}}),e)})),C=function(){var e=this,t=arguments;return new Promise((function(n,r){var i=x.apply(e,t);function o(e){E(i,n,r,o,s,"next",e)}function s(e){E(i,n,r,o,s,"throw",e)}o(void 0)}))},function(){return C.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,n){return{type:"humidifier",entity:(0,b.j)(e,1,t,n,["humidifier"])[0]||""}}},{kind:"field",decorators:[(0,h.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,h.SB)()],key:"_setHum",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 6}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity||"humidifier"!==e.entity.split(".")[0])throw new Error("Specify an entity from within the humidifier domain");this._config=e}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return(0,f.dy)(r||(r=_([""])));var e=this.hass.states[this._config.entity];if(!e)return(0,f.dy)(i||(i=_(["\n        <hui-warning>\n          ","\n        </hui-warning>\n      "])),(0,k.i)(this.hass,this._config.entity));var t=this._config.name||(0,y.C)(this.hass.states[this._config.entity]),n=null!==e.attributes.humidity&&Number.isFinite(Number(e.attributes.humidity))?e.attributes.humidity:e.attributes.min_humidity,u=(0,v.Zu)(this.hass),h=g.V_.includes(e.state)?(0,f.dy)(o||(o=_([' <round-slider disabled="true"></round-slider> ']))):(0,f.dy)(s||(s=_(["\n          <round-slider\n            .value=","\n            .min=","\n            .max=","\n            .rtl=",'\n            step="1"\n            @value-changing=',"\n            @value-changed=","\n          ></round-slider>\n        "])),n,e.attributes.min_humidity,e.attributes.max_humidity,"rtl"===u,this._dragEvent,this._setHumidity),p=(0,f.YP)(a||(a=_(['\n      <svg viewBox="0 0 40 20">\n        <text\n          x="50%"\n          dx="1"\n          y="60%"\n          text-anchor="middle"\n          style="font-size: 13px;"\n          class="set-value"\n        >\n          ','\n        </text>\n      </svg>\n      <svg id="set-values">\n        <g>\n          <text\n            dy="22"\n            text-anchor="middle"\n            id="set-mode"\n          >\n            ',"\n            ","\n          </text>\n        </g>\n      </svg>\n    "])),g.V_.includes(e.state)||void 0===this._setHum||null===this._setHum?"":(0,f.YP)(c||(c=_(["\n                    ",'\n                    <tspan dx="-3" dy="-6.5" style="font-size: 4px;">\n                      %\n                    </tspan>\n                    '])),this._setHum.toFixed()),this.hass.localize("state.default.".concat(e.state)),e.attributes.mode&&!g.V_.includes(e.state)?(0,f.dy)(l||(l=_(["\n                    -\n                    ","\n                  "])),this.hass.localize("state_attributes.humidifier.mode.".concat(e.attributes.mode))||e.attributes.mode):"");return(0,f.dy)(d||(d=_(['\n      <ha-card>\n        <ha-icon-button\n          icon="hass:dots-vertical"\n          class="more-info"\n          @click=','\n          tabindex="0"\n        ></ha-icon-button>\n\n        <div class="content">\n          <div id="controls">\n            <div id="slider">\n              ','\n              <div id="slider-center">\n                <div id="humidity">','</div>\n              </div>\n            </div>\n          </div>\n          <div id="info">',"</div>\n        </div>\n      </ha-card>\n    "])),this._handleMoreInfo,h,p,t)}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,w.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(I(q(j.prototype),"updated",this).call(this,e),this._config&&this.hass&&(e.has("hass")||e.has("_config"))){var t=e.get("hass"),n=e.get("_config");t&&n&&t.themes===this.hass.themes&&n.theme===this._config.theme||(0,p.R)(this,this.hass.themes,this._config.theme);var r=this.hass.states[this._config.entity];r&&(t&&t.states[this._config.entity]===r||this._rescale_svg())}}},{kind:"method",key:"willUpdate",value:function(e){if(this.hass&&this._config&&e.has("hass")){var t=this.hass.states[this._config.entity];if(t){var n=e.get("hass");n&&n.states[this._config.entity]===t||(this._setHum=this._getSetHum(t))}}}},{kind:"method",key:"_rescale_svg",value:function(){var e=this;this.shadowRoot&&this.shadowRoot.querySelector("ha-card")&&this.shadowRoot.querySelector("ha-card").updateComplete.then((function(){var t=e.shadowRoot.querySelector("#set-values"),n=t.querySelector("g").getBBox();t.setAttribute("viewBox","".concat(n.x," ").concat(n.y," ").concat(n.width," ").concat(n.height)),t.setAttribute("width","".concat(n.width)),t.setAttribute("height","".concat(n.height))}))}},{kind:"method",key:"_getSetHum",value:function(e){if(!g.V_.includes(e.state))return e.attributes.humidity}},{kind:"method",key:"_dragEvent",value:function(e){this._setHum=e.detail.value}},{kind:"method",key:"_setHumidity",value:function(e){this.hass.callService("humidifier","set_humidity",{entity_id:this._config.entity,humidity:e.detail.value})}},{kind:"method",key:"_handleMoreInfo",value:function(){(0,m.B)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,f.iv)(u||(u=_(["\n      :host {\n        display: block;\n      }\n\n      ha-card {\n        height: 100%;\n        position: relative;\n        overflow: hidden;\n        --name-font-size: 1.2rem;\n        --brightness-font-size: 1.2rem;\n        --rail-border-color: transparent;\n      }\n\n      .more-info {\n        position: absolute;\n        cursor: pointer;\n        top: 0;\n        right: 0;\n        border-radius: 100%;\n        color: var(--secondary-text-color);\n        z-index: 25;\n      }\n\n      .content {\n        height: 100%;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n      }\n\n      #controls {\n        display: flex;\n        justify-content: center;\n        padding: 16px;\n        position: relative;\n      }\n\n      #slider {\n        height: 100%;\n        width: 100%;\n        position: relative;\n        max-width: 250px;\n        min-width: 100px;\n      }\n\n      round-slider {\n        --round-slider-path-color: var(--disabled-text-color);\n        --round-slider-bar-color: var(--mode-color);\n        padding-bottom: 10%;\n      }\n\n      #slider-center {\n        position: absolute;\n        width: calc(100% - 40px);\n        height: calc(100% - 40px);\n        box-sizing: border-box;\n        border-radius: 100%;\n        left: 20px;\n        top: 20px;\n        text-align: center;\n        overflow-wrap: break-word;\n        pointer-events: none;\n      }\n\n      #humidity {\n        position: absolute;\n        transform: translate(-50%, -50%);\n        width: 100%;\n        height: 50%;\n        top: 45%;\n        left: 50%;\n      }\n\n      #set-values {\n        max-width: 80%;\n        transform: translate(0, -50%);\n        font-size: 20px;\n      }\n\n      #set-mode {\n        fill: var(--secondary-text-color);\n        font-size: 16px;\n      }\n\n      #info {\n        display: flex-vertical;\n        justify-content: center;\n        text-align: center;\n        padding: 16px;\n        margin-top: -60px;\n        font-size: var(--name-font-size);\n      }\n\n      #modes > * {\n        color: var(--disabled-text-color);\n        cursor: pointer;\n        display: inline-block;\n      }\n\n      #modes .selected-icon {\n        color: var(--mode-color);\n      }\n\n      text {\n        fill: var(--primary-text-color);\n      }\n    "])))}}]}}),f.oi)}}]);
//# sourceMappingURL=chunk.38b0f650eefe2ce58915.js.map