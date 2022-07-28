import type { OAuthConfig, OAuthUserConfig } from ".";
export interface PatreonProfile {
    sub: string;
    nickname: string;
    email: string;
    picture: string;
}
export default function Patreon<P extends Record<string, any> = PatreonProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
