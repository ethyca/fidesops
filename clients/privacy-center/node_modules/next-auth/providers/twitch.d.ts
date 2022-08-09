import type { OAuthConfig, OAuthUserConfig } from ".";
export interface TwitchProfile {
    sub: string;
    preferred_username: string;
    email: string;
    picture: string;
}
export default function Twitch<P extends Record<string, any> = TwitchProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
