(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7987],{96151:function(e,t,n){"use strict";n.d(t,{T:function(){return r},y:function(){return i}});var r=function(e){requestAnimationFrame((function(){return setTimeout(e,0)}))},i=function(){return new Promise((function(e){r(e)}))}},22814:function(e,t,n){"use strict";function r(e,t,n,r,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void n(l)}s.done?t(c):Promise.resolve(c).then(r,i)}function i(e){return function(){var t=this,n=arguments;return new Promise((function(i,o){var a=e.apply(t,n);function s(e){r(a,i,o,s,c,"next",e)}function c(e){r(a,i,o,s,c,"throw",e)}s(void 0)}))}}n.d(t,{uw:function(){return s},iI:function(){return c},W2:function(){return l},TZ:function(){return u}});var o,a,s="".concat(location.protocol,"//").concat(location.host),c=function(e,t){return e.callWS({type:"auth/sign_path",path:t})},l=2143==n.j?(o=i(regeneratorRuntime.mark((function e(t,n,r,i){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",t.callWS({type:"config/auth_provider/homeassistant/create",user_id:n,username:r,password:i}));case 1:case"end":return e.stop()}}),e)}))),function(e,t,n,r){return o.apply(this,arguments)}):null,u=2143==n.j?(a=i(regeneratorRuntime.mark((function e(t,n,r){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",t.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:n,password:r}));case 1:case"end":return e.stop()}}),e)}))),function(e,t,n){return a.apply(this,arguments)}):null},66621:function(e,t,n){"use strict";n.r(t);var r,i,o,a,s,c,l,u,f,d=n(50424),h=n(55358),p=n(76666),m=n(82816),y=n(49706),v=n(62877),g=n(58831),b=n(29171),w=n(91741),_=n(36145),k=(n(22098),n(10983),n(93491)),E=n(15688),x=n(22503),P=n(22193),D=n(53658),S=n(90271),A=(n(97282),n(75502));n(65082);function C(e){return(C="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function O(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function T(e,t){var n="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!n){if(Array.isArray(e)||(n=q(e))||t&&e&&"number"==typeof e.length){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return a=e.done,e},e:function(e){s=!0,o=e},f:function(){try{a||null==n.return||n.return()}finally{if(s)throw o}}}}function j(e,t,n,r,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void n(l)}s.done?t(c):Promise.resolve(c).then(r,i)}function z(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function R(e,t){return(R=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function I(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=Z(e);if(t){var i=Z(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return F(this,n)}}function F(e,t){return!t||"object"!==C(t)&&"function"!=typeof t?B(e):t}function B(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function H(){H=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!W(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||q(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=U(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:G(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=G(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function K(e){var t,n=U(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function M(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function W(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function G(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function U(e){var t=function(e,t){if("object"!==C(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==C(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===C(t)?t:String(t)}function q(e,t){if(e){if("string"==typeof e)return N(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?N(e,t):void 0}}function N(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function V(e,t,n){return(V="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Z(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function Z(e){return(Z=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var J=new Set(["closed","locked","not_home","off"]);!function(e,t,n,r){var i=H();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),n),s=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if($(o.descriptor)||$(i.descriptor)){if(W(o)||W(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(W(o)){if(W(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}M(o,i)}else t.push(o)}return t}(a.d.map(K)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,h.Mo)("hui-picture-glance-card")],(function(e,t){var C,F,H=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&R(e,t)}(r,t);var n=I(r);function r(){var t;z(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(B(t)),t}return r}(t);return{F:H,d:[{kind:"method",static:!0,key:"getConfigElement",value:(C=regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([n.e(5009),n.e(2955),n.e(8161),n.e(1041),n.e(1657),n.e(4444),n.e(8644),n.e(4268),n.e(7724),n.e(2296),n.e(2613),n.e(9799),n.e(3098),n.e(6294),n.e(8595),n.e(6087),n.e(6002),n.e(6363),n.e(9266),n.e(7008),n.e(2990),n.e(4535),n.e(3822),n.e(8331),n.e(8101),n.e(6902),n.e(33),n.e(3902),n.e(259),n.e(3911)]).then(n.bind(n,33785));case 2:return e.abrupt("return",document.createElement("hui-picture-glance-card-editor"));case 3:case"end":return e.stop()}}),e)})),F=function(){var e=this,t=arguments;return new Promise((function(n,r){var i=C.apply(e,t);function o(e){j(i,n,r,o,a,"next",e)}function a(e){j(i,n,r,o,a,"throw",e)}o(void 0)}))},function(){return F.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,n){return{type:"picture-glance",title:"Kitchen",image:"https://demo.home-assistant.io/stub_config/kitchen.png",entities:(0,E.j)(e,2,t,n,["sensor","binary_sensor"])}}},{kind:"field",decorators:[(0,h.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.SB)()],key:"_config",value:void 0},{kind:"field",key:"_entitiesDialog",value:void 0},{kind:"field",key:"_entitiesToggle",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){var t=this;if(!e||!e.entities||!Array.isArray(e.entities)||!(e.image||e.camera_image||e.state_image)||e.state_image&&!e.entity)throw new Error("Invalid configuration");var n=(0,S.A)(e.entities);this._entitiesDialog=[],this._entitiesToggle=[],n.forEach((function(n){e.force_dialog||!y.Kk.has((0,g.M)(n.entity))?t._entitiesDialog.push(n):t._entitiesToggle.push(n)})),this._config=Object.assign({hold_action:{action:"more-info"}},e)}},{kind:"method",key:"shouldUpdate",value:function(e){if((0,D.G)(this,e))return!0;var t=e.get("hass");if(!t||t.themes!==this.hass.themes||t.locale!==this.hass.locale)return!0;if(this._entitiesDialog){var n,r=T(this._entitiesDialog);try{for(r.s();!(n=r.n()).done;){var i=n.value;if(t.states[i.entity]!==this.hass.states[i.entity])return!0}}catch(c){r.e(c)}finally{r.f()}}if(this._entitiesToggle){var o,a=T(this._entitiesToggle);try{for(a.s();!(o=a.n()).done;){var s=o.value;if(t.states[s.entity]!==this.hass.states[s.entity])return!0}}catch(c){a.e(c)}finally{a.f()}}return!1}},{kind:"method",key:"updated",value:function(e){if(V(Z(H.prototype),"updated",this).call(this,e),this._config&&this.hass){var t=e.get("hass"),n=e.get("_config");t&&n&&t.themes===this.hass.themes&&n.theme===this._config.theme||(0,v.R)(this,this.hass.themes,this._config.theme)}}},{kind:"method",key:"render",value:function(){var e=this;return this._config&&this.hass?(0,d.dy)(i||(i=O(["\n      <ha-card>\n        <hui-image\n          class=","\n          @action=","\n          .actionHandler=","\n          tabindex=","\n          .config=","\n          .hass=","\n          .image=","\n          .stateImage=","\n          .stateFilter=","\n          .cameraImage=","\n          .cameraView=","\n          .entity=","\n          .aspectRatio=",'\n        ></hui-image>\n        <div class="box">\n          ','\n          <div class="row">\n            ','\n          </div>\n          <div class="row">\n            ',"\n          </div>\n        </div>\n      </ha-card>\n    "])),(0,p.$)({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.camera_image)}),this._handleAction,(0,k.K)({hasHold:(0,P._)(this._config.hold_action),hasDoubleClick:(0,P._)(this._config.double_tap_action)}),(0,m.o)((0,P._)(this._config.tap_action)?"0":void 0),this._config,this.hass,this._config.image,this._config.state_image,this._config.state_filter,this._config.camera_image,this._config.camera_view,this._config.entity,this._config.aspect_ratio,this._config.title?(0,d.dy)(o||(o=O([' <div class="title">',"</div> "])),this._config.title):"",this._entitiesDialog.map((function(t){return e.renderEntity(t,!0)})),this._entitiesToggle.map((function(t){return e.renderEntity(t,!1)}))):(0,d.dy)(r||(r=O([""])))}},{kind:"method",key:"renderEntity",value:function(e,t){var n=this.hass.states[e.entity];return e=Object.assign({tap_action:{action:t?"more-info":"toggle"},hold_action:{action:"more-info"}},e),n?(0,d.dy)(s||(s=O(['\n      <div class="wrapper">\n        <ha-icon-button\n          @action=',"\n          .actionHandler=","\n          tabindex=","\n          .disabled=","\n          .config=","\n          class=","\n          .icon=","\n          title=","\n        ></ha-icon-button>\n        ","\n      </div>\n    "])),this._handleAction,(0,k.K)({hasHold:(0,P._)(e.hold_action),hasDoubleClick:(0,P._)(e.double_tap_action)}),(0,m.o)((0,P._)(e.tap_action)?void 0:"-1"),!(0,P._)(e.tap_action),e,(0,p.$)({"state-on":!J.has(n.state)}),e.icon||(0,_.M)(n),"".concat((0,w.C)(n)," : ").concat((0,b.D)(this.hass.localize,n,this.hass.locale)),!0!==this._config.show_state&&!0!==e.show_state?(0,d.dy)(c||(c=O(['<div class="state"></div>']))):(0,d.dy)(l||(l=O(['\n              <div class="state">\n                ',"\n              </div>\n            "])),e.attribute?(0,d.dy)(u||(u=O(["\n                      ","","","\n                    "])),e.prefix,n.attributes[e.attribute],e.suffix):(0,b.D)(this.hass.localize,n,this.hass.locale))):(0,d.dy)(a||(a=O(["\n        <hui-warning-element\n          .label=","\n        ></hui-warning-element>\n      "])),(0,A.i)(this.hass,e.entity))}},{kind:"method",key:"_handleAction",value:function(e){var t=e.currentTarget.config;(0,x.G)(this,this.hass,t,e.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return(0,d.iv)(f||(f=O(["\n      ha-card {\n        position: relative;\n        min-height: 48px;\n        overflow: hidden;\n        height: 100%;\n        box-sizing: border-box;\n      }\n\n      hui-image.clickable {\n        cursor: pointer;\n      }\n\n      .box {\n        /* start paper-font-common-nowrap style */\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n        /* end paper-font-common-nowrap style */\n\n        position: absolute;\n        left: 0;\n        right: 0;\n        bottom: 0;\n        background-color: var(\n          --ha-picture-card-background-color,\n          rgba(0, 0, 0, 0.3)\n        );\n        padding: 4px 8px;\n        font-size: 16px;\n        line-height: 40px;\n        color: var(--ha-picture-card-text-color, white);\n        display: flex;\n        justify-content: space-between;\n        flex-direction: row;\n      }\n\n      .box .title {\n        font-weight: 500;\n        margin-left: 8px;\n      }\n\n      ha-icon-button {\n        --mdc-icon-button-size: 40px;\n        --disabled-text-color: currentColor;\n        color: var(--ha-picture-icon-button-color, #a9a9a9);\n      }\n\n      ha-icon-button.state-on {\n        color: var(--ha-picture-icon-button-on-color, white);\n      }\n      .state {\n        display: block;\n        font-size: 12px;\n        text-align: center;\n        line-height: 12px;\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n      }\n      .row {\n        display: flex;\n        flex-direction: row;\n      }\n      .wrapper {\n        display: flex;\n        flex-direction: column;\n        width: 40px;\n      }\n    "])))}}]}}),d.oi)}}]);
//# sourceMappingURL=chunk.282071ec3d16f00382c9.js.map