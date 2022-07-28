/// <reference types="react" />
import { Theme } from "../..";
import { InternalUrl } from "../../lib/parse-url";
export interface SignoutProps {
    url: InternalUrl;
    csrfToken: string;
    theme: Theme;
}
export default function SignoutPage(props: SignoutProps): JSX.Element;
