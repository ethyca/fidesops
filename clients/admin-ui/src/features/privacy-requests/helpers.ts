import { useSelector } from 'react-redux';
import { selectRevealPII } from './privacy-requests.slice';

// eslint-disable-next-line import/prefer-default-export
export const useObscurePII = (pii: string) => {
  const revealPII = useSelector(selectRevealPII);
  if (revealPII) {
    return pii;
  }
  return revealPII ? pii : pii.replace(/./g, '*');
};
