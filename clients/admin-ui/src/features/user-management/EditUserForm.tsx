import { Divider, Heading, useToast } from "@fidesui/react";
import { useRouter } from "next/router";
import React from "react";
import { useSelector } from "react-redux";

import { USER_MANAGEMENT_ROUTE } from "../../constants";
import { selectUser } from "../auth";
import { isErrorWithDetail, isErrorWithDetailArray } from "../common/helpers";
import { User } from "./types";
import {
  useEditUserMutation,
  useGetUserPermissionsQuery,
  useUpdateUserPermissionsMutation,
} from "./user-management.slice";
import UserForm, { FormValues } from "./UserForm";

const useUserForm = (profile: User) => {
  const router = useRouter();
  const currentUser = useSelector(selectUser);
  const [updateUserPermissions] = useUpdateUserPermissionsMutation();
  const [editUser] = useEditUserMutation();
  const { data: profileScopes } = useGetUserPermissionsQuery(profile.id);
  const toast = useToast();

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
    const editUserResult = await editUser(userBody);

    if ("error" in editUserResult) {
      let errorMsg = "An unexpected error occurred. Please try again.";
      if (isErrorWithDetail(editUserResult.error)) {
        errorMsg = editUserResult.error.data.detail;
      } else if (isErrorWithDetailArray(editUserResult.error)) {
        const { error } = editUserResult;
        errorMsg = error.data.detail[0].msg;
      }
      toast({
        status: "error",
        description: errorMsg,
      });
      return;
    }

    const { data } = editUserResult;

    // then issue a separate call to update their permissions
    const userWithPrivileges = {
      id: data.id,
      scopes: [...new Set([...values.scopes, "privacy-request:read"])],
    };
    const updateUserPermissionsResult = await updateUserPermissions(
      userWithPrivileges
    );

    if (!("error" in updateUserPermissionsResult)) {
      router.push(USER_MANAGEMENT_ROUTE);
    }
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
