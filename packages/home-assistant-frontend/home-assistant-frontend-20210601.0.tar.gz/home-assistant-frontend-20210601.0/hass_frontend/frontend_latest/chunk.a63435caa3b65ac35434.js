(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7873],{95282:(e,t,r)=>{"use strict";r.d(t,{_:()=>i,B:()=>o});var n=r(12902);const i=(e,t,r,i)=>{if(e[t])return e[t];let o,s=0,a=(0,n.M)();const c=()=>r(e).then((e=>a.setState(e,!0))),l=()=>c().catch((t=>{if(e.connected)throw t}));return e[t]={get state(){return a.state},refresh:c,subscribe(t){s++,1===s&&(i&&(o=i(e,a)),e.addEventListener("ready",l),l());const r=a.subscribe(t);return void 0!==a.state&&setTimeout((()=>t(a.state)),0),()=>{r(),s--,s||(o&&o.then((e=>{e()})),e.removeEventListener("ready",c))}}},e[t]},o=(e,t,r,n,o)=>i(n,e,t,r).subscribe(o)},23553:(e,t,r)=>{"use strict";r.d(t,{Pz:()=>i,U2:()=>o,iE:()=>s,PR:()=>a,_D:()=>c});var n=r(36007);const i=e=>e.sendMessagePromise(n.$q()),o=e=>e.sendMessagePromise(n.uZ()),s=e=>e.sendMessagePromise(n.vc()),a=e=>e.sendMessagePromise(n.EA()),c=(e,t,r,i,o)=>e.sendMessagePromise(n._D(t,r,i,o))},4915:(e,t,r)=>{"use strict";r.d(t,{wQ:()=>c,UE:()=>l,dL:()=>u,u5:()=>d});var n=r(95282),i=r(23553);function o(e,t){return void 0===e?null:{components:e.components.concat(t.data.component)}}const s=e=>(0,i.iE)(e),a=(e,t)=>Promise.all([e.subscribeEvents(t.action(o),"component_loaded"),e.subscribeEvents((()=>s(e).then((e=>t.setState(e,!0)))),"core_config_updated")]).then((e=>()=>e.forEach((e=>e())))),c=(e,t)=>(e=>(0,n._)(e,"_cnf",s,a))(e).subscribe(t),l="NOT_RUNNING",u="STARTING",d="RUNNING"},36007:(e,t,r)=>{"use strict";function n(e){return{type:"auth",access_token:e}}function i(){return{type:"get_states"}}function o(){return{type:"get_config"}}function s(){return{type:"get_services"}}function a(){return{type:"auth/current_user"}}function c(e,t,r,n){const i={type:"call_service",domain:e,service:t,target:n};return r&&(i.service_data=r),i}function l(e){const t={type:"subscribe_events"};return e&&(t.event_type=e),t}function u(e){return{type:"unsubscribe_events",subscription:e}}function d(){return{type:"ping"}}function f(e,t){return{type:"result",success:!1,error:{code:e,message:t}}}r.d(t,{I8:()=>n,$q:()=>i,vc:()=>o,uZ:()=>s,EA:()=>a,_D:()=>c,a:()=>l,Mt:()=>u,qE:()=>d,vU:()=>f})},12902:(e,t,r)=>{"use strict";r.d(t,{M:()=>n});const n=e=>{let t=[];function r(r,n){e=n?r:Object.assign(Object.assign({},e),r);let i=t;for(let t=0;t<i.length;t++)i[t](e)}return{get state(){return e},action(t){function n(e){r(e,!1)}return function(){let r=[e];for(let e=0;e<arguments.length;e++)r.push(arguments[e]);let i=t.apply(this,r);if(null!=i)return i instanceof Promise?i.then(n):n(i)}},setState:r,subscribe:e=>(t.push(e),()=>{!function(e){let r=[];for(let n=0;n<t.length;n++)t[n]===e?e=null:r.push(t[n]);t=r}(e)})}}},47873:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiStartingCard:()=>v});r(53918);var n=r(4915),i=r(50424),o=r(55358),s=r(47181);r(22098),r(31206);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function m(e,t,r){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let v=function(e,t,r,n){var i=a();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var s=t((function(e){i.initializeInstanceElements(e,f.elements)}),r),f=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(d(o.descriptor)||d(i.descriptor)){if(u(o)||u(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(u(o)){if(u(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}l(o,i)}else t.push(o)}return t}(s.d.map(c)),e);return i.initializeClassElements(s.F,f.elements),i.runClassFinishers(s.F,f.finishers)}([(0,o.Mo)("hui-starting-card")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 2}},{kind:"method",key:"setConfig",value:function(e){}},{kind:"method",key:"updated",value:function(e){m(y(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.hass.config&&this.hass.config.state!==n.UE&&(0,s.B)(this,"config-refresh")}},{kind:"method",key:"render",value:function(){return this.hass?i.dy`
      <div class="content">
        <ha-circular-progress active></ha-circular-progress>
        ${this.hass.localize("ui.panel.lovelace.cards.starting.description")}
      </div>
    `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: block;
        height: calc(100vh - var(--header-height));
      }
      ha-circular-progress {
        padding-bottom: 20px;
      }
      .content {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }
    `}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.a63435caa3b65ac35434.js.map