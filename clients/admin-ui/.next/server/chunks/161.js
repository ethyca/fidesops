"use strict";
exports.id = 161;
exports.ids = [161];
exports.modules = {

/***/ 9110:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dy": () => (/* binding */ selectUser),
/* harmony export */   "rK": () => (/* binding */ selectToken),
/* harmony export */   "x4": () => (/* binding */ login),
/* harmony export */   "kS": () => (/* binding */ logout),
/* harmony export */   "fc": () => (/* binding */ credentialStorage),
/* harmony export */   "iJ": () => (/* binding */ authApi),
/* harmony export */   "YA": () => (/* binding */ useLoginMutation),
/* harmony export */   "I6": () => (/* binding */ reducer)
/* harmony export */ });
/* unused harmony exports authSlice, selectAuth */
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5184);
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4335);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var _common_CommonHeaders__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(2409);
/* harmony import */ var _common_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(61);
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }






const initialState = {
  token: null,
  user: null
}; // Auth slice

const authSlice = (0,_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__.createSlice)({
  name: "auth",
  initialState,
  reducers: {
    login(state, {
      payload: {
        user_data,
        token_data
      }
    }) {
      return Object.assign(state, {
        user: user_data,
        token: token_data.access_token
      });
    },

    logout(state) {
      return Object.assign(state, {
        user: null,
        token: null
      });
    }

  }
});
const selectAuth = state => state.auth;
const selectUser = state => selectAuth(state).user;
const selectToken = state => selectAuth(state).token;
const {
  login,
  logout
} = authSlice.actions;
const credentialStorage = (0,_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__.createListenerMiddleware)();
credentialStorage.startListening({
  actionCreator: login,
  effect: (action, {
    getState
  }) => {
    if (window && window.localStorage) {
      localStorage.setItem(_constants__WEBPACK_IMPORTED_MODULE_2__/* .STORED_CREDENTIALS_KEY */ .O_, JSON.stringify(selectAuth(getState())));
    }
  }
});
credentialStorage.startListening({
  actionCreator: logout,
  effect: () => {
    if (window && window.localStorage) {
      localStorage.removeItem(_constants__WEBPACK_IMPORTED_MODULE_2__/* .STORED_CREDENTIALS_KEY */ .O_);
    }
  }
}); // Auth API

const authApi = (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.createApi)({
  reducerPath: "authApi",
  baseQuery: (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.fetchBaseQuery)({
    baseUrl: _constants__WEBPACK_IMPORTED_MODULE_2__/* .BASE_URL */ ._n,
    prepareHeaders: (headers, {
      getState
    }) => {
      const token = selectToken(getState());
      (0,_common_CommonHeaders__WEBPACK_IMPORTED_MODULE_3__/* .addCommonHeaders */ .E)(headers, token);
      return headers;
    }
  }),
  tagTypes: ["Auth"],
  endpoints: build => ({
    login: build.mutation({
      query: credentials => ({
        url: "login",
        method: "POST",
        body: _objectSpread(_objectSpread({}, credentials), {}, {
          password: (0,_common_utils__WEBPACK_IMPORTED_MODULE_4__/* .utf8ToB64 */ .J)(credentials.password)
        })
      }),
      invalidatesTags: () => ["Auth"]
    })
  })
});
const {
  useLoginMutation
} = authApi;
const {
  reducer
} = authSlice;

/***/ }),

/***/ 7161:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "iJ": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.iJ),
/* harmony export */   "fc": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.fc),
/* harmony export */   "x4": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.x4),
/* harmony export */   "kS": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.kS),
/* harmony export */   "I6": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.I6),
/* harmony export */   "rK": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.rK),
/* harmony export */   "dy": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.dy),
/* harmony export */   "YA": () => (/* reexport safe */ _auth_slice__WEBPACK_IMPORTED_MODULE_0__.YA)
/* harmony export */ });
/* harmony import */ var _auth_slice__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(9110);


/***/ }),

/***/ 2409:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "E": () => (/* binding */ addCommonHeaders)
/* harmony export */ });
/**
 * Adds common headers to all api calls to fidesops
 */
function addCommonHeaders(headers, token) {
  headers.set("Access-Control-Allow-Origin", "*");
  headers.set("X-Fides-Source", "fidesops-admin-ui");

  if (token) {
    headers.set("authorization", `Bearer ${token}`);
  }

  return headers;
}

/***/ }),

/***/ 61:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "k": () => (/* binding */ capitalize),
/* harmony export */   "J": () => (/* binding */ utf8ToB64)
/* harmony export */ });
// eslint-disable-next-line import/prefer-default-export
function capitalize(text) {
  return text.replace(/^\w/, c => c.toUpperCase());
} // eslint-disable-next-line import/prefer-default-export

function utf8ToB64(str) {
  return window.btoa(unescape(encodeURIComponent(str)));
}

/***/ })

};
;