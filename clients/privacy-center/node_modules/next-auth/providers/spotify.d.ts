import type { OAuthConfig, OAuthUserConfig } from ".";
export interface SpotifyImage {
    url: string;
}
export interface SpotifyProfile {
    id: string;
    display_name: string;
    email: string;
    images: SpotifyImage[];
}
export default function Spotify<P extends Record<string, any> = SpotifyProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
