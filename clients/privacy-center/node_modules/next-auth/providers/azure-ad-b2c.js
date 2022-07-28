"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = AzureADB2C;

function AzureADB2C(options) {
  const {
    tenantId,
    primaryUserFlow
  } = options;
  return {
    id: "azure-ad-b2c",
    name: "Azure Active Directory B2C",
    type: "oauth",
    wellKnown: `https://${tenantId}.b2clogin.com/${tenantId}.onmicrosoft.com/${primaryUserFlow}/v2.0/.well-known/openid-configuration`,
    idToken: true,

    profile(profile) {
      return {
        id: profile.sub,
        name: profile.name,
        email: profile.emails[0],
        image: null
      };
    },

    options
  };
}