(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4933],{68928:(e,t,r)=>{"use strict";r.d(t,{WU:()=>D});var n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,o="[1-9]\\d?",i="\\d\\d",a="[^\\s]+",s=/\[([^]*?)\]/gm;function c(e,t){for(var r=[],n=0,o=e.length;n<o;n++)r.push(e[n].substr(0,t));return r}var l=function(e){return function(t,r){var n=r[e].map((function(e){return e.toLowerCase()})).indexOf(t.toLowerCase());return n>-1?n:null}};function d(e){for(var t=[],r=1;r<arguments.length;r++)t[r-1]=arguments[r];for(var n=0,o=t;n<o.length;n++){var i=o[n];for(var a in i)e[a]=i[a]}return e}var u=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],f=["January","February","March","April","May","June","July","August","September","October","November","December"],p=c(f,3),m={dayNamesShort:c(u,3),dayNames:u,monthNamesShort:p,monthNames:f,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10?1:0)*e%10]}},h=d({},m),g=function(e,t){for(void 0===t&&(t=2),e=String(e);e.length<t;)e="0"+e;return e},y={D:function(e){return String(e.getDate())},DD:function(e){return g(e.getDate())},Do:function(e,t){return t.DoFn(e.getDate())},d:function(e){return String(e.getDay())},dd:function(e){return g(e.getDay())},ddd:function(e,t){return t.dayNamesShort[e.getDay()]},dddd:function(e,t){return t.dayNames[e.getDay()]},M:function(e){return String(e.getMonth()+1)},MM:function(e){return g(e.getMonth()+1)},MMM:function(e,t){return t.monthNamesShort[e.getMonth()]},MMMM:function(e,t){return t.monthNames[e.getMonth()]},YY:function(e){return g(String(e.getFullYear()),4).substr(2)},YYYY:function(e){return g(e.getFullYear(),4)},h:function(e){return String(e.getHours()%12||12)},hh:function(e){return g(e.getHours()%12||12)},H:function(e){return String(e.getHours())},HH:function(e){return g(e.getHours())},m:function(e){return String(e.getMinutes())},mm:function(e){return g(e.getMinutes())},s:function(e){return String(e.getSeconds())},ss:function(e){return g(e.getSeconds())},S:function(e){return String(Math.round(e.getMilliseconds()/100))},SS:function(e){return g(Math.round(e.getMilliseconds()/10),2)},SSS:function(e){return g(e.getMilliseconds(),3)},a:function(e,t){return e.getHours()<12?t.amPm[0]:t.amPm[1]},A:function(e,t){return e.getHours()<12?t.amPm[0].toUpperCase():t.amPm[1].toUpperCase()},ZZ:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+g(100*Math.floor(Math.abs(t)/60)+Math.abs(t)%60,4)},Z:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+g(Math.floor(Math.abs(t)/60),2)+":"+g(Math.abs(t)%60,2)}},w=function(e){return+e-1},v=[null,o],b=[null,a],k=["isPm",a,function(e,t){var r=e.toLowerCase();return r===t.amPm[0]?0:r===t.amPm[1]?1:null}],_=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(e){var t=(e+"").match(/([+-]|\d\d)/gi);if(t){var r=60*+t[1]+parseInt(t[2],10);return"+"===t[0]?r:-r}return 0}],S=(l("monthNamesShort"),l("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),D=function(e,t,r){if(void 0===t&&(t=S.default),void 0===r&&(r={}),"number"==typeof e&&(e=new Date(e)),"[object Date]"!==Object.prototype.toString.call(e)||isNaN(e.getTime()))throw new Error("Invalid Date pass to format");var o=[];t=(t=S[t]||t).replace(s,(function(e,t){return o.push(t),"@@@"}));var i=d(d({},h),r);return(t=t.replace(n,(function(t){return y[t](e,i)}))).replace(/@@@/g,(function(){return o.shift()}))}},43274:(e,t,r)=>{"use strict";r.d(t,{Sb:()=>n,BF:()=>o,Op:()=>i});const n=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),o=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),i=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},44583:(e,t,r)=>{"use strict";r.d(t,{o:()=>c,E:()=>d});var n=r(68928),o=r(14516),i=r(43274),a=r(65810);const s=(0,o.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)}))),c=i.Op?(e,t)=>s(t).format(e):(e,t)=>(0,n.WU)(e,((0,a.y)(t)," A")),l=(0,o.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(e)}))),d=i.Op?(e,t)=>l(t).format(e):(e,t)=>(0,n.WU)(e,((0,a.y)(t)," A"))},49684:(e,t,r)=>{"use strict";r.d(t,{mr:()=>c,Vu:()=>d,xO:()=>f});var n=r(68928),o=r(14516),i=r(43274),a=r(65810);const s=(0,o.Z)((e=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)}))),c=i.BF?(e,t)=>s(t).format(e):(e,t)=>(0,n.WU)(e,((0,a.y)(t)," A")),l=(0,o.Z)((e=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(e)}))),d=i.BF?(e,t)=>l(t).format(e):(e,t)=>(0,n.WU)(e,((0,a.y)(t)," A")),u=(0,o.Z)((e=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)}))),f=i.BF?(e,t)=>u(t).format(e):(e,t)=>(0,n.WU)(e,((0,a.y)(t)," A"))},65810:(e,t,r)=>{"use strict";r.d(t,{y:()=>o});var n=r(66477);const o=e=>{if(e.time_format===n.zt.language||e.time_format===n.zt.system){const t=e.time_format===n.zt.language?e.language:void 0,r=(new Date).toLocaleString(t);return r.includes("AM")||r.includes("PM")}return e.time_format===n.zt.am_pm}},84627:(e,t,r)=>{"use strict";r.d(t,{T:()=>o});const n=/^(\w+)\.(\w+)$/,o=e=>n.test(e)},85415:(e,t,r)=>{"use strict";r.d(t,{q:()=>n,w:()=>o});const n=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>n(e.toLowerCase(),t.toLowerCase())},10983:(e,t,r)=>{"use strict";r(25230);var n=r(50424),o=r(55358);r(16509);function i(){i=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var o=t.placement;if(t.kind===n&&("static"===o||"prototype"===o)){var i="static"===o?e:r;this.defineClassElement(i,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var i=this.decorateConstructor(r,t);return n.push.apply(n,i.finishers),i.finishers=n,i},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],o=e.decorators,i=o.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[i])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var o=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[n])(o)||o);if(void 0!==i.finisher&&r.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:r,placement:n,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var o=i();if(n)for(var d=0;d<n.length;d++)o=n[d](o);var u=t((function(e){o.initializeInstanceElements(e,f.elements)}),r),f=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},n=0;n<e.length;n++){var o,i=e[n];if("method"===i.kind&&(o=t.find(r)))if(l(i.descriptor)||l(o.descriptor)){if(c(i)||c(o))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");o.descriptor=i.descriptor}else{if(c(i)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");o.decorators=i.decorators}s(i,o)}else t.push(i)}return t}(u.d.map(a)),e);o.initializeClassElements(u.F,f.elements),o.runClassFinishers(u.F,f.finishers)}([(0,o.Mo)("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"icon",value:()=>""},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"label",value:()=>""},{kind:"field",static:!0,key:"shadowRootOptions",value:()=>({mode:"open",delegatesFocus:!0})},{kind:"method",key:"render",value:function(){return n.dy`
      <mwc-icon-button .label=${this.label} .disabled=${this.disabled}>
        <ha-icon .icon=${this.icon}></ha-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),n.oi)},73728:(e,t,r)=>{"use strict";r.d(t,{pV:()=>a,P3:()=>s,Ky:()=>l,D4:()=>d,XO:()=>u,zO:()=>f,oi:()=>p,d4:()=>m,D7:()=>h,ZJ:()=>y,V3:()=>w,WW:()=>v});var n=r(95282),o=r(38346),i=r(5986);const a=["unignore","dhcp","homekit","ssdp","zeroconf","discovery","mqtt","hassio"],s=["reauth"],c={"HA-Frontend-Base":`${location.protocol}//${location.host}`},l=(e,t)=>{var r;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(r=e.userData)||void 0===r?void 0:r.showAdvanced)},c)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,c),u=(e,t,r)=>e.callApi("POST",`config/config_entries/flow/${t}`,r,c),f=(e,t,r)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:r}),p=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),m=e=>e.callApi("GET","config/config_entries/flow_handlers"),h=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),g=(e,t)=>e.subscribeEvents((0,o.D)((()=>h(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),y=e=>(0,n._)(e,"_configFlowProgress",h,g),w=(e,t)=>y(e.connection).subscribe(t),v=(e,t)=>{const r=t.context.title_placeholders||{},n=Object.keys(r);if(0===n.length)return(0,i.Lh)(e,t.handler);const o=[];return n.forEach((e=>{o.push(e),o.push(r[e])})),e(`component.${t.handler}.config.flow_title`,...o)}},2852:(e,t,r)=>{"use strict";r.d(t,{t:()=>c});var n=r(50424),o=r(85415),i=r(73728),a=r(5986),s=r(52871);const c=(e,t)=>(0,s.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,i.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,r)=>(0,o.w)((0,a.Lh)(e.localize,t),(0,a.Lh)(e.localize,r))))},createFlow:async(e,t)=>{const[r]=await Promise.all([(0,i.Ky)(e,t),e.loadBackendTranslation("config",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,i.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),r},handleFlowStep:i.XO,deleteFlow:i.oi,renderAbortDescription(e,t){const r=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${r.name}`),renderShowFormStepFieldError:(e,t,r)=>e.localize(`component.${t.handler}.config.error.${r}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return n.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const r=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return n.dy`
        ${r?n.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const r=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return r?n.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""}})},52871:(e,t,r)=>{"use strict";r.d(t,{w:()=>i});var n=r(47181);const o=()=>Promise.all([r.e(5009),r.e(8161),r.e(2955),r.e(8200),r.e(879),r.e(3967),r.e(1041),r.e(1657),r.e(5829),r.e(1480),r.e(7024),r.e(2374),r.e(6509),r.e(8331),r.e(8101),r.e(4940),r.e(91),r.e(423)]).then(r.bind(r,27234)),i=(e,t,r)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:o,dialogParams:{...t,flowConfig:r}})}},86334:(e,t,r)=>{"use strict";r.r(t);r(53268),r(12730);var n=r(50856),o=r(28426),i=(r(60010),r(38353),r(63081),r(2852)),a=r(47181),s=(r(44608),r(90271));class c extends o.H3{static get template(){return n.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button on-click="showLocalIpInfo"
                      >[[aisLocalHostName]]</mwc-button
                    ><ha-icon-button
                      class="user-button"
                      icon="hass:cog"
                      on-click="createFlowHostName"
                    ></ha-icon-button>
                  </div>
                </div>
                <div on-click="showLocalIpInfo" style="text-align: center;">
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisLocalIP]]</mwc-button>
                  </div>
                </div>
                <div on-click="showWiFiSpeedInfo" style="text-align: center;">
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisWiFiSpeed]]</mwc-button>
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    on-click="showWiFiGroup"
                  ></ha-icon-button
                  ><mwc-button on-click="createFlowWifi"
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,aisLocalHostName:{type:String,computed:"_computeAisLocalHostName(hass)"},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},aisWiFiSpeed:{type:String,computed:"_computeAisWiFiSpeed(hass)"},_config:Object,_names:Object,_entities:Array,_cacheConfig:Object}}computeClasses(e){return e?"content":"content narrow"}_computeAisLocalHostName(e){return e.states["sensor.local_host_name"].state}_computeAisLocalIP(e){return e.states["sensor.internal_ip_address"].state}_computeAisWiFiSpeed(e){return e.states["sensor.ais_wifi_service_current_network_info"].state}showWiFiGroup(){(0,a.B)(this,"hass-more-info",{entityId:"group.internet_status"})}showWiFiSpeedInfo(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}showLocalIpInfo(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}_continueFlow(e){(0,i.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}createFlowHostName(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}createFlowWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}ready(){super.ready();const e=(0,s.A)(["sensor.ais_wifi_service_current_network_info"]),t=[],r={};for(const n of e)t.push(n.entity),n.name&&(r[n.entity]=n.name);this.setProperties({_cacheConfig:{cacheKey:t.join(),hoursToShow:24,refresh:0},_entities:t,_names:r})}}customElements.define("ha-config-ais-dom-config-wifi",c)},90271:(e,t,r)=>{"use strict";r.d(t,{A:()=>o});var n=r(84627);const o=e=>{if(!e||!Array.isArray(e))throw new Error("Entities need to be an array");return e.map(((e,t)=>{if("object"==typeof e&&!Array.isArray(e)&&e.type)return e;let r;if("string"==typeof e)r={entity:e};else{if("object"!=typeof e||Array.isArray(e))throw new Error(`Invalid entity specified at position ${t}.`);if(!("entity"in e))throw new Error(`Entity object at position ${t} is missing entity field.`);r=e}if(!(0,n.T)(r.entity))throw new Error(`Invalid entity ID at position ${t}: ${r.entity}`);return r}))}}}]);
//# sourceMappingURL=chunk.54324335a8c65f08071e.js.map