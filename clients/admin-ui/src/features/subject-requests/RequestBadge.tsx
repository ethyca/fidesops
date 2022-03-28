import { ComponentProps } from 'react';
import { Badge } from '@fidesui/react';
import { SubjectRequestStatus } from './subject-requests.slice';

const statusPropMap: {
  [key in SubjectRequestStatus]: ComponentProps<typeof Badge>;
} = {
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
  'in-progress': {
    bg: 'orange.500',
    color: 'white',
    children: 'In Progress',
  },
  new: {
    bg: 'blue.400',
    color: 'white',
    children: 'New',
  },
  completed: {
    bg: 'green.500',
    color: 'white',
    children: 'Completed',
  },
  pending: {
    bg: 'gray.500',
    color: 'white',
    children: 'Pending',
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
