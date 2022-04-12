"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
exports.getServerSession = getServerSession;

var _core = require("../core");

var _utils = require("./utils");

async function NextAuthNextHandler(req, res, options) {
  var _ref, _options$secret, _options$jwt, _ref2, _handler$status, _handler$cookies, _handler$headers;

  const {
    nextauth,
    ...query
  } = req.query;
  options.secret = (_ref = (_options$secret = options.secret) !== null && _options$secret !== void 0 ? _options$secret : (_options$jwt = options.jwt) === null || _options$jwt === void 0 ? void 0 : _options$jwt.secret) !== null && _ref !== void 0 ? _ref : process.env.NEXTAUTH_SECRET;
  const handler = await (0, _core.NextAuthHandler)({
    req: {
      host: (0, _utils.detectHost)(req.headers["x-forwarded-host"]),
      body: req.body,
      query,
      cookies: req.cookies,
      headers: req.headers,
      method: req.method,
      action: nextauth === null || nextauth === void 0 ? void 0 : nextauth[0],
      providerId: nextauth === null || nextauth === void 0 ? void 0 : nextauth[1],
      error: (_ref2 = req.query.error) !== null && _ref2 !== void 0 ? _ref2 : nextauth === null || nextauth === void 0 ? void 0 : nextauth[1]
    },
    options
  });
  res.status((_handler$status = handler.status) !== null && _handler$status !== void 0 ? _handler$status : 200);
  (_handler$cookies = handler.cookies) === null || _handler$cookies === void 0 ? void 0 : _handler$cookies.forEach(cookie => (0, _utils.setCookie)(res, cookie));
  (_handler$headers = handler.headers) === null || _handler$headers === void 0 ? void 0 : _handler$headers.forEach(h => res.setHeader(h.key, h.value));

  if (handler.redirect) {
    var _req$body;

    if (((_req$body = req.body) === null || _req$body === void 0 ? void 0 : _req$body.json) !== "true") {
      res.status(302).setHeader("Location", handler.redirect);
      return res.end();
    }

    return res.json({
      url: handler.redirect
    });
  }

  return res.send(handler.body);
}

function NextAuth(...args) {
  if (args.length === 1) {
    return async (req, res) => await NextAuthNextHandler(req, res, args[0]);
  }

  return NextAuthNextHandler(args[0], args[1], args[2]);
}

var _default = NextAuth;
exports.default = _default;

async function getServerSession(context, options) {
  const session = await (0, _core.NextAuthHandler)({
    options,
    req: {
      host: (0, _utils.detectHost)(context.req.headers["x-forwarded-host"]),
      action: "session",
      method: "GET",
      cookies: context.req.cookies,
      headers: context.req.headers
    }
  });
  const {
    body,
    cookies
  } = session;
  cookies === null || cookies === void 0 ? void 0 : cookies.forEach(cookie => (0, _utils.setCookie)(context.res, cookie));
  if (body && Object.keys(body).length) return body;
  return null;
}