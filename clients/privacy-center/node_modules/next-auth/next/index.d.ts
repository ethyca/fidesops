import type { GetServerSidePropsContext, NextApiRequest, NextApiResponse } from "next";
import type { NextAuthOptions, Session } from "..";
declare function NextAuth(options: NextAuthOptions): any;
declare function NextAuth(req: NextApiRequest, res: NextApiResponse, options: NextAuthOptions): any;
export default NextAuth;
export declare function getServerSession(context: GetServerSidePropsContext | {
    req: NextApiRequest;
    res: NextApiResponse;
}, options: NextAuthOptions): Promise<Session | null>;
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            NEXTAUTH_URL?: string;
            VERCEL?: "1";
        }
    }
}
