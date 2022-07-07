import { Divider, Heading, useToast } from "@fidesui/react";
import { useRouter } from "next/router";
import React from "react";
import { useSelector } from "react-redux";

import { USER_MANAGEMENT_ROUTE } from "../../constants";
import { selectUser } from "../auth";
import { User } from "./types";
import {
  useEditUserMutation,
  useGetUserByIdQuery,
  useGetUserPermissionsQuery,
  useUpdateUserPermissionsMutation,
} from "./user-management.slice";
import UserForm from "./UserForm";

const useUserForm = (profileId: string) => {
  const router = useRouter();
  const currentUser = useSelector(selectUser);
  const [updateUserPermissions] = useUpdateUserPermissionsMutation();
  const [editUser] = useEditUserMutation({ id: profileId });
  const { data: existingUser } = useGetUserByIdQuery(profileId);
  const { data: existingScopes } = useGetUserPermissionsQuery(profileId);
  const toast = useToast();

  const initialValues = {
    username: existingUser?.username ?? "",
    first_name: existingUser?.first_name ?? "",
    last_name: existingUser?.last_name ?? "",
    password: existingUser?.password ?? "",
    scopes: existingScopes?.scopes ?? "",
    id: existingUser?.id ?? "",
  };

  const handleSubmit = async (values) => {
    const userBody = {
      username: values.username ? values.username : existingUser?.username,
      first_name: values.first_name
        ? values.first_name
        : existingUser?.first_name,
      last_name: values.last_name ? values.last_name : existingUser?.last_name,
      password: values.password ? values.password : existingUser?.password,
      id: existingUser?.id,
    };

    const { error: editUserError, data } = await editUser(userBody);

    if (editUserError) {
      toast({
        status: "error",
        description: editUserError.data.detail.length
          ? `${editUserError.data.detail[0].msg}`
          : "An unexpected error occurred. Please try again.",
      });
      return;
    }

    if (editUserError && editUserError.status === 422) {
      toast({
        status: "error",
        description: editUserError.data.detail.length
          ? `${editUserError.data.detail[0].msg}`
          : "An unexpected error occurred. Please try again.",
      });
    }

    const userWithPrivileges = {
      id: data ? data.id : null,
      scopes: [...new Set(values.scopes, "privacy-request:read")],
    };

    const { error: updatePermissionsError } = await updateUserPermissions(
      userWithPrivileges
    );

    if (!updatePermissionsError) {
      router.push(USER_MANAGEMENT_ROUTE);
    }
  };

  let canUpdateUser = false;
  const { data: userPermissions = { scopes: [] } } = useGetUserPermissionsQuery(
    currentUser.id
  );
  canUpdateUser = userPermissions.scopes.includes("user:update");

  return {
    handleSubmit,
    isOwnProfile: profileId === currentUser.id,
    canUpdateUser,
    initialValues,
  };
};

interface Props {
  profileId: string;
}
const EditUserForm: React.FC = ({ profileId }: Props) => {
  const { isOwnProfile, handleSubmit, canUpdateUser, initialValues } =
    useUserForm(profileId);

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
