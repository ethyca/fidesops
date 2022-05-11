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
  useCreateUserMutation,
  useUpdateUserPermissionsMutation,
} from '../user/user.slice';
import { userPrivilegesArray, User, UserResponse } from '../user/types';
import { useRouter } from 'next/router';

const useUserForm = () => {
  const token = useSelector(selectUserToken);
  const [createUser, createUserResult] = useCreateUserMutation();
  const [updateUserPermissions, updateUserPermissionsResult] =
    useUpdateUserPermissionsMutation();
  const router = useRouter();

  const formik = useFormik({
    initialValues: {
      username: '',
      first_name: '',
      last_name: '',
      password: '',
      scopes: [],
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

      await createUser(userBody)
        .then((result) => {
          const userWithPrivileges = {
            id: 'data' in result ? result.data.id : null,
            scopes: values.scopes,
          };

          return userWithPrivileges;
        })
        .then((result) => {
          console.log('PERMISSIONS TO PASS', result);
          const permissionsToAddToUser = updateUserPermissions(result);

          return permissionsToAddToUser;
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

      if (!values.username) {
        errors.username = 'Username is required';
      }

      if (!values.password) {
        errors.password = 'Password is required';
      }

      return errors;
    },
  });

  return {
    ...formik,
  };
};

const UserForm: NextPage<{
  existingUser?: User;
}> = () => {
  const {
    dirty,
    errors,
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
                placeholder={'Enter new username'}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.username}
                isInvalid={touched.username && Boolean(errors.username)}
              />
              <FormErrorMessage>{errors.username}</FormErrorMessage>
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
                placeholder={'Enter first name of user'}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.first_name}
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
                placeholder={'Enter last name of user'}
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.last_name}
              />
            </FormControl>

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
                  isInvalid={touched.password && Boolean(errors.password)}
                />
                <FormErrorMessage>{errors.password}</FormErrorMessage>
              </FormControl>
            </>

            <Heading fontSize="xl" colorScheme="primary">
              Preferences
            </Heading>
            <Text>Select privileges to assign to this user</Text>
            <CheckboxGroup colorScheme="secondary">
              <Stack spacing={[1, 5]} direction={'column'}>
                {userPrivilegesArray.map((policy, idx) => (
                  <Checkbox
                    defaultChecked={policy.scope === 'privacy-request:read'}
                    key={`${policy.privilege}-${idx}`}
                    onChange={handleChange}
                    id={`scopes-${policy.privilege}-${idx}`}
                    name="scopes"
                    isChecked={values.scopes[idx]}
                    value={
                      policy.scope === 'privacy-request:read'
                        ? undefined
                        : policy.scope
                    }
                    isDisabled={policy.scope === 'privacy-request:read'}
                    isReadOnly={policy.scope === 'privacy-request:read'}
                  >
                    {policy.privilege}
                  </Checkbox>
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
            disabled={!(isValid && dirty)}
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
