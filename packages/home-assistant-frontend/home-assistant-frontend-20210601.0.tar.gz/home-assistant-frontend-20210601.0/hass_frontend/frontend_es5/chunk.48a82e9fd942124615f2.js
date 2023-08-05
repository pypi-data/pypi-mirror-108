/*! For license information please see chunk.48a82e9fd942124615f2.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7895],{87895:function(e,t,n){"use strict";function r(e){return(r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}n.d(t,{r:function(){return T}});function o(e,t,n,o){var i,c=arguments.length,a=c<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,n):o;if("object"===("undefined"==typeof Reflect?"undefined":r(Reflect))&&"function"==typeof Reflect.decorate)a=Reflect.decorate(e,t,n,o);else for(var s=e.length-1;s>=0;s--)(i=e[s])&&(a=(c<3?i(a):c>3?i(t,n,a):i(t,n))||a);return c>3&&a&&Object.defineProperty(t,n,a),a}Object.create;Object.create;var i,c,a=n(55704),s=(n(66702),n(38103)),l=n(18601),u=n(14114),d=n(98734),p=n(87480),h=n(72774),f={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},b={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"},m=function(e){function t(n){return e.call(this,(0,p.__assign)((0,p.__assign)({},t.defaultAdapter),n))||this}return(0,p.__extends)(t,e),Object.defineProperty(t,"strings",{get:function(){return b},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return f},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(f.DISABLED):this.adapter.removeClass(f.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(f.CHECKED):this.adapter.removeClass(f.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(b.ARIA_CHECKED_ATTR,""+!!e)},t}(h.K),y=n(49629);function v(e){return(v="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function w(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function _(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function k(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function g(e,t){return(g=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function R(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=x(e);if(t){var o=x(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return C(this,n)}}function C(e,t){return!t||"object"!==v(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function x(e){return(x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var O,E=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&g(e,t)}(s,e);var t,n,r,o=R(s);function s(){var e;return _(this,s),(e=o.apply(this,arguments)).checked=!1,e.disabled=!1,e.shouldRenderRipple=!1,e.mdcFoundationClass=m,e.rippleHandlers=new d.A((function(){return e.shouldRenderRipple=!0,e.ripple})),e}return t=s,(n=[{key:"changeHandler",value:function(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}},{key:"createAdapter",value:function(){var e=this;return Object.assign(Object.assign({},(0,l.qN)(this.mdcRoot)),{setNativeControlChecked:function(t){e.formElement.checked=t},setNativeControlDisabled:function(t){e.formElement.disabled=t},setNativeControlAttr:function(t,n){e.formElement.setAttribute(t,n)}})}},{key:"renderRipple",value:function(){return this.shouldRenderRipple?(0,a.dy)(i||(i=w(['\n        <mwc-ripple\n          .accent="','"\n          .disabled="','"\n          unbounded>\n        </mwc-ripple>'])),this.checked,this.disabled):""}},{key:"focus",value:function(){var e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}},{key:"blur",value:function(){var e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}},{key:"render",value:function(){return(0,a.dy)(c||(c=w(['\n      <div class="mdc-switch">\n        <div class="mdc-switch__track"></div>\n        <div class="mdc-switch__thumb-underlay">\n          ','\n          <div class="mdc-switch__thumb">\n            <input\n              type="checkbox"\n              id="basic-switch"\n              class="mdc-switch__native-control"\n              role="switch"\n              aria-label="','"\n              aria-labelledby="','"\n              @change="','"\n              @focus="','"\n              @blur="','"\n              @mousedown="','"\n              @mouseenter="','"\n              @mouseleave="','"\n              @touchstart="','"\n              @touchend="','"\n              @touchcancel="','">\n          </div>\n        </div>\n      </div>'])),this.renderRipple(),(0,y.o)(this.ariaLabel),(0,y.o)(this.ariaLabelledBy),this.changeHandler,this.handleRippleFocus,this.handleRippleBlur,this.handleRippleMouseDown,this.handleRippleMouseEnter,this.handleRippleMouseLeave,this.handleRippleTouchStart,this.handleRippleDeactivate,this.handleRippleDeactivate)}},{key:"handleRippleMouseDown",value:function(e){var t=this;window.addEventListener("mouseup",(function e(){window.removeEventListener("mouseup",e),t.handleRippleDeactivate()})),this.rippleHandlers.startPress(e)}},{key:"handleRippleTouchStart",value:function(e){this.rippleHandlers.startPress(e)}},{key:"handleRippleDeactivate",value:function(){this.rippleHandlers.endPress()}},{key:"handleRippleMouseEnter",value:function(){this.rippleHandlers.startHover()}},{key:"handleRippleMouseLeave",value:function(){this.rippleHandlers.endHover()}},{key:"handleRippleFocus",value:function(){this.rippleHandlers.startFocus()}},{key:"handleRippleBlur",value:function(){this.rippleHandlers.endFocus()}}])&&k(t.prototype,n),r&&k(t,r),s}(l.Wg);o([(0,a.Cb)({type:Boolean}),(0,u.P)((function(e){this.mdcFoundation.setChecked(e)}))],E.prototype,"checked",void 0),o([(0,a.Cb)({type:Boolean}),(0,u.P)((function(e){this.mdcFoundation.setDisabled(e)}))],E.prototype,"disabled",void 0),o([s.L,(0,a.Cb)({attribute:"aria-label"})],E.prototype,"ariaLabel",void 0),o([s.L,(0,a.Cb)({attribute:"aria-labelledby"})],E.prototype,"ariaLabelledBy",void 0),o([(0,a.IO)(".mdc-switch")],E.prototype,"mdcRoot",void 0),o([(0,a.IO)("input")],E.prototype,"formElement",void 0),o([(0,a.GC)("mwc-ripple")],E.prototype,"ripple",void 0),o([(0,a.SB)()],E.prototype,"shouldRenderRipple",void 0),o([(0,a.hO)({passive:!0})],E.prototype,"handleRippleMouseDown",null),o([(0,a.hO)({passive:!0})],E.prototype,"handleRippleTouchStart",null);var j=(0,a.iv)(O||(O=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}([".mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}"])));function S(e){return(S="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function P(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function D(e,t){return(D=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function A(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=L(e);if(t){var o=L(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return H(this,n)}}function H(e,t){return!t||"object"!==S(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function L(e){return(L=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var T=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&D(e,t)}(n,e);var t=A(n);function n(){return P(this,n),t.apply(this,arguments)}return n}(E);T.styles=j,T=o([(0,a.Mo)("mwc-switch")],T)}}]);
//# sourceMappingURL=chunk.48a82e9fd942124615f2.js.map