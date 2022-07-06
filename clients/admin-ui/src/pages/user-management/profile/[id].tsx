import React from "react";

import EditUserForm from "../../../features/user-management/EditUserForm";
import UserManagementLayout from "../../../features/user-management/UserManagementLayout";

const Profile = () => (
  <UserManagementLayout title="Edit User">
    <EditUserForm />
  </UserManagementLayout>
);

export default Profile;
