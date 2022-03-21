export type SubjectRequestStatus =
  | 'error'
  | 'denied'
  | 'in-progress'
  | 'new'
  | 'completed';

export interface SubjectRequest {
  status: SubjectRequestStatus;
  identity: {
    email?: string;
    phone?: string;
  };
  created_at: string;
  reviewed_by: string;
  id: string;
}
