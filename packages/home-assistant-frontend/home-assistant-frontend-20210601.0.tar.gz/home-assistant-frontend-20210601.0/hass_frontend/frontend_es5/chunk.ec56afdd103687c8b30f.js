/*! For license information please see chunk.ec56afdd103687c8b30f.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[5004],{7323:function(e,t,n){"use strict";n.d(t,{p:function(){return r}});var r=function(e,t){return e&&e.config.components.includes(t)}},51444:function(e,t,n){"use strict";n.d(t,{_:function(){return o}});var r=n(47181),i=function(){return Promise.all([n.e(5009),n.e(9462),n.e(2420)]).then(n.bind(n,72420))},o=function(e){(0,r.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:i,dialogParams:{}})}},27849:function(e,t,n){"use strict";n(39841);var r,i=n(50856);n(28426);function o(e){return(o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function a(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function s(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function l(e,t){return(l=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function c(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=f(e);if(t){var i=f(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return u(this,n)}}function u(e,t){return!t||"object"!==o(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var p=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&l(e,t)}(f,customElements.get("app-header-layout"));var t,n,o,u=c(f);function f(){return a(this,f),u.apply(this,arguments)}return t=f,o=[{key:"template",get:function(){return(0,i.d)(r||(e=['\n      <style>\n        :host {\n          display: block;\n          /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using `isolation: isolate`, but that\'s not well supported\n         * across browsers.\n         */\n          position: relative;\n          z-index: 0;\n        }\n\n        #wrapper ::slotted([slot="header"]) {\n          @apply --layout-fixed-top;\n          z-index: 1;\n        }\n\n        #wrapper.initializing ::slotted([slot="header"]) {\n          position: relative;\n        }\n\n        :host([has-scrolling-region]) {\n          height: 100%;\n        }\n\n        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {\n          position: absolute;\n        }\n\n        :host([has-scrolling-region])\n          #wrapper.initializing\n          ::slotted([slot="header"]) {\n          position: relative;\n        }\n\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          @apply --layout-fit;\n          overflow-y: auto;\n          -webkit-overflow-scrolling: touch;\n        }\n\n        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n          position: relative;\n        }\n\n        #contentContainer {\n          /* Create a stacking context here so that all children appear below the header. */\n          position: relative;\n          z-index: 0;\n          /* Using \'transform\' will cause \'position: fixed\' elements to behave like\n           \'position: absolute\' relative to this element. */\n          transform: translate(0);\n          margin-left: env(safe-area-inset-left);\n          margin-right: env(safe-area-inset-right);\n        }\n\n        @media print {\n          :host([has-scrolling-region]) #wrapper #contentContainer {\n            overflow-y: visible;\n          }\n        }\n      </style>\n\n      <div id="wrapper" class="initializing">\n        <slot id="headerSlot" name="header"></slot>\n\n        <div id="contentContainer"><slot></slot></div>\n        <slot id="fab" name="fab"></slot>\n      </div>\n    '],(t=['\n      <style>\n        :host {\n          display: block;\n          /**\n         * Force app-header-layout to have its own stacking context so that its parent can\n         * control the stacking of it relative to other elements (e.g. app-drawer-layout).\n         * This could be done using \\`isolation: isolate\\`, but that\'s not well supported\n         * across browsers.\n         */\n          position: relative;\n          z-index: 0;\n        }\n\n        #wrapper ::slotted([slot="header"]) {\n          @apply --layout-fixed-top;\n          z-index: 1;\n        }\n\n        #wrapper.initializing ::slotted([slot="header"]) {\n          position: relative;\n        }\n\n        :host([has-scrolling-region]) {\n          height: 100%;\n        }\n\n        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {\n          position: absolute;\n        }\n\n        :host([has-scrolling-region])\n          #wrapper.initializing\n          ::slotted([slot="header"]) {\n          position: relative;\n        }\n\n        :host([has-scrolling-region]) #wrapper #contentContainer {\n          @apply --layout-fit;\n          overflow-y: auto;\n          -webkit-overflow-scrolling: touch;\n        }\n\n        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {\n          position: relative;\n        }\n\n        #contentContainer {\n          /* Create a stacking context here so that all children appear below the header. */\n          position: relative;\n          z-index: 0;\n          /* Using \'transform\' will cause \'position: fixed\' elements to behave like\n           \'position: absolute\' relative to this element. */\n          transform: translate(0);\n          margin-left: env(safe-area-inset-left);\n          margin-right: env(safe-area-inset-right);\n        }\n\n        @media print {\n          :host([has-scrolling-region]) #wrapper #contentContainer {\n            overflow-y: visible;\n          }\n        }\n      </style>\n\n      <div id="wrapper" class="initializing">\n        <slot id="headerSlot" name="header"></slot>\n\n        <div id="contentContainer"><slot></slot></div>\n        <slot id="fab" name="fab"></slot>\n      </div>\n    '])||(t=e.slice(0)),r=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))));var e,t}}],(n=null)&&s(t.prototype,n),o&&s(t,o),f}();customElements.define("ha-app-layout",p)},51153:function(e,t,n){"use strict";n.d(t,{l$:function(){return a},Z6:function(){return s},Do:function(){return l}});n(10175),n(80251),n(99471),n(14888),n(69377),n(95035),n(38026),n(89173),n(41043),n(57464),n(24617),n(26136),n(82778);var r=n(7778),i=new Set(["entity","entities","button","entity-button","glance","history-graph","horizontal-stack","light","sensor","thermostat","vertical-stack","weather-forecast"]),o={"alarm-panel":function(){return n.e(7639).then(n.bind(n,77639))},error:function(){return Promise.all([n.e(8595),n.e(5796)]).then(n.bind(n,55796))},"empty-state":function(){return n.e(7284).then(n.bind(n,67284))},grid:function(){return n.e(6169).then(n.bind(n,6169))},starting:function(){return n.e(7873).then(n.bind(n,47873))},"entity-filter":function(){return n.e(3688).then(n.bind(n,33688))},humidifier:function(){return n.e(8558).then(n.bind(n,68558))},"media-control":function(){return Promise.all([n.e(7794),n.e(3525)]).then(n.bind(n,13525))},"picture-elements":function(){return Promise.all([n.e(4909),n.e(319),n.e(7282),n.e(9810),n.e(7364),n.e(1267)]).then(n.bind(n,83358))},"picture-entity":function(){return Promise.all([n.e(319),n.e(7282),n.e(8317)]).then(n.bind(n,41500))},"picture-glance":function(){return Promise.all([n.e(319),n.e(7282),n.e(7987)]).then(n.bind(n,66621))},"plant-status":function(){return n.e(8723).then(n.bind(n,48723))},"safe-mode":function(){return Promise.all([n.e(4066),n.e(4503)]).then(n.bind(n,24503))},"shopping-list":function(){return Promise.all([n.e(2296),n.e(3376)]).then(n.bind(n,43376))},conditional:function(){return n.e(8857).then(n.bind(n,68857))},gauge:function(){return n.e(5223).then(n.bind(n,25223))},iframe:function(){return n.e(5018).then(n.bind(n,95018))},map:function(){return n.e(76).then(n.bind(n,60076))},markdown:function(){return Promise.all([n.e(4940),n.e(6474)]).then(n.bind(n,51282))},picture:function(){return n.e(5338).then(n.bind(n,45338))},calendar:function(){return Promise.resolve().then(n.bind(n,80251))},logbook:function(){return Promise.all([n.e(3511),n.e(1855),n.e(4302)]).then(n.bind(n,8436))}},a=function(e){return(0,r.Xm)("card",e,i,o,void 0,void 0)},s=function(e){return(0,r.Tw)("card",e,i,o,void 0,void 0)},l=function(e){return(0,r.ED)(e,"card",i,o)}},89026:function(e,t,n){"use strict";n.d(t,{t:function(){return o},Q:function(){return a}});var r=n(7778),i={picture:function(){return n.e(9130).then(n.bind(n,69130))},buttons:function(){return Promise.all([n.e(2109),n.e(2587)]).then(n.bind(n,32587))},graph:function(){return n.e(5773).then(n.bind(n,25773))}},o=function(e){return(0,r.Tw)("header-footer",e,void 0,i,void 0,void 0)},a=function(e){return(0,r.ED)(e,"header-footer",void 0,i)}},44295:function(e,t,n){"use strict";n.r(t);var r,i,o,a=n(55317),s=(n(53268),n(12730),n(50424)),l=n(55358),c=n(14516),u=n(7323),f=(n(48932),n(51444)),p=(n(27849),n(11654)),d=n(51153);function h(e){return(h="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function m(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function y(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function v(e,t){return(v=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function b(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=S(e);if(t){var i=S(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return g(this,n)}}function g(e,t){return!t||"object"!==h(t)&&"function"!=typeof t?w(e):t}function w(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!x(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);n.push.apply(n,c)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=_(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:C(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=C(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function E(e){var t,n=_(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function x(e){return e.decorators&&e.decorators.length}function O(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function C(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function _(e){var t=function(e,t){if("object"!==h(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==h(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===h(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function j(e,t,n){return(j="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=S(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function S(e){return(S=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,n,r){var i=k();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),n),s=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(O(o.descriptor)||O(i.descriptor)){if(x(o)||x(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(x(o)){if(x(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}P(o,i)}else t.push(o)}return t}(a.d.map(E)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,l.Mo)("ha-panel-shopping-list")],(function(e,t){var n=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&v(e,t)}(r,t);var n=b(r);function r(){var t;y(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(w(t)),t}return r}(t);return{F:n,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_card",value:void 0},{kind:"field",key:"_conversation",value:function(){var e=this;return(0,c.Z)((function(t){return(0,u.p)(e.hass,"conversation")}))}},{kind:"method",key:"firstUpdated",value:function(e){j(S(n.prototype),"firstUpdated",this).call(this,e),this._card=(0,d.Z6)({type:"shopping-list"}),this._card.hass=this.hass}},{kind:"method",key:"updated",value:function(e){j(S(n.prototype),"updated",this).call(this,e),e.has("hass")&&(this._card.hass=this.hass)}},{kind:"method",key:"render",value:function(){return(0,s.dy)(r||(r=m(['\n      <ha-app-layout>\n        <app-header fixed slot="header">\n          <app-toolbar>\n            <ha-menu-button\n              .hass=',"\n              .narrow=","\n            ></ha-menu-button>\n            <div main-title>","</div>\n            ",'\n          </app-toolbar>\n        </app-header>\n        <div id="columns">\n          <div class="column">',"</div>\n        </div>\n      </ha-app-layout>\n    "])),this.hass,this.narrow,this.hass.localize("panel.shopping_list"),this._conversation(this.hass.config.components)?(0,s.dy)(i||(i=m(["\n                  <mwc-icon-button\n                    .label=","\n                    @click=","\n                  >\n                    <ha-svg-icon .path=","></ha-svg-icon>\n                  </mwc-icon-button>\n                "])),this.hass.localize("ui.panel.shopping_list.start_conversation"),this._showVoiceCommandDialog,a.N3O):"",this._card)}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,f._)(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[p.Qx,(0,s.iv)(o||(o=m(["\n        :host {\n          --mdc-theme-primary: var(--app-header-text-color);\n          display: block;\n          height: 100%;\n        }\n        :host([narrow]) app-toolbar mwc-button {\n          width: 65px;\n        }\n        .heading {\n          overflow: hidden;\n          white-space: nowrap;\n          margin-top: 4px;\n        }\n        #columns {\n          display: flex;\n          flex-direction: row;\n          justify-content: center;\n          margin-left: 4px;\n          margin-right: 4px;\n        }\n        .column {\n          flex: 1 0 0;\n          max-width: 500px;\n          min-width: 0;\n        }\n      "])))]}}]}}),s.oi)}}]);
//# sourceMappingURL=chunk.ec56afdd103687c8b30f.js.map