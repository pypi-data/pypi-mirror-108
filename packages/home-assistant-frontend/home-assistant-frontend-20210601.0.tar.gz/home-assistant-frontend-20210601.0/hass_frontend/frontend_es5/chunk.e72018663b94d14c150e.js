(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7529],{42657:function(e,t,n){"use strict";n(53918),n(25230);var r,i,o,a,c=n(50424),s=n(55358),l=n(92483),d=n(47181);n(52039);function u(e){return(u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function f(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function h(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function p(e,t){return(p=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function v(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=b(e);if(t){var i=b(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return y(this,n)}}function y(e,t){return!t||"object"!==u(t)&&"function"!=typeof t?m(e):t}function m(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function w(){w=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!E(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&r.push(s.finisher);var l=s.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=C(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:P(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=P(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function g(e){var t,n=C(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function P(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function C(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==u(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}!function(e,t,n,r){var i=w();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),n),c=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(x(o.descriptor)||x(i.descriptor)){if(E(o)||E(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(E(o)){if(E(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}k(o,i)}else t.push(o)}return t}(a.d.map(g)),e);i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,s.Mo)("ha-button-toggle-group")],(function(e,t){return{F:function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&p(e,t)}(r,t);var n=v(r);function r(){var t;h(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(m(t)),t}return r}(t),d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"buttons",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"active",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"fullWidth",value:function(){return!1}},{kind:"method",key:"render",value:function(){var e=this;return(0,c.dy)(r||(r=f(["\n      <div>\n        ","\n      </div>\n    "])),this.buttons.map((function(t){return t.iconPath?(0,c.dy)(i||(i=f(["<mwc-icon-button\n                .label=","\n                .value=","\n                ?active=","\n                @click=","\n              >\n                <ha-svg-icon .path=","></ha-svg-icon>\n              </mwc-icon-button>"])),t.label,t.value,e.active===t.value,e._handleClick,t.iconPath):(0,c.dy)(o||(o=f(["<mwc-button\n                style=","\n                .value=","\n                ?active=","\n                @click=","\n                >","</mwc-button\n              >"])),(0,l.V)({width:e.fullWidth?"".concat(100/e.buttons.length,"%"):"initial"}),t.value,e.active===t.value,e._handleClick,t.label)})))}},{kind:"method",key:"_handleClick",value:function(e){this.active=e.currentTarget.value,(0,d.B)(this,"value-changed",{value:this.active})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,c.iv)(a||(a=f(['\n      div {\n        display: flex;\n        --mdc-icon-button-size: var(--button-toggle-size, 36px);\n        --mdc-icon-size: var(--button-toggle-icon-size, 20px);\n      }\n      mwc-icon-button,\n      mwc-button {\n        border: 1px solid var(--primary-color);\n        border-right-width: 0px;\n        position: relative;\n        cursor: pointer;\n      }\n      mwc-icon-button::before,\n      mwc-button::before {\n        top: 0;\n        left: 0;\n        width: 100%;\n        height: 100%;\n        position: absolute;\n        background-color: currentColor;\n        opacity: 0;\n        pointer-events: none;\n        content: "";\n        transition: opacity 15ms linear, background-color 15ms linear;\n      }\n      mwc-icon-button[active]::before,\n      mwc-button[active]::before {\n        opacity: var(--mdc-icon-button-ripple-opacity, 0.12);\n      }\n      mwc-icon-button:first-child,\n      mwc-button:first-child {\n        border-radius: 4px 0 0 4px;\n      }\n      mwc-icon-button:last-child,\n      mwc-button:last-child {\n        border-radius: 0 4px 4px 0;\n        border-right-width: 1px;\n      }\n      mwc-icon-button:only-child,\n      mwc-button:only-child {\n        border-radius: 4px;\n        border-right-width: 1px;\n      }\n    '])))}}]}}),c.oi)},51144:function(e,t,n){"use strict";n.d(t,{G:function(){return c},t:function(){return l}});var r=n(49706);if(2143==n.j)var i=n(58831);if(2143==n.j)var o=n(91741);function a(e,t,n,r,i,o,a){try{var c=e[o](a),s=c.value}catch(l){return void n(l)}c.done?t(s):Promise.resolve(s).then(r,i)}var c=function(){var e,t=(e=regeneratorRuntime.mark((function e(t,n,r,i){var o,a,c;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return o=encodeURI("?start=".concat(n.toISOString(),"&end=").concat(r.toISOString())),a=[],c=[],i.forEach((function(e){c.push(t.callApi("GET","calendars/".concat(e.entity_id).concat(o)))})),e.next=6,Promise.all(c);case 6:return e.sent.forEach((function(e,t){var n=i[t];e.forEach((function(e){var t=s(e.start);if(t){var r={start:t,end:s(e.end),title:e.summary,summary:e.summary,backgroundColor:n.backgroundColor,borderColor:n.backgroundColor,calendar:n.entity_id};a.push(r)}}))})),e.abrupt("return",a);case 9:case"end":return e.stop()}}),e)})),function(){var t=this,n=arguments;return new Promise((function(r,i){var o=e.apply(t,n);function c(e){a(o,r,i,c,s,"next",e)}function s(e){a(o,r,i,c,s,"throw",e)}c(void 0)}))});return function(e,n,r,i){return t.apply(this,arguments)}}(),s=function(e){return"string"==typeof e?e:e.dateTime?e.dateTime:e.date?e.date:void 0},l=function(e){return Object.keys(e.states).filter((function(e){return"calendar"===(0,i.M)(e)})).sort().map((function(t,n){return{entity_id:t,name:(0,o.C)(e.states[t]),backgroundColor:"#".concat(r.AZ[n%r.AZ.length])}}))}},2471:function(e,t,n){"use strict";var r,i,o,a,c,s=n(43924),l=n(98868),d=n(78541),u=n(82387),f=n(61716),h=n(13692),p=n(53842),v=n(7623),y=(n(53918),n(55317)),m=n(50424),b=n(55358),w=n(14516),g=n(47181),k=(n(42657),n(10983),n(11654));function E(e){return(E="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function x(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function P(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function C(e,t){return(C=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function _(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=F(e);if(t){var i=F(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return D(this,n)}}function D(e,t){return!t||"object"!==E(t)&&"function"!=typeof t?S(e):t}function S(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function O(){O=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!A(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&r.push(s.finisher);var l=s.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return G(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?G(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=R(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:V(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=V(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function j(e){var t,n=R(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function A(e){return e.decorators&&e.decorators.length}function T(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function V(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function R(e){var t=function(e,t){if("object"!==E(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==E(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===E(t)?t:String(t)}function G(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function M(e,t,n){return(M="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=F(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function F(e){return(F=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var I={headerToolbar:!1,plugins:[u.ZP,p.Z,h.ZP],initialView:"dayGridMonth",dayMaxEventRows:!0,height:"parent",eventDisplay:"list-item",locales:d.Z,views:{list:{visibleRange:function(e){var t=new Date(e.valueOf()),n=new Date(e.valueOf());return n.setDate(n.getDate()+7),{start:t,end:n}}}}},B=[{label:"Month View",value:"dayGridMonth",iconPath:y.SI1},{label:"Week View",value:"dayGridWeek",iconPath:y.KXE},{label:"Day View",value:"dayGridDay",iconPath:y.r3U},{label:"List View",value:"list",iconPath:y.uay}],Z=function(e,t,n,r){var i=O();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),n),c=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(T(o.descriptor)||T(i.descriptor)){if(A(o)||A(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(A(o)){if(A(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}z(o,i)}else t.push(o)}return t}(a.d.map(j)),e);return i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}(null,(function(e,t){var n=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&C(e,t)}(r,t);var n=_(r);function r(){var t;P(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(S(t)),t}return r}(t);return{F:n,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,b.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,b.Cb)({attribute:!1})],key:"events",value:function(){return[]}},{kind:"field",decorators:[(0,b.Cb)({attribute:!1})],key:"views",value:function(){return["dayGridMonth","dayGridWeek","dayGridDay"]}},{kind:"field",decorators:[(0,b.Cb)()],key:"initialView",value:function(){return"dayGridMonth"}},{kind:"field",key:"calendar",value:void 0},{kind:"field",decorators:[(0,b.SB)()],key:"_activeView",value:function(){return this.initialView}},{kind:"method",key:"updateSize",value:function(){var e;null===(e=this.calendar)||void 0===e||e.updateSize()}},{kind:"method",key:"render",value:function(){var e=this._viewToggleButtons(this.views);return(0,m.dy)(r||(r=x(["\n      ",'\n      <div id="calendar"></div>\n    '])),this.calendar?(0,m.dy)(i||(i=x(['\n            <div class="header">\n              ',"\n            </div>\n          "])),this.narrow?(0,m.dy)(a||(a=x(['\n                    <div class="controls">\n                      <h1>',"</h1>\n                      <div>\n                        <ha-icon-button\n                          label=",'\n                          icon="hass:chevron-left"\n                          class="prev"\n                          @click=',"\n                        >\n                        </ha-icon-button>\n                        <ha-icon-button\n                          label=",'\n                          icon="hass:chevron-right"\n                          class="next"\n                          @click=','\n                        >\n                        </ha-icon-button>\n                      </div>\n                    </div>\n                    <div class="controls">\n                      <mwc-button\n                        outlined\n                        class="today"\n                        @click=',"\n                        >","</mwc-button\n                      >\n                      <ha-button-toggle-group\n                        .buttons=","\n                        .active=","\n                        @value-changed=","\n                      ></ha-button-toggle-group>\n                    </div>\n                  "])),this.calendar.view.title,this.hass.localize("ui.common.previous"),this._handlePrev,this.hass.localize("ui.common.next"),this._handleNext,this._handleToday,this.hass.localize("ui.components.calendar.today"),e,this._activeView,this._handleView):(0,m.dy)(o||(o=x(['\n                    <div class="navigation">\n                      <mwc-button\n                        outlined\n                        class="today"\n                        @click=',"\n                        >","</mwc-button\n                      >\n                      <ha-icon-button\n                        label=",'\n                        icon="hass:chevron-left"\n                        class="prev"\n                        @click=',"\n                      >\n                      </ha-icon-button>\n                      <ha-icon-button\n                        label=",'\n                        icon="hass:chevron-right"\n                        class="next"\n                        @click=',"\n                      >\n                      </ha-icon-button>\n                    </div>\n                    <h1>","</h1>\n                    <ha-button-toggle-group\n                      .buttons=","\n                      .active=","\n                      @value-changed=","\n                    ></ha-button-toggle-group>\n                  "])),this._handleToday,this.hass.localize("ui.components.calendar.today"),this.hass.localize("ui.common.previous"),this._handlePrev,this.hass.localize("ui.common.next"),this._handleNext,this.calendar.view.title,e,this._activeView,this._handleView)):"")}},{kind:"method",key:"willUpdate",value:function(e){if(M(F(n.prototype),"willUpdate",this).call(this,e),this.calendar){e.has("events")&&(this.calendar.removeAllEventSources(),this.calendar.addEventSource(this.events)),e.has("views")&&!this.views.includes(this._activeView)&&(this._activeView=this.initialView&&this.views.includes(this.initialView)?this.initialView:this.views[0],this.calendar.changeView(this._activeView),this._fireViewChanged());var t=e.get("hass");t&&t.language!==this.hass.language&&this.calendar.setOption("locale",this.hass.language)}}},{kind:"method",key:"firstUpdated",value:function(){var e=this,t=Object.assign({},I,{locale:this.hass.language,initialView:this.initialView});t.dateClick=function(t){return e._handleDateClick(t)},t.eventClick=function(t){return e._handleEventClick(t)},this.calendar=new l.faS(this.shadowRoot.getElementById("calendar"),t),this.calendar.render(),this._fireViewChanged()}},{kind:"method",key:"_handleEventClick",value:function(e){"dayGridMonth"===e.view.type&&(this._activeView="dayGridDay",this.calendar.changeView("dayGridDay"),this.calendar.gotoDate(e.event.startStr))}},{kind:"method",key:"_handleDateClick",value:function(e){"dayGridMonth"===e.view.type&&(this._activeView="dayGridDay",this.calendar.changeView("dayGridDay"),this.calendar.gotoDate(e.dateStr))}},{kind:"method",key:"_handleNext",value:function(){this.calendar.next(),this._fireViewChanged()}},{kind:"method",key:"_handlePrev",value:function(){this.calendar.prev(),this._fireViewChanged()}},{kind:"method",key:"_handleToday",value:function(){this.calendar.today(),this._fireViewChanged()}},{kind:"method",key:"_handleView",value:function(e){this._activeView=e.detail.value,this.calendar.changeView(this._activeView),this._fireViewChanged()}},{kind:"method",key:"_fireViewChanged",value:function(){(0,g.B)(this,"view-changed",{start:this.calendar.view.activeStart,end:this.calendar.view.activeEnd,view:this.calendar.view.type})}},{kind:"field",key:"_viewToggleButtons",value:function(){return(0,w.Z)((function(e){return B.filter((function(t){return e.includes(t.value)}))}))}},{kind:"get",static:!0,key:"styles",value:function(){return[k.Qx,(0,m.iv)(c||(c=x(["\n        ","\n        ","\n        ",'\n\n        :host {\n          display: flex;\n          flex-direction: column;\n          --fc-theme-standard-border-color: var(--divider-color);\n        }\n\n        .header {\n          display: flex;\n          align-items: center;\n          justify-content: space-between;\n          padding-bottom: 8px;\n        }\n\n        :host([narrow]) .header {\n          padding-right: 8px;\n          padding-left: 8px;\n          flex-direction: column;\n          align-items: flex-start;\n          justify-content: initial;\n        }\n\n        .navigation {\n          display: flex;\n          align-items: center;\n          flex-grow: 0;\n        }\n\n        a {\n          color: var(--primary-text-color);\n        }\n\n        .controls {\n          display: flex;\n          justify-content: space-between;\n          align-items: center;\n          width: 100%;\n        }\n\n        .today {\n          margin-right: 20px;\n        }\n\n        .prev,\n        .next {\n          --mdc-icon-button-size: 32px;\n        }\n\n        ha-button-toggle-group {\n          color: var(--primary-color);\n        }\n\n        #calendar {\n          flex-grow: 1;\n          background-color: var(\n            --ha-card-background,\n            var(--card-background-color, white)\n          );\n          min-height: 400px;\n          --fc-neutral-bg-color: var(\n            --ha-card-background,\n            var(--card-background-color, white)\n          );\n          --fc-list-event-hover-bg-color: var(\n            --ha-card-background,\n            var(--card-background-color, white)\n          );\n          --fc-theme-standard-border-color: var(--divider-color);\n          --fc-border-color: var(--divider-color);\n        }\n\n        a {\n          color: inherit !important;\n        }\n\n        .fc-theme-standard .fc-scrollgrid {\n          border: 1px solid var(--divider-color);\n        }\n\n        .fc-scrollgrid-section-header td {\n          border: none;\n        }\n\n        th.fc-col-header-cell.fc-day {\n          color: var(--secondary-text-color);\n          font-size: 11px;\n          font-weight: 400;\n          text-transform: uppercase;\n        }\n\n        .fc-daygrid-dot-event:hover {\n          background-color: inherit;\n        }\n\n        .fc-daygrid-day-top {\n          text-align: center;\n          padding-top: 5px;\n          justify-content: center;\n        }\n\n        table.fc-scrollgrid-sync-table\n          tbody\n          tr:first-child\n          .fc-daygrid-day-top {\n          padding-top: 0;\n        }\n\n        a.fc-daygrid-day-number {\n          float: none !important;\n          font-size: 12px;\n        }\n\n        .fc .fc-daygrid-day-number {\n          padding: 3px !important;\n        }\n\n        .fc .fc-daygrid-day.fc-day-today {\n          background: inherit;\n        }\n\n        td.fc-day-today .fc-daygrid-day-top {\n          padding-top: 4px;\n        }\n\n        td.fc-day-today .fc-daygrid-day-number {\n          height: 24px;\n          color: var(--text-primary-color) !important;\n          background-color: var(--primary-color);\n          border-radius: 50%;\n          display: inline-block;\n          text-align: center;\n          white-space: nowrap;\n          width: max-content;\n          min-width: 24px;\n          line-height: 140%;\n        }\n\n        .fc-daygrid-day-events {\n          margin-top: 4px;\n        }\n\n        .fc-event {\n          border-radius: 4px;\n          line-height: 1.7;\n        }\n\n        .fc-daygrid-block-event .fc-event-main {\n          padding: 0 1px;\n        }\n\n        .fc-day-past .fc-daygrid-day-events {\n          opacity: 0.5;\n        }\n\n        .fc-icon-x:before {\n          font-family: var(--material-font-family);\n          content: "X";\n        }\n\n        .fc-popover {\n          background-color: var(--primary-background-color) !important;\n        }\n\n        .fc-popover-header {\n          background-color: var(--secondary-background-color) !important;\n        }\n\n        .fc-theme-standard .fc-list-day-frame {\n          background-color: transparent;\n        }\n\n        .fc-list.fc-view,\n        .fc-list-event.fc-event td {\n          border: none;\n        }\n\n        .fc-list-day.fc-day th {\n          border-bottom: none;\n          border-top: 1px solid var(--fc-theme-standard-border-color, #ddd) !important;\n        }\n\n        .fc-list-day-text {\n          font-size: 16px;\n          font-weight: 400;\n        }\n\n        .fc-list-day-side-text {\n          font-weight: 400;\n          font-size: 16px;\n          color: var(--primary-color);\n        }\n\n        .fc-list-table td,\n        .fc-list-day-frame {\n          padding-top: 12px;\n          padding-bottom: 12px;\n        }\n\n        :host([narrow])\n          .fc-dayGridMonth-view\n          .fc-daygrid-dot-event\n          .fc-event-time,\n        :host([narrow])\n          .fc-dayGridMonth-view\n          .fc-daygrid-dot-event\n          .fc-event-title,\n        :host([narrow]) .fc-dayGridMonth-view .fc-daygrid-day-bottom {\n          display: none;\n        }\n\n        :host([narrow])\n          .fc\n          .fc-dayGridMonth-view\n          .fc-daygrid-event-harness-abs {\n          visibility: visible !important;\n          position: static;\n        }\n\n        :host([narrow]) .fc-dayGridMonth-view .fc-daygrid-day-events {\n          display: flex;\n          min-height: 2em !important;\n          justify-content: center;\n          flex-wrap: wrap;\n          max-height: 2em;\n          height: 2em;\n          overflow: hidden;\n        }\n\n        :host([narrow]) .fc-dayGridMonth-view .fc-scrollgrid-sync-table {\n          overflow: hidden;\n        }\n\n        .fc-scroller::-webkit-scrollbar {\n          width: 0.4rem;\n          height: 0.4rem;\n        }\n\n        .fc-scroller::-webkit-scrollbar-thumb {\n          -webkit-border-radius: 4px;\n          border-radius: 4px;\n          background: var(--scrollbar-thumb-color);\n        }\n\n        .fc-scroller {\n          overflow-y: auto;\n          scrollbar-color: var(--scrollbar-thumb-color) transparent;\n          scrollbar-width: thin;\n        }\n      '])),(0,m.$m)(s.Z),(0,m.$m)(f.Z),(0,m.$m)(v.Z))]}}]}}),m.oi);window.customElements.define("ha-full-calendar",Z)}}]);
//# sourceMappingURL=chunk.e72018663b94d14c150e.js.map