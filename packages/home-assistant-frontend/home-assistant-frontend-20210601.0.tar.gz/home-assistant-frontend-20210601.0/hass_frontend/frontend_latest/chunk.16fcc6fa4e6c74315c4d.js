(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8116],{98251:(e,t)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0});const n=new WeakMap,r=new WeakMap;function o(e){const t=n.get(e);return console.assert(null!=t,"'this' is expected an Event object, but got",e),t}function l(e){null==e.passiveListener?e.event.cancelable&&(e.canceled=!0,"function"==typeof e.event.preventDefault&&e.event.preventDefault()):"undefined"!=typeof console&&"function"==typeof console.error&&console.error("Unable to preventDefault inside passive event listener invocation.",e.passiveListener)}function i(e,t){n.set(this,{eventTarget:e,event:t,eventPhase:2,currentTarget:e,canceled:!1,stopped:!1,immediateStopped:!1,passiveListener:null,timeStamp:t.timeStamp||Date.now()}),Object.defineProperty(this,"isTrusted",{value:!1,enumerable:!0});const r=Object.keys(t);for(let e=0;e<r.length;++e){const t=r[e];t in this||Object.defineProperty(this,t,s(t))}}function s(e){return{get(){return o(this).event[e]},set(t){o(this).event[e]=t},configurable:!0,enumerable:!0}}function u(e){return{value(){const t=o(this).event;return t[e].apply(t,arguments)},configurable:!0,enumerable:!0}}function a(e){if(null==e||e===Object.prototype)return i;let t=r.get(e);return null==t&&(t=function(e,t){const n=Object.keys(t);if(0===n.length)return e;function r(t,n){e.call(this,t,n)}r.prototype=Object.create(e.prototype,{constructor:{value:r,configurable:!0,writable:!0}});for(let o=0;o<n.length;++o){const l=n[o];if(!(l in e.prototype)){const e="function"==typeof Object.getOwnPropertyDescriptor(t,l).value;Object.defineProperty(r.prototype,l,e?u(l):s(l))}}return r}(a(Object.getPrototypeOf(e)),e),r.set(e,t)),t}function c(e){return o(e).immediateStopped}function p(e,t){o(e).passiveListener=t}i.prototype={get type(){return o(this).event.type},get target(){return o(this).eventTarget},get currentTarget(){return o(this).currentTarget},composedPath(){const e=o(this).currentTarget;return null==e?[]:[e]},get NONE(){return 0},get CAPTURING_PHASE(){return 1},get AT_TARGET(){return 2},get BUBBLING_PHASE(){return 3},get eventPhase(){return o(this).eventPhase},stopPropagation(){const e=o(this);e.stopped=!0,"function"==typeof e.event.stopPropagation&&e.event.stopPropagation()},stopImmediatePropagation(){const e=o(this);e.stopped=!0,e.immediateStopped=!0,"function"==typeof e.event.stopImmediatePropagation&&e.event.stopImmediatePropagation()},get bubbles(){return Boolean(o(this).event.bubbles)},get cancelable(){return Boolean(o(this).event.cancelable)},preventDefault(){l(o(this))},get defaultPrevented(){return o(this).canceled},get composed(){return Boolean(o(this).event.composed)},get timeStamp(){return o(this).timeStamp},get srcElement(){return o(this).eventTarget},get cancelBubble(){return o(this).stopped},set cancelBubble(e){if(!e)return;const t=o(this);t.stopped=!0,"boolean"==typeof t.event.cancelBubble&&(t.event.cancelBubble=!0)},get returnValue(){return!o(this).canceled},set returnValue(e){e||l(o(this))},initEvent(){}},Object.defineProperty(i.prototype,"constructor",{value:i,configurable:!0,writable:!0}),"undefined"!=typeof window&&void 0!==window.Event&&(Object.setPrototypeOf(i.prototype,window.Event.prototype),r.set(window.Event.prototype,i));const f=new WeakMap;function v(e){return null!==e&&"object"==typeof e}function d(e){const t=f.get(e);if(null==t)throw new TypeError("'this' is expected an EventTarget object, but got another value.");return t}function y(e,t){Object.defineProperty(e,`on${t}`,function(e){return{get(){let t=d(this).get(e);for(;null!=t;){if(3===t.listenerType)return t.listener;t=t.next}return null},set(t){"function"==typeof t||v(t)||(t=null);const n=d(this);let r=null,o=n.get(e);for(;null!=o;)3===o.listenerType?null!==r?r.next=o.next:null!==o.next?n.set(e,o.next):n.delete(e):r=o,o=o.next;if(null!==t){const o={listener:t,listenerType:3,passive:!1,once:!1,next:null};null===r?n.set(e,o):r.next=o}},configurable:!0,enumerable:!0}}(t))}function g(e){function t(){h.call(this)}t.prototype=Object.create(h.prototype,{constructor:{value:t,configurable:!0,writable:!0}});for(let n=0;n<e.length;++n)y(t.prototype,e[n]);return t}function h(){if(!(this instanceof h)){if(1===arguments.length&&Array.isArray(arguments[0]))return g(arguments[0]);if(arguments.length>0){const e=new Array(arguments.length);for(let t=0;t<arguments.length;++t)e[t]=arguments[t];return g(e)}throw new TypeError("Cannot call a class as a function")}f.set(this,new Map)}h.prototype={addEventListener(e,t,n){if(null==t)return;if("function"!=typeof t&&!v(t))throw new TypeError("'listener' should be a function or an object.");const r=d(this),o=v(n),l=(o?Boolean(n.capture):Boolean(n))?1:2,i={listener:t,listenerType:l,passive:o&&Boolean(n.passive),once:o&&Boolean(n.once),next:null};let s=r.get(e);if(void 0===s)return void r.set(e,i);let u=null;for(;null!=s;){if(s.listener===t&&s.listenerType===l)return;u=s,s=s.next}u.next=i},removeEventListener(e,t,n){if(null==t)return;const r=d(this),o=(v(n)?Boolean(n.capture):Boolean(n))?1:2;let l=null,i=r.get(e);for(;null!=i;){if(i.listener===t&&i.listenerType===o)return void(null!==l?l.next=i.next:null!==i.next?r.set(e,i.next):r.delete(e));l=i,i=i.next}},dispatchEvent(e){if(null==e||"string"!=typeof e.type)throw new TypeError('"event.type" should be a string.');const t=d(this),n=e.type;let r=t.get(n);if(null==r)return!0;const l=function(e,t){return new(a(Object.getPrototypeOf(t)))(e,t)}(this,e);let i=null;for(;null!=r;){if(r.once?null!==i?i.next=r.next:null!==r.next?t.set(n,r.next):t.delete(n):i=r,p(l,r.passive?r.listener:null),"function"==typeof r.listener)try{r.listener.call(this,l)}catch(e){"undefined"!=typeof console&&"function"==typeof console.error&&console.error(e)}else 3!==r.listenerType&&"function"==typeof r.listener.handleEvent&&r.listener.handleEvent(l);if(c(l))break;r=r.next}return p(l,null),function(e,t){o(e).eventPhase=t}(l,0),function(e,t){o(e).currentTarget=t}(l,null),!l.defaultPrevented}},Object.defineProperty(h.prototype,"constructor",{value:h,configurable:!0,writable:!0}),"undefined"!=typeof window&&void 0!==window.EventTarget&&Object.setPrototypeOf(h.prototype,window.EventTarget.prototype),t.defineEventAttribute=y,t.EventTarget=h,t.default=h,e.exports=h,e.exports.EventTarget=e.exports.default=h,e.exports.defineEventAttribute=y}}]);
//# sourceMappingURL=chunk.16fcc6fa4e6c74315c4d.js.map