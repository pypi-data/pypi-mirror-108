(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[63238],{63238:function(t,e,n){"use strict";n.r(e);var o=n(47181);function r(t){return(r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function i(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function c(t,e){for(var n=0;n<e.length;n++){var o=e[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}function u(t,e,n){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,n){var o=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=y(t)););return t}(t,e);if(o){var r=Object.getOwnPropertyDescriptor(o,e);return r.get?r.get.call(n):r.value}})(t,e,n||t)}function a(t,e){return!e||"object"!==r(e)&&"function"!=typeof e?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function s(t){var e="function"==typeof Map?new Map:void 0;return(s=function(t){if(null===t||(n=t,-1===Function.toString.call(n).indexOf("[native code]")))return t;var n;if("function"!=typeof t)throw new TypeError("Super expression must either be null or a function");if(void 0!==e){if(e.has(t))return e.get(t);e.set(t,o)}function o(){return f(t,arguments,y(this).constructor)}return o.prototype=Object.create(t.prototype,{constructor:{value:o,enumerable:!1,writable:!0,configurable:!0}}),p(o,t)})(t)}function f(t,e,n){return(f=l()?Reflect.construct:function(t,e,n){var o=[null];o.push.apply(o,e);var r=new(Function.bind.apply(t,o));return n&&p(r,n.prototype),r}).apply(null,arguments)}function l(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}function p(t,e){return(p=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function y(t){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var h=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&p(t,e)}(b,t);var e,n,r,s,f,h=(e=b,n=l(),function(){var t,o=y(e);if(n){var r=y(this).constructor;t=Reflect.construct(o,arguments,r)}else t=o.apply(this,arguments);return a(this,t)});function b(){return i(this,b),h.apply(this,arguments)}return r=b,(s=[{key:"hass",set:function(t){if(!this.content){var e=document.createElement("ha-card");this.content=document.createElement("div"),e.appendChild(this.content),e.style="background:none; width: 110px; border-radius: 52.5px; cursor: pointer;",this.appendChild(e),this.addEventListener("click",(function(){this._onClick(t)})),this.addEventListener("dblclick",(function(){this._onDbClick()}))}var n=this.config.entity,o=this.config.class||this.config.entity.replace(".","_");this.setAttribute("class",o);var r=t.states[n],i=this.config.image_on||"/static/ais_dom/design_tool/light_on.png",c=this.config.image_off||"/static/ais_dom/design_tool/light_off.png";if(r)if("on"===r.state){var u=r.attributes.rgb_color,a=r.attributes.hs_color,s="";a&&"255,255,255"!==u&&(s=" hue-rotate("+a[0]+"deg)");var f=r.attributes.brightness/205;this.content.innerHTML='<img src="'.concat(i,'" style="position: absolute; filter: opacity(').concat(f,") ").concat(s,'!important;">')}else this.content.innerHTML='<img src="'.concat(c,'" class="').concat(o,'"  style="position: absolute;">');else this.content.innerHTML='<img src="'.concat(c,'" class="').concat(o,'" style="position: absolute;">')}},{key:"_onClick",value:function(t){var e=this.config.tap_action||"toggle";t.callService("light",e,{entity_id:this.config.entity})}},{key:"_onDbClick",value:function(){(0,o.B)(this,"hass-more-info",{entityId:this.config.entity})}},{key:"ready",value:function(){u(y(b.prototype),"ready",this).call(this)}},{key:"setConfig",value:function(t){if(!t.entity)throw new Error("You need to define an entity");this.config=t}},{key:"getCardSize",value:function(){return 3}}])&&c(r.prototype,s),f&&c(r,f),b}(s(HTMLElement));customElements.define("hui-ais-light-card",h)}}]);
//# sourceMappingURL=chunk.ded1dda096e6927f4963.js.map