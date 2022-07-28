import type { OAuthConfig, OAuthUserConfig } from ".";
export interface FacebookProfile {
    id: string;
    picture: {
        data: {
            url: string;
        };
    };
}
export default function Facebook<P extends Record<string, any> = FacebookProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
