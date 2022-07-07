import { Divider, Heading } from "@fidesui/react";
import React from "react";
import { useSelector } from "react-redux";

import { selectUser } from "../auth";
import { User } from "./types";
import {
  useEditUserMutation,
  useGetUserPermissionsQuery,
} from "./user-management.slice";
import UserForm, { FormValues } from "./UserForm";

const useUserForm = (profile: User) => {
  const currentUser = useSelector(selectUser);
  const [editUser] = useEditUserMutation();
  const { data: profileScopes } = useGetUserPermissionsQuery(profile.id);

  const initialValues = {
    username: profile.username ?? "",
    first_name: profile.first_name ?? "",
    last_name: profile.last_name ?? "",
    password: profile.password ?? "",
    scopes: profileScopes?.scopes ?? [],
    id: profile.id,
  };

  const handleSubmit = async (values: FormValues) => {
    // first update the user object
    const userBody = Object.assign(profile, values);
    return editUser(userBody);
  };

  const isOwnProfile = currentUser ? currentUser.id === profile.id : false;
  let canUpdateUser = false;
  const { data: userPermissions } = useGetUserPermissionsQuery(
    currentUser?.id ?? ""
  );
  if (isOwnProfile) {
    canUpdateUser = true;
  } else {
    canUpdateUser = userPermissions
      ? userPermissions.scopes.includes("user:update")
      : false;
  }

  return {
    handleSubmit,
    isOwnProfile,
    canUpdateUser,
    initialValues,
  };
};

interface Props {
  user: User;
}
const EditUserForm = ({ user }: Props) => {
  const { isOwnProfile, handleSubmit, canUpdateUser, initialValues } =
    useUserForm(user);

  return (
    <div>
      <main>
        <Heading mb={4} fontSize="xl" colorScheme="primary">
          Profile
        </Heading>
        <Divider mb={7} />
        <UserForm
          onSubmit={handleSubmit}
          initialValues={initialValues}
          canEditNames={canUpdateUser}
          canChangePassword={isOwnProfile}
        />
      </main>
    </div>
  );
};

export default EditUserForm;
