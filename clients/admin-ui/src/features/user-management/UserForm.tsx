import React, { useEffect, useState } from 'react';
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
  useEditUserMutation,
  useUpdateUserPermissionsMutation,
  useCreateUserMutation,
  useCreateUserPermissionsMutation,
  useGetUserByIdQuery,
  useGetUserPermissionsQuery,
} from '../user/user.slice';
import { userPrivilegesArray } from '../user/types';

import { useRouter } from 'next/router';

const useUserForm = (
  existingUser?: {
    data: { id: string; username: string; password: string; name: string };
  } | null
) => {
  const token = useSelector(selectUserToken);
  const [createUser, createUserResult] = useCreateUserMutation();
  const [createUserPermissions, createUserPermissionsResult] =
    useCreateUserPermissionsMutation();
  // const [editUser, editUserResult] = useEditUserMutation();
  const router = useRouter();

  const formik = useFormik({
    initialValues: {
      username: existingUser?.data?.username || '',
      name: existingUser?.data?.name || '',
      password: existingUser?.data?.password ? '********' : '',
      scopes: existingUser
        ? useGetUserPermissionsQuery(existingUser.data.id)
        : [],
    },
    onSubmit: async (values) => {
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;

      const userBody = {
        username: values.username,
        name: values.name,
        password: values.password,
      };

      const permissionsBody = () => {
        const permissionsForUser: string[] = [];
        // add values.checkbox to array
        // map through userPrivilegesArray
        // map through checkboxes - if the value matches
        // the privilege.privilege, then spread the privilege.scopes
        // into the permissionsForUser array declared above
        // use Set to check for duplicates

        return existingUser
          ? {
              scopes: permissionsForUser,
              id: existingUser.data.id,
            }
          : {
              scopes: permissionsForUser,
            };
      };

      if (!existingUser) {
        createUser(userBody);
        createUserPermissions(permissionsBody());
        router.replace('/user-management');
      } else {
        console.log('on edit page');
        // editUser({existingId, ...body})
      }

      // redirect after creating/editing
      // router.push('/user-management');
    },
    validate: (values) => {
      const errors: {
        username?: string;
        name?: string;
        password?: string;
      } = {};

      if (!values.username) {
        errors.username = 'Username is required';
      }

      if (!values.name) {
        errors.name = 'Name is required';
      }

      if (!values.password) {
        errors.password = 'Password is required';
      }

      return errors;
    },
  });

  return {
    ...formik,
    // isLoading: createUserResult.isLoading,
    existingUser,
  };
};

const UserForm: NextPage<{
  existingUser?: {
    data: { id: string; username: string; password: string; name: string };
  } | null;
}> = ({ existingUser }) => {
  const {
    dirty,
    errors,
    handleBlur,
    handleChange,
    handleSubmit,
    isValid,
    // isLoading,
    touched,
    values,
  } = useUserForm(existingUser);

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
                name="username"
                focusBorderColor="primary.500"
                placeholder="Enter new username"
                onChange={handleChange}
                onBlur={handleBlur}
                value={
                  existingUser ? existingUser?.data?.username : values.username
                }
                isInvalid={touched.username && Boolean(errors.username)}
                isReadOnly={existingUser ? true : false}
                isDisabled={existingUser ? true : false}
              />
              <FormErrorMessage>{errors.username}</FormErrorMessage>
            </FormControl>

            <FormControl
              id="name"
              isInvalid={touched.name && Boolean(errors.name)}
            >
              <FormLabel htmlFor="name" fontWeight="medium">
                Name
              </FormLabel>
              <Input
                id="name"
                name="name"
                focusBorderColor="primary.500"
                placeholder="Enter name of user"
                onChange={handleChange}
                onBlur={handleBlur}
                value={existingUser ? existingUser?.data?.name : values.name}
                isInvalid={touched.name && Boolean(errors.name)}
              />
              <FormErrorMessage>{errors.name}</FormErrorMessage>
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
                name="password"
                focusBorderColor="primary.500"
                placeholder="********"
                type="password"
                value={
                  existingUser ? existingUser?.data?.password : values.password
                }
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
                      value={policy.privilege}
                      id="checkbox"
                      name="checkbox"
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
