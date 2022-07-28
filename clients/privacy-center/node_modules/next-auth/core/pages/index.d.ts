import type { InternalOptions } from "../../lib/types";
import type { IncomingRequest, OutgoingResponse } from "..";
import type { Cookie } from "../lib/cookie";
import type { ErrorType } from "./error";
declare type RenderPageParams = {
    query?: IncomingRequest["query"];
    cookies?: Cookie[];
} & Partial<Pick<InternalOptions, "url" | "callbackUrl" | "csrfToken" | "providers" | "theme">>;
/**
 * Unless the user defines their [own pages](https://next-auth.js.org/configuration/pages),
 * we render a set of default ones, using Preact SSR.
 */
export default function renderPage(params: RenderPageParams): {
    signin(props?: any): OutgoingResponse<any>;
    signout(props?: any): OutgoingResponse<any>;
    verifyRequest(props?: any): OutgoingResponse<any>;
    error(props?: {
        error?: ErrorType | undefined;
    } | undefined): OutgoingResponse<any>;
};
export {};
