import type { OAuthConfig, OAuthUserConfig } from ".";
/** https://developers.naver.com/docs/login/profile/profile.md */
export interface NaverProfile {
    resultcode: string;
    message: string;
    response: {
        id: string;
        nickname?: string;
        name?: string;
        email?: string;
        gender?: "F" | "M" | "U";
        age?: string;
        birthday?: string;
        profile_image?: string;
        birthyear?: string;
        mobile?: string;
    };
}
export default function Naver<P extends Record<string, any> = NaverProfile>(options: OAuthUserConfig<P>): OAuthConfig<P>;
