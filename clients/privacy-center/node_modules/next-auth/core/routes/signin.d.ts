import { IncomingRequest, OutgoingResponse } from "..";
import { InternalOptions } from "../../lib/types";
/** Handle requests to /api/auth/signin */
export default function signin(params: {
    options: InternalOptions<"oauth" | "email">;
    query: IncomingRequest["query"];
    body: IncomingRequest["body"];
}): Promise<OutgoingResponse>;
