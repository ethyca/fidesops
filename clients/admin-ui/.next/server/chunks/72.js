"use strict";
exports.id = 72;
exports.ids = [72];
exports.modules = {

/***/ 3072:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "YA": () => (/* binding */ setPage),
/* harmony export */   "SY": () => (/* binding */ setUsernameSearch),
/* harmony export */   "lq": () => (/* binding */ selectUserFilters),
/* harmony export */   "I6": () => (/* binding */ reducer),
/* harmony export */   "BG": () => (/* binding */ userApi),
/* harmony export */   "wv": () => (/* binding */ useGetAllUsersQuery),
/* harmony export */   "Fk": () => (/* binding */ useGetUserByIdQuery),
/* harmony export */   "ny": () => (/* binding */ useCreateUserMutation),
/* harmony export */   "Gl": () => (/* binding */ useEditUserMutation),
/* harmony export */   "I1": () => (/* binding */ useDeleteUserMutation),
/* harmony export */   "ev": () => (/* binding */ useUpdateUserPasswordMutation),
/* harmony export */   "lD": () => (/* binding */ useUpdateUserPermissionsMutation),
/* harmony export */   "gU": () => (/* binding */ useGetUserPermissionsQuery)
/* harmony export */ });
/* unused harmony exports userManagementSlice, mapFiltersToSearchParams, useCreateUserPermissionsMutation */
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5184);
/* harmony import */ var _reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4335);
/* harmony import */ var _reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var _auth__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7161);
/* harmony import */ var _common_CommonHeaders__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(2409);
/* harmony import */ var _common_utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(61);
const _excluded = ["id"],
      _excluded2 = ["id"];

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }







const initialState = {
  id: "",
  page: 1,
  size: 25,
  token: null,
  username: ""
};
const userManagementSlice = (0,_reduxjs_toolkit__WEBPACK_IMPORTED_MODULE_0__.createSlice)({
  name: "userManagement",
  initialState,
  reducers: {
    assignToken: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      token: action.payload
    }),
    setUsernameSearch: (state, action) => _objectSpread(_objectSpread({}, state), {}, {
      page: initialState.page,
      username: action.payload
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
  setPage,
  setUsernameSearch
} = userManagementSlice.actions;
const selectUserFilters = state => ({
  page: state.userManagement.page,
  size: state.userManagement.size,
  username: state.userManagement.username
});
const {
  reducer
} = userManagementSlice; // Helpers

const mapFiltersToSearchParams = ({
  page,
  size,
  username
}) => _objectSpread(_objectSpread(_objectSpread({}, page ? {
  page: `${page}`
} : {}), typeof size !== "undefined" ? {
  size: `${size}`
} : {}), username ? {
  username
} : {});
const userApi = (0,_reduxjs_toolkit_query_react__WEBPACK_IMPORTED_MODULE_1__.createApi)({
  reducerPath: "userApi",
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
  tagTypes: ["User"],
  endpoints: build => ({
    getAllUsers: build.query({
      query: filters => ({
        url: `user`,
        params: mapFiltersToSearchParams(filters)
      }),
      providesTags: () => ["User"]
    }),
    getUserById: build.query({
      query: id => ({
        url: `user/${id}`
      }),
      providesTags: ["User"]
    }),
    getUserPermissions: build.query({
      query: id => ({
        url: `user/${id}/permission`
      }),
      providesTags: ["User"]
    }),
    createUser: build.mutation({
      query: user => ({
        url: "user",
        method: "POST",
        body: user
      }),
      invalidatesTags: ["User"]
    }),
    createUserPermissions: build.mutation({
      query: user => {
        var _user$data;

        return {
          url: `user/${user === null || user === void 0 ? void 0 : (_user$data = user.data) === null || _user$data === void 0 ? void 0 : _user$data.id}/permission`,
          method: "POST",
          body: {
            scopes: user.scope
          }
        };
      },
      invalidatesTags: ["User"]
    }),
    editUser: build.mutation({
      query: _ref => {
        let {
          id
        } = _ref,
            patch = _objectWithoutProperties(_ref, _excluded);

        return {
          url: `user/${id}`,
          method: "PUT",
          body: patch
        };
      },
      invalidatesTags: ["User"],

      // For optimistic updates
      async onQueryStarted(_ref2, {
        dispatch,
        queryFulfilled
      }) {
        let {
          id
        } = _ref2,
            patch = _objectWithoutProperties(_ref2, _excluded2);

        const patchResult = dispatch( // @ts-ignore
        userApi.util.updateQueryData("getUserById", id, draft => {
          Object.assign(draft, patch);
        }));

        try {
          await queryFulfilled;
        } catch {
          patchResult.undo();
          /**
           * Alternatively, on failure you can invalidate the corresponding cache tags
           * to trigger a re-fetch:
           * dispatch(api.util.invalidateTags(['User']))
           */
        }
      }

    }),
    updateUserPassword: build.mutation({
      query: ({
        id,
        old_password,
        new_password
      }) => ({
        url: `user/${id}/reset-password`,
        method: "POST",
        body: {
          old_password: (0,_common_utils__WEBPACK_IMPORTED_MODULE_5__/* .utf8ToB64 */ .J)(old_password),
          new_password: (0,_common_utils__WEBPACK_IMPORTED_MODULE_5__/* .utf8ToB64 */ .J)(new_password)
        }
      }),
      invalidatesTags: ["User"]
    }),
    updateUserPermissions: build.mutation({
      query: ({
        id,
        scopes
      }) => ({
        url: `user/${id}/permission`,
        method: "PUT",
        body: {
          id,
          scopes
        }
      }),
      invalidatesTags: ["User"]
    }),
    deleteUser: build.mutation({
      query: id => ({
        url: `user/${id}`,
        method: "DELETE"
      }),
      // Invalidates all queries that subscribe to this User `id` only
      invalidatesTags: ["User"]
    })
  })
});
const {
  useGetAllUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useEditUserMutation,
  useDeleteUserMutation,
  useUpdateUserPasswordMutation,
  useUpdateUserPermissionsMutation,
  useCreateUserPermissionsMutation,
  useGetUserPermissionsQuery
} = userApi;

/***/ })

};
;