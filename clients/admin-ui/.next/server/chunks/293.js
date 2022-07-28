"use strict";
exports.id = 293;
exports.ids = [293];
exports.modules = {

/***/ 8293:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1447);
/* harmony import */ var _fidesui_react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(997);
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__);





const PaginationFooter = ({
  page,
  size,
  total,
  handleNextPage,
  handlePreviousPage
}) => {
  const startingItem = (page - 1) * size + 1;
  const endingItem = Math.min(total, page * size);
  return /*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsxs)(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Flex, {
    justifyContent: "space-between",
    mt: 6,
    children: [/*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsx(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Text, {
      fontSize: "xs",
      color: "gray.600",
      children: total > 0 ? /*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.Fragment, {
        children: ["Showing ", Number.isNaN(startingItem) ? 0 : startingItem, " to", " ", Number.isNaN(endingItem) ? 0 : endingItem, " of", " ", Number.isNaN(total) ? 0 : total, " results"]
      }) : "0 results"
    }), /*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsxs)("div", {
      children: [/*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsx(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Button, {
        disabled: page <= 1,
        onClick: handlePreviousPage,
        mr: 2,
        size: "sm",
        children: "Previous"
      }), /*#__PURE__*/react_jsx_runtime__WEBPACK_IMPORTED_MODULE_1__.jsx(_fidesui_react__WEBPACK_IMPORTED_MODULE_0__.Button, {
        disabled: page * size >= total,
        onClick: handleNextPage,
        size: "sm",
        children: "Next"
      })]
    })]
  });
};

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PaginationFooter);

/***/ })

};
;