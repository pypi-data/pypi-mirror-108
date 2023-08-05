!(function (e) {
  var t = {};
  function o(n) {
    if (t[n]) return t[n].exports;
    var r = (t[n] = { i: n, l: !1, exports: {} });
    return e[n].call(r.exports, r, r.exports, o), (r.l = !0), r.exports;
  }
  (o.m = e),
    (o.c = t),
    (o.d = function (e, t, n) {
      o.o(e, t) || Object.defineProperty(e, t, { enumerable: !0, get: n });
    }),
    (o.r = function (e) {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(e, "__esModule", { value: !0 });
    }),
    (o.t = function (e, t) {
      if ((1 & t && (e = o(e)), 8 & t)) return e;
      if (4 & t && "object" == typeof e && e && e.__esModule) return e;
      var n = Object.create(null);
      if (
        (o.r(n),
        Object.defineProperty(n, "default", { enumerable: !0, value: e }),
        2 & t && "string" != typeof e)
      )
        for (var r in e)
          o.d(
            n,
            r,
            function (t) {
              return e[t];
            }.bind(null, r)
          );
      return n;
    }),
    (o.n = function (e) {
      var t =
        e && e.__esModule
          ? function () {
              return e.default;
            }
          : function () {
              return e;
            };
      return o.d(t, "a", t), t;
    }),
    (o.o = function (e, t) {
      return Object.prototype.hasOwnProperty.call(e, t);
    }),
    (o.p = ""),
    o((o.s = 1));
})([
  function (e) {
    e.exports = JSON.parse(
      '{"name":"card-mod","private":true,"version":"2.0.2","description":"","scripts":{"build":"webpack","watch":"webpack --watch --mode=development","update-card-tools":"npm uninstall card-tools && npm install thomasloven/lovelace-card-tools"},"keywords":[],"author":"Thomas Lovén","license":"MIT","devDependencies":{"webpack":"^4.44.2","webpack-cli":"^3.3.12"},"dependencies":{"card-tools":"github:thomasloven/lovelace-card-tools"}}'
    );
  },
  function (e, t, o) {
    "use strict";
    o.r(t);
    const n = customElements.get("home-assistant-main")
        ? Object.getPrototypeOf(customElements.get("home-assistant-main"))
        : Object.getPrototypeOf(customElements.get("hui-view")),
      r = n.prototype.html;
    n.prototype.css;
    function a() {
      return document.querySelector("hc-main")
        ? document.querySelector("hc-main").hass
        : document.querySelector("home-assistant")
        ? document.querySelector("home-assistant").hass
        : void 0;
    }
    const s = "lovelace-player-device-id";
    function i() {
      if (!localStorage[s]) {
        const e = () =>
          Math.floor(1e5 * (1 + Math.random()))
            .toString(16)
            .substring(1);
        window.fully && "function" == typeof fully.getDeviceId
          ? (localStorage[s] = fully.getDeviceId())
          : (localStorage[s] = `${e()}${e()}-${e()}${e()}`);
      }
      return localStorage[s];
    }
    let l = i();
    const c = new URLSearchParams(window.location.search);
    var d;
    c.get("deviceID") &&
      null !== (d = c.get("deviceID")) &&
      ("clear" === d ? localStorage.removeItem(s) : (localStorage[s] = d),
      (l = i()));
    const p = async (e) => {
      await (async () => {
        if (customElements.get("developer-tools-event")) return;
        await customElements.whenDefined("partial-panel-resolver");
        const e = document.createElement("partial-panel-resolver");
        (e.hass = {
          panels: [{ url_path: "tmp", component_name: "developer-tools" }],
        }),
          e._updateRoutes(),
          await e.routerOptions.routes.tmp.load(),
          await customElements.whenDefined("developer-tools-router");
        const t = document.createElement("developer-tools-router");
        await t.routerOptions.routes.event.load();
      })();
      return document
        .createElement("developer-tools-event")
        ._computeParsedEventData(e);
    };
    async function u(e, t, o = !1) {
      let n = e;
      "string" == typeof t && (t = t.split(/(\$| )/)),
        "" === t[t.length - 1] && t.pop();
      for (const [e, r] of t.entries())
        if (r.trim().length) {
          if (!n) return null;
          n.localName &&
            n.localName.includes("-") &&
            (await customElements.whenDefined(n.localName)),
            n.updateComplete && (await n.updateComplete),
            (n =
              "$" === r
                ? o && e == t.length - 1
                  ? [n.shadowRoot]
                  : n.shadowRoot
                : o && e == t.length - 1
                ? n.querySelectorAll(r)
                : n.querySelector(r));
        }
      return n;
    }
    async function h(e, t, o = !1, n = 1e4) {
      return Promise.race([
        u(e, t, o),
        new Promise((e, t) => setTimeout(() => t(new Error("timeout")), n)),
      ]).catch((e) => {
        if (!e.message || "timeout" !== e.message) throw e;
        return null;
      });
    }
    const m = { template: "", variables: {}, entity_ids: [] },
      y = async (e, t, o, n, r, a = !0) => {
        e.localName.includes("-") &&
          (await customElements.whenDefined(e.localName)),
          e.updateComplete && (await e.updateComplete),
          (e._cardMod = e._cardMod || document.createElement("card-mod"));
        ((a && e.shadowRoot) || e).appendChild(e._cardMod),
          e.updateComplete && (await e.updateComplete),
          (e._cardMod.type = t),
          (e._cardMod.template = { template: o, variables: n, entity_ids: r });
      };
    class f extends n {
      static get properties() {
        return { _renderedStyles: {}, _renderer: {} };
      }
      static get applyToElement() {
        return y;
      }
      constructor() {
        super(),
          document
            .querySelector("home-assistant")
            .addEventListener("settheme", () => {
              this._setTemplate(this._data);
            });
      }
      connectedCallback() {
        super.connectedCallback(),
          (this.template = this._data),
          this.setAttribute("slot", "none");
      }
      async getTheme() {
        if (!this.type) return null;
        let e = this.parentElement ? this.parentElement : this;
        const t = window
            .getComputedStyle(e)
            .getPropertyValue("--card-mod-theme"),
          o = a().themes.themes;
        return o[t]
          ? o[t][`card-mod-${this.type}-yaml`]
            ? await p(o[t][`card-mod-${this.type}-yaml`])
            : o[t]["card-mod-" + this.type]
            ? o[t]["card-mod-" + this.type]
            : null
          : null;
      }
      set template(e) {
        e &&
          ((this._data = JSON.parse(JSON.stringify(e))),
          (this.themeApplied = this._setTemplate(this._data)));
      }
      async _setTemplate(e) {
        this._parent ||
          ((e.theme_template = await this.getTheme()),
          "string" == typeof e.template && (e.template = { ".": e.template }),
          "string" == typeof e.theme_template &&
            (e.theme_template = { ".": e.theme_template })),
          await this.setStyle(e);
      }
      async unStyle() {
        this._styledChildren = this._styledChildren || new Set();
        for (const e of this._styledChildren) e.template = m;
      }
      _mergeDeep(e, t) {
        const o = (e) => e && "object" == typeof e && !Array.isArray(e);
        if (o(e) && o(t))
          for (const n in t)
            o(t[n])
              ? (e[n] || Object.assign(e, { [n]: {} }),
                "string" == typeof e[n] && (e[n] = { ".": e[n] }),
                this._mergeDeep(e[n], t[n]))
              : e[n]
              ? (e[n] = t[n] + e[n])
              : (e[n] = t[n]);
        return e;
      }
      async setStyle(e) {
        let { template: t, theme_template: o, variables: n, entity_ids: r } = e;
        if (
          (await this.unStyle(),
          t || (t = {}),
          (t = JSON.parse(JSON.stringify(t))),
          this._mergeDeep(t, o),
          "string" == typeof t)
        ) {
          if (((this._renderedStyles = t), this._renderer)) {
            try {
              await this._renderer();
            } catch (e) {
              if (!e.code || "not_found" !== e.code) throw e;
            }
            this._renderer = void 0;
          }
          return (
            (s = t),
            void (
              (String(s).includes("{%") || String(s).includes("{{")) &&
              (this._renderer = await (function (e, t, o) {
                e || (e = a().connection);
                let n = {
                    user: a().user.name,
                    browser: l,
                    hash: location.hash.substr(1) || " ",
                    ...o.variables,
                  },
                  r = o.template,
                  s = o.entity_ids;
                return e.subscribeMessage(
                  (e) => {
                    let o = e.result;
                    (o = o.replace(
                      /_\([^)]*\)/g,
                      (e) => a().localize(e.substring(2, e.length - 1)) || e
                    )),
                      t(o);
                  },
                  {
                    type: "render_template",
                    template: r,
                    variables: n,
                    entity_ids: s,
                  }
                );
              })(
                null,
                (e) => {
                  this._renderedStyles = e;
                },
                { template: t, variables: n }
              ))
            )
          );
        }
        var s;
        await this.updateComplete;
        const i = this.parentElement || this.parentNode;
        if (!i) return { template: "", variable: variable, entity_ids: r };
        i.updateComplete && (await i.updateComplete);
        for (const e of Object.keys(t)) {
          let o = [];
          if ("." !== e) {
            if (((o = await h(i, e, !0)), o.length))
              for (const a of o) {
                if (!a) continue;
                let o = a.querySelector(":scope > card-mod");
                (o && o._parent === (this._parent || this)) ||
                  ((o = document.createElement("card-mod")),
                  this._styledChildren.add(o),
                  (o._parent = this._parent || this)),
                  (o.template = {
                    template: t[e],
                    variables: n,
                    entity_ids: r,
                  }),
                  a.appendChild(o),
                  await o.themeApplied;
              }
          } else this.setStyle({ template: t[e], variables: n, entity_ids: r });
        }
      }
      createRenderRoot() {
        return this;
      }
      render() {
        return r`
      <style>
        ${this._renderedStyles}
      </style>
    `;
      }
    }
    if (!customElements.get("card-mod")) {
      customElements.define("card-mod", f);
      const e = o(0);
      console.info(
        `%cCARD-MOD ${e.version} IS INSTALLED`,
        "color: green; font-weight: bold",
        ""
      );
    }
    function g(e, t, o = null) {
      if (
        (((e = new Event(e, {
          bubbles: !0,
          cancelable: !1,
          composed: !0,
        })).detail = t || {}),
        o)
      )
        o.dispatchEvent(e);
      else {
        var n = (function () {
          var e = document.querySelector("hc-main");
          return (e = e
            ? ((e =
                (e =
                  (e = e && e.shadowRoot) && e.querySelector("hc-lovelace")) &&
                e.shadowRoot) &&
                e.querySelector("hui-view")) ||
              e.querySelector("hui-panel-view")
            : (e =
                (e =
                  (e =
                    (e =
                      (e =
                        (e =
                          (e =
                            ((e =
                              (e =
                                (e =
                                  (e =
                                    (e = document.querySelector(
                                      "home-assistant"
                                    )) && e.shadowRoot) &&
                                  e.querySelector("home-assistant-main")) &&
                                e.shadowRoot) &&
                              e.querySelector(
                                "app-drawer-layout partial-panel-resolver"
                              )) &&
                              e.shadowRoot) ||
                            e) && e.querySelector("ha-panel-lovelace")) &&
                        e.shadowRoot) && e.querySelector("hui-root")) &&
                    e.shadowRoot) && e.querySelector("ha-app-layout")) &&
                e.querySelector("#view")) && e.firstElementChild);
        })();
        n && n.dispatchEvent(e);
      }
    }
    customElements.whenDefined("ha-card").then(() => {
      const e = customElements.get("ha-card");
      if (e.prototype.cardmod_patched) return;
      e.prototype.cardmod_patched = !0;
      const t = function (e) {
          return e.config
            ? e.config
            : e._config
            ? e._config
            : e.host
            ? t(e.host)
            : e.parentElement
            ? t(e.parentElement)
            : e.parentNode
            ? t(e.parentNode)
            : null;
        },
        o = e.prototype.firstUpdated;
      (e.prototype.firstUpdated = function () {
        o && o();
        const e = this.shadowRoot.querySelector(".card-header");
        e && this.insertBefore(e, this.children[0]);
        const n = t(this);
        if (!n) return;
        n.class && this.classList.add(n.class),
          n.type && this.classList.add("type-" + n.type.replace(":", "-"));
        (() => {
          y(this, "card", n.style, { config: n }, n.entity_ids, !1);
        })();
      }),
        g("ll-rebuild", {});
    }),
      customElements.whenDefined("hui-entities-card").then(() => {
        const e = customElements.get("hui-entities-card");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.renderEntity;
        (e.prototype.renderEntity = function (e) {
          const o = t.bind(this)(e);
          if (!e) return o;
          if (!o || !o.values) return o;
          const n = o.values[0];
          if (!n) return o;
          e.entity_ids;
          e.class && n.classList.add(e.class);
          const r = () => y(n, "row", e.style, { config: e }, e.entity_ids);
          return (
            r(), o.values[0] && o.values[0].addEventListener("ll-rebuild", r), o
          );
        }),
          g("ll-rebuild", {});
      }),
      customElements.whenDefined("hui-glance-card").then(() => {
        const e = customElements.get("hui-glance-card");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.firstUpdated;
        (e.prototype.firstUpdated = function () {
          t && t();
          this.shadowRoot
            .querySelectorAll("ha-card div.entity")
            .forEach((e) => {
              const t = e.attachShadow({ mode: "open" });
              [...e.children].forEach((e) => t.appendChild(e));
              const o = document.createElement("style");
              t.appendChild(o),
                (o.innerHTML =
                  "\n      :host {\n        box-sizing: border-box;\n        padding: 0 4px;\n        display: flex;\n        flex-direction: column;\n        align-items: center;\n        cursor: pointer;\n        margin-bottom: 12px;\n        width: var(--glance-column-width, 20%);\n      }\n      div {\n        width: 100%;\n        text-align: center;\n        white-space: nowrap;\n        overflow: hidden;\n        text-overflow: ellipsis;\n      }\n      .name {\n        min-height: var(--paper-font-body1_-_line-height, 20px);\n      }\n      state-badge {\n        margin: 8px 0;\n      }\n      ");
              const n = e.config || e.entityConf;
              if (!n) return;
              n.entity_ids;
              n.class && e.classList.add(n.class);
              y(e, "glance", n.style, { config: n }, n.entity_ids);
            });
        }),
          g("ll-rebuild", {});
      }),
      customElements.whenDefined("hui-state-label-badge").then(() => {
        const e = customElements.get("hui-state-label-badge");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.firstUpdated;
        (e.prototype.firstUpdated = function () {
          t && t();
          const e = this._config;
          if (!e) return;
          e.entity_ids;
          e.class && this.classList.add(e.class);
          (() => {
            y(this, "badge", e.style, { config: e }, e.entity_ids);
          })();
        }),
          g("ll-rebuild", {});
      }),
      customElements.whenDefined("hui-view").then(() => {
        const e = customElements.get("hui-view");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.firstUpdated;
        (e.prototype.firstUpdated = function () {
          t && t();
          (() => {
            y(this, "view", "", {}, []);
          })();
        }),
          g("ll-rebuild", {});
      }),
      customElements.whenDefined("hui-root").then(() => {
        const e = customElements.get("hui-root");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.firstUpdated;
        (e.prototype.firstUpdated = async function () {
          t && t();
          (() => {
            y(this, "root", "", {}, []);
          })();
        }),
          g("ll-rebuild", {});
        let o = document.querySelector("home-assistant");
        (o = o && o.shadowRoot),
          (o = o && o.querySelector("home-assistant-main")),
          (o = o && o.shadowRoot),
          (o =
            o && o.querySelector("app-drawer-layout partial-panel-resolver")),
          (o = o && o.querySelector("ha-panel-lovelace")),
          (o = o && o.shadowRoot),
          (o = o && o.querySelector("hui-root")),
          o && o.firstUpdated();
      }),
      customElements.whenDefined("ha-more-info-dialog").then(() => {
        const e = customElements.get("ha-more-info-dialog");
        if (e.prototype.cardmod_patched) return;
        e.prototype.cardmod_patched = !0;
        const t = e.prototype.showDialog;
        e.prototype.showDialog = function (e) {
          const o = () => {
            y(
              this.shadowRoot.querySelector("ha-dialog"),
              "more-info",
              "",
              { config: e },
              [e.entityId],
              !1
            );
          };
          t.bind(this)(e),
            this.requestUpdate().then(async () => {
              await this.shadowRoot.querySelector("ha-dialog").updateComplete,
                o();
            });
        };
        let o = document.querySelector("home-assistant");
        (o = o && o.shadowRoot),
          (o = o && o.querySelector("ha-more-info-dialog")),
          o &&
            ((o.showDialog = e.prototype.showDialog.bind(o)),
            o.showDialog({ entityId: o.entityId }));
      });
    let w = window.cardHelpers;
    const _ = new Promise(async (e, t) => {
      w && e();
      const o = async () => {
        (w = await window.loadCardHelpers()), (window.cardHelpers = w), e();
      };
      window.loadCardHelpers
        ? o()
        : window.addEventListener("load", async () => {
            !(async function () {
              if (customElements.get("hui-view")) return !0;
              await customElements.whenDefined("partial-panel-resolver");
              const e = document.createElement("partial-panel-resolver");
              if (
                ((e.hass = {
                  panels: [{ url_path: "tmp", component_name: "lovelace" }],
                }),
                e._updateRoutes(),
                await e.routerOptions.routes.tmp.load(),
                !customElements.get("ha-panel-lovelace"))
              )
                return !1;
              const t = document.createElement("ha-panel-lovelace");
              (t.hass = a()),
                void 0 === t.hass &&
                  (await new Promise((e) => {
                    window.addEventListener(
                      "connection-status",
                      (t) => {
                        console.log(t), e();
                      },
                      { once: !0 }
                    );
                  }),
                  (t.hass = a())),
                (t.panel = { config: { mode: null } }),
                t._fetchConfig();
            })(),
              window.loadCardHelpers && o();
          });
    });
    function v(e, t) {
      const o = { type: "error", error: e, origConfig: t },
        n = document.createElement("hui-error-card");
      return (
        customElements.whenDefined("hui-error-card").then(() => {
          const e = document.createElement("hui-error-card");
          e.setConfig(o), n.parentElement && n.parentElement.replaceChild(e, n);
        }),
        _.then(() => {
          g("ll-rebuild", {}, n);
        }),
        n
      );
    }
    function b(e, t) {
      if (!t || "object" != typeof t || !t.type)
        return v(`No ${e} type configured`, t);
      let o = t.type;
      if (
        ((o = o.startsWith("custom:")
          ? o.substr("custom:".length)
          : `hui-${o}-${e}`),
        customElements.get(o))
      )
        return (function (e, t) {
          let o = document.createElement(e);
          try {
            o.setConfig(JSON.parse(JSON.stringify(t)));
          } catch (e) {
            o = v(e, t);
          }
          return (
            _.then(() => {
              g("ll-rebuild", {}, o);
            }),
            o
          );
        })(o, t);
      const n = v(`Custom element doesn't exist: ${o}.`, t);
      n.style.display = "None";
      const r = setTimeout(() => {
        n.style.display = "";
      }, 2e3);
      return (
        customElements.whenDefined(o).then(() => {
          clearTimeout(r), g("ll-rebuild", {}, n);
        }),
        n
      );
    }
    const S = "\nha-card {\n  background: none;\n  box-shadow: none;\n}";
    customElements.define(
      "mod-card",
      class extends n {
        static get properties() {
          return { hass: {} };
        }
        setConfig(e) {
          (this._config = JSON.parse(JSON.stringify(e))),
            void 0 === e.style
              ? (this._config.style = S)
              : "string" == typeof e.style
              ? (this._config.style = S + e.style)
              : e.style["."]
              ? (this._config.style["."] = S + e.style["."])
              : (this._config.style["."] = S),
            (this.card = (function (e) {
              return w ? w.createCardElement(e) : b("card", e);
            })(this._config.card)),
            (this.card.hass = a());
        }
        render() {
          return r`
          <ha-card modcard>
          ${this.card}
          </ha-card>
        `;
        }
        set hass(e) {
          this.card && (this.card.hass = e);
        }
        getCardSize() {
          if (this._config.report_size) return this._config.report_size;
          let e = this.shadowRoot;
          return (
            e && (e = e.querySelector("ha-card card-maker")),
            e && (e = e.getCardSize),
            e && (e = e()),
            e || 1
          );
        }
      }
    );
  },
]);
