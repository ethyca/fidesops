"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = Email;

var _nodemailer = require("nodemailer");

function Email(options) {
  return {
    id: "email",
    type: "email",
    name: "Email",
    server: {
      host: "localhost",
      port: 25,
      auth: {
        user: "",
        pass: ""
      }
    },
    from: "NextAuth <no-reply@example.com>",
    maxAge: 24 * 60 * 60,

    async sendVerificationRequest({
      identifier: email,
      url,
      provider: {
        server,
        from
      }
    }) {
      const {
        host
      } = new URL(url);
      const transport = (0, _nodemailer.createTransport)(server);
      await transport.sendMail({
        to: email,
        from,
        subject: `Sign in to ${host}`,
        text: text({
          url,
          host
        }),
        html: html({
          url,
          host,
          email
        })
      });
    },

    options
  };
}

function html({
  url,
  host,
  email
}) {
  const escapedEmail = `${email.replace(/\./g, "&#8203;.")}`;
  const escapedHost = `${host.replace(/\./g, "&#8203;.")}`;
  const backgroundColor = "#f9f9f9";
  const textColor = "#444444";
  const mainBackgroundColor = "#ffffff";
  const buttonBackgroundColor = "#346df1";
  const buttonBorderColor = "#346df1";
  const buttonTextColor = "#ffffff";
  return `
<body style="background: ${backgroundColor};">
  <table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
      <td align="center" style="padding: 10px 0px 20px 0px; font-size: 22px; font-family: Helvetica, Arial, sans-serif; color: ${textColor};">
        <strong>${escapedHost}</strong>
      </td>
    </tr>
  </table>
  <table width="100%" border="0" cellspacing="20" cellpadding="0" style="background: ${mainBackgroundColor}; max-width: 600px; margin: auto; border-radius: 10px;">
    <tr>
      <td align="center" style="padding: 10px 0px 0px 0px; font-size: 18px; font-family: Helvetica, Arial, sans-serif; color: ${textColor};">
        Sign in as <strong>${escapedEmail}</strong>
      </td>
    </tr>
    <tr>
      <td align="center" style="padding: 20px 0;">
        <table border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td align="center" style="border-radius: 5px;" bgcolor="${buttonBackgroundColor}"><a href="${url}" target="_blank" style="font-size: 18px; font-family: Helvetica, Arial, sans-serif; color: ${buttonTextColor}; text-decoration: none; border-radius: 5px; padding: 10px 20px; border: 1px solid ${buttonBorderColor}; display: inline-block; font-weight: bold;">Sign in</a></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td align="center" style="padding: 0px 0px 10px 0px; font-size: 16px; line-height: 22px; font-family: Helvetica, Arial, sans-serif; color: ${textColor};">
        If you did not request this email you can safely ignore it.
      </td>
    </tr>
  </table>
</body>
`;
}

function text({
  url,
  host
}) {
  return `Sign in to ${host}\n${url}\n\n`;
}