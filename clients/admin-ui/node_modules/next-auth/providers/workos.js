"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = WorkOS;

function WorkOS(options) {
  const {
    issuer = "https://api.workos.com/"
  } = options;
  return {
    id: "workos",
    name: "WorkOS",
    type: "oauth",
    authorization: `${issuer}sso/authorize`,
    token: `${issuer}sso/token`,
    userinfo: `${issuer}sso/profile`,

    profile(profile) {
      return {
        id: profile.id,
        name: `${profile.first_name} ${profile.last_name}`,
        email: profile.email,
        image: null
      };
    },

    options
  };
}