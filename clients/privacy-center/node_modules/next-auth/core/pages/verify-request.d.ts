/// <reference types="react" />
import { Theme } from "../..";
import { InternalUrl } from "../../lib/parse-url";
interface VerifyRequestPageProps {
    url: InternalUrl;
    theme: Theme;
}
export default function VerifyRequestPage(props: VerifyRequestPageProps): JSX.Element;
export {};
