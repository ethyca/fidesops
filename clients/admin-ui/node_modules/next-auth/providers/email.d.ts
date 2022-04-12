import type { CommonProviderOptions } from ".";
import type { Options as SMTPConnectionOptions } from "nodemailer/lib/smtp-connection";
import type { Awaitable } from "..";
export interface EmailConfig extends CommonProviderOptions {
    type: "email";
    server: string | SMTPConnectionOptions;
    /** @default "NextAuth <no-reply@example.com>" */
    from?: string;
    /**
     * How long until the e-mail can be used to log the user in,
     * in seconds. Defaults to 1 day
     * @default 86400
     */
    maxAge?: number;
    sendVerificationRequest: (params: {
        identifier: string;
        url: string;
        expires: Date;
        provider: EmailConfig;
        token: string;
    }) => Awaitable<void>;
    /**
     * By default, we are generating a random verification token.
     * You can make it predictable or modify it as you like with this method.
     * @example
     * ```js
     *  Providers.Email({
     *    async generateVerificationToken() {
     *      return "ABC123"
     *    }
     *  })
     * ```
     * [Documentation](https://next-auth.js.org/providers/email#customising-the-verification-token)
     */
    generateVerificationToken?: () => Awaitable<string>;
    /** If defined, it is used to hash the verification token when saving to the database . */
    secret?: string;
    options: EmailUserConfig;
}
export declare type EmailUserConfig = Partial<Omit<EmailConfig, "options">>;
export declare type EmailProvider = (options: EmailUserConfig) => EmailConfig;
export declare type EmailProviderType = "Email";
export default function Email(options: EmailUserConfig): EmailConfig;
