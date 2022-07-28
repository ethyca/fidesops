"use strict";
exports.id = 918;
exports.ids = [918];
exports.modules = {

/***/ 918:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "$I": () => (/* binding */ privacyRequestApi),
/* harmony export */   "QA": () => (/* binding */ useGetAllPrivacyRequestsQuery),
/* harmony export */   "RW": () => (/* binding */ useApproveRequestMutation),
/* harmony export */   "F1": () => (/* binding */ useDenyRequestMutation),
/* harmony export */   "py": () => (/* binding */ requestCSVDownload),
/* harmony export */   "dX": () => (/* binding */ setRevealPII),
/* harmony export */   "Nl": () => (/* binding */ setRequestId),
/* harmony export */   "CI": () => (/* binding */ setRequestStatus),
/* harmony export */   "su": () => (/* binding */ setRequestFrom),
/* harmony export */   "Ue": () => (/* binding */ setRequestTo),
/* harmony export */   "YA": () => (/* binding */ setPage),
/* harmony export */   "Mk": () => (/* binding */ clearAllFilters),
/* harmony export */   "hG": () => (/* binding */ selectRevealPII),
/* harmony export */   "dp": () => (/* binding */ selectPrivacyRequestFilters),
/* harmony export */   "I6": () => (/* binding */ reducer)
/* harmony export */ });
/* unused harmony exports mapFiltersToSearchParams, subjectRequestsSlice, setVerbose, selectRequestStatus */
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5184);
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4335);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var _auth__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7161);
/* harmony import */ var _common_CommonHeaders__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(2409);
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }






// Helpers
function mapFiltersToSearchParams({
  status,
  id,
  from,
  to,
  page,
  size,
  verbose
}) {
  let fromISO;

  if (from) {
    fromISO = new Date(from);
    fromISO.setUTCHours(0, 0, 0);
  }

  let toISO;

  if (to) {
    toISO = new Date(to);
    toISO.setUTCHours(23, 59, 59);
  }

  return _objectSpread(_objectSpread(_objectSpread(_objectSpread(_objectSpread(_objectSpread(_objectSpread({
    include_identities: "true"
  }, status && status.length > 0 ? {
    status: status.join("&status=")
  } : {}), id ? {
    request_id: id
  } : {}), fromISO ? {
    created_gt: fromISO.toISOString()
  } : {}), toISO ? {
    created_lt: toISO.toISOString()
  } : {}), page ? {
    page: `${page}`
  } : {}), typeof size !== "undefined" ? {
    size: `${size}`
  } : {}), verbose ? {
    verbose
  } : {});
} // Subject requests API

const privacyRequestApi = (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.createApi)({
  reducerPath: "privacyRequestApi",
  baseQuery: (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.fetchBaseQuery)({
    baseUrl: _constants__WEBPACK_IMPORTED_MODULE_2__/* .BASE_URL */ ._n,
    prepareHeaders: (headers, {
      getState
    }) => {
      const token = (0,_auth__WEBPACK_IMPORTED_MODULE_3__/* .selectToken */ .rK)(getState());
      (0,_common_CommonHeaders__WEBPACK_IMPORTED_MODULE_4__/* .addCommonHeaders */ .E)(headers, token);
      return headers;
    }
  }),
  tagTypes: ["Request"],
  endpoints: build => ({
    getAllPrivacyRequests: build.query({
      query: filters => ({
        url: `privacy-request?${decodeURIComponent(new URLSearchParams(mapFiltersToSearchParams(filters)).toString())}`
      }),
      providesTags: () => ["Request"]
    }),
    approveRequest: build.mutation({
      query: ({
        id
      }) => ({
        url: "privacy-request/administrate/approve",
        method: "PATCH",
        body: {
          request_ids: [id]
        }
      }),
      invalidatesTags: ["Request"]
    }),
    denyRequest: build.mutation({
      query: ({
        id,
        reason
      }) => ({
        url: "privacy-request/administrate/deny",
        method: "PATCH",
        body: {
          request_ids: [id],
          reason
        }
      }),
      invalidatesTags: ["Request"]
    })
  })
});
const {
  useGetAllPrivacyRequestsQuery,
  useApproveRequestMutation,
  useDenyRequestMutation
} = privacyRequestApi;
const requestCSVDownload = async ({
  id,
  from,
  to,
  status,
  token
}) => {
  if (!token) {
    return null;
  }

  return fetch(`${_constants__WEBPACK_IMPORTED_MODULE_2__/* .BASE_API_URN */ .eU}/privacy-request?${new URLSearchParams(_objectSpread(_objectSpread({}, mapFiltersToSearchParams({
    id,
    from,
    to,
    status
  })), {}, {
    download_csv: "true"
  }))}`, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: `Bearer ${token}`,
      "X-Fides-Source": "fidesops-admin-ui"
    }
  }).then(response => {
    if (!response.ok) {
      throw new Error("Got a bad response from the server");
    }

    return response.blob();
  }).then(data => {
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(data);
    a.download = "privacy-requests.csv";
    a.click();
  }).catch(error => Promise.reject(error));
}; // Subject requests state (filters, etc.)

const initialState = {
  revealPII: false,
  id: "",
  from: "",
  to: "",
  page: 1,
  size: 25
};
const subjectRequestsSlice = (0,_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__.createSlice)({
  name: "subjectRequests",
  initialState,
  reducers: {
    setRevealPII: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      revealPII: action.payload
    }),
    setRequestStatus: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      status: action.payload
    }),
    setRequestId: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      id: action.payload
    }),
    setRequestFrom: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      from: action.payload
    }),
    setRequestTo: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      to: action.payload
    }),
    clearAllFilters: ({
      revealPII
    }) => _objectSpread(_objectSpread({}, initialState), {}, {
      revealPII
    }),
    setPage: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: action.payload
    }),
    setSize: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      size: action.payload
    }),
    setVerbose: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      verbose: action.payload
    })
  }
});
const {
  setRevealPII,
  setRequestId,
  setRequestStatus,
  setRequestFrom,
  setRequestTo,
  setPage,
  setVerbose,
  clearAllFilters
} = subjectRequestsSlice.actions;
const selectRevealPII = state => state.subjectRequests.revealPII;
const selectRequestStatus = state => state.subjectRequests.status;
const selectPrivacyRequestFilters = state => ({
  status: state.subjectRequests.status,
  id: state.subjectRequests.id,
  from: state.subjectRequests.from,
  to: state.subjectRequests.to,
  page: state.subjectRequests.page,
  size: state.subjectRequests.size,
  verbose: state.subjectRequests.verbose
});
const {
  reducer
} = subjectRequestsSlice;

/***/ })

};
;