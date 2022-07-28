import type { OAuthConfig, OAuthUserConfig } from ".";
export interface LineProfile {
    iss: string;
    sub: string;
    aud: string;
    exp: number;
    iat: number;
    amr: string[];
    name: string;
    picture: string;
    user: any;
}
export default function LINE<P extends Record<string, any> = LineProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
