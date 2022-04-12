import React, { useState } from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { useFormik } from 'formik';

import {
  Stack,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  FormErrorMessage,
  chakra,
  // useToast,
} from '@fidesui/react';

// Can we use the same form for the create, view, and edit pages? The only difference is breadcrumbs

const useUserForm = () => {
  const [isLoading, setIsLoading] = useState(false);
  const formik = useFormik({
    initialValues: {
      username: '',
      name: '',
      password: '',
    },
    onSubmit: async (values) => {
      setIsLoading(true);
      // const response = await 
      // });
      setIsLoading(false);
      // if (response && response.ok) {
      // } else {
      //   toast({
      //     status: 'error',
      //     description:
      //       'Creating new user failed.',
      //   });
      // }
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
        errors.username = 'Name is required';
      }

      if (!values.password) {
        errors.password = 'Password is required';
      }

      return errors;
    },
  });

  return { ...formik, isLoading };
};

const UserForm: NextPage = () => {
  const {
    errors,
    handleBlur,
    handleChange,
    handleSubmit,
    isLoading,
    touched,
    values,
  } = useUserForm();
  return (
    <div>
      <Head>
        <title>FidesUI App - User Management - Add New User</title>
        <meta name="description" content="Add a new user" />
      </Head>

      <main>
        {/* Breadcrumb component here */}
        <Heading fontSize="3xl" colorScheme="primary">
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

            {/* Preferences checkboxes here */}
            <Button
              variant="outline"
              flex="1"
              mr={3}
              size="sm"
              onClick={cancelCreateNewUser}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              flex="1"
              bg="primary.800"
              _hover={{ bg: 'primary.400' }}
              _active={{ bg: 'primary.500' }}
              colorScheme="primary"
              disabled={!(isValid && dirty)}
              size="sm"
            >
              Save
            </Button>
          </Stack>
        </chakra.form>
      </main>
    </div>
  );
};

export default UserForm;
