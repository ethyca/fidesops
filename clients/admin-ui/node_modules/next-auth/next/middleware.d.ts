import type { NextMiddleware, NextFetchEvent } from "next/server";
import type { Awaitable, NextAuthOptions } from "..";
import type { JWT } from "../jwt";
import { NextRequest } from "next/server";
declare type AuthorizedCallback = (params: {
    token: JWT | null;
    req: NextRequest;
}) => Awaitable<boolean>;
export interface NextAuthMiddlewareOptions {
    /**
     * Where to redirect the user in case of an error if they weren't logged in.
     * Similar to `pages` in `NextAuth`.
     *
     * ---
     * [Documentation](https://next-auth.js.org/configuration/pages)
     */
    pages?: NextAuthOptions["pages"];
    callbacks?: {
        /**
         * Callback that receives the user's JWT payload
         * and returns `true` to allow the user to continue.
         *
         * This is similar to the `signIn` callback in `NextAuthOptions`.
         *
         * If it returns `false`, the user is redirected to the sign-in page instead
         *
         * The default is to let the user continue if they have a valid JWT (basic authentication).
         *
         * How to restrict a page and all of it's subpages for admins-only:
         * @example
         *
         * ```js
         * // `pages/admin/_middleware.js`
         * import { withAuth } from "next-auth/middleware"
         *
         * export default withAuth({
         *   callbacks: {
         *     authorized: ({ token }) => token?.user.isAdmin
         *   }
         * })
         * ```
         *
         * ---
         * [Documentation](https://next-auth.js.org/getting-started/nextjs/middleware#api) | [`signIn` callback](configuration/callbacks#sign-in-callback)
         */
        authorized?: AuthorizedCallback;
    };
}
export declare type WithAuthArgs = [NextRequest] | [NextRequest, NextFetchEvent] | [NextRequest, NextAuthMiddlewareOptions] | [NextMiddleware] | [NextMiddleware, NextAuthMiddlewareOptions] | [NextAuthMiddlewareOptions] | [];
/**
 * Middleware that checks if the user is authenticated/authorized.
 * If if they aren't, they will be redirected to the login page.
 * Otherwise, continue.
 *
 * @example
 *
 * ```js
 * // `pages/_middleware.js`
 * export { default } from "next-auth/middleware"
 * ```
 *
 * ---
 * [Documentation](https://next-auth.js.org/getting-started/middleware)
 */
export declare function withAuth(...args: WithAuthArgs): Promise<any> | ((request: NextRequest, event: NextFetchEvent) => Promise<any>);
export default withAuth;
