import type { OAuthConfig, OAuthUserConfig } from ".";
export interface Auth0Profile {
    sub: string;
    nickname: string;
    email: string;
    picture: string;
}
export default function Auth0<P extends Record<string, any> = Auth0Profile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
