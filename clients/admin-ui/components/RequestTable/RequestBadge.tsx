import { Badge } from '@fidesui/react';

const statusPropMap = {
  error: {
    bg: 'red.800',
    color: 'white',
    children: 'Error',
  },
  denied: {
    bg: 'red.500',
    color: 'white',
    children: 'Denied',
  },
};

interface RequestBadgeProps {
  status: keyof typeof statusPropMap;
}

const RequestBadge: React.FC<RequestBadgeProps> = ({ status }) => (
  <Badge
    {...statusPropMap[status]}
    width={107}
    lineHeight="18px"
    textAlign="center"
  />
);

export default RequestBadge;
