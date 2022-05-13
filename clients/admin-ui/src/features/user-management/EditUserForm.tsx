// @ts-nocheck
import React, { ChangeEvent, useEffect } from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import { useFormik } from 'formik';
import {
  Button,
  chakra,
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
  const router = useRouter();
  const { id } = router.query;
  const [updateUserPermissions, updateUserPermissionsResult] =
    useUpdateUserPermissionsMutation();
  const [editUser, editUserResult] = useEditUserMutation(id as string);
  const { data: existingUser } = useGetUserByIdQuery(id as string);
  const { data: existingScopes, isLoading: scopesLoading } =
    useGetUserPermissionsQuery(id as string);

  const formik = useFormik({
    initialValues: {
      username: existingUser?.username ?? '',
      first_name: existingUser?.first_name ?? '',
      last_name: existingUser?.last_name ?? '',
      password: '********',
      scopes: existingScopes?.scopes ?? '',
      id: existingUser?.id ?? '',
    },
    enableReinitialize: true,
    onSubmit: async (values) => {
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;

      const userBody = {
        username: values.username ? values.username : existingUser?.username,
        first_name: values.first_name
          ? values.first_name
          : existingUser?.first_name,
        last_name: values.last_name
          ? values.last_name
          : existingUser?.last_name,
        password: values.password ? values.password : existingUser?.password,
        id: existingUser?.id,
      };

      await editUser(userBody)
        .then((result) => {
          const userWithPrivileges = {
            id: 'data' in result ? result.data.id : null,
            scopes: [...values.scopes, 'privacy-request:read'],
          };
          return userWithPrivileges;
        })
        .then((result) => {
          updateUserPermissions(result);
          return result;
        })
        .then(() => {
          router.replace('/user-management');
        });
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

  return {
    ...formik,
    existingScopes,
    existingUser,
    id,
  };
};

const EditUserForm: NextPage<{
  existingUser?: User;
}> = (user) => {
  const {
    dirty,
    errors,
    existingUser,
    id,
    handleBlur,
    handleChange,
    handleSubmit,
    isValid,
    touched,
    values,
    setFieldValue,
  } = useUserForm();

  const { data: loggedInUser, isLoading: loggedInUserLoading } =
    useGetUserPermissionsQuery(user.user.id as string);

  const hasAdminPermission = loggedInUser?.scopes?.includes('user:update');

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
                isReadOnly={!hasAdminPermission}
                isDisabled={!hasAdminPermission}
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
                isReadOnly={!hasAdminPermission}
                isDisabled={!hasAdminPermission}
              />
            </FormControl>

            {/* Only the associated user can change their own password */}
            {id === user.user.id && (
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
                  />
                  <FormErrorMessage>{errors.password}</FormErrorMessage>
                </FormControl>
              </>
            )}

            <Divider mb={7} mt={7} />

            <Heading fontSize="xl" colorScheme="primary">
              Privileges
            </Heading>
            <Text>Edit privileges assigned to this user</Text>
            <Divider mb={2} mt={2} />

            <Stack spacing={[1, 5]} direction={'column'}>
              {userPrivilegesArray.map((policy, idx) => {
                const isChecked = values.scopes
                  ? values.scopes.indexOf(policy.scope) >= 0
                  : false;
                return (
                  <Checkbox
                    colorScheme="purple"
                    isChecked={isChecked}
                    key={`${policy.privilege}-${idx}`}
                    onChange={(e) => {
                      if (!isChecked) {
                        setFieldValue(`scopes`, [
                          ...values.scopes,
                          policy.scope,
                        ]);
                      } else {
                        setFieldValue(
                          'scopes',
                          values.scopes.filter(
                            (scope) => scope !== policy.scope
                          )
                        );
                      }
                    }}
                    id={`scopes-${policy.privilege}-${idx}`}
                    name="scopes"
                    value={policy.scope}
                    isDisabled={policy.scope === 'privacy-request:read'}
                    isReadOnly={policy.scope === 'privacy-request:read'}
                  >
                    {policy.privilege}
                  </Checkbox>
                );
              })}
            </Stack>
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

export default EditUserForm;
