(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[65992],{65992:function(e,t,r){"use strict";r(54444);var n,i,o,a,s,l=r(50424),c=r(55358),f=r(91741),d=r(87744);r(42952),r(3143);function u(e){return(u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function p(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function h(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){return(m=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function y(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=D(e);if(t){var i=D(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return v(this,r)}}function v(e,t){return!t||"object"!==u(t)&&"function"!=typeof t?b(e):t}function b(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function w(){w=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!E(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var f=0;f<c.length;f++)this.addElementPlacement(c[f],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return P(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?P(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=j(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:O(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function g(e){var t,r=j(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function j(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==u(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function P(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function C(e,t,r){return(C="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=D(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function D(e){return(D=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,n){var i=w();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(x(o.descriptor)||x(i.descriptor)){if(E(o)||E(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(E(o)){if(E(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}k(o,i)}else t.push(o)}return t}(a.d.map(g)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,c.Mo)("state-info")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&m(e,t)}(n,t);var r=y(n);function n(){var t;h(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(b(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,c.Cb)({type:Boolean})],key:"inDialog",value:function(){return!1}},{kind:"field",decorators:[(0,c.Cb)({type:Boolean,reflect:!0})],key:"rtl",value:function(){return!1}},{kind:"method",key:"render",value:function(){return this.hass&&this.stateObj?(0,l.dy)(i||(i=p(["<state-badge\n        .stateObj=","\n        .stateColor=",'\n      ></state-badge>\n      <div class="info">\n        <div class="name" .inDialog=',">\n          ","\n        </div>\n        ","\n      </div>"])),this.stateObj,!0,this.inDialog,(0,f.C)(this.stateObj),this.inDialog?(0,l.dy)(o||(o=p(['<div class="time-ago">\n              <ha-relative-time\n                id="last_changed"\n                .hass=',"\n                .datetime=",'\n              ></ha-relative-time>\n              <paper-tooltip animation-delay="0" for="last_changed">\n                <div>\n                  <div class="row">\n                    <span class="column-name">\n                      ',":\n                    </span>\n                    <ha-relative-time\n                      .hass=","\n                      .datetime=",'\n                    ></ha-relative-time>\n                  </div>\n                  <div class="row">\n                    <span>\n                      ',":\n                    </span>\n                    <ha-relative-time\n                      .hass=","\n                      .datetime=","\n                    ></ha-relative-time>\n                  </div>\n                </div>\n              </paper-tooltip>\n            </div>"])),this.hass,this.stateObj.last_changed,this.hass.localize("ui.dialogs.more_info_control.last_changed"),this.hass,this.stateObj.last_changed,this.hass.localize("ui.dialogs.more_info_control.last_updated"),this.hass,this.stateObj.last_updated):(0,l.dy)(a||(a=p(['<div class="extra-info"><slot></slot></div>'])))):(0,l.dy)(n||(n=p([""])))}},{kind:"method",key:"updated",value:function(e){if(C(D(r.prototype),"updated",this).call(this,e),e.has("hass")){var t=e.get("hass");t&&t.locale===this.hass.locale||(this.rtl=(0,d.HE)(this.hass))}}},{kind:"get",static:!0,key:"styles",value:function(){return(0,l.iv)(s||(s=p(["\n      :host {\n        min-width: 120px;\n        white-space: nowrap;\n      }\n\n      state-badge {\n        float: left;\n      }\n\n      :host([rtl]) state-badge {\n        float: right;\n      }\n\n      .info {\n        margin-left: 56px;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        height: 100%;\n      }\n\n      :host([rtl]) .info {\n        margin-right: 56px;\n        margin-left: 0;\n        text-align: right;\n      }\n\n      .name {\n        color: var(--primary-text-color);\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n      }\n\n      .name[in-dialog],\n      :host([secondary-line]) .name {\n        line-height: 20px;\n      }\n\n      .time-ago,\n      .extra-info,\n      .extra-info > * {\n        color: var(--secondary-text-color);\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n      }\n\n      .row {\n        display: flex;\n        flex-direction: row;\n        flex-wrap: no-wrap;\n        width: 100%;\n        justify-content: space-between;\n        margin: 0 2px 4px 0;\n      }\n\n      .row:last-child {\n        margin-bottom: 0px;\n      }\n    "])))}}]}}),l.oi)}}]);
//# sourceMappingURL=chunk.c5013ace057912975514.js.map