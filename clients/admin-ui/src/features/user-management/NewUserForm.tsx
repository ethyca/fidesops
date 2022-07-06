import { Divider, Heading, useToast } from "@fidesui/react";
import { useRouter } from "next/router";
import React from "react";

import { USER_MANAGEMENT_ROUTE } from "../../constants";
import { isErrorWithDetail, isErrorWithDetailArray } from "../common/helpers";
import {
  useCreateUserMutation,
  useUpdateUserPermissionsMutation,
} from "./user-management.slice";
import type { FormValues } from "./UserForm";
import UserForm from "./UserForm";

const NewUserForm = () => {
  const [createUser] = useCreateUserMutation();
  const [updateUserPermissions] = useUpdateUserPermissionsMutation();
  const router = useRouter();
  const toast = useToast();

  const handleSubmit = async (values: FormValues) => {
    const createUserResult = await createUser(values);

    if ("error" in createUserResult) {
      let errorMsg = "An unexpected error occurred. Please try again.";
      if (isErrorWithDetail(createUserResult.error)) {
        errorMsg = createUserResult.error.data.detail;
      } else if (isErrorWithDetailArray(createUserResult.error)) {
        const { error } = createUserResult;
        errorMsg = error.data.detail[0].msg;
      }
      toast({
        status: "error",
        description: errorMsg,
      });
      return;
    }

    const { data } = createUserResult;

    const userWithPrivileges = {
      id: data ? data.id : null,
      scopes: [...values.scopes, "privacy-request:read"],
    };

    const updateUserPermissionsResult = await updateUserPermissions(
      userWithPrivileges as { id: string }
    );

    if (!("error" in updateUserPermissionsResult)) {
      router.push(USER_MANAGEMENT_ROUTE);
    }
  };

  return (
    <div>
      <main>
        <Heading mb={4} fontSize="xl" colorScheme="primary">
          Profile
        </Heading>
        <Divider mb={7} />
        <UserForm onSubmit={handleSubmit} />
      </main>
    </div>
  );
};

export default NewUserForm;
