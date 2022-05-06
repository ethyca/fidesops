import React from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import { useFormik } from 'formik';
import {
  Button,
  chakra,
  CheckboxGroup,
  Checkbox,
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
  selectManagedUser,
  useEditUserMutation,
  useUpdateUserPermissionsMutation,
  useCreateUserMutation,
  useCreateUserPermissionsMutation,
  useGetUserByIdQuery,
  useGetUserPermissionsQuery,
} from '../user/user.slice';
import { userPrivilegesArray, User } from '../user/types';
import { useRouter } from 'next/router';

const useUserForm = () => {
  const token = useSelector(selectUserToken);
  const [createUser, createUserResult] = useCreateUserMutation();
  const [createUserPermissions, createUserPermissionsResult] =
    useCreateUserPermissionsMutation();
  // const [editUser, editUserResult] = useEditUserMutation();
  const router = useRouter();
  const existingUser = useSelector(selectManagedUser);
  const existingScopes = useGetUserPermissionsQuery(existingUser?.id);
  // console.log('EXISTING', existingScopes.data.scopes);

  const formik = useFormik({
    initialValues: {
      username: existingUser ? existingUser?.username : '',
      first_name: existingUser ? existingUser?.first_name : '',
      last_name: existingUser ? existingUser?.last_name : '',
      password: existingUser ? '********' : '',
      // scopes: existingUser
      //   ? existingScopes?.data?.scopes.filter(
      //       (scope) => scope === values.scopes
      //     )
      //   : [],
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

      const permissionsBody = () => {
        const allScopes = [...values.scopes];
        return allScopes;
      };

      if (!existingUser) {
        createUser(userBody)
          .then((result) => {
            result = { ...result, scopes: permissionsBody() };
            console.log('result', result);
            createUserPermissions(result);
          })
          .then((result) => router.replace('/user-management'));
      } else {
        console.log('on edit page');
        console.log('permissionsBody', permissionsBody());
        // editUser({existingId, ...body})
        // router.push('/user-management');
      }
    },
    validate: (values) => {
      const errors: {
        username?: string;
        first_name?: string;
        last_name?: string;
        password?: string;
      } = {};

      if (!values.username) {
        errors.username = 'Username is required';
      }

      if (!values.first_name) {
        errors.first_name = 'First name is required';
      }

      if (!values.last_name) {
        errors.last_name = 'Last name is required';
      }

      if (!values.password) {
        errors.password = 'Password is required';
      }

      return errors;
    },
  });

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
        <Heading fontSize="xl" colorScheme="primary">
          Profile
        </Heading>
        <chakra.form
          onSubmit={handleSubmit}
          maxW={['xs', 'xs', '100%']}
          width="100%"
        >
          <Stack spacing={6}>
            <FormControl
              id="username"
              isInvalid={touched.username && Boolean(errors.username)}
            >
              <FormLabel htmlFor="username" fontWeight="medium">
                Username
              </FormLabel>
              <Input
                id="username"
                maxWidth={'40%'}
                name="username"
                focusBorderColor="primary.500"
                placeholder={
                  existingUser ? existingUser?.last_name : 'Enter new username'
                }
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.username}
                isInvalid={touched.username && Boolean(errors.username)}
                isReadOnly={existingUser ? true : false}
                isDisabled={existingUser ? true : false}
              />
              <FormErrorMessage>{errors.username}</FormErrorMessage>
            </FormControl>

            <FormControl
              id="first_name"
              isInvalid={touched.first_name && Boolean(errors.first_name)}
            >
              <FormLabel htmlFor="first_name" fontWeight="medium">
                First Name
              </FormLabel>
              <Input
                id="first_name"
                maxWidth={'40%'}
                name="first_name"
                focusBorderColor="primary.500"
                placeholder={
                  existingUser
                    ? existingUser?.last_name
                    : 'Enter first name of user'
                }
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.first_name}
                isInvalid={touched.first_name && Boolean(errors.first_name)}
              />
              <FormErrorMessage>{errors.first_name}</FormErrorMessage>
            </FormControl>

            <FormControl
              id="last_name"
              isInvalid={touched.last_name && Boolean(errors.last_name)}
            >
              <FormLabel htmlFor="last_name" fontWeight="medium">
                Last Name
              </FormLabel>
              <Input
                id="last_name"
                maxWidth={'40%'}
                name="last_name"
                focusBorderColor="primary.500"
                placeholder={
                  existingUser
                    ? existingUser?.last_name
                    : 'Enter last name of user'
                }
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.last_name}
                isInvalid={touched.last_name && Boolean(errors.last_name)}
              />
              <FormErrorMessage>{errors.last_name}</FormErrorMessage>
            </FormControl>

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
                placeholder={existingUser ? existingUser?.password : '********'}
                type="password"
                value={values.password}
                onChange={handleChange}
                onBlur={handleBlur}
                isInvalid={touched.password && Boolean(errors.password)}
              />
              <FormErrorMessage>{errors.password}</FormErrorMessage>
            </FormControl>

            <Heading fontSize="xl" colorScheme="primary">
              Preferences
            </Heading>
            <Text>Select privileges to assign to this user</Text>
            <CheckboxGroup colorScheme="secondary">
              <Stack spacing={[1, 5]} direction={'column'}>
                {userPrivilegesArray.map((policy, idx) => (
                  <>
                    <Checkbox
                      key={`${policy.privilege}-${idx}`}
                      onChange={handleChange}
                      value={policy.scope}
                      id={`scopes-${policy.privilege}-${idx}`}
                      name="scopes"
                      checked={values.scopes}
                    >
                      {policy.privilege}
                    </Checkbox>
                  </>
                ))}
              </Stack>
            </CheckboxGroup>
          </Stack>

          <NextLink href="/user-management" passHref>
            <Button variant="outline" size="sm">
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
