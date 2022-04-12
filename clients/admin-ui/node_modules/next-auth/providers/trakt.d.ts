import type { OAuthConfig, OAuthUserConfig } from ".";
export interface TraktUser {
    username: string;
    private: boolean;
    name: string;
    vip: boolean;
    vip_ep: boolean;
    ids: {
        slug: string;
    };
    joined_at: string;
    location: string | null;
    about: string | null;
    gender: string | null;
    age: number | null;
    images: {
        avatar: {
            full: string;
        };
    };
}
export default function Trakt<P extends Record<string, any> = TraktUser>(options: OAuthUserConfig<P>): OAuthConfig<P>;
