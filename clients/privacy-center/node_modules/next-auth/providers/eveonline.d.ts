import type { OAuthConfig, OAuthUserConfig } from ".";
export interface EVEOnlineProfile {
    CharacterID: number;
    CharacterName: string;
    ExpiresOn: string;
    Scopes: string;
    TokenType: string;
    CharacterOwnerHash: string;
    IntellectualProperty: string;
}
export default function EVEOnline<P extends Record<string, any> = EVEOnlineProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
