import type { OAuthConfig, OAuthUserConfig } from ".";
export interface CognitoProfile {
    sub: string;
    name: string;
    email: string;
    picture: string;
}
export default function Cognito<P extends Record<string, any> = CognitoProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
