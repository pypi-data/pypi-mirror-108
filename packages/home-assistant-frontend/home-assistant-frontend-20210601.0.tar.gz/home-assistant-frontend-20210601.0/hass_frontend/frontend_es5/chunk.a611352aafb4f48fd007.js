(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2575],{62575:function(e,t,n){"use strict";n.r(t);n(53918);var i,r,s,o,a,c,l,u,d,h,f,p,v,m,g,y,_,b,w=n(55317),k=n(50424),z=n(55358),E=n(47181),S=(n(31206),n(34821)),D=(n(52039),n(22383)),x=n(11654);function P(e){return(P="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function A(e,t,n,i,r,s,o){try{var a=e[s](o),c=a.value}catch(l){return void n(l)}a.done?t(c):Promise.resolve(c).then(i,r)}function O(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function C(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function j(e,t){return(j=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function T(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,i=F(e);if(t){var r=F(this).constructor;n=Reflect.construct(i,arguments,r)}else n=i.apply(this,arguments);return R(this,n)}}function R(e,t){return!t||"object"!==P(t)&&"function"!=typeof t?B(e):t}function B(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function F(e){return(F=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function M(){M=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var r=t.placement;if(t.kind===i&&("static"===r||"prototype"===r)){var s="static"===r?e:n;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var i=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],i=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!q(e))return n.push(e);var t=this.decorateElement(e,r);n.push(t.element),n.push.apply(n,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:n,finishers:i};var s=this.decorateConstructor(n,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,n){var i=t[e.placement];if(!n&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var n=[],i=[],r=e.decorators,s=r.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,r[s])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:i,extras:n}},decorateConstructor:function(e,t){for(var n=[],i=t.length-1;i>=0;i--){var r=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(r)||r);if(void 0!==s.finisher&&n.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return H(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?H(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=$(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:n,placement:i,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:U(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=U(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var i=(0,t[n])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function I(e){var t,n=$(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function Y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function q(e){return e.decorators&&e.decorators.length}function N(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function U(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function $(e){var t=function(e,t){if("object"!==P(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var i=n.call(e,t||"default");if("object"!==P(i))return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===P(t)?t:String(t)}function H(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,i=new Array(t);n<t;n++)i[n]=e[n];return i}!function(e,t,n,i){var r=M();if(i)for(var s=0;s<i.length;s++)r=i[s](r);var o=t((function(e){r.initializeInstanceElements(e,a.elements)}),n),a=r.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var r,s=e[i];if("method"===s.kind&&(r=t.find(n)))if(N(s.descriptor)||N(r.descriptor)){if(q(s)||q(r))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");r.descriptor=s.descriptor}else{if(q(s)){if(q(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");r.decorators=s.decorators}Y(s,r)}else t.push(s)}return t}(o.d.map(I)),e);r.initializeClassElements(o.F,a.elements),r.runClassFinishers(o.F,a.finishers)}([(0,z.Mo)("dialog-zha-reconfigure-device")],(function(e,t){var n,P;return{F:function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&j(e,t)}(i,t);var n=T(i);function i(){var t;C(this,i);for(var r=arguments.length,s=new Array(r),o=0;o<r;o++)s[o]=arguments[o];return t=n.call.apply(n,[this].concat(s)),e(B(t)),t}return i}(t),d:[{kind:"field",decorators:[(0,z.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,z.SB)()],key:"_status",value:void 0},{kind:"field",decorators:[(0,z.SB)()],key:"_stages",value:void 0},{kind:"field",decorators:[(0,z.SB)()],key:"_clusterConfigurationStatuses",value:function(){return new Map}},{kind:"field",decorators:[(0,z.SB)()],key:"_params",value:function(){}},{kind:"field",decorators:[(0,z.SB)()],key:"_allSuccessful",value:function(){return!0}},{kind:"field",decorators:[(0,z.SB)()],key:"_showDetails",value:function(){return!1}},{kind:"field",key:"_subscribed",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._stages=void 0}},{kind:"method",key:"closeDialog",value:function(){this._unsubscribe(),this._params=void 0,this._status=void 0,this._stages=void 0,this._clusterConfigurationStatuses=void 0,(0,E.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var e,t,n=this;return this._params?(0,k.dy)(r||(r=O(['\n      <ha-dialog\n        open\n        @closed="','"\n        .heading=',"\n      >\n        ","\n        ","\n        ","\n        ","\n        ","\n        ","\n      </ha-dialog>\n    "])),this.closeDialog,(0,S.i)(this.hass,this.hass.localize("ui.dialogs.zha_reconfigure_device.heading")+": "+((null===(e=this._params)||void 0===e?void 0:e.device.user_given_name)||(null===(t=this._params)||void 0===t?void 0:t.device.name))),this._status?"":(0,k.dy)(s||(s=O(["\n              <p>\n                ","\n              </p>\n              <p>\n                <em>\n                  ",'\n                </em>\n              </p>\n              <mwc-button\n                slot="primaryAction"\n                @click=',"\n              >\n                ","\n              </mwc-button>\n            "])),this.hass.localize("ui.dialogs.zha_reconfigure_device.introduction"),this.hass.localize("ui.dialogs.zha_reconfigure_device.battery_device_warning"),this._startReconfiguration,this.hass.localize("ui.dialogs.zha_reconfigure_device.start_reconfiguration")),"started"===this._status?(0,k.dy)(o||(o=O(['\n              <div class="flex-container">\n                <ha-circular-progress active></ha-circular-progress>\n                <div class="status">\n                  <p>\n                    <b>\n                      ',"\n                    </b>\n                  </p>\n                  <p>\n                    ",'\n                  </p>\n                </div>\n              </div>\n              <mwc-button slot="primaryAction" @click=',">\n                ",'\n              </mwc-button>\n              <mwc-button slot="secondaryAction" @click=',">\n                ","\n              </mwc-button>\n            "])),this.hass.localize("ui.dialogs.zha_reconfigure_device.in_progress"),this.hass.localize("ui.dialogs.zha_reconfigure_device.run_in_background"),this.closeDialog,this.hass.localize("ui.dialogs.generic.close"),this._toggleDetails,this._showDetails?this.hass.localize("ui.dialogs.zha_reconfigure_device.button_hide"):this.hass.localize("ui.dialogs.zha_reconfigure_device.button_show")):"","failed"===this._status?(0,k.dy)(a||(a=O(['\n              <div class="flex-container">\n                <ha-svg-icon\n                  .path=','\n                  class="failed"\n                ></ha-svg-icon>\n                <div class="status">\n                  <p>\n                    ','\n                  </p>\n                </div>\n              </div>\n              <mwc-button slot="primaryAction" @click=',">\n                ",'\n              </mwc-button>\n              <mwc-button slot="secondaryAction" @click=',">\n                ","\n              </mwc-button>\n            "])),w.lY3,this.hass.localize("ui.dialogs.zha_reconfigure_device.configuration_failed"),this.closeDialog,this.hass.localize("ui.dialogs.generic.close"),this._toggleDetails,this._showDetails?this.hass.localize("ui.dialogs.zha_reconfigure_device.button_hide"):this.hass.localize("ui.dialogs.zha_reconfigure_device.button_show")):"","finished"===this._status?(0,k.dy)(c||(c=O(['\n              <div class="flex-container">\n                <ha-svg-icon\n                  .path=','\n                  class="success"\n                ></ha-svg-icon>\n                <div class="status">\n                  <p>\n                    ','\n                  </p>\n                </div>\n              </div>\n              <mwc-button slot="primaryAction" @click=',">\n                ",'\n              </mwc-button>\n              <mwc-button slot="secondaryAction" @click=',">\n                ","\n              </mwc-button>\n            "])),w.OE9,this.hass.localize("ui.dialogs.zha_reconfigure_device.configuration_complete"),this.closeDialog,this.hass.localize("ui.dialogs.generic.close"),this._toggleDetails,this._showDetails?this.hass.localize("ui.dialogs.zha_reconfigure_device.button_hide"):this.hass.localize("ui.dialogs.zha_reconfigure_device.button_show")):"",this._stages?(0,k.dy)(l||(l=O(['\n              <div class="stages">\n                ',"\n              </div>\n            "])),this._stages.map((function(e){return(0,k.dy)(u||(u=O(['\n                    <span class="stage">\n                      <ha-svg-icon\n                        .path=','\n                        class="success"\n                      ></ha-svg-icon>\n                      ',"\n                    </span>\n                  "])),w.OE9,e)}))):"",this._showDetails?(0,k.dy)(d||(d=O(['\n              <div class="wrapper">\n                <h2 class="grid-item">\n                  ','\n                </h2>\n                <h2 class="grid-item">\n                  ','\n                </h2>\n                <h2 class="grid-item">\n                  ',"\n                </h2>\n\n                ","\n              </div>\n            "])),this.hass.localize("ui.dialogs.zha_reconfigure_device.cluster_header"),this.hass.localize("ui.dialogs.zha_reconfigure_device.bind_header"),this.hass.localize("ui.dialogs.zha_reconfigure_device.reporting_header"),this._clusterConfigurationStatuses.size>0?(0,k.dy)(h||(h=O(["\n                      ","\n                    "])),Array.from(this._clusterConfigurationStatuses.values()).map((function(e){return(0,k.dy)(f||(f=O(['\n                          <div class="grid-item">\n                            ','\n                          </div>\n                          <div class="grid-item">\n                            ','\n                          </div>\n                          <div class="grid-item">\n                            ',"\n                          </div>\n                        "])),e.cluster.name,void 0!==e.bindSuccess?e.bindSuccess?(0,k.dy)(p||(p=O(['\n                                    <span class="stage">\n                                      <ha-svg-icon\n                                        .path=','\n                                        class="success"\n                                      ></ha-svg-icon>\n                                    </span>\n                                  '])),w.OE9):(0,k.dy)(v||(v=O(['\n                                    <span class="stage">\n                                      <ha-svg-icon\n                                        .path=','\n                                        class="failed"\n                                      ></ha-svg-icon>\n                                    </span>\n                                  '])),w.lY3):"",e.attributes.size>0?(0,k.dy)(m||(m=O(['\n                                  <div class="attributes">\n                                    <div class="grid-item">\n                                      ','\n                                    </div>\n                                    <div class="grid-item">\n                                      <div>\n                                        ',"\n                                      </div>\n                                    </div>\n                                    ","\n                                  </div>\n                                "])),n.hass.localize("ui.dialogs.zha_reconfigure_device.attribute"),n.hass.localize("ui.dialogs.zha_reconfigure_device.min_max_change"),Array.from(e.attributes.values()).map((function(e){return(0,k.dy)(g||(g=O(['\n                                        <span class="grid-item">\n                                          ',":\n                                          ",'\n                                        </span>\n                                        <div class="grid-item">\n                                          ',"/","/","\n                                        </div>\n                                      "])),e.name,e.success?(0,k.dy)(y||(y=O(['\n                                                <span class="stage">\n                                                  <ha-svg-icon\n                                                    .path=','\n                                                    class="success"\n                                                  ></ha-svg-icon>\n                                                </span>\n                                              '])),w.OE9):(0,k.dy)(_||(_=O(['\n                                                <span class="stage">\n                                                  <ha-svg-icon\n                                                    .path=','\n                                                    class="failed"\n                                                  ></ha-svg-icon>\n                                                </span>\n                                              '])),w.lY3),e.min,e.max,e.change)}))):"")}))):""):""):(0,k.dy)(i||(i=O([""])))}},{kind:"method",key:"_startReconfiguration",value:(n=regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.hass&&this._params){e.next=2;break}return e.abrupt("return");case 2:return e.t0=Map,e.next=5,(0,D.qm)(this.hass,this._params.device.ieee);case 5:e.t1=e.sent.map((function(e){return[e.id,{cluster:e,bindSuccess:void 0,attributes:new Map}]})),this._clusterConfigurationStatuses=new e.t0(e.t1),this._subscribe(this._params),this._status="started";case 9:case"end":return e.stop()}}),e,this)})),P=function(){var e=this,t=arguments;return new Promise((function(i,r){var s=n.apply(e,t);function o(e){A(s,i,r,o,a,"next",e)}function a(e){A(s,i,r,o,a,"throw",e)}o(void 0)}))},function(){return P.apply(this,arguments)})},{kind:"method",key:"_handleMessage",value:function(e){var t=this;if(e.type===D.H4)this._unsubscribe(),this._status=this._allSuccessful?"finished":"failed";else{var n=this._clusterConfigurationStatuses.get(e.zha_channel_msg_data.cluster_id);if(e.type===D.mS){this._stages||(this._stages=["binding"]);var i=e.zha_channel_msg_data.success;n.bindSuccess=i,this._allSuccessful=this._allSuccessful&&i}if(e.type===D.lu){this._stages&&!this._stages.includes("reporting")&&this._stages.push("reporting");var r=e.zha_channel_msg_data.attributes;Object.keys(r).forEach((function(e){var i=r[e];n.attributes.set(i.id,i),t._allSuccessful=t._allSuccessful&&i.success}))}this.requestUpdate()}}},{kind:"method",key:"_unsubscribe",value:function(){this._subscribed&&(this._subscribed.then((function(e){return e()})),this._subscribed=void 0)}},{kind:"method",key:"_subscribe",value:function(e){this.hass&&(this._subscribed=(0,D.$l)(this.hass,e.device.ieee,this._handleMessage.bind(this)))}},{kind:"method",key:"_toggleDetails",value:function(){this._showDetails=!this._showDetails}},{kind:"get",static:!0,key:"styles",value:function(){return[x.yu,(0,k.iv)(b||(b=O(["\n        .wrapper {\n          display: grid;\n          grid-template-columns: 3fr 1fr 2fr;\n        }\n        .attributes {\n          display: grid;\n          grid-template-columns: 1fr 1fr;\n        }\n        .grid-item {\n          border: 1px solid;\n          padding: 7px;\n        }\n        .success {\n          color: var(--success-color);\n        }\n\n        .failed {\n          color: var(--warning-color);\n        }\n\n        .flex-container {\n          display: flex;\n          align-items: center;\n        }\n\n        .stages {\n          margin-top: 16px;\n        }\n\n        .stage ha-svg-icon {\n          width: 16px;\n          height: 16px;\n        }\n        .stage {\n          padding: 8px;\n        }\n\n        ha-svg-icon {\n          width: 68px;\n          height: 48px;\n        }\n\n        .flex-container ha-circular-progress,\n        .flex-container ha-svg-icon {\n          margin-right: 20px;\n        }\n      "])))]}}]}}),k.oi)}}]);
//# sourceMappingURL=chunk.a611352aafb4f48fd007.js.map