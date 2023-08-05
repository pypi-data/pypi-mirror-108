/*! For license information please see chunk.360dd71f056486030390.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6294],{6294:function(e,t,n){"use strict";var o,r=n(99525),i=n(55704),u=(n(62613),n(59799),{MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"}),c={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected"},a={FOCUS_ROOT_INDEX:-1};!function(e){e[e.NONE=0]="NONE",e[e.LIST_ROOT=1]="LIST_ROOT",e[e.FIRST_ITEM=2]="FIRST_ITEM",e[e.LAST_ITEM=3]="LAST_ITEM"}(o||(o={}));var s,l=n(87480),f=n(72774),d=n(74015),p=n(6945),m=function(e){function t(n){var r=e.call(this,(0,l.__assign)((0,l.__assign)({},t.defaultAdapter),n))||this;return r.closeAnimationEndTimerId=0,r.defaultFocusState=o.LIST_ROOT,r}return(0,l.__extends)(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return u},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return c},enumerable:!1,configurable:!0}),Object.defineProperty(t,"numbers",{get:function(){return a},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),t.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},t.prototype.handleKeydown=function(e){var t=e.key,n=e.keyCode;("Tab"===t||9===n)&&this.adapter.closeSurface(!0)},t.prototype.handleItemAction=function(e){var t=this,n=this.adapter.getElementIndex(e);n<0||(this.adapter.notifySelected({index:n}),this.adapter.closeSurface(),this.closeAnimationEndTimerId=setTimeout((function(){var n=t.adapter.getElementIndex(e);n>=0&&t.adapter.isSelectableItemAtIndex(n)&&t.setSelectedIndex(n)}),p.k.numbers.TRANSITION_CLOSE_DURATION))},t.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case o.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case o.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case o.NONE:break;default:this.adapter.focusListRoot()}},t.prototype.setDefaultFocusState=function(e){this.defaultFocusState=e},t.prototype.setSelectedIndex=function(e){if(this.validatedIndex(e),!this.adapter.isSelectableItemAtIndex(e))throw new Error("MDCMenuFoundation: No selection group at specified index.");var t=this.adapter.getSelectedSiblingOfItemAtIndex(e);t>=0&&(this.adapter.removeAttributeFromElementAtIndex(t,c.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(t,u.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(e,u.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(e,c.ARIA_CHECKED_ATTR,"true")},t.prototype.setEnabled=function(e,t){this.validatedIndex(e),t?(this.adapter.removeClassFromElementAtIndex(e,d.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(e,c.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(e,d.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(e,c.ARIA_DISABLED_ATTR,"true"))},t.prototype.validatedIndex=function(e){var t=this.adapter.getMenuItemCount();if(!(e>=0&&e<t))throw new Error("MDCMenuFoundation: No list item at specified index.")},t}(f.K),y=n(78220),h=n(14114);function v(e){return(v="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function b(e,t,n,o,r,i,u){try{var c=e[i](u),a=c.value}catch(s){return void n(s)}c.done?t(a):Promise.resolve(a).then(o,r)}function E(e){return function(){var t=this,n=arguments;return new Promise((function(o,r){var i=e.apply(t,n);function u(e){b(i,o,r,u,c,"next",e)}function c(e){b(i,o,r,u,c,"throw",e)}u(void 0)}))}}function I(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function g(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function _(e,t,n){return(_="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=T(e)););return e}(e,t);if(o){var r=Object.getOwnPropertyDescriptor(o,t);return r.get?r.get.call(n):r.value}})(e,t,n||e)}function S(e,t){return(S=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function A(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=T(e);if(t){var r=T(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return C(this,n)}}function C(e,t){return!t||"object"!==v(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function T(e){return(T=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var O,x=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&S(e,t)}(l,e);var t,n,o,r,u,c,a=A(l);function l(){var e;return I(this,l),(e=a.apply(this,arguments)).mdcFoundationClass=m,e.listElement_=null,e.anchor=null,e.open=!1,e.quick=!1,e.wrapFocus=!1,e.innerRole="menu",e.corner="TOP_START",e.x=null,e.y=null,e.absolute=!1,e.multi=!1,e.activatable=!1,e.fixed=!1,e.forceGroupSelection=!1,e.fullwidth=!1,e.menuCorner="START",e.stayOpenOnBodyClick=!1,e.defaultFocus="LIST_ROOT",e._listUpdateComplete=null,e}return t=l,(n=[{key:"listElement",get:function(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}},{key:"items",get:function(){var e=this.listElement;return e?e.items:[]}},{key:"index",get:function(){var e=this.listElement;return e?e.index:-1}},{key:"selected",get:function(){var e=this.listElement;return e?e.selected:null}},{key:"render",value:function(){var e="menu"===this.innerRole?"menuitem":"option";return(0,i.dy)(s||(s=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["\n      <mwc-menu-surface\n          ?hidden=","\n          .anchor=","\n          .open=","\n          .quick=","\n          .corner=","\n          .x=","\n          .y=","\n          .absolute=","\n          .fixed=","\n          .fullwidth=","\n          .menuCorner=","\n          ?stayOpenOnBodyClick=",'\n          class="mdc-menu mdc-menu-surface"\n          @closed=',"\n          @opened=","\n          @keydown=",">\n        <mwc-list\n          rootTabbable\n          .innerRole=","\n          .multi=",'\n          class="mdc-deprecated-list"\n          .itemRoles=',"\n          .wrapFocus=","\n          .activatable=","\n          @action=",">\n        <slot></slot>\n      </mwc-list>\n    </mwc-menu-surface>"])),!this.open,this.anchor,this.open,this.quick,this.corner,this.x,this.y,this.absolute,this.fixed,this.fullwidth,this.menuCorner,this.stayOpenOnBodyClick,this.onClosed,this.onOpened,this.onKeydown,this.innerRole,this.multi,e,this.wrapFocus,this.activatable,this.onAction)}},{key:"createAdapter",value:function(){var e=this;return{addClassToElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&("mdc-menu-item--selected"===n?e.forceGroupSelection&&!r.selected&&o.toggle(t,!0):r.classList.add(n))}},removeClassFromElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&("mdc-menu-item--selected"===n?r.selected&&o.toggle(t,!1):r.classList.remove(n))}},addAttributeToElementAtIndex:function(t,n,o){var r=e.listElement;if(r){var i=r.items[t];i&&i.setAttribute(n,o)}},removeAttributeFromElementAtIndex:function(t,n){var o=e.listElement;if(o){var r=o.items[t];r&&r.removeAttribute(n)}},elementContainsClass:function(e,t){return e.classList.contains(t)},closeSurface:function(){e.open=!1},getElementIndex:function(t){var n=e.listElement;return n?n.items.indexOf(t):-1},notifySelected:function(){},getMenuItemCount:function(){var t=e.listElement;return t?t.items.length:0},focusItemAtIndex:function(t){var n=e.listElement;if(n){var o=n.items[t];o&&o.focus()}},focusListRoot:function(){e.listElement&&e.listElement.focus()},getSelectedSiblingOfItemAtIndex:function(t){var n=e.listElement;if(!n)return-1;var o=n.items[t];if(!o||!o.group)return-1;for(var r=0;r<n.items.length;r++)if(r!==t){var i=n.items[r];if(i.selected&&i.group===o.group)return r}return-1},isSelectableItemAtIndex:function(t){var n=e.listElement;if(!n)return!1;var o=n.items[t];return!!o&&o.hasAttribute("group")}}}},{key:"onKeydown",value:function(e){this.mdcFoundation&&this.mdcFoundation.handleKeydown(e)}},{key:"onAction",value:function(e){var t=this.listElement;if(this.mdcFoundation&&t){var n=e.detail.index,o=t.items[n];o&&this.mdcFoundation.handleItemAction(o)}}},{key:"onOpened",value:function(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}},{key:"onClosed",value:function(){this.open=!1}},{key:"_getUpdateComplete",value:(c=E(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",this.getUpdateComplete());case 1:case"end":return e.stop()}}),e,this)}))),function(){return c.apply(this,arguments)})},{key:"getUpdateComplete",value:(u=E(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t=!1,e.next=3,this._listUpdateComplete;case 3:if(!_(T(l.prototype),"getUpdateComplete",this)){e.next=9;break}return e.next=6,_(T(l.prototype),"getUpdateComplete",this).call(this);case 6:t=e.sent,e.next=11;break;case 9:return e.next=11,_(T(l.prototype),"_getUpdateComplete",this).call(this);case 11:return e.abrupt("return",t);case 12:case"end":return e.stop()}}),e,this)}))),function(){return u.apply(this,arguments)})},{key:"firstUpdated",value:(r=E(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(_(T(l.prototype),"firstUpdated",this).call(this),!(t=this.listElement)){e.next=6;break}return this._listUpdateComplete=t.updateComplete,e.next=6,this._listUpdateComplete;case 6:case"end":return e.stop()}}),e,this)}))),function(){return r.apply(this,arguments)})},{key:"select",value:function(e){var t=this.listElement;t&&t.select(e)}},{key:"close",value:function(){this.open=!1}},{key:"show",value:function(){this.open=!0}},{key:"getFocusedItemIndex",value:function(){var e=this.listElement;return e?e.getFocusedItemIndex():-1}},{key:"focusItemAtIndex",value:function(e){var t=this.listElement;t&&t.focusItemAtIndex(e)}},{key:"layout",value:function(){var e=!(arguments.length>0&&void 0!==arguments[0])||arguments[0],t=this.listElement;t&&t.layout(e)}}])&&g(t.prototype,n),o&&g(t,o),l}(y.H);(0,r.gn)([(0,i.IO)(".mdc-menu")],x.prototype,"mdcRoot",void 0),(0,r.gn)([(0,i.IO)("slot")],x.prototype,"slotElement",void 0),(0,r.gn)([(0,i.Cb)({type:Object})],x.prototype,"anchor",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean,reflect:!0})],x.prototype,"open",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"quick",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"wrapFocus",void 0),(0,r.gn)([(0,i.Cb)({type:String})],x.prototype,"innerRole",void 0),(0,r.gn)([(0,i.Cb)({type:String})],x.prototype,"corner",void 0),(0,r.gn)([(0,i.Cb)({type:Number})],x.prototype,"x",void 0),(0,r.gn)([(0,i.Cb)({type:Number})],x.prototype,"y",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"absolute",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"multi",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"activatable",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"fixed",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"forceGroupSelection",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"fullwidth",void 0),(0,r.gn)([(0,i.Cb)({type:String})],x.prototype,"menuCorner",void 0),(0,r.gn)([(0,i.Cb)({type:Boolean})],x.prototype,"stayOpenOnBodyClick",void 0),(0,r.gn)([(0,i.Cb)({type:String}),(0,h.P)((function(e){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(o[e])}))],x.prototype,"defaultFocus",void 0);var R=(0,i.iv)(O||(O=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["mwc-list ::slotted([mwc-list-item]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}"])));function w(e){return(w="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function k(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function F(e,t){return(F=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function L(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=j(e);if(t){var r=j(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return M(this,n)}}function M(e,t){return!t||"object"!==w(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function j(e){return(j=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var D=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&F(e,t)}(n,e);var t=L(n);function n(){return k(this,n),t.apply(this,arguments)}return n}(x);D.styles=R,D=(0,r.gn)([(0,i.Mo)("mwc-menu")],D)}}]);
//# sourceMappingURL=chunk.360dd71f056486030390.js.map