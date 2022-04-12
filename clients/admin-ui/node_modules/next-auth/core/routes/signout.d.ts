import type { InternalOptions } from "../../lib/types";
import type { OutgoingResponse } from "..";
import type { SessionStore } from "../lib/cookie";
/** Handle requests to /api/auth/signout */
export default function signout(params: {
    options: InternalOptions;
    sessionStore: SessionStore;
}): Promise<OutgoingResponse>;
