/*! For license information please see chunk.bba0618327bc1eb8a4ec.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[68644],{68644:function(e,c,o){"use strict";function t(e){return(t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}o.d(c,{X:function(){return T}});function r(e,c,o,r){var n,a=arguments.length,i=a<3?c:null===r?r=Object.getOwnPropertyDescriptor(c,o):r;if("object"===("undefined"==typeof Reflect?"undefined":t(Reflect))&&"function"==typeof Reflect.decorate)i=Reflect.decorate(e,c,o,r);else for(var d=e.length-1;d>=0;d--)(n=e[d])&&(i=(a<3?n(i):a>3?n(c,o,i):n(c,o))||i);return a>3&&i&&Object.defineProperty(c,o,i),i}Object.create;Object.create;var n,a,i=o(55704),d=(o(66702),o(38103)),m=o(18601),h=o(98734),b=o(81471),l=o(49629);function k(e){return(k="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function p(e,c){return c||(c=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(c)}}))}function s(e,c){if(!(e instanceof c))throw new TypeError("Cannot call a class as a function")}function u(e,c){for(var o=0;o<c.length;o++){var t=c[o];t.enumerable=t.enumerable||!1,t.configurable=!0,"value"in t&&(t.writable=!0),Object.defineProperty(e,t.key,t)}}function x(e,c,o){return(x="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,c,o){var t=function(e,c){for(;!Object.prototype.hasOwnProperty.call(e,c)&&null!==(e=v(e)););return e}(e,c);if(t){var r=Object.getOwnPropertyDescriptor(t,c);return r.get?r.get.call(o):r.value}})(e,c,o||e)}function f(e,c){return(f=Object.setPrototypeOf||function(e,c){return e.__proto__=c,e})(e,c)}function _(e){var c=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var o,t=v(e);if(c){var r=v(this).constructor;o=Reflect.construct(t,arguments,r)}else o=t.apply(this,arguments);return y(this,o)}}function y(e,c){return!c||"object"!==k(c)&&"function"!=typeof c?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):c}function v(e){return(v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var g,w=function(e){!function(e,c){if("function"!=typeof c&&null!==c)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(c&&c.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),c&&f(e,c)}(d,e);var c,o,t,r=_(d);function d(){var e;return s(this,d),(e=r.apply(this,arguments)).checked=!1,e.indeterminate=!1,e.disabled=!1,e.value="",e.reducedTouchTarget=!1,e.animationClass="",e.shouldRenderRipple=!1,e.focused=!1,e.mdcFoundationClass=void 0,e.mdcFoundation=void 0,e.rippleElement=null,e.rippleHandlers=new h.A((function(){return e.shouldRenderRipple=!0,e.ripple.then((function(c){return e.rippleElement=c})),e.ripple})),e}return c=d,(o=[{key:"createAdapter",value:function(){return{}}},{key:"update",value:function(e){var c=e.get("indeterminate"),o=e.get("checked"),t=e.get("disabled");if(void 0!==c||void 0!==o||void 0!==t){var r=this.calculateAnimationStateName(!!o,!!c,!!t),n=this.calculateAnimationStateName(this.checked,this.indeterminate,this.disabled);this.animationClass="".concat(r,"-").concat(n)}x(v(d.prototype),"update",this).call(this,e)}},{key:"calculateAnimationStateName",value:function(e,c,o){return o?"disabled":c?"indeterminate":e?"checked":"unchecked"}},{key:"renderRipple",value:function(){return this.shouldRenderRipple?(0,i.dy)(n||(n=p(['<mwc-ripple\n        .disabled="','"\n        unbounded></mwc-ripple>'])),this.disabled):""}},{key:"render",value:function(){var e=this.indeterminate||this.checked,c={"mdc-checkbox--disabled":this.disabled,"mdc-checkbox--selected":e,"mdc-checkbox--touch":!this.reducedTouchTarget,"mdc-ripple-upgraded--background-focused":this.focused,"mdc-checkbox--anim-checked-indeterminate":"checked-indeterminate"==this.animationClass,"mdc-checkbox--anim-checked-unchecked":"checked-unchecked"==this.animationClass,"mdc-checkbox--anim-indeterminate-checked":"indeterminate-checked"==this.animationClass,"mdc-checkbox--anim-indeterminate-unchecked":"indeterminate-unchecked"==this.animationClass,"mdc-checkbox--anim-unchecked-checked":"unchecked-checked"==this.animationClass,"mdc-checkbox--anim-unchecked-indeterminate":"unchecked-indeterminate"==this.animationClass},o=this.indeterminate?"mixed":void 0;return(0,i.dy)(a||(a=p(['\n      <div class="mdc-checkbox mdc-checkbox--upgraded ','">\n        <input type="checkbox"\n              class="mdc-checkbox__native-control"\n              name="','"\n              aria-checked="','"\n              aria-label="','"\n              aria-labelledby="','"\n              aria-describedby="','"\n              data-indeterminate="','"\n              ?disabled="','"\n              .indeterminate="','"\n              .checked="','"\n              .value="','"\n              @change="','"\n              @focus="','"\n              @blur="','"\n              @mousedown="','"\n              @mouseenter="','"\n              @mouseleave="','"\n              @touchstart="','"\n              @touchend="','"\n              @touchcancel="','">\n        <div class="mdc-checkbox__background"\n          @animationend="','">\n          <svg class="mdc-checkbox__checkmark"\n              viewBox="0 0 24 24">\n            <path class="mdc-checkbox__checkmark-path"\n                  fill="none"\n                  d="M1.73,12.91 8.1,19.28 22.79,4.59"></path>\n          </svg>\n          <div class="mdc-checkbox__mixedmark"></div>\n        </div>\n        ',"\n      </div>"])),(0,b.$)(c),(0,l.o)(this.name),(0,l.o)(o),(0,l.o)(this.ariaLabel),(0,l.o)(this.ariaLabelledBy),(0,l.o)(this.ariaDescribedBy),this.indeterminate?"true":"false",this.disabled,this.indeterminate,this.checked,this.value,this.handleChange,this.handleFocus,this.handleBlur,this.handleRippleMouseDown,this.handleRippleMouseEnter,this.handleRippleMouseLeave,this.handleRippleTouchStart,this.handleRippleDeactivate,this.handleRippleDeactivate,this.resetAnimationClass,this.renderRipple())}},{key:"handleFocus",value:function(){this.focused=!0,this.handleRippleFocus()}},{key:"handleBlur",value:function(){this.focused=!1,this.handleRippleBlur()}},{key:"handleRippleMouseDown",value:function(e){var c=this;window.addEventListener("mouseup",(function e(){window.removeEventListener("mouseup",e),c.handleRippleDeactivate()})),this.rippleHandlers.startPress(e)}},{key:"handleRippleTouchStart",value:function(e){this.rippleHandlers.startPress(e)}},{key:"handleRippleDeactivate",value:function(){this.rippleHandlers.endPress()}},{key:"handleRippleMouseEnter",value:function(){this.rippleHandlers.startHover()}},{key:"handleRippleMouseLeave",value:function(){this.rippleHandlers.endHover()}},{key:"handleRippleFocus",value:function(){this.rippleHandlers.startFocus()}},{key:"handleRippleBlur",value:function(){this.rippleHandlers.endFocus()}},{key:"handleChange",value:function(){this.checked=this.formElement.checked,this.indeterminate=this.formElement.indeterminate}},{key:"resetAnimationClass",value:function(){this.animationClass=""}},{key:"isRippleActive",get:function(){var e;return(null===(e=this.rippleElement)||void 0===e?void 0:e.isActive)||!1}}])&&u(c.prototype,o),t&&u(c,t),d}(m.Wg);r([(0,i.IO)(".mdc-checkbox")],w.prototype,"mdcRoot",void 0),r([(0,i.IO)("input")],w.prototype,"formElement",void 0),r([(0,i.Cb)({type:Boolean,reflect:!0})],w.prototype,"checked",void 0),r([(0,i.Cb)({type:Boolean})],w.prototype,"indeterminate",void 0),r([(0,i.Cb)({type:Boolean,reflect:!0})],w.prototype,"disabled",void 0),r([(0,i.Cb)({type:String,reflect:!0})],w.prototype,"name",void 0),r([(0,i.Cb)({type:String})],w.prototype,"value",void 0),r([d.L,(0,i.Cb)({type:String,attribute:"aria-label"})],w.prototype,"ariaLabel",void 0),r([d.L,(0,i.Cb)({type:String,attribute:"aria-labelledby"})],w.prototype,"ariaLabelledBy",void 0),r([d.L,(0,i.Cb)({type:String,attribute:"aria-describedby"})],w.prototype,"ariaDescribedBy",void 0),r([(0,i.Cb)({type:Boolean})],w.prototype,"reducedTouchTarget",void 0),r([(0,i.SB)()],w.prototype,"animationClass",void 0),r([(0,i.SB)()],w.prototype,"shouldRenderRipple",void 0),r([(0,i.SB)()],w.prototype,"focused",void 0),r([(0,i.GC)("mwc-ripple")],w.prototype,"ripple",void 0),r([(0,i.hO)({passive:!0})],w.prototype,"handleRippleTouchStart",null);var R,z,O=(0,i.iv)(g||(R=[".mdc-checkbox{padding:calc((40px - 18px) / 2);padding:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);margin:calc((40px - 40px) / 2);margin:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-ripple-size, 40px)) / 2)}.mdc-checkbox .mdc-checkbox__ripple::before,.mdc-checkbox .mdc-checkbox__ripple::after{background-color:#000;background-color:var(--mdc-ripple-color, #000)}.mdc-checkbox:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox.mdc-checkbox--selected:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox .mdc-checkbox__background{top:calc((40px - 18px) / 2);top:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);left:calc((40px - 18px) / 2);left:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2)}.mdc-checkbox .mdc-checkbox__native-control{top:calc((40px - 40px) / 2);top:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-ripple-size, 40px)) / 2);right:calc((40px - 40px) / 2);right:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-ripple-size, 40px)) / 2);left:calc((40px - 40px) / 2);left:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-ripple-size, 40px)) / 2);width:40px;width:var(--mdc-checkbox-ripple-size, 40px);height:40px;height:var(--mdc-checkbox-ripple-size, 40px)}.mdc-checkbox .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control:enabled:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control:enabled:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true]:enabled~.mdc-checkbox__background{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}@keyframes mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786{0%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}50%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}}@keyframes mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786{0%,80%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}100%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}}.mdc-checkbox.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786}.mdc-checkbox.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786}.mdc-checkbox .mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.38);border-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:transparent;background-color:rgba(0, 0, 0, 0.38);background-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38))}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-touch-target-wrapper{display:inline}@keyframes mdc-checkbox-unchecked-checked-checkmark-path{0%,50%{stroke-dashoffset:29.7833385}50%{animation-timing-function:cubic-bezier(0, 0, 0.2, 1)}100%{stroke-dashoffset:0}}@keyframes mdc-checkbox-unchecked-indeterminate-mixedmark{0%,68.2%{transform:scaleX(0)}68.2%{animation-timing-function:cubic-bezier(0, 0, 0, 1)}100%{transform:scaleX(1)}}@keyframes mdc-checkbox-checked-unchecked-checkmark-path{from{animation-timing-function:cubic-bezier(0.4, 0, 1, 1);opacity:1;stroke-dashoffset:0}to{opacity:0;stroke-dashoffset:-29.7833385}}@keyframes mdc-checkbox-checked-indeterminate-checkmark{from{animation-timing-function:cubic-bezier(0, 0, 0.2, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(45deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-checked-checkmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(45deg);opacity:0}to{transform:rotate(360deg);opacity:1}}@keyframes mdc-checkbox-checked-indeterminate-mixedmark{from{animation-timing-function:mdc-animation-deceleration-curve-timing-function;transform:rotate(-45deg);opacity:0}to{transform:rotate(0deg);opacity:1}}@keyframes mdc-checkbox-indeterminate-checked-mixedmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(315deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-unchecked-mixedmark{0%{animation-timing-function:linear;transform:scaleX(1);opacity:1}32.8%,100%{transform:scaleX(0);opacity:0}}.mdc-checkbox{display:inline-block;position:relative;flex:0 0 18px;box-sizing:content-box;width:18px;height:18px;line-height:0;white-space:nowrap;cursor:pointer;vertical-align:bottom}@media screen and (-ms-high-contrast: active){.mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:GrayText;border-color:var(--mdc-checkbox-disabled-color, GrayText);background-color:transparent}.mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:GrayText;background-color:transparent;background-color:var(--mdc-checkbox-disabled-color, transparent)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:GrayText;color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:GrayText;border-color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__mixedmark{margin:0 1px}}.mdc-checkbox--disabled{cursor:default;pointer-events:none}.mdc-checkbox__background{display:inline-flex;position:absolute;align-items:center;justify-content:center;box-sizing:border-box;width:18px;height:18px;border:2px solid currentColor;border-radius:2px;background-color:transparent;pointer-events:none;will-change:background-color,border-color;transition:background-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),border-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__checkmark{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;opacity:0;transition:opacity 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--upgraded .mdc-checkbox__checkmark{opacity:1}.mdc-checkbox__checkmark-path{transition:stroke-dashoffset 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1);stroke:currentColor;stroke-width:3.12px;stroke-dashoffset:29.7833385;stroke-dasharray:29.7833385}.mdc-checkbox__mixedmark{width:100%;height:0;transform:scaleX(0) rotate(0deg);border-width:1px;border-style:solid;opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__background,.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__background,.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__background,.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__background{animation-duration:180ms;animation-timing-function:linear}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-unchecked-checked-checkmark-path 180ms linear 0s;transition:none}.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-unchecked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-checked-unchecked-checkmark-path 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__checkmark{animation:mdc-checkbox-checked-indeterminate-checkmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-checked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__checkmark{animation:mdc-checkbox-indeterminate-checked-checkmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-checked-mixedmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-unchecked-mixedmark 300ms linear 0s;transition:none}.mdc-checkbox__native-control:checked~.mdc-checkbox__background,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background{transition:border-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1),background-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark-path{stroke-dashoffset:0}.mdc-checkbox__native-control{position:absolute;margin:0;padding:0;opacity:0;cursor:inherit}.mdc-checkbox__native-control:disabled{cursor:default;pointer-events:none}.mdc-checkbox--touch{margin:calc((48px - 40px) / 2);margin:calc((var(--mdc-checkbox-touch-target-size, 48px) - var(--mdc-checkbox-ripple-size, 40px)) / 2)}.mdc-checkbox--touch .mdc-checkbox__native-control{top:calc((40px - 48px) / 2);top:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-touch-target-size, 48px)) / 2);right:calc((40px - 48px) / 2);right:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-touch-target-size, 48px)) / 2);left:calc((40px - 48px) / 2);left:calc((var(--mdc-checkbox-ripple-size, 40px) - var(--mdc-checkbox-touch-target-size, 48px)) / 2);width:48px;width:var(--mdc-checkbox-touch-target-size, 48px);height:48px;height:var(--mdc-checkbox-touch-target-size, 48px)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark{transition:opacity 180ms 0ms cubic-bezier(0, 0, 0.2, 1),transform 180ms 0ms cubic-bezier(0, 0, 0.2, 1);opacity:1}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(-45deg)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark{transform:rotate(45deg);opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__mixedmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(0deg);opacity:1}.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark-path,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__mixedmark{transition:none}:host{outline:none;display:inline-flex;-webkit-tap-highlight-color:transparent}:host([checked]),:host([indeterminate]){--mdc-ripple-color:var(--mdc-theme-secondary, #018786)}.mdc-checkbox .mdc-checkbox__background::before{content:none}"],z||(z=R.slice(0)),g=Object.freeze(Object.defineProperties(R,{raw:{value:Object.freeze(z)}}))));function C(e){return(C="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function S(e,c){if(!(e instanceof c))throw new TypeError("Cannot call a class as a function")}function j(e,c){return(j=Object.setPrototypeOf||function(e,c){return e.__proto__=c,e})(e,c)}function F(e){var c=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var o,t=P(e);if(c){var r=P(this).constructor;o=Reflect.construct(t,arguments,r)}else o=t.apply(this,arguments);return B(this,o)}}function B(e,c){return!c||"object"!==C(c)&&"function"!=typeof c?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):c}function P(e){return(P=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var T=function(e){!function(e,c){if("function"!=typeof c&&null!==c)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(c&&c.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),c&&j(e,c)}(o,e);var c=F(o);function o(){return S(this,o),c.apply(this,arguments)}return o}(w);T.styles=O,T=r([(0,i.Mo)("mwc-checkbox")],T)}}]);
//# sourceMappingURL=chunk.bba0618327bc1eb8a4ec.js.map