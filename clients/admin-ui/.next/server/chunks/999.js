"use strict";
exports.id = 999;
exports.ids = [999];
exports.modules = {

/***/ 2367:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var next_head__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(968);
/* harmony import */ var next_head__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(next_head__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6689);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(997);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__);






const FidesHead = () => /*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__.jsxs)((next_head__WEBPACK_IMPORTED_MODULE_0___default()), {
  children: [/*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__.jsx("title", {
    children: "fidesops"
  }), /*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__.jsx("meta", {
    name: "description",
    content: "admin ui"
  }), /*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_3__.jsx("link", {
    rel: "icon",
    href: `${_constants__WEBPACK_IMPORTED_MODULE_2__/* .BASE_ASSET_URN */ .MY}/favicon.ico`
  })]
});

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FidesHead);

/***/ }),

/***/ 1258:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Z": () => (/* binding */ common_PII)
});

// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__(6689);
// EXTERNAL MODULE: external "react-redux"
var external_react_redux_ = __webpack_require__(6022);
// EXTERNAL MODULE: ./src/features/privacy-requests/privacy-requests.slice.ts
var privacy_requests_slice = __webpack_require__(918);
;// CONCATENATED MODULE: ./src/features/privacy-requests/helpers.ts

 // eslint-disable-next-line import/prefer-default-export

const useObscuredPII = pii => {
  const revealPII = (0,external_react_redux_.useSelector)(privacy_requests_slice/* selectRevealPII */.hG);

  if (revealPII) {
    return pii;
  }

  return revealPII ? pii : pii.replace(/./g, "*");
};
// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__(997);
;// CONCATENATED MODULE: ./src/features/common/PII.tsx





const PII = ({
  data
}) => /*#__PURE__*/jsx_runtime_.jsx(jsx_runtime_.Fragment, {
  children: useObscuredPII(data)
});

/* harmony default export */ const common_PII = (PII);

/***/ }),

/***/ 6012:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1447);
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6689);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6022);
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_redux__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _privacy_requests_privacy_requests_slice__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(918);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(997);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_4__);






const PIIToggle = () => {
  const dispatch = (0,react_redux__WEBPACK_IMPORTED_MODULE_2__.useDispatch)();

  const handleToggle = event => dispatch((0,_privacy_requests_privacy_requests_slice__WEBPACK_IMPORTED_MODULE_3__/* .setRevealPII */ .dX)(event.target.checked));

  return /*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_4__.jsx(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Switch, {
    colorScheme: "secondary",
    onChange: handleToggle
  });
};

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PIIToggle);

/***/ }),

/***/ 9234:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* unused harmony export statusPropMap */
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1447);
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(997);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__);


const statusPropMap = {
  approved: {
    bg: "yellow.500",
    label: "Approved"
  },
  complete: {
    bg: "green.500",
    label: "Completed"
  },
  denied: {
    bg: "red.500",
    label: "Denied"
  },
  canceled: {
    bg: "red.600",
    label: "Canceled"
  },
  error: {
    bg: "red.800",
    label: "Error"
  },
  in_processing: {
    bg: "orange.500",
    label: "In Progress"
  },
  paused: {
    bg: "gray.400",
    label: "Paused"
  },
  pending: {
    bg: "blue.400",
    label: "New"
  }
};

const RequestStatusBadge = ({
  status
}) => /*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsx(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Badge, {
  color: "white",
  bg: statusPropMap[status].bg,
  width: 107,
  lineHeight: "18px",
  textAlign: "center",
  children: statusPropMap[status].label
});

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (RequestStatusBadge);

/***/ })

};
;