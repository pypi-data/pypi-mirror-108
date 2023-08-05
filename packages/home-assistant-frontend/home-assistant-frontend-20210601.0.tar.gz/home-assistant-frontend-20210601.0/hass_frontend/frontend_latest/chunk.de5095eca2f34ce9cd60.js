/*! For license information please see chunk.de5095eca2f34ce9cd60.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6294],{6294:(t,e,n)=>{"use strict";var o,i=n(99525),s=n(55704),r=(n(62613),n(59799),{MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"}),l={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected"},d={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(o||(o={}));var a=n(87480),c=n(72774),u=n(74015),m=n(6945);const p=function(t){function e(n){var i=t.call(this,(0,a.__assign)((0,a.__assign)({},e.defaultAdapter),n))||this;return i.closeAnimationEndTimerId=0,i.defaultFocusState=o.LIST_ROOT,i}return(0,a.__extends)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return r},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return l},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return d},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,n=t.keyCode;("Tab"===e||9===n)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,n=this.adapter.getElementIndex(t);n<0||(this.adapter.notifySelected({index:n}),this.adapter.closeSurface(),this.closeAnimationEndTimerId=setTimeout((function(){var n=e.adapter.getElementIndex(t);n>=0&&e.adapter.isSelectableItemAtIndex(n)&&e.setSelectedIndex(n)}),m.k.numbers.TRANSITION_CLOSE_DURATION))},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case o.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case o.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case o.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState=t},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,l.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,r.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,r.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,l.ARIA_CHECKED_ATTR,"true")},e.prototype.setEnabled=function(t,e){this.validatedIndex(t),e?(this.adapter.removeClassFromElementAtIndex(t,u.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,l.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,u.UX.LIST_ITEM_DISABLED_CLASS),this.adapter.addAttributeToElementAtIndex(t,l.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(c.K);var h=n(78220),f=n(14114);class I extends h.H{constructor(){super(...arguments),this.mdcFoundationClass=p,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){const t="menu"===this.innerRole?"menuitem":"option";return s.dy`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-deprecated-list"
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!o.selected&&n.toggle(t,!0):o.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&("mdc-menu-item--selected"===e?o.selected&&n.toggle(t,!1):o.classList.remove(e))},addAttributeToElementAtIndex:(t,e,n)=>{const o=this.listElement;if(!o)return;const i=o.items[t];i&&i.setAttribute(e,n)},removeAttributeFromElementAtIndex:(t,e)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&o.removeAttribute(e)},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const n=e.items[t];n&&n.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const n=e.items[t];if(!n||!n.group)return-1;for(let o=0;o<e.items.length;o++){if(o===t)continue;const i=e.items[o];if(i.selected&&i.group===n.group)return o}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const n=e.items[t];return!!n&&n.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const n=t.detail.index,o=e.items[n];o&&this.mdcFoundation.handleItemAction(o)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async _getUpdateComplete(){return this.getUpdateComplete()}async getUpdateComplete(){let t=!1;return await this._listUpdateComplete,super.getUpdateComplete?t=await super.getUpdateComplete():await super._getUpdateComplete(),t}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}(0,i.gn)([(0,s.IO)(".mdc-menu")],I.prototype,"mdcRoot",void 0),(0,i.gn)([(0,s.IO)("slot")],I.prototype,"slotElement",void 0),(0,i.gn)([(0,s.Cb)({type:Object})],I.prototype,"anchor",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean,reflect:!0})],I.prototype,"open",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"quick",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"wrapFocus",void 0),(0,i.gn)([(0,s.Cb)({type:String})],I.prototype,"innerRole",void 0),(0,i.gn)([(0,s.Cb)({type:String})],I.prototype,"corner",void 0),(0,i.gn)([(0,s.Cb)({type:Number})],I.prototype,"x",void 0),(0,i.gn)([(0,s.Cb)({type:Number})],I.prototype,"y",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"absolute",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"multi",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"activatable",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"fixed",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"forceGroupSelection",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"fullwidth",void 0),(0,i.gn)([(0,s.Cb)({type:String})],I.prototype,"menuCorner",void 0),(0,i.gn)([(0,s.Cb)({type:Boolean})],I.prototype,"stayOpenOnBodyClick",void 0),(0,i.gn)([(0,s.Cb)({type:String}),(0,f.P)((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(o[t])}))],I.prototype,"defaultFocus",void 0);const E=s.iv`mwc-list ::slotted([mwc-list-item]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let A=class extends I{};A.styles=E,A=(0,i.gn)([(0,s.Mo)("mwc-menu")],A)}}]);
//# sourceMappingURL=chunk.de5095eca2f34ce9cd60.js.map