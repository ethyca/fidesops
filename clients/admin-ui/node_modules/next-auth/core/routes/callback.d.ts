import type { InternalOptions } from "../../lib/types";
import type { IncomingRequest, OutgoingResponse } from "..";
import type { SessionStore } from "../lib/cookie";
/** Handle callbacks from login services */
export default function callback(params: {
    options: InternalOptions<"oauth" | "credentials" | "email">;
    query: IncomingRequest["query"];
    method: Required<IncomingRequest>["method"];
    body: IncomingRequest["body"];
    headers: IncomingRequest["headers"];
    cookies: IncomingRequest["cookies"];
    sessionStore: SessionStore;
}): Promise<OutgoingResponse>;
