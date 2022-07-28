"use strict";
exports.id = 114;
exports.ids = [114];
exports.modules = {

/***/ 9699:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1853);
/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6022);
/* harmony import */ var react_redux__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_redux__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8459);
/* harmony import */ var _auth_slice__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(9110);





const useProtectedRoute = redirectUrl => {
  const router = (0,next_router__WEBPACK_IMPORTED_MODULE_0__.useRouter)();
  const token = (0,react_redux__WEBPACK_IMPORTED_MODULE_1__.useSelector)(_auth_slice__WEBPACK_IMPORTED_MODULE_3__/* .selectToken */ .rK); // TODO: check for token invalidation

  if (!token && false) {}

  return true;
};

const ProtectedRoute = ({
  children,
  redirectUrl,
  authenticatedBlock
}) => {
  const authenticated = useProtectedRoute(redirectUrl);
  return authenticated ? children : authenticatedBlock;
};

ProtectedRoute.defaultProps = {
  authenticatedBlock: null,
  redirectUrl: _constants__WEBPACK_IMPORTED_MODULE_2__/* .LOGIN_ROUTE */ ._e
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ProtectedRoute);

/***/ }),

/***/ 4571:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "mC": () => (/* reexport */ ArrowDownLine),
  "LG": () => (/* reexport */ CloseSolid),
  "$I": () => (/* reexport */ DownloadSolid),
  "nX": () => (/* reexport */ More),
  "PT": () => (/* reexport */ SearchLine),
  "tB": () => (/* reexport */ User)
});

// UNUSED EXPORTS: GearIcon, GreenCheckCircle

// EXTERNAL MODULE: external "@fidesui/react"
var react_ = __webpack_require__(1447);
;// CONCATENATED MODULE: ./src/features/common/Icon/ArrowDownLine.tsx

/* harmony default export */ const ArrowDownLine = ((0,react_.createIcon)({
  displayName: "ArrowDownLineIcon",
  viewBox: "0 0 24 24",
  defaultProps: {
    width: "20px",
    height: "20px"
  },
  d: "M12 13.1719L16.95 8.22192L18.364 9.63592L12 15.9999L5.63599 9.63592L7.04999 8.22192L12 13.1719Z"
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/CloseSolid.tsx

/* harmony default export */ const CloseSolid = ((0,react_.createIcon)({
  displayName: "CloseSolidIcon",
  viewBox: "0 0 24 24",
  d: "M19.1841 17.5875C19.9562 18.3687 19.9562 19.6343 19.1841 20.4156C18.8012 20.8062 18.2947 21 17.7882 21C17.2818 21 16.7765 20.8047 16.3911 20.414L9.88235 13.8312L3.37421 20.4125C2.98818 20.8062 2.48232 21 1.97647 21C1.47062 21 0.965382 20.8062 0.579044 20.4125C-0.193015 19.6312 -0.193015 18.3656 0.579044 17.5843L7.08904 10.9968L0.579044 4.41248C-0.193015 3.63123 -0.193015 2.3656 0.579044 1.58435C1.3511 0.803101 2.60184 0.803101 3.3739 1.58435L9.88235 8.17497L16.3924 1.58748C17.1644 0.806226 18.4151 0.806226 19.1872 1.58748C19.9593 2.36873 19.9593 3.63435 19.1872 4.4156L12.6772 11.0031L19.1841 17.5875Z"
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/DownloadSolid.tsx

/* harmony default export */ const DownloadSolid = ((0,react_.createIcon)({
  displayName: "DownloadSolidIcon",
  viewBox: "0 0 24 24",
  d: "M20.75 15.75H15.5352L13.7676 17.5176C13.2969 17.9883 12.668 18.25 12 18.25C11.332 18.25 10.7047 17.99 10.2324 17.5176L8.46484 15.75H3.25C2.55977 15.75 2 16.3098 2 17V20.75C2 21.4402 2.55977 22 3.25 22H20.75C21.4402 22 22 21.4402 22 20.75V17C22 16.3086 21.4414 15.75 20.75 15.75ZM18.875 19.8125C18.3594 19.8125 17.9375 19.3906 17.9375 18.875C17.9375 18.3594 18.3594 17.9375 18.875 17.9375C19.3906 17.9375 19.8125 18.3594 19.8125 18.875C19.8125 19.3906 19.3906 19.8125 18.875 19.8125ZM11.1172 16.6328C11.3594 16.8789 11.6797 17 12 17C12.3203 17 12.6398 16.8779 12.8836 16.6338L17.8836 11.6338C18.3715 11.1455 18.3715 10.3545 17.8836 9.86621C17.3953 9.37793 16.6039 9.37793 16.116 9.86621L13.25 12.7344V3.25C13.25 2.55977 12.6902 2 12 2C11.3086 2 10.75 2.55977 10.75 3.25V12.7344L7.88281 9.86719C7.39492 9.37891 6.60352 9.37891 6.11523 9.86719C5.62734 10.3555 5.62734 11.1465 6.11523 11.6348L11.1172 16.6328Z"
}));
// EXTERNAL MODULE: external "@chakra-ui/react"
var external_chakra_ui_react_ = __webpack_require__(8930);
;// CONCATENATED MODULE: ./src/features/common/Icon/Gear.tsx

/* harmony default export */ const Gear = ((0,external_chakra_ui_react_.createIcon)({
  displayName: "GearIcon",
  viewBox: "0 0 24 24",
  d: "M21.371 8.50781C21.4999 8.84375 21.3906 9.22266 21.1249 9.46875L19.4335 11.0078C19.4765 11.332 19.4999 11.6641 19.4999 12C19.4999 12.3359 19.4765 12.668 19.4335 12.9922L21.1249 14.5312C21.3906 14.7773 21.4999 15.1562 21.371 15.4922C21.1992 15.957 20.9921 16.4063 20.7578 16.832L20.5742 17.1484C20.3163 17.5781 20.0273 17.9844 19.7109 18.3711C19.4765 18.6484 19.0976 18.7461 18.7538 18.6367L16.5781 17.9414C16.0546 18.3438 15.4413 18.6797 14.8593 18.9375L14.371 21.168C14.2929 21.5195 14.0195 21.7695 13.6601 21.8633C13.121 21.9531 12.5663 22 11.9648 22C11.4335 22 10.8788 21.9531 10.3398 21.8633C9.9804 21.7695 9.70696 21.5195 9.62884 21.168L9.14056 18.9375C8.52337 18.6797 7.94524 18.3438 7.4218 17.9414L5.24758 18.6367C4.90227 18.7461 4.52141 18.6484 4.29016 18.3711C3.97336 17.9844 3.6843 17.5781 3.42649 17.1484L3.24368 16.832C3.00657 16.4063 2.80032 15.957 2.62727 15.4922C2.50071 15.1562 2.60735 14.7773 2.87532 14.5312L4.56516 12.9922C4.52219 12.668 4.49993 12.3359 4.49993 12C4.49993 11.6641 4.52219 11.332 4.56516 11.0078L2.87532 9.46875C2.60735 9.22266 2.50071 8.84766 2.62727 8.50781C2.80032 8.04297 3.00696 7.59375 3.24368 7.16797L3.4261 6.85156C3.6843 6.42188 3.97336 6.01562 4.29016 5.63086C4.52141 5.35156 4.90227 5.25469 5.24758 5.36484L7.4218 6.05859C7.94524 5.65469 8.52337 5.31875 9.14056 5.06367L9.62884 2.8332C9.70696 2.47852 9.9804 2.19688 10.3398 2.13711C10.8788 2.04691 11.4335 2 11.9999 2C12.5663 2 13.121 2.04691 13.6601 2.13711C14.0195 2.19688 14.2929 2.47852 14.371 2.8332L14.8593 5.06367C15.4413 5.31875 16.0546 5.65469 16.5781 6.05859L18.7538 5.36484C19.0976 5.25469 19.4765 5.35156 19.7109 5.63086C20.0273 6.01562 20.3163 6.42188 20.5742 6.85156L20.7578 7.16797C20.9921 7.59375 21.1992 8.04297 21.371 8.50781ZM11.9999 15.125C13.7265 15.125 15.1249 13.7266 15.1249 11.9648C15.1249 10.2734 13.7265 8.83984 11.9999 8.83984C10.2734 8.83984 8.87493 10.2734 8.87493 11.9648C8.87493 13.7266 10.2734 15.125 11.9999 15.125Z"
}));
// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__(997);
;// CONCATENATED MODULE: ./src/features/common/Icon/GreenCheckCircle.tsx


/* harmony default export */ const GreenCheckCircle = ((0,external_chakra_ui_react_.createIcon)({
  displayName: "GreenCheckCircle",
  viewBox: "0 0 16 16",
  defaultProps: {
    width: "16px",
    height: "16px"
  },
  path: /*#__PURE__*/jsx_runtime_.jsx("path", {
    fill: "#38A169",
    d: "M7.00065 13.6663C3.31865 13.6663 0.333984 10.6817 0.333984 6.99967C0.333984 3.31767 3.31865 0.333008 7.00065 0.333008C10.6827 0.333008 13.6673 3.31767 13.6673 6.99967C13.6673 10.6817 10.6827 13.6663 7.00065 13.6663ZM6.33598 9.66634L11.0493 4.95234L10.1067 4.00967L6.33598 7.78101L4.44998 5.89501L3.50732 6.83767L6.33598 9.66634Z"
  })
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/More.tsx

/* harmony default export */ const More = ((0,react_.createIcon)({
  displayName: "MoreIcon",
  viewBox: "0 0 24 24",
  d: "M4.5 10.5C3.675 10.5 3 11.175 3 12C3 12.825 3.675 13.5 4.5 13.5C5.325 13.5 6 12.825 6 12C6 11.175 5.325 10.5 4.5 10.5ZM19.5 10.5C18.675 10.5 18 11.175 18 12C18 12.825 18.675 13.5 19.5 13.5C20.325 13.5 21 12.825 21 12C21 11.175 20.325 10.5 19.5 10.5ZM12 10.5C11.175 10.5 10.5 11.175 10.5 12C10.5 12.825 11.175 13.5 12 13.5C12.825 13.5 13.5 12.825 13.5 12C13.5 11.175 12.825 10.5 12 10.5Z"
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/SearchLine.tsx

/* harmony default export */ const SearchLine = ((0,react_.createIcon)({
  displayName: "SearchLineIcon",
  viewBox: "0 0 24 24",
  d: "M16.031 14.617L20.314 18.899L18.899 20.314L14.617 16.031C13.0237 17.3082 11.042 18.0029 9 18C4.032 18 0 13.968 0 9C0 4.032 4.032 0 9 0C13.968 0 18 4.032 18 9C18.0029 11.042 17.3082 13.0237 16.031 14.617ZM14.025 13.875C15.2941 12.5699 16.0029 10.8204 16 9C16 5.132 12.867 2 9 2C5.132 2 2 5.132 2 9C2 12.867 5.132 16 9 16C10.8204 16.0029 12.5699 15.2941 13.875 14.025L14.025 13.875Z"
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/User.tsx

/* harmony default export */ const User = ((0,react_.createIcon)({
  displayName: "UserIcon",
  viewBox: "0 0 24 24",
  d: "M20 22H4V20C4 18.6739 4.52678 17.4021 5.46447 16.4645C6.40215 15.5268 7.67392 15 9 15H15C16.3261 15 17.5979 15.5268 18.5355 16.4645C19.4732 17.4021 20 18.6739 20 20V22ZM12 13C11.2121 13 10.4319 12.8448 9.7039 12.5433C8.97595 12.2417 8.31451 11.7998 7.75736 11.2426C7.20021 10.6855 6.75825 10.0241 6.45672 9.2961C6.15519 8.56815 6 7.78793 6 7C6 6.21207 6.15519 5.43185 6.45672 4.7039C6.75825 3.97595 7.20021 3.31451 7.75736 2.75736C8.31451 2.20021 8.97595 1.75825 9.7039 1.45672C10.4319 1.15519 11.2121 1 12 1C13.5913 1 15.1174 1.63214 16.2426 2.75736C17.3679 3.88258 18 5.4087 18 7C18 8.5913 17.3679 10.1174 16.2426 11.2426C15.1174 12.3679 13.5913 13 12 13Z"
}));
;// CONCATENATED MODULE: ./src/features/common/Icon/index.tsx









/***/ }),

/***/ 4510:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Z": () => (/* binding */ common_NavBar)
});

// EXTERNAL MODULE: external "@fidesui/react"
var react_ = __webpack_require__(1447);
// EXTERNAL MODULE: ./node_modules/next/link.js
var next_link = __webpack_require__(1664);
// EXTERNAL MODULE: external "next/router"
var router_ = __webpack_require__(1853);
// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__(6689);
// EXTERNAL MODULE: ./src/constants.ts
var constants = __webpack_require__(8459);
// EXTERNAL MODULE: external "react-redux"
var external_react_redux_ = __webpack_require__(6022);
// EXTERNAL MODULE: ./src/features/auth/index.ts
var auth = __webpack_require__(7161);
// EXTERNAL MODULE: ./src/features/common/Icon/index.tsx + 8 modules
var Icon = __webpack_require__(4571);
// EXTERNAL MODULE: ./src/features/common/Image.tsx
var Image = __webpack_require__(8101);
// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__(997);
;// CONCATENATED MODULE: ./src/features/common/Header.tsx











const useHeader = () => {
  var _useSelector;

  const dispatch = (0,external_react_redux_.useDispatch)();

  const handleLogout = () => dispatch((0,auth/* logout */.kS)());

  const {
    username
  } = (_useSelector = (0,external_react_redux_.useSelector)(auth/* selectUser */.dy)) !== null && _useSelector !== void 0 ? _useSelector : {
    username: ""
  };
  return {
    handleLogout,
    username
  };
};

const Header = () => {
  const {
    handleLogout,
    username
  } = useHeader();
  return /*#__PURE__*/jsx_runtime_.jsx("header", {
    children: /*#__PURE__*/(0,jsx_runtime_.jsxs)(react_.Flex, {
      bg: "gray.50",
      width: "100%",
      py: 3,
      px: 10,
      justifyContent: "space-between",
      alignItems: "center",
      children: [/*#__PURE__*/jsx_runtime_.jsx(next_link["default"], {
        href: constants/* INDEX_ROUTE */.gp,
        passHref: true,
        children: /*#__PURE__*/jsx_runtime_.jsx(react_.Link, {
          display: "flex",
          children: /*#__PURE__*/jsx_runtime_.jsx(Image/* default */.Z, {
            src: `${constants/* BASE_ASSET_URN */.MY}/logo.svg`,
            width: 83,
            height: 26,
            alt: "FidesOps Logo"
          })
        })
      }), /*#__PURE__*/jsx_runtime_.jsx(react_.Flex, {
        alignItems: "center",
        children: /*#__PURE__*/(0,jsx_runtime_.jsxs)(react_.Menu, {
          children: [/*#__PURE__*/jsx_runtime_.jsx(react_.MenuButton, {
            as: react_.Button,
            size: "sm",
            variant: "ghost",
            children: /*#__PURE__*/jsx_runtime_.jsx(Icon/* UserIcon */.tB, {
              color: "gray.700"
            })
          }), /*#__PURE__*/(0,jsx_runtime_.jsxs)(react_.MenuList, {
            shadow: "xl",
            children: [/*#__PURE__*/jsx_runtime_.jsx(react_.Stack, {
              px: 3,
              py: 2,
              spacing: 0,
              children: /*#__PURE__*/jsx_runtime_.jsx(react_.Text, {
                fontWeight: "medium",
                children: username
              })
            }), /*#__PURE__*/jsx_runtime_.jsx(react_.MenuDivider, {}), /*#__PURE__*/jsx_runtime_.jsx(react_.MenuItem, {
              px: 3,
              _focus: {
                color: "complimentary.500",
                bg: "gray.100"
              },
              onClick: handleLogout,
              children: "Sign out"
            })]
          })]
        })
      })]
    })
  });
};

/* harmony default export */ const common_Header = (Header);
;// CONCATENATED MODULE: ./src/features/common/NavBar.tsx











const NavBar = () => {
  const router = (0,router_.useRouter)();
  return /*#__PURE__*/(0,jsx_runtime_.jsxs)(jsx_runtime_.Fragment, {
    children: [/*#__PURE__*/jsx_runtime_.jsx(common_Header, {}), /*#__PURE__*/(0,jsx_runtime_.jsxs)(react_.Flex, {
      borderBottom: "1px",
      borderTop: "1px",
      px: 9,
      py: 1,
      borderColor: "gray.100",
      children: [/*#__PURE__*/jsx_runtime_.jsx(next_link["default"], {
        href: constants/* INDEX_ROUTE */.gp,
        passHref: true,
        children: /*#__PURE__*/jsx_runtime_.jsx(react_.Button, {
          as: "a",
          variant: "ghost",
          mr: 4,
          colorScheme: router && router.pathname === constants/* INDEX_ROUTE */.gp ? "complimentary" : "ghost",
          children: "Subject Requests"
        })
      }), /*#__PURE__*/jsx_runtime_.jsx(next_link["default"], {
        href: constants/* DATASTORE_CONNECTION_ROUTE */.JR,
        passHref: true,
        children: /*#__PURE__*/jsx_runtime_.jsx(react_.Button, {
          as: "a",
          variant: "ghost",
          mr: 4,
          colorScheme: router && router.pathname.startsWith(constants/* DATASTORE_CONNECTION_ROUTE */.JR) ? "complimentary" : "ghost",
          children: "Datastore Connections"
        })
      }), /*#__PURE__*/jsx_runtime_.jsx(next_link["default"], {
        href: constants/* USER_MANAGEMENT_ROUTE */.e3,
        passHref: true,
        children: /*#__PURE__*/jsx_runtime_.jsx(react_.Button, {
          as: "a",
          variant: "ghost",
          mr: 4,
          colorScheme: router && router.pathname.startsWith(constants/* USER_MANAGEMENT_ROUTE */.e3) ? "complimentary" : "ghost",
          children: "User Management"
        })
      }), /*#__PURE__*/jsx_runtime_.jsx(next_link["default"], {
        href: "#",
        passHref: true,
        children: /*#__PURE__*/jsx_runtime_.jsx(react_.Button, {
          as: "a",
          variant: "ghost",
          disabled: true,
          rightIcon: /*#__PURE__*/jsx_runtime_.jsx(Icon/* ArrowDownLineIcon */.mC, {}),
          children: "More"
        })
      })]
    })]
  });
};

/* harmony default export */ const common_NavBar = (NavBar);

/***/ })

};
;