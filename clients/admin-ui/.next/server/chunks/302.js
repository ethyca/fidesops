"use strict";
exports.id = 302;
exports.ids = [302];
exports.modules = {

/***/ 4302:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "qP": () => (/* binding */ setSearch),
/* harmony export */   "YA": () => (/* binding */ setPage),
/* harmony export */   "Iw": () => (/* binding */ setConnectionType),
/* harmony export */   "zq": () => (/* binding */ setSystemType),
/* harmony export */   "Ri": () => (/* binding */ setTestingStatus),
/* harmony export */   "Ru": () => (/* binding */ setDisabledStatus),
/* harmony export */   "dR": () => (/* binding */ selectDatastoreConnectionFilters),
/* harmony export */   "I6": () => (/* binding */ reducer),
/* harmony export */   "DM": () => (/* binding */ datastoreConnectionApi),
/* harmony export */   "AZ": () => (/* binding */ useGetAllDatastoreConnectionsQuery),
/* harmony export */   "h2": () => (/* binding */ useLazyGetDatastoreConnectionStatusQuery),
/* harmony export */   "XX": () => (/* binding */ usePatchDatastoreConnectionsMutation),
/* harmony export */   "R5": () => (/* binding */ useDeleteDatastoreConnectionMutation)
/* harmony export */ });
/* unused harmony exports datastoreConnectionSlice, setSize */
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5184);
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4335);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var _auth__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7161);
/* harmony import */ var _common_CommonHeaders__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(2409);
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(4807);
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }








function mapFiltersToSearchParams({
  search,
  page,
  size,
  connection_type,
  test_status,
  system_type,
  disabled_status
}) {
  let queryString = "";

  if (connection_type) {
    connection_type.forEach(d => {
      queryString += queryString ? `&connection_type=${d}` : `connection_type=${d}`;
    });
  }

  if (search) {
    queryString += queryString ? `&search=${search}` : `search=${search}`;
  }

  if (typeof size !== "undefined") {
    queryString += queryString ? `&size=${size}` : `size=${size}`;
  }

  if (page) {
    queryString += queryString ? `&page=${page}` : `page=${page}`;
  }

  if (test_status) {
    queryString += queryString ? `&test_status=${test_status}` : `test_status=${test_status}`;
  }

  if (system_type) {
    queryString += queryString ? `&system_type=${system_type}` : `system_type=${system_type}`;
  }

  if (disabled_status) {
    const value = disabled_status === _types__WEBPACK_IMPORTED_MODULE_4__/* .DisabledStatus.DISABLED */ .QI.DISABLED;
    queryString += queryString ? `&disabled=${value}` : `disabled=${value}`;
  }

  return queryString ? `?${queryString}` : "";
}

const initialState = {
  search: "",
  page: 1,
  size: 25
};
const datastoreConnectionSlice = (0,_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__.createSlice)({
  name: "datastoreConnections",
  initialState,
  reducers: {
    setSearch: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      search: action.payload
    }),
    setConnectionType: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      connection_type: action.payload
    }),
    setTestingStatus: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      test_status: action.payload
    }),
    setSystemType: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      system_type: action.payload
    }),
    setDisabledStatus: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      disabled_status: action.payload
    }),
    setPage: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: action.payload
    }),
    setSize: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      size: action.payload
    })
  }
});
const {
  setSearch,
  setSize,
  setPage,
  setConnectionType,
  setSystemType,
  setTestingStatus,
  setDisabledStatus
} = datastoreConnectionSlice.actions;
const selectDatastoreConnectionFilters = state => ({
  search: state.datastoreConnections.search,
  page: state.datastoreConnections.page,
  size: state.datastoreConnections.size,
  connection_type: state.datastoreConnections.connection_type,
  system_type: state.datastoreConnections.system_type,
  test_status: state.datastoreConnections.test_status,
  disabled_status: state.datastoreConnections.disabled_status
});
const {
  reducer
} = datastoreConnectionSlice;
const datastoreConnectionApi = (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.createApi)({
  reducerPath: "datastoreConnectionApi",
  baseQuery: (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.fetchBaseQuery)({
    baseUrl: _constants__WEBPACK_IMPORTED_MODULE_2__/* .BASE_URL */ ._n,
    prepareHeaders: (headers, {
      getState
    }) => {
      const token = (0,_auth__WEBPACK_IMPORTED_MODULE_3__/* .selectToken */ .rK)(getState());
      (0,_common_CommonHeaders__WEBPACK_IMPORTED_MODULE_5__/* .addCommonHeaders */ .E)(headers, token);
      return headers;
    }
  }),
  tagTypes: ["DatastoreConnection"],
  endpoints: build => ({
    getAllDatastoreConnections: build.query({
      query: filters => ({
        url: _constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF + mapFiltersToSearchParams(filters)
      }),
      providesTags: () => ["DatastoreConnection"]
    }),
    getDatastoreConnectionByKey: build.query({
      query: key => ({
        url: `${_constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF}/${key}`
      }),
      providesTags: result => [{
        type: "DatastoreConnection",
        id: result.key
      }],
      keepUnusedDataFor: 1
    }),
    getDatastoreConnectionStatus: build.query({
      query: id => ({
        url: `${_constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF}/${id}/test`
      }),
      providesTags: () => ["DatastoreConnection"],

      async onQueryStarted(key, {
        dispatch,
        queryFulfilled,
        getState
      }) {
        try {
          await queryFulfilled;
          const request = dispatch(datastoreConnectionApi.endpoints.getDatastoreConnectionByKey.initiate(key));
          const result = await request.unwrap();
          request.unsubscribe();
          const state = getState();
          const filters = selectDatastoreConnectionFilters(state);
          dispatch(datastoreConnectionApi.util.updateQueryData("getAllDatastoreConnections", filters, draft => {
            const newList = draft.items.map(d => {
              if (d.key === key) {
                return _objectSpread({}, result);
              }

              return _objectSpread({}, d);
            }); // eslint-disable-next-line no-param-reassign

            draft.items = newList;
          }));
        } catch {
          throw new Error("Error while testing connection");
        }
      }

    }),
    patchDatastoreConnections: build.mutation({
      query: ({
        key,
        name,
        disabled,
        connection_type,
        access
      }) => ({
        url: _constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF,
        method: "PATCH",
        body: [{
          key,
          name,
          disabled,
          connection_type,
          access
        }]
      }),
      invalidatesTags: () => ["DatastoreConnection"]
    }),
    deleteDatastoreConnection: build.mutation({
      query: id => ({
        url: `${_constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF}/${id}`,
        method: "DELETE"
      }),
      invalidatesTags: () => ["DatastoreConnection"]
    }),
    updateDatastoreConnectionSecrets: build.mutation({
      query: id => ({
        url: `${_constants__WEBPACK_IMPORTED_MODULE_2__/* .CONNECTION_ROUTE */ .DF}/${id}/secret`,
        method: "PUT",
        body: {}
      }),
      invalidatesTags: () => ["DatastoreConnection"]
    })
  })
});
const {
  useGetAllDatastoreConnectionsQuery,
  useLazyGetDatastoreConnectionStatusQuery,
  usePatchDatastoreConnectionsMutation,
  useDeleteDatastoreConnectionMutation
} = datastoreConnectionApi;

/***/ }),

/***/ 4807:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Rj": () => (/* binding */ ConnectionType),
/* harmony export */   "Zi": () => (/* binding */ SystemType),
/* harmony export */   "i0": () => (/* binding */ TestingStatus),
/* harmony export */   "QI": () => (/* binding */ DisabledStatus)
/* harmony export */ });
/* unused harmony exports AccessLevel, ConnectionTestStatus */
let ConnectionType;

(function (ConnectionType) {
  ConnectionType["POSTGRES"] = "postgres";
  ConnectionType["MONGODB"] = "mongodb";
  ConnectionType["MYSQL"] = "mysql";
  ConnectionType["HTTPS"] = "https";
  ConnectionType["SAAS"] = "saas";
  ConnectionType["REDSHIFT"] = "redshift";
  ConnectionType["SNOWFLAKE"] = "snowflake";
  ConnectionType["MSSQL"] = "mssql";
  ConnectionType["MARIADB"] = "mariadb";
  ConnectionType["BIGQUERY"] = "bigquery";
  ConnectionType["MANUAL"] = "manual";
})(ConnectionType || (ConnectionType = {}));

let SystemType;

(function (SystemType) {
  SystemType["SAAS"] = "saas";
  SystemType["DATABASE"] = "database";
  SystemType["MANUAL"] = "manual";
})(SystemType || (SystemType = {}));

let TestingStatus;

(function (TestingStatus) {
  TestingStatus["PASSED"] = "passed";
  TestingStatus["FAILED"] = "failed";
  TestingStatus["UNTESTED"] = "untested";
})(TestingStatus || (TestingStatus = {}));

let AccessLevel;

(function (AccessLevel) {
  AccessLevel["READ"] = "read";
  AccessLevel["WRITE"] = "write";
})(AccessLevel || (AccessLevel = {}));

let DisabledStatus;

(function (DisabledStatus) {
  DisabledStatus["ACTIVE"] = "active";
  DisabledStatus["DISABLED"] = "disabled";
})(DisabledStatus || (DisabledStatus = {}));

let ConnectionTestStatus;

(function (ConnectionTestStatus) {
  ConnectionTestStatus["SUCCEEDED"] = "succeeded";
  ConnectionTestStatus["FAILED"] = "failed";
  ConnectionTestStatus["SKIPPED"] = "skipped";
})(ConnectionTestStatus || (ConnectionTestStatus = {}));

/***/ })

};
;