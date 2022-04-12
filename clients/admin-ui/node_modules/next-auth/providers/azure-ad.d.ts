import type { OAuthConfig, OAuthUserConfig } from ".";
export interface AzureADProfile {
    sub: string;
    nicname: string;
    email: string;
    picture: string;
}
export default function AzureAD<P extends Record<string, any> = AzureADProfile>(options: OAuthUserConfig<P> & {
    /**
     * https://docs.microsoft.com/en-us/graph/api/profilephoto-get?view=graph-rest-1.0#examples
     * @default 48
     */
    profilePhotoSize?: 48 | 64 | 96 | 120 | 240 | 360 | 432 | 504 | 648;
    /** @default "common" */
    tenantId?: string;
}): OAuthConfig<P>;
