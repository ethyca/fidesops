"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = VK;

function VK(options) {
  const apiVersion = "5.126";
  return {
    id: "vk",
    name: "VK",
    type: "oauth",
    authorization: `https://oauth.vk.com/authorize?scope=email&v=${apiVersion}`,
    token: `https://oauth.vk.com/access_token?v=${apiVersion}`,
    userinfo: `https://api.vk.com/method/users.get?fields=photo_100&v=${apiVersion}`,

    profile(result) {
      var _result$response$, _result$response;

      const profile = (_result$response$ = (_result$response = result.response) === null || _result$response === void 0 ? void 0 : _result$response[0]) !== null && _result$response$ !== void 0 ? _result$response$ : {};
      return {
        id: profile.id,
        name: [profile.first_name, profile.last_name].filter(Boolean).join(" "),
        email: profile.email,
        image: profile.photo_100
      };
    },

    options
  };
}