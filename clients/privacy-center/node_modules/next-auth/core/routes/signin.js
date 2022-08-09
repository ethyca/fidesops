"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = signin;

var _authorizationUrl = _interopRequireDefault(require("../lib/oauth/authorization-url"));

var _signin = _interopRequireDefault(require("../lib/email/signin"));

async function signin(params) {
  const {
    options,
    query,
    body
  } = params;
  const {
    url,
    adapter,
    callbacks,
    logger,
    provider
  } = options;

  if (!provider.type) {
    return {
      status: 500,
      text: `Error: Type not specified for ${provider.name}`
    };
  }

  if (provider.type === "oauth") {
    try {
      const response = await (0, _authorizationUrl.default)({
        options,
        query
      });
      return response;
    } catch (error) {
      logger.error("SIGNIN_OAUTH_ERROR", {
        error: error,
        provider
      });
      return {
        redirect: `${url}/error?error=OAuthSignin`
      };
    }
  } else if (provider.type === "email") {
    var _body$email$toLowerCa, _body$email, _ref;

    const email = (_body$email$toLowerCa = body === null || body === void 0 ? void 0 : (_body$email = body.email) === null || _body$email === void 0 ? void 0 : _body$email.toLowerCase()) !== null && _body$email$toLowerCa !== void 0 ? _body$email$toLowerCa : null;
    const {
      getUserByEmail
    } = adapter;
    const user = (_ref = email ? await getUserByEmail(email) : null) !== null && _ref !== void 0 ? _ref : {
      email,
      id: email
    };
    const account = {
      providerAccountId: email,
      userId: email,
      type: "email",
      provider: provider.id
    };

    try {
      const signInCallbackResponse = await callbacks.signIn({
        user,
        account,
        email: {
          verificationRequest: true
        }
      });

      if (!signInCallbackResponse) {
        return {
          redirect: `${url}/error?error=AccessDenied`
        };
      } else if (typeof signInCallbackResponse === "string") {
        return {
          redirect: signInCallbackResponse
        };
      }
    } catch (error) {
      return {
        redirect: `${url}/error?${new URLSearchParams({
          error: error
        })}`
      };
    }

    try {
      await (0, _signin.default)(email, options);
    } catch (error) {
      logger.error("SIGNIN_EMAIL_ERROR", error);
      return {
        redirect: `${url}/error?error=EmailSignin`
      };
    }

    const params = new URLSearchParams({
      provider: provider.id,
      type: provider.type
    });
    return {
      redirect: `${url}/verify-request?${params}`
    };
  }

  return {
    redirect: `${url}/signin`
  };
}