export type PrivacyRequestStatus =
  | 'approved'
  | 'complete'
  | 'denied'
  | 'error'
  | 'in_processing'
  | 'paused'
  | 'pending';

export interface PrivacyRequest {
  status: PrivacyRequestStatus;
  identity: {
    email?: string;
    phone?: string;
  };
  created_at: string;
  reviewed_by: string;
  id: string;
}

export interface PrivacyRequestResponse {
  items: PrivacyRequest[];
}
