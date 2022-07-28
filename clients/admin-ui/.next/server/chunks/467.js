"use strict";
exports.id = 467;
exports.ids = [467];
exports.modules = {

/***/ 8459:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "eU": () => (/* binding */ BASE_API_URN),
/* harmony export */   "MY": () => (/* binding */ BASE_ASSET_URN),
/* harmony export */   "_n": () => (/* binding */ BASE_URL),
/* harmony export */   "O_": () => (/* binding */ STORED_CREDENTIALS_KEY),
/* harmony export */   "GM": () => (/* binding */ USER_PRIVILEGES),
/* harmony export */   "gp": () => (/* binding */ INDEX_ROUTE),
/* harmony export */   "_e": () => (/* binding */ LOGIN_ROUTE),
/* harmony export */   "e3": () => (/* binding */ USER_MANAGEMENT_ROUTE),
/* harmony export */   "DF": () => (/* binding */ CONNECTION_ROUTE),
/* harmony export */   "JR": () => (/* binding */ DATASTORE_CONNECTION_ROUTE)
/* harmony export */ });
const BASE_API_URN = "/api/v1";
const BASE_ASSET_URN =  false ? 0 : "/static";
const API_URL = process.env.NEXT_PUBLIC_FIDESOPS_API ? process.env.NEXT_PUBLIC_FIDESOPS_API : "";
const BASE_URL = API_URL + BASE_API_URN;
const STORED_CREDENTIALS_KEY = "auth.fidesops-admin-ui";
const USER_PRIVILEGES = [{
  privilege: "View subject requests",
  scope: "privacy-request:read"
}, {
  privilege: "Approve subject requests",
  scope: "privacy-request:review"
}, {
  privilege: "View datastore connections",
  scope: "connection:read"
}, {
  privilege: "Create or Update datastore connections",
  scope: "connection:create_or_update"
}, {
  privilege: "Delete datastore connections",
  scope: "connection:delete"
}, {
  privilege: "View policies",
  scope: "policy:read"
}, {
  privilege: "Create policies",
  scope: "policy:create_or_update"
}, {
  privilege: "View users",
  scope: "user:read"
}, {
  privilege: "Create users",
  scope: "user:create"
}, {
  privilege: "Create roles",
  scope: "user-permission:create"
}, {
  privilege: "View roles",
  scope: "user-permission:read"
}]; // API ROUTES

const INDEX_ROUTE = "/";
const LOGIN_ROUTE = "/login";
const USER_MANAGEMENT_ROUTE = "/user-management";
const CONNECTION_ROUTE = "/connection"; // UI ROUTES

const DATASTORE_CONNECTION_ROUTE = "/datastore-connection";

/***/ })

};
;