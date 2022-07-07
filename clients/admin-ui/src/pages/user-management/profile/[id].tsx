import { Spinner } from "@fidesui/react";
import { useRouter } from "next/router";
import React from "react";

import EditUserForm from "../../../features/user-management/EditUserForm";
import { useGetUserByIdQuery } from "../../../features/user-management/user-management.slice";
import UserManagementLayout from "../../../features/user-management/UserManagementLayout";

const Profile = () => {
  const router = useRouter();
  let profileId = "";
  if (router.query.id) {
    profileId = Array.isArray(router.query.id)
      ? router.query.id[0]
      : router.query.id;
  } else {
    profileId = "";
  }
  const { data: existingUser, isLoading } = useGetUserByIdQuery(profileId);

  if (isLoading) {
    return (
      <UserManagementLayout title="Edit User">
        <Spinner />
      </UserManagementLayout>
    );
  }

  if (existingUser == null) {
    return (
      <UserManagementLayout title="Edit User">
        Could not find profile ID.
      </UserManagementLayout>
    );
  }

  return (
    <UserManagementLayout title="Edit User">
      <EditUserForm user={existingUser} />
    </UserManagementLayout>
  );
};

export default Profile;
