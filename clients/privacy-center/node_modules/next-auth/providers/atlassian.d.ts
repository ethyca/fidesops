import type { OAuthConfig, OAuthUserConfig } from ".";
interface AtlassianProfile {
    account_id: string;
    name: string;
    email: string;
    picture: string;
}
export default function Atlassian<P extends AtlassianProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
export {};
