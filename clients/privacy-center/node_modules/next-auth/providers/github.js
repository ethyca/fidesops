"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = GitHub;

function GitHub(options) {
  return {
    id: "github",
    name: "GitHub",
    type: "oauth",
    authorization: "https://github.com/login/oauth/authorize?scope=read:user+user:email",
    token: "https://github.com/login/oauth/access_token",
    userinfo: {
      url: "https://api.github.com/user",

      async request({
        client,
        tokens
      }) {
        const profile = await client.userinfo(tokens);

        if (!profile.email) {
          const emails = await (await fetch("https://api.github.com/user/emails", {
            headers: {
              Authorization: `token ${tokens.access_token}`
            }
          })).json();

          if ((emails === null || emails === void 0 ? void 0 : emails.length) > 0) {
            var _emails$find;

            profile.email = (_emails$find = emails.find(email => email.primary)) === null || _emails$find === void 0 ? void 0 : _emails$find.email;
            if (!profile.email) profile.email = emails[0].email;
          }
        }

        return profile;
      }

    },

    profile(profile) {
      return {
        id: profile.id.toString(),
        name: profile.name || profile.login,
        email: profile.email,
        image: profile.avatar_url
      };
    },

    options
  };
}