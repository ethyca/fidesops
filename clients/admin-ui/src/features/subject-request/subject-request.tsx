import React from 'react';

import { PrivacyRequest } from '../privacy-requests/types';
import EventsAndLogs from './events-and-logs';
import RequestDetails from './request-details';
import SubjectIdentities from './subject-indentities';

type SubjectRequestProps = {
  subjectRequest: PrivacyRequest;
};

const SubjectRequest = ({ subjectRequest }: SubjectRequestProps) => (
  <>
    <RequestDetails subjectRequest={subjectRequest} />
    <SubjectIdentities subjectRequest={subjectRequest} />
    <EventsAndLogs subjectRequest={subjectRequest} />
  </>
);

export default SubjectRequest;
