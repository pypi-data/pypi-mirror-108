(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6184],{349:(e,t,r)=>{"use strict";function i(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}r.d(t,{m:()=>o});const n=new class{constructor(){i(this,"_storage",{}),i(this,"_listeners",{}),window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const r=this._listeners[e].indexOf(t);-1!==r&&this._listeners[e].splice(r,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(e){}}},o=(e,t,r)=>i=>{const o=String(i.key);e=e||String(i.key);const a=i.initializer?i.initializer():void 0;n.addFromStorage(e);const s=()=>n.hasKey(e)?n.getValue(e):a;return{kind:"method",placement:"prototype",key:i.key,descriptor:{set(r){((r,o)=>{let a;t&&(a=s()),n.setValue(e,o),t&&r.requestUpdate(i.key,a)})(this,r)},get:()=>s(),enumerable:!0,configurable:!0},finisher(a){if(t){const t=a.prototype.connectedCallback,s=a.prototype.disconnectedCallback;a.prototype.connectedCallback=function(){var r;t.call(this),this[`__unbsubLocalStorage${o}`]=(r=this,n.subscribeChanges(e,(e=>{r.requestUpdate(i.key,e)})))},a.prototype.disconnectedCallback=function(){s.call(this),this[`__unbsubLocalStorage${o}`]()},a.createProperty(i.key,{noAccessor:!0,...r})}}}}},27269:(e,t,r)=>{"use strict";r.d(t,{p:()=>i});const i=e=>e.substr(e.indexOf(".")+1)},22311:(e,t,r)=>{"use strict";r.d(t,{N:()=>n});var i=r(58831);const n=e=>(0,i.M)(e.entity_id)},91741:(e,t,r)=>{"use strict";r.d(t,{C:()=>n});var i=r(27269);const n=e=>void 0===e.attributes.friendly_name?(0,i.p)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},40095:(e,t,r)=>{"use strict";r.d(t,{e:()=>i});const i=(e,t)=>0!=(e.attributes.supported_features&t)},34821:(e,t,r)=>{"use strict";r.d(t,{i:()=>v});var i=r(13967),n=r(55317),o=r(50424),a=r(55358),s=r(87744);r(10983);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function y(e,t,r){return(y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const v=(e,t)=>o.dy`
  <span class="header_title">${t}</span>
  <mwc-icon-button
    aria-label=${e.localize("ui.dialogs.generic.close")}
    dialogAction="close"
    class="header_button"
    dir=${(0,s.Zu)(e)}
  >
    <ha-svg-icon .path=${n.r5M}></ha-svg-icon>
  </mwc-icon-button>
`;!function(e,t,r,i){var n=l();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(u(o.descriptor)||u(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(a.d.map(c)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,a.Mo)("ha-dialog")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return o.dy`<slot name="heading"> ${y(g(r.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"get",static:!0,key:"styles",value:function(){return[i.V.styles,o.iv`
        .mdc-dialog {
          --mdc-dialog-scroll-divider-color: var(--divider-color);
          z-index: var(--dialog-z-index, 7);
          backdrop-filter: var(--dialog-backdrop-filter, none);
        }
        .mdc-dialog__actions {
          justify-content: var(--justify-action-buttons, flex-end);
          padding-bottom: max(env(safe-area-inset-bottom), 8px);
        }
        .mdc-dialog__container {
          align-items: var(--vertial-align-dialog, center);
        }
        .mdc-dialog__title::before {
          display: block;
          height: 20px;
        }
        .mdc-dialog .mdc-dialog__content {
          position: var(--dialog-content-position, relative);
          padding: var(--dialog-content-padding, 20px 24px);
        }
        :host([hideactions]) .mdc-dialog .mdc-dialog__content {
          padding-bottom: max(
            var(--dialog-content-padding, 20px),
            env(safe-area-inset-bottom)
          );
        }
        .mdc-dialog .mdc-dialog__surface {
          position: var(--dialog-surface-position, relative);
          top: var(--dialog-surface-top);
          min-height: var(--mdc-dialog-min-height, auto);
        }
        :host([flexContent]) .mdc-dialog .mdc-dialog__content {
          display: flex;
          flex-direction: column;
        }
        .header_button {
          position: absolute;
          right: 16px;
          top: 10px;
          text-decoration: none;
          color: inherit;
        }
        .header_title {
          margin-right: 40px;
        }
        [dir="rtl"].header_button {
          right: auto;
          left: 16px;
        }
        [dir="rtl"].header_title {
          margin-left: 40px;
          margin-right: 0px;
        }
      `]}}]}}),i.V)},81303:(e,t,r)=>{"use strict";r(8878);const i=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends i{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},56007:(e,t,r)=>{"use strict";r.d(t,{nZ:()=>i,lz:()=>n,V_:()=>o});const i="unavailable",n="unknown",o=[i,n]},69371:(e,t,r)=>{"use strict";r.d(t,{MU:()=>a,xh:()=>s,X6:()=>l,y:()=>c,Y3:()=>d,Bp:()=>p,rv:()=>u,VJ:()=>f,WE:()=>h,B6:()=>m,Hy:()=>y,VH:()=>g,S6:()=>v,Dh:()=>b,pu:()=>w,N8:()=>k,Fn:()=>_,zz:()=>E,b:()=>x,rs:()=>P,Mj:()=>S,xt:()=>D});var i=r(55317),n=r(40095),o=r(56007);const a=1,s=2,l=4,c=8,d=16,p=32,u=128,f=256,h=512,m=1024,y=2048,g=4096,v=16384,b=65536,w=131072,k="browser",_={album:{icon:i.eBO,layout:"grid"},app:{icon:i.Kpn,layout:"grid"},artist:{icon:i.HwD,layout:"grid",show_list_images:!0},channel:{icon:i.nTs,thumbnail_ratio:"portrait",layout:"grid"},composer:{icon:i.vmK,layout:"grid",show_list_images:!0},contributing_artist:{icon:i.HwD,layout:"grid",show_list_images:!0},directory:{icon:i.in3,layout:"grid",show_list_images:!0},episode:{icon:i.nTs,layout:"grid",thumbnail_ratio:"portrait"},game:{icon:i.qK8,layout:"grid",thumbnail_ratio:"portrait"},genre:{icon:i.vXW,layout:"grid",show_list_images:!0},image:{icon:i.TaT,layout:"grid"},movie:{icon:i.l1p,thumbnail_ratio:"portrait",layout:"grid"},music:{icon:i.MxT},playlist:{icon:i.MxF,layout:"grid",show_list_images:!0},podcast:{icon:i.wu9,layout:"grid"},season:{icon:i.nTs,layout:"grid",thumbnail_ratio:"portrait"},track:{icon:i.ZH0},tv_show:{icon:i.nTs,layout:"grid",thumbnail_ratio:"portrait"},url:{icon:i.m5Y},video:{icon:i.Jhp,layout:"grid"}},E=(e,t,r,i)=>e.callWS({type:"media_player/browse_media",entity_id:t,media_content_id:r,media_content_type:i}),x=(e,t)=>e.callWS({type:"media_source/browse_media",media_content_id:t}),P=e=>{let t=e.attributes.media_position;return"playing"!==e.state||(t+=(Date.now()-new Date(e.attributes.media_position_updated_at).getTime())/1e3),t},S=e=>{let t;switch(e.attributes.media_content_type){case"music":case"image":t=e.attributes.media_artist;break;case"playlist":t=e.attributes.media_playlist;break;case"tvshow":t=e.attributes.media_series_title,e.attributes.media_season&&(t+=" S"+e.attributes.media_season,e.attributes.media_episode&&(t+="E"+e.attributes.media_episode));break;default:t=e.attributes.app_name||""}return t},D=e=>{if(!e)return;const t=e.state;if(o.V_.includes(t))return;if("off"===t)return(0,n.e)(e,u)?[{icon:"hass:power",action:"turn_on"}]:void 0;const r=[];return(0,n.e)(e,f)&&r.push({icon:"hass:power",action:"turn_off"}),"playing"!==t&&"paused"!==t||!(0,n.e)(e,d)||r.push({icon:"hass:skip-previous",action:"media_previous_track"}),("playing"===t&&((0,n.e)(e,a)||(0,n.e)(e,g))||("paused"===t||"idle"===t)&&(0,n.e)(e,v)||"on"===t&&((0,n.e)(e,v)||(0,n.e)(e,a)))&&r.push({icon:"on"===t?"hass:play-pause":"playing"!==t?"hass:play":(0,n.e)(e,a)?"hass:pause":"hass:stop",action:"playing"!==t?"media_play":(0,n.e)(e,a)?"media_pause":"media_stop"}),"playing"!==t&&"paused"!==t||!(0,n.e)(e,p)||r.push({icon:"hass:skip-next",action:"media_next_track"}),r.length>0?r:void 0}},86184:(e,t,r)=>{"use strict";r.r(t),r.d(t,{DialogTryTts:()=>E});r(53918);var i=r(55317),n=(r(25856),r(53973),r(51095),r(50424)),o=r(55358),a=r(349),s=r(47181),l=r(22311),c=r(91741),d=r(40095),p=r(34821),u=(r(81303),r(69371));var f=r(26765),h=r(11654);function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!v(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=k(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function y(e){var t,r=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function g(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let E=function(e,t,r,i){var n=m();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(b(o.descriptor)||b(n.descriptor)){if(v(o)||v(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(v(o)){if(v(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}g(o,n)}else t.push(o)}return t}(a.d.map(y)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("dialog-cloud-try-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_loadingExample",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.IO)("#target")],key:"_targetInput",value:void 0},{kind:"field",decorators:[(0,o.IO)("#message")],key:"_messageInput",value:void 0},{kind:"field",decorators:[(0,a.m)("cloudTtsTryMessage")],key:"_message",value:void 0},{kind:"field",decorators:[(0,a.m)("cloudTtsTryTarget")],key:"_target",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?n.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${(0,p.i)(this.hass,this.hass.localize("ui.panel.config.cloud.account.tts.dialog.header"))}
      >
        <div>
          <paper-textarea
            id="message"
            label="Message"
            .value=${this._message||this.hass.localize("ui.panel.config.cloud.account.tts.dialog.example_message","name",this.hass.user.name)}
          >
          </paper-textarea>

          <ha-paper-dropdown-menu
            .label=${this.hass.localize("ui.panel.config.cloud.account.tts.dialog.target")}
          >
            <paper-listbox
              id="target"
              slot="dropdown-content"
              attr-for-selected="item-value"
              .selected=${this._target||"browser"}
            >
              <paper-item item-value="browser">
                ${this.hass.localize("ui.panel.config.cloud.account.tts.dialog.target_browser")}
              </paper-item>
              ${Object.values(this.hass.states).filter((e=>"media_player"===(0,l.N)(e)&&(0,d.e)(e,u.WE))).map((e=>n.dy`
                    <paper-item .itemValue=${e.entity_id}>
                      ${(0,c.C)(e)}
                    </paper-item>
                  `))}
            </paper-listbox>
          </ha-paper-dropdown-menu>
        </div>
        <mwc-button
          slot="primaryAction"
          @click=${this._playExample}
          .disabled=${this._loadingExample}
        >
          <ha-svg-icon .path=${i.g3n}></ha-svg-icon>
          &nbsp;${this.hass.localize("ui.panel.config.cloud.account.tts.dialog.play")}
        </mwc-button>
      </ha-dialog>
    `:n.dy``}},{kind:"method",key:"_playExample",value:async function(){var e,t;const r=String(null===(e=this._targetInput)||void 0===e?void 0:e.selected),i=null===(t=this._messageInput)||void 0===t?void 0:t.value;if(i&&r)if(this._message=i,this._target=r,"browser"===r){const e=new Audio;e.play(),this._playBrowser(i,e)}else this.hass.callService("tts","cloud_say",{entity_id:r,message:i})}},{kind:"method",key:"_playBrowser",value:async function(e,t){this._loadingExample=!0;const r=this._params.defaultVoice[0],i=this._params.defaultVoice[1];let n;try{n=(await(o=this.hass,a={platform:"cloud",message:e,language:r,options:{gender:i}},o.callApi("POST","tts_get_url",a))).path}catch(e){return this._loadingExample=!1,void(0,f.Ys)(this,{text:`Unable to load example. ${e.error||e.body||e}`,warning:!0})}var o,a;t.src=n,t.addEventListener("canplaythrough",(()=>{t.play()})),t.addEventListener("playing",(()=>{this._loadingExample=!1})),t.addEventListener("error",(()=>{(0,f.Ys)(this,{title:"Error playing audio."}),this._loadingExample=!1}))}},{kind:"get",static:!0,key:"styles",value:function(){return[h.yu,n.iv`
        ha-dialog {
          --mdc-dialog-max-width: 500px;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.7c34d55a380836a49457.js.map