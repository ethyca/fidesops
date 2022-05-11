// @ts-nocheck
import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import { useFormik } from 'formik';
import {
  Button,
  chakra,
  CheckboxGroup,
  Checkbox,
  Divider,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Stack,
  Text,
} from '@fidesui/react';
import config from './config/config.json';
import {
  selectUserToken,
  useEditUserMutation,
  useUpdateUserPermissionsMutation,
  useGetUserByIdQuery,
  useGetUserPermissionsQuery,
} from '../user/user.slice';
import { userPrivilegesArray, User } from '../user/types';
import { useRouter } from 'next/router';

const useUserForm = () => {
  const token = useSelector(selectUserToken);
  // const [editUser, editUserResult] = useEditUserMutation();
  const router = useRouter();
  const { id } = router.query;
  const { data: existingUser } = useGetUserByIdQuery(id as string);
  const { data: existingScopes, isLoading: scopesLoading } =
    useGetUserPermissionsQuery(id as string);

  const formik = useFormik({
    initialValues: {
      username: existingUser?.username,
      first_name: existingUser?.first_name,
      last_name: existingUser?.last_name,
      password: '********',
      scopes: existingScopes?.scopes | [],
    },
    onSubmit: async (values) => {
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;

      const userBody = {
        username: values.username,
        first_name: values.first_name,
        last_name: values.last_name,
        password: values.password,
      };

      // edit user / user permissions
    },
    validate: (values) => {
      const errors: {
        username?: string;
        first_name?: string;
        last_name?: string;
        password?: string;
      } = {};

      if (!values.password && !existingUser) {
        errors.password = 'Password is required';
      }

      return errors;
    },
  });

  useEffect(() => {
    // TODO: write in some error handling
    if (existingScopes) {
      formik.setFieldValue(
        'scopes',
        existingScopes.scopes.reduce(
          (scopes: string[], scope: string) => ({
            ...scopes,
            [scope]: true,
          }),
          {} as {
            [key: string]: boolean;
          }
        )
      );
    }
  }, [scopesLoading]);

  return {
    ...formik,
    existingUser,
  };
};

const UserForm: NextPage<{
  existingUser?: User;
}> = () => {
  const {
    dirty,
    errors,
    existingUser,
    handleBlur,
    handleChange,
    handleSubmit,
    isValid,
    touched,
    values,
  } = useUserForm();

  return (
    <div>
      <main>
        <Heading mb={4} fontSize="xl" colorScheme="primary">
          Profile
        </Heading>
        <Divider mb={7} />
        <chakra.form
          onSubmit={handleSubmit}
          maxW={['xs', 'xs', '100%']}
          width="100%"
        >
          <Stack mb={8} spacing={6}>
            <FormControl id="username">
              <FormLabel htmlFor="username" fontWeight="medium">
                Username
              </FormLabel>
              <Input
                id="username"
                maxWidth={'40%'}
                name="username"
                focusBorderColor="primary.500"
                placeholder={existingUser?.username}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.username}
                isReadOnly={true}
                isDisabled={true}
              />
            </FormControl>

            <FormControl id="first_name">
              <FormLabel htmlFor="first_name" fontWeight="medium">
                First Name
              </FormLabel>
              <Input
                id="first_name"
                maxWidth={'40%'}
                name="first_name"
                focusBorderColor="primary.500"
                placeholder={existingUser?.first_name}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.first_name}
                // Only admins can edit names - need to add a check for admin role here
                // isReadOnly={existingUser && !adminUser ? true : false}
                // isDisabled={existingUser ? && !adminUser ? true : false}
              />
            </FormControl>

            <FormControl id="last_name">
              <FormLabel htmlFor="last_name" fontWeight="medium">
                Last Name
              </FormLabel>
              <Input
                id="last_name"
                maxWidth={'40%'}
                name="last_name"
                focusBorderColor="primary.500"
                placeholder={existingUser?.last_name}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.last_name}
                // Only admins can edit names - need to add a check for admin role here
                // isReadOnly={existingUser && !adminUser ? true : false}
                // isDisabled={existingUser && !adminUser ? true : false}
              />
            </FormControl>

            {/* existing user and it's that user's specific profile */}
            {/* {existingUser && !adminUser ? (
              <div>Change Password</div>
            ) : ( */}
            <>
              <FormControl
                id="password"
                isInvalid={touched.password && Boolean(errors.password)}
              >
                <FormLabel htmlFor="password" fontWeight="medium">
                  Password
                </FormLabel>
                <Input
                  id="password"
                  maxWidth={'40%'}
                  name="password"
                  focusBorderColor="primary.500"
                  placeholder={'********'}
                  type="password"
                  value={values.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  isInvalid={
                    !existingUser?.password &&
                    touched.password &&
                    Boolean(errors.password)
                  }
                  // Only the associated user can edit names - need to add a check for the user id here
                  // isReadOnly={existingUser && adminUser ? true : false}
                  // isDisabled={existingUser && adminUser ? true : false}
                />
                <FormErrorMessage>{errors.password}</FormErrorMessage>
              </FormControl>
            </>
            {/* )} */}
            <Divider mb={7} mt={7} />

            <Heading fontSize="xl" colorScheme="primary">
              Privileges
            </Heading>
            <Text>Edit privileges assigned to this user</Text>
            <Divider mb={2} mt={2} />
            <CheckboxGroup colorScheme="secondary">
              <Stack spacing={[1, 5]} direction={'column'}>
                {userPrivilegesArray.map((policy, idx) => (
                  <>
                    <Checkbox
                      key={`${policy.privilege}-${idx}`}
                      onChange={handleChange}
                      id={`scopes-${policy.privilege}-${idx}`}
                      name="scopes"
                      isChecked={values.scopes[policy.scope]}
                    >
                      {/* Only admins can edit privileges - need to add a check for admin role here */}
                      {/* isReadOnly={existingUser && !adminUser ? true : false} */}
                      {/* isDisabled={existingUser && !adminUser ? true : false} */}
                      {policy.privilege}
                    </Checkbox>
                  </>
                ))}
              </Stack>
            </CheckboxGroup>
          </Stack>

          <NextLink href="/user-management" passHref>
            <Button mr={3} variant="outline" size="sm">
              Cancel
            </Button>
          </NextLink>
          <Button
            type="submit"
            bg="primary.800"
            _hover={{ bg: 'primary.400' }}
            _active={{ bg: 'primary.500' }}
            colorScheme="primary"
            disabled={!existingUser && !(isValid && dirty)}
            size="sm"
          >
            Save
          </Button>
        </chakra.form>
      </main>
    </div>
  );
};

export default UserForm;
