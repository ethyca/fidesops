import { Divider, Heading } from "@fidesui/react";
import React from "react";

import { useCreateUserMutation } from "./user-management.slice";
import UserForm from "./UserForm";

const NewUserForm = () => {
  const [createUser] = useCreateUserMutation();

  return (
    <div>
      <main>
        <Heading mb={4} fontSize="xl" colorScheme="primary">
          Profile
        </Heading>
        <Divider mb={7} />
        <UserForm onSubmit={createUser} />
      </main>
    </div>
  );
};

export default NewUserForm;
