import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import { useFormik } from 'formik';
import {
  Button,
  chakra,
  CheckboxGroup,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input, 
  Stack,
  Text,
} from '@fidesui/react';
import config from './config/config.json';
import { selectUserToken, useEditUserMutation, useCreateUserMutation, useGetUserByIdQuery} from '../user/user.slice';
import { useRouter } from 'next/router';

const useUserForm = (existingId: string | null) => {
  const token = useSelector(selectUserToken);
  const [createUser, createUserResult] = useCreateUserMutation();
  const [editUser, editUserResult] = useEditUserMutation();
  // const {getUser, getUserResult} = useGetUserByIdQuery(existingId || null);
  const router = useRouter();

  // Initial values - GET individual user values if coming from the ID path
  useEffect(() => {
    console.log("initial")
    // if(existingId) {
      // getUser(existingId)
    // }
  }, []);

  const getUserResult = {
    // username: "test",
    // name: "test name",
    // password: "test pass",
    username: null,
    name: null,
    password: null,
  }

  const formik = useFormik({
    initialValues: {
      username: getUserResult?.username || '',
      name: getUserResult?.name || '',
      password: getUserResult?.password ? '********' : '',
    },
    onSubmit: async (values) => {
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;

      const body = 
        {
          username: values.username,
          name: values.name,
          password: values.password,
        }
      ;

      if(!getUserResult) {
        createUser(body);
      }
      // else {
      //   console.log("editing")
      //   editUser({existingId, ...body})
      // }
      // redirect after creating/editing?
      router.push('/user-management')
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

  // const { data, isLoading } = useGetUserQuery(userId);
  // const { user } = data || { user: {} };
  const user = existingId ? getUserResult : null

  console.log(user)

  return {
     ...formik, 
    // isLoading: createUserResult.isLoading,
    user
  };
};

const UserForm: NextPage<{existingId: string}> = ({ existingId }) => {
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
    user,
  } = useUserForm(existingId);

  console.log(existingId)

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
                  placeholder="Enter new user name"
                  onChange={handleChange}
                  onBlur={handleBlur}
                  value={values.username}
                  isInvalid={touched.username && Boolean(errors.username)}
                  isReadOnly={existingId ? true : false}
                  isDisabled={existingId ? true : false}
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
                  value={values.name}
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
                value={values.password}
                onChange={handleChange}
                onBlur={handleBlur}
                isInvalid={touched.password && Boolean(errors.password)}
              />
              <FormErrorMessage>{errors.password}</FormErrorMessage>
            </FormControl>

            {/* <Heading fontSize="xl" colorScheme="primary">
              Preferences
            </Heading>
            <Text>Select privileges to assign to this user</Text>
            <CheckboxGroup colorScheme="secondary">
              <Stack spacing={[1, 5]} direction={'column'}> */}
                {/* {userPrivilegesArray.map((policy, idx) => (
                  <>
                    <Checkbox value={policy.privilege}>{policy.privilege}</Checkbox>
                    <div>{policy.description}</div>
                  </>
                ))} */}
              {/* </Stack>
            </CheckboxGroup> */}
          </Stack>
            
            <NextLink href="/user-management" passHref>
              <Button
                variant="outline"
                size="sm"
              >
                Cancel
              </Button>
            </NextLink>
            <Button
              type="submit"
              bg="primary.800"
              _hover={{ bg: 'primary.400' }}
              _active={{ bg: 'primary.500' }}
              colorScheme="primary"
              disabled={!existingId && !(isValid && dirty)}
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
