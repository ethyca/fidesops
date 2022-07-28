"use strict";
(() => {
var exports = {};
exports.id = 888;
exports.ids = [888];
exports.modules = {

/***/ 7971:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "$I": () => (/* reexport safe */ _privacy_requests_slice__WEBPACK_IMPORTED_MODULE_0__.$I),
/* harmony export */   "I6": () => (/* reexport safe */ _privacy_requests_slice__WEBPACK_IMPORTED_MODULE_0__.I6),
/* harmony export */   "QA": () => (/* reexport safe */ _privacy_requests_slice__WEBPACK_IMPORTED_MODULE_0__.QA)
/* harmony export */ });
/* harmony import */ var _privacy_requests_slice__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(918);


/***/ }),

/***/ 7230:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
if (false) {} else {
  // eslint-disable-next-line global-require
  const {
    server
  } = __webpack_require__(6069);

  server.listen();
}



/***/ }),

/***/ 6069:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "server": () => (/* binding */ server)
});

;// CONCATENATED MODULE: external "msw/node"
const node_namespaceObject = require("msw/node");
;// CONCATENATED MODULE: external "msw"
const external_msw_namespaceObject = require("msw");
;// CONCATENATED MODULE: ./src/mocks/handlers.ts

const mockSubjectRequestPreviewResponse = {
  items: [{
    status: "error",
    identity: {
      email: "james.braithwaite@email.com"
    },
    created_at: "August 4, 2021, 09:35:46 PST",
    reviewed_by: "Sammie_Shanahan@gmail.com",
    id: "123"
  }, {
    status: "denied",
    identity: {
      phone: "555-325-685-126"
    },
    created_at: "August 4, 2021, 09:35:46 PST",
    reviewed_by: "Richmond33@yahoo.com",
    id: "456"
  }, {
    status: "pending",
    identity: {
      email: "mary.jane.@email.com"
    },
    created_at: "August 4, 2021, 09:35:46 PST",
    reviewed_by: "Oceane.Volkman@gmail.com",
    id: "789"
  }, {
    status: "new",
    identity: {
      email: "jeremiah.stones@email.com"
    },
    created_at: "August 4, 2021, 09:35:46 PST",
    reviewed_by: "Verdie64@yahoo.com",
    id: "012"
  }, {
    status: "completed",
    identity: {
      phone: "283-774-5003"
    },
    created_at: "August 4, 2021, 09:35:46 PST",
    reviewed_by: "Maximo_Willms0@gmail.com",
    id: "345"
  }]
}; // eslint-disable-next-line import/prefer-default-export

const handlers = [external_msw_namespaceObject.rest.get("http://localhost:8080/api/v1/privacy-request", async (req, res, ctx) => {
  // mock loading response
  await new Promise(resolve => {
    setTimeout(() => resolve(null), 1000);
  });
  return res(ctx.json(mockSubjectRequestPreviewResponse));
})];
;// CONCATENATED MODULE: ./src/mocks/server.ts

 // eslint-disable-next-line import/prefer-default-export

const server = (0,node_namespaceObject.setupServer)(...handlers);

/***/ }),

/***/ 2265:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ _app)
});

// EXTERNAL MODULE: external "@chakra-ui/react"
var react_ = __webpack_require__(8930);
// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__(6689);
// EXTERNAL MODULE: external "react-redux"
var external_react_redux_ = __webpack_require__(6022);
// EXTERNAL MODULE: external "@reduxjs/toolkit"
var toolkit_ = __webpack_require__(5184);
// EXTERNAL MODULE: external "@reduxjs/toolkit/query/react"
var query_react_ = __webpack_require__(4335);
// EXTERNAL MODULE: ./src/constants.ts
var constants = __webpack_require__(8459);
// EXTERNAL MODULE: ./src/features/auth/index.ts
var auth = __webpack_require__(7161);
// EXTERNAL MODULE: ./src/features/datastore-connections/datastore-connection.slice.ts
var datastore_connection_slice = __webpack_require__(4302);
;// CONCATENATED MODULE: ./src/features/datastore-connections/index.ts

// EXTERNAL MODULE: ./src/features/privacy-requests/index.ts
var privacy_requests = __webpack_require__(7971);
// EXTERNAL MODULE: ./src/features/user-management/user-management.slice.ts
var user_management_slice = __webpack_require__(3072);
;// CONCATENATED MODULE: ./src/features/user-management/index.ts

;// CONCATENATED MODULE: ./src/app/store.ts







const reducer = {
  [privacy_requests/* privacyRequestApi.reducerPath */.$I.reducerPath]: privacy_requests/* privacyRequestApi.reducer */.$I.reducer,
  subjectRequests: privacy_requests/* reducer */.I6,
  [user_management_slice/* userApi.reducerPath */.BG.reducerPath]: user_management_slice/* userApi.reducer */.BG.reducer,
  [auth/* authApi.reducerPath */.iJ.reducerPath]: auth/* authApi.reducer */.iJ.reducer,
  userManagement: user_management_slice/* reducer */.I6,
  [datastore_connection_slice/* datastoreConnectionApi.reducerPath */.DM.reducerPath]: datastore_connection_slice/* datastoreConnectionApi.reducer */.DM.reducer,
  datastoreConnections: datastore_connection_slice/* reducer */.I6,
  auth: auth/* reducer */.I6
};
const makeStore = preloadedState => (0,toolkit_.configureStore)({
  reducer,
  middleware: getDefaultMiddleware => getDefaultMiddleware().concat(auth/* credentialStorage.middleware */.fc.middleware, privacy_requests/* privacyRequestApi.middleware */.$I.middleware, user_management_slice/* userApi.middleware */.BG.middleware, auth/* authApi.middleware */.iJ.middleware, datastore_connection_slice/* datastoreConnectionApi.middleware */.DM.middleware),
  devTools: true,
  preloadedState
});
let storedAuthState;

if (false) {}

const store = makeStore({
  auth: storedAuthState
});
(0,query_react_.setupListeners)(store.dispatch);
/* harmony default export */ const app_store = (store);
// EXTERNAL MODULE: external "@fidesui/react"
var external_fidesui_react_ = __webpack_require__(1447);
;// CONCATENATED MODULE: ./src/theme/index.ts

const theme = (0,external_fidesui_react_.extendTheme)({
  styles: {
    global: {
      body: {
        bg: "white"
      },
      html: {
        height: "100%"
      }
    }
  }
});
/* harmony default export */ const src_theme = (theme);
// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__(997);
;// CONCATENATED MODULE: ./src/pages/_app.tsx
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }











if (process.env.NEXT_PUBLIC_MOCK_API) {
  // eslint-disable-next-line global-require
  __webpack_require__(7230);
}

const SafeHydrate = ({
  children
}) => /*#__PURE__*/jsx_runtime_.jsx("div", {
  suppressHydrationWarning: true,
  children:  true ? null : 0
});

const MyApp = ({
  Component,
  pageProps
}) => /*#__PURE__*/jsx_runtime_.jsx(SafeHydrate, {
  children: /*#__PURE__*/jsx_runtime_.jsx(external_react_redux_.Provider, {
    store: app_store,
    children: /*#__PURE__*/jsx_runtime_.jsx(react_.ChakraProvider, {
      theme: src_theme,
      children: /*#__PURE__*/jsx_runtime_.jsx(Component, _objectSpread({}, pageProps))
    })
  })
});

/* harmony default export */ const _app = (MyApp);

/***/ }),

/***/ 8930:
/***/ ((module) => {

module.exports = require("@chakra-ui/react");

/***/ }),

/***/ 1447:
/***/ ((module) => {

module.exports = require("@fidesui/react");

/***/ }),

/***/ 5184:
/***/ ((module) => {

module.exports = require("@reduxjs/toolkit");

/***/ }),

/***/ 4335:
/***/ ((module) => {

module.exports = require("@reduxjs/toolkit/query/react");

/***/ }),

/***/ 6689:
/***/ ((module) => {

module.exports = require("react");

/***/ }),

/***/ 6022:
/***/ ((module) => {

module.exports = require("react-redux");

/***/ }),

/***/ 997:
/***/ ((module) => {

module.exports = require("react/jsx-runtime");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, [467,161,72,918,302], () => (__webpack_exec__(2265)));
module.exports = __webpack_exports__;

})();