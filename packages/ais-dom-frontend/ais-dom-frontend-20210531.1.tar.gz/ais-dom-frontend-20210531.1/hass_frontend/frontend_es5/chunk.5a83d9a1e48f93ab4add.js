/*! For license information please see chunk.5a83d9a1e48f93ab4add.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[29981],{23916:function(e,t,n){"use strict";n.d(t,{N:function(){return d}});n(65233);var i,s=n(9672),r=n(50856);var o,a,d=(0,s.k)({_template:(0,r.d)(i||(o=['\n    <style>\n      :host {\n        display: inline-block;\n        position: fixed;\n        clip: rect(0px,0px,0px,0px);\n      }\n    </style>\n    <div aria-live$="[[mode]]">[[_text]]</div>\n'],a||(a=o.slice(0)),i=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(a)}})))),is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){d.instance||(d.instance=this),document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(e){this._text="",this.async((function(){this._text=e}),100)},_onIronAnnounce:function(e){e.detail&&e.detail.text&&this.announce(e.detail.text)}});d.instance=null,d.requestAvailability=function(){d.instance||(d.instance=document.createElement("iron-a11y-announcer")),document.body.appendChild(d.instance)}},8621:function(e,t,n){"use strict";n.d(t,{G:function(){return y}});n(65233);var i={"U+0008":"backspace","U+0009":"tab","U+001B":"esc","U+0020":"space","U+007F":"del"},s={8:"backspace",9:"tab",13:"enter",27:"esc",33:"pageup",34:"pagedown",35:"end",36:"home",32:"space",37:"left",38:"up",39:"right",40:"down",46:"del",106:"*"},r={shift:"shiftKey",ctrl:"ctrlKey",alt:"altKey",meta:"metaKey"},o=/[a-z0-9*]/,a=/U\+/,d=/^arrow/,c=/^space(bar)?/,h=/^escape$/;function u(e,t){var n="";if(e){var i=e.toLowerCase();" "===i||c.test(i)?n="space":h.test(i)?n="esc":1==i.length?t&&!o.test(i)||(n=i):n=d.test(i)?i.replace("arrow",""):"multiply"==i?"*":i}return n}function l(e,t){return e.key?u(e.key,t):e.detail&&e.detail.key?u(e.detail.key,t):(n=e.keyIdentifier,r="",n&&(n in i?r=i[n]:a.test(n)?(n=parseInt(n.replace("U+","0x"),16),r=String.fromCharCode(n).toLowerCase()):r=n.toLowerCase()),r||function(e){var t="";return Number(e)&&(t=e>=65&&e<=90?String.fromCharCode(32+e):e>=112&&e<=123?"f"+(e-112+1):e>=48&&e<=57?String(e-48):e>=96&&e<=105?String(e-96):s[e]),t}(e.keyCode)||"");var n,r}function f(e,t){return l(t,e.hasModifiers)===e.key&&(!e.hasModifiers||!!t.shiftKey==!!e.shiftKey&&!!t.ctrlKey==!!e.ctrlKey&&!!t.altKey==!!e.altKey&&!!t.metaKey==!!e.metaKey)}function p(e){return e.trim().split(" ").map((function(e){return function(e){return 1===e.length?{combo:e,key:e,event:"keydown"}:e.split("+").reduce((function(e,t){var n=t.split(":"),i=n[0],s=n[1];return i in r?(e[r[i]]=!0,e.hasModifiers=!0):(e.key=i,e.event=s||"keydown"),e}),{combo:e.split(":").shift()})}(e)}))}var y={properties:{keyEventTarget:{type:Object,value:function(){return this}},stopKeyboardEventPropagation:{type:Boolean,value:!1},_boundKeyHandlers:{type:Array,value:function(){return[]}},_imperativeKeyBindings:{type:Object,value:function(){return{}}}},observers:["_resetKeyEventListeners(keyEventTarget, _boundKeyHandlers)"],keyBindings:{},registered:function(){this._prepKeyBindings()},attached:function(){this._listenKeyEventListeners()},detached:function(){this._unlistenKeyEventListeners()},addOwnKeyBinding:function(e,t){this._imperativeKeyBindings[e]=t,this._prepKeyBindings(),this._resetKeyEventListeners()},removeOwnKeyBindings:function(){this._imperativeKeyBindings={},this._prepKeyBindings(),this._resetKeyEventListeners()},keyboardEventMatchesKeys:function(e,t){for(var n=p(t),i=0;i<n.length;++i)if(f(n[i],e))return!0;return!1},_collectKeyBindings:function(){var e=this.behaviors.map((function(e){return e.keyBindings}));return-1===e.indexOf(this.keyBindings)&&e.push(this.keyBindings),e},_prepKeyBindings:function(){for(var e in this._keyBindings={},this._collectKeyBindings().forEach((function(e){for(var t in e)this._addKeyBinding(t,e[t])}),this),this._imperativeKeyBindings)this._addKeyBinding(e,this._imperativeKeyBindings[e]);for(var t in this._keyBindings)this._keyBindings[t].sort((function(e,t){var n=e[0].hasModifiers;return n===t[0].hasModifiers?0:n?-1:1}))},_addKeyBinding:function(e,t){p(e).forEach((function(e){this._keyBindings[e.event]=this._keyBindings[e.event]||[],this._keyBindings[e.event].push([e,t])}),this)},_resetKeyEventListeners:function(){this._unlistenKeyEventListeners(),this.isAttached&&this._listenKeyEventListeners()},_listenKeyEventListeners:function(){this.keyEventTarget&&Object.keys(this._keyBindings).forEach((function(e){var t=this._keyBindings[e],n=this._onKeyBindingEvent.bind(this,t);this._boundKeyHandlers.push([this.keyEventTarget,e,n]),this.keyEventTarget.addEventListener(e,n)}),this)},_unlistenKeyEventListeners:function(){for(var e,t,n,i;this._boundKeyHandlers.length;)t=(e=this._boundKeyHandlers.pop())[0],n=e[1],i=e[2],t.removeEventListener(n,i)},_onKeyBindingEvent:function(e,t){if(this.stopKeyboardEventPropagation&&t.stopPropagation(),!t.defaultPrevented)for(var n=0;n<e.length;n++){var i=e[n][0],s=e[n][1];if(f(i,t)&&(this._triggerKeyHandler(i,s,t),t.defaultPrevented))return}},_triggerKeyHandler:function(e,t,n){var i=Object.create(e);i.keyboardEvent=n;var s=new CustomEvent(e.event,{detail:i,cancelable:!0});this[t].call(this,s),s.defaultPrevented&&n.preventDefault()}}},72986:function(e,t,n){"use strict";n.d(t,{z:function(){return o}});n(65233);var i=n(87156),s=n(74460),r=new Set,o={properties:{_parentResizable:{type:Object,observer:"_parentResizableChanged"},_notifyingDescendant:{type:Boolean,value:!1}},listeners:{"iron-request-resize-notifications":"_onIronRequestResizeNotifications"},created:function(){this._interestedResizables=[],this._boundNotifyResize=this.notifyResize.bind(this),this._boundOnDescendantIronResize=this._onDescendantIronResize.bind(this)},attached:function(){this._requestResizeNotifications()},detached:function(){this._parentResizable?this._parentResizable.stopResizeNotificationsFor(this):(r.delete(this),window.removeEventListener("resize",this._boundNotifyResize)),this._parentResizable=null},notifyResize:function(){this.isAttached&&(this._interestedResizables.forEach((function(e){this.resizerShouldNotify(e)&&this._notifyDescendant(e)}),this),this._fireResize())},assignParentResizable:function(e){this._parentResizable&&this._parentResizable.stopResizeNotificationsFor(this),this._parentResizable=e,e&&-1===e._interestedResizables.indexOf(this)&&(e._interestedResizables.push(this),e._subscribeIronResize(this))},stopResizeNotificationsFor:function(e){var t=this._interestedResizables.indexOf(e);t>-1&&(this._interestedResizables.splice(t,1),this._unsubscribeIronResize(e))},_subscribeIronResize:function(e){e.addEventListener("iron-resize",this._boundOnDescendantIronResize)},_unsubscribeIronResize:function(e){e.removeEventListener("iron-resize",this._boundOnDescendantIronResize)},resizerShouldNotify:function(e){return!0},_onDescendantIronResize:function(e){this._notifyingDescendant?e.stopPropagation():s.my||this._fireResize()},_fireResize:function(){this.fire("iron-resize",null,{node:this,bubbles:!1})},_onIronRequestResizeNotifications:function(e){var t=(0,i.vz)(e).rootTarget;t!==this&&(t.assignParentResizable(this),this._notifyDescendant(t),e.stopPropagation())},_parentResizableChanged:function(e){e&&window.removeEventListener("resize",this._boundNotifyResize)},_notifyDescendant:function(e){this.isAttached&&(this._notifyingDescendant=!0,e.notifyResize(),this._notifyingDescendant=!1)},_requestResizeNotifications:function(){if(this.isAttached)if("loading"===document.readyState){var e=this._requestResizeNotifications.bind(this);document.addEventListener("readystatechange",(function t(){document.removeEventListener("readystatechange",t),e()}))}else this._findParent(),this._parentResizable?this._parentResizable._interestedResizables.forEach((function(e){e!==this&&e._findParent()}),this):(r.forEach((function(e){e!==this&&e._findParent()}),this),window.addEventListener("resize",this._boundNotifyResize),this.notifyResize())},_findParent:function(){this.assignParentResizable(null),this.fire("iron-request-resize-notifications",null,{node:this,bubbles:!0,cancelable:!0}),this._parentResizable?r.delete(this):r.add(this)}}},34709:function(e,t,n){"use strict";var i,s=n(23916),r=n(75009),o=n(9672),a=n(50856),d=n(65233);var c,h,u=null;(0,o.k)({_template:(0,a.d)(i||(c=['\n    <style>\n      :host {\n        display: block;\n        position: fixed;\n        background-color: var(--paper-toast-background-color, #323232);\n        color: var(--paper-toast-color, #f1f1f1);\n        min-height: 48px;\n        min-width: 288px;\n        padding: 16px 24px;\n        box-sizing: border-box;\n        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.26);\n        border-radius: 2px;\n        margin: 12px;\n        font-size: 14px;\n        cursor: default;\n        -webkit-transition: -webkit-transform 0.3s, opacity 0.3s;\n        transition: transform 0.3s, opacity 0.3s;\n        opacity: 0;\n        -webkit-transform: translateY(100px);\n        transform: translateY(100px);\n        @apply --paper-font-common-base;\n      }\n\n      :host(.capsule) {\n        border-radius: 24px;\n      }\n\n      :host(.fit-bottom) {\n        width: 100%;\n        min-width: 0;\n        border-radius: 0;\n        margin: 0;\n      }\n\n      :host(.paper-toast-open) {\n        opacity: 1;\n        -webkit-transform: translateY(0px);\n        transform: translateY(0px);\n      }\n    </style>\n\n    <span id="label">{{text}}</span>\n    <slot></slot>\n'],h||(h=c.slice(0)),i=Object.freeze(Object.defineProperties(c,{raw:{value:Object.freeze(h)}})))),is:"paper-toast",behaviors:[r.$],properties:{fitInto:{type:Object,value:window,observer:"_onFitIntoChanged"},horizontalAlign:{type:String,value:"left"},verticalAlign:{type:String,value:"bottom"},duration:{type:Number,value:3e3},text:{type:String,value:""},noCancelOnOutsideClick:{type:Boolean,value:!0},noAutoFocus:{type:Boolean,value:!0}},listeners:{transitionend:"__onTransitionEnd"},get visible(){return d.XY._warn("`visible` is deprecated, use `opened` instead"),this.opened},get _canAutoClose(){return this.duration>0&&this.duration!==1/0},created:function(){this._autoClose=null,s.N.requestAvailability()},show:function(e){for(var t in"string"==typeof e&&(e={text:e}),e)0===t.indexOf("_")?d.XY._warn('The property "'+t+'" is private and was not set.'):t in this?this[t]=e[t]:d.XY._warn('The property "'+t+'" is not valid.');this.open()},hide:function(){this.close()},__onTransitionEnd:function(e){e&&e.target===this&&"opacity"===e.propertyName&&(this.opened?this._finishRenderOpened():this._finishRenderClosed())},_openedChanged:function(){null!==this._autoClose&&(this.cancelAsync(this._autoClose),this._autoClose=null),this.opened?(u&&u!==this&&u.close(),u=this,this.fire("iron-announce",{text:this.text}),this._canAutoClose&&(this._autoClose=this.async(this.close,this.duration))):u===this&&(u=null),r.Q._openedChanged.apply(this,arguments)},_renderOpened:function(){this.classList.add("paper-toast-open")},_renderClosed:function(){this.classList.remove("paper-toast-open")},_onFitIntoChanged:function(e){this.positionTarget=e}})}}]);
//# sourceMappingURL=chunk.5a83d9a1e48f93ab4add.js.map