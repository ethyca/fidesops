"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
exports.withAuth = withAuth;

var _server = require("next/server");

var _jwt = require("../jwt");

var _parseUrl = _interopRequireDefault(require("../lib/parse-url"));

async function handleMiddleware(req, options, onSuccess) {
  var _options$pages$signIn, _options$pages, _options$pages$error, _options$pages2, _await$options$callba, _options$callbacks, _options$callbacks$au;

  const signInPage = (_options$pages$signIn = options === null || options === void 0 ? void 0 : (_options$pages = options.pages) === null || _options$pages === void 0 ? void 0 : _options$pages.signIn) !== null && _options$pages$signIn !== void 0 ? _options$pages$signIn : "/api/auth/signin";
  const errorPage = (_options$pages$error = options === null || options === void 0 ? void 0 : (_options$pages2 = options.pages) === null || _options$pages2 === void 0 ? void 0 : _options$pages2.error) !== null && _options$pages$error !== void 0 ? _options$pages$error : "/api/auth/error";
  const basePath = (0, _parseUrl.default)(process.env.NEXTAUTH_URL).path;

  if (req.nextUrl.pathname.startsWith(basePath) || [signInPage, errorPage].includes(req.nextUrl.pathname)) {
    return;
  }

  if (!process.env.NEXTAUTH_SECRET) {
    console.error(`[next-auth][error][NO_SECRET]`, `\nhttps://next-auth.js.org/errors#no_secret`);
    const errorUrl = new URL(errorPage, req.nextUrl.origin);
    errorUrl.searchParams.append("error", "Configuration");
    return _server.NextResponse.redirect(errorUrl);
  }

  const token = await (0, _jwt.getToken)({
    req: req
  });
  const isAuthorized = (_await$options$callba = await (options === null || options === void 0 ? void 0 : (_options$callbacks = options.callbacks) === null || _options$callbacks === void 0 ? void 0 : (_options$callbacks$au = _options$callbacks.authorized) === null || _options$callbacks$au === void 0 ? void 0 : _options$callbacks$au.call(_options$callbacks, {
    req,
    token
  }))) !== null && _await$options$callba !== void 0 ? _await$options$callba : !!token;
  if (isAuthorized) return await (onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess(token));
  const signInUrl = new URL(signInPage, req.nextUrl.origin);
  signInUrl.searchParams.append("callbackUrl", req.url);
  return _server.NextResponse.redirect(signInUrl);
}

function withAuth(...args) {
  if (!args.length || args[0] instanceof _server.NextRequest) {
    return handleMiddleware(...args);
  }

  if (typeof args[0] === "function") {
    const middleware = args[0];
    const options = args[1];
    return async (...args) => await handleMiddleware(args[0], options, async token => {
      ;
      args[0].nextauth = {
        token
      };
      return await middleware(...args);
    });
  }

  const options = args[0];
  return async (...args) => await handleMiddleware(args[0], options);
}

var _default = withAuth;
exports.default = _default;