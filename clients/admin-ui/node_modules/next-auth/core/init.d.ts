import { NextAuthOptions } from "..";
import { InternalOptions } from "../lib/types";
import * as cookie from "./lib/cookie";
import { IncomingRequest } from ".";
interface InitParams {
    host?: string;
    userOptions: NextAuthOptions;
    providerId?: string;
    action: InternalOptions["action"];
    /** Callback URL value extracted from the incoming request. */
    callbackUrl?: string;
    /** CSRF token value extracted from the incoming request. From body if POST, from query if GET */
    csrfToken?: string;
    /** Is the incoming request a POST request? */
    isPost: boolean;
    cookies: IncomingRequest["cookies"];
}
/** Initialize all internal options and cookies. */
export declare function init({ userOptions, providerId, action, host, cookies: reqCookies, callbackUrl: reqCallbackUrl, csrfToken: reqCsrfToken, isPost, }: InitParams): Promise<{
    options: InternalOptions;
    cookies: cookie.Cookie[];
}>;
export {};
