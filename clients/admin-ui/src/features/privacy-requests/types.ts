export type PrivacyRequestStatus =
  | 'approved'
  | 'complete'
  | 'denied'
  | 'error'
  | 'in_processing'
  | 'paused'
  | 'pending';


export interface DenyPrivacyRequest{
  id:string,
  reason: string
}


interface FieldsAffected{
  path: string;
  field_name: string;
  data_categories: string[];
}

export interface ExecutionLog{
  collection_name: string;
  fields_affected: FieldsAffected[];
  message: string;
  action_type: string;
  status: string;
  updated_at: string;

}
export interface PrivacyRequest {
  status: PrivacyRequestStatus;
  results?: Record<string, ExecutionLog[]>;
  identity: {
    email?: string;
    phone_number?: string;
  };
  policy: {
    name: string;
    key: string;
  };
  reviewer: {
    id: string;
    username: string;
  };
  created_at: string;
  reviewed_by: string;
  id: string;
}

export interface PrivacyRequestResponse {
  items: PrivacyRequest[];
  total: number;
}

export interface PrivacyRequestParams {
  status?: PrivacyRequestStatus;
  id: string;
  from: string;
  to: string;
  page: number;
  size: number;
  verbose?: boolean;
}
