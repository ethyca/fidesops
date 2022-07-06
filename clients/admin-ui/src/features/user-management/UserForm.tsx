import {
  Button,
  chakra,
  Checkbox,
  Divider,
  Heading,
  Stack,
  Text,
} from "@fidesui/react";
import { Formik } from "formik";
import NextLink from "next/link";
import { useRouter } from "next/router";
import React from "react";

import { USER_MANAGEMENT_ROUTE, USER_PRIVILEGES } from "../../constants";
import { CustomTextInput } from "./form/inputs";
import UpdatePasswordModal from "./UpdatePasswordModal";

const defaultInitialValues = {
  username: "",
  first_name: "",
  last_name: "",
  password: "",
  scopes: ["privacy-request:read"],
};

type FormValues = typeof defaultInitialValues;

interface Props {
  onSubmit: (values: FormValues) => void;
  initialValues?: FormValues;
  canEditNames?: boolean;
  canChangePassword?: boolean;
}

const UserForm = ({
  onSubmit,
  initialValues,
  canEditNames,
  canChangePassword,
}: Props) => {
  const router = useRouter();
  const profileId = Array.isArray(router.query.id)
    ? router.query.id[0]
    : router.query.id;
  const isNewUser = profileId != null;

  <Formik
    onSubmit={onSubmit}
    initialValues={initialValues ?? defaultInitialValues}
  >
    {({ values, setFieldValue }) => (
      <chakra.form maxW={["xs", "xs", "100%"]} width="100%">
        <Stack mb={8} spacing={6}>
          <CustomTextInput
            name="username"
            label="Username"
            placeholder="Enter new username"
          />
          <CustomTextInput
            name="first_name"
            label="First Name"
            placeholder="Enter first name of user"
            disabled={!canEditNames}
          />
          <CustomTextInput
            name="last_name"
            label="Last Name"
            placeholder="Enter last name of user"
            disabled={!canEditNames}
          />
          {isNewUser ? (
            <CustomTextInput
              name="password"
              label="Password"
              placeholder="********"
              type="password"
            />
          ) : (
            canChangePassword &&
            profileId != null && <UpdatePasswordModal id={profileId} />
          )}
          <Divider mb={7} mt={7} />
          <Heading fontSize="xl" colorScheme="primary">
            Privileges
          </Heading>
          <Text>
            {isNewUser
              ? "Select privileges assigned to this user"
              : "Edit privileges assigned to this user"}
          </Text>
          <Divider mb={2} mt={2} />

          <Stack spacing={[1, 5]} direction="column">
            {USER_PRIVILEGES.map((policy) => {
              const isChecked = values.scopes.indexOf(policy.scope) >= 0;
              return (
                <Checkbox
                  colorScheme="purple"
                  key={policy.privilege}
                  onChange={() => {
                    if (!isChecked) {
                      setFieldValue(`scopes`, [...values.scopes, policy.scope]);
                    } else {
                      setFieldValue(
                        "scopes",
                        values.scopes.filter((scope) => scope !== policy.scope)
                      );
                    }
                  }}
                  id={`scopes-${policy.privilege}`}
                  name="scopes"
                  isChecked={isChecked}
                  value={
                    policy.scope === "privacy-request:read"
                      ? undefined
                      : policy.scope
                  }
                  isDisabled={policy.scope === "privacy-request:read"}
                  isReadOnly={policy.scope === "privacy-request:read"}
                >
                  {policy.privilege}
                </Checkbox>
              );
            })}
          </Stack>
        </Stack>

        <NextLink href={USER_MANAGEMENT_ROUTE} passHref>
          <Button variant="outline" mr={3} size="sm">
            Cancel
          </Button>
        </NextLink>
        <Button
          type="submit"
          bg="primary.800"
          _hover={{ bg: "primary.400" }}
          _active={{ bg: "primary.500" }}
          colorScheme="primary"
          size="sm"
        >
          Save
        </Button>
      </chakra.form>
    )}
  </Formik>;
};

export default UserForm;
