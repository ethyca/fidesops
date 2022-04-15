import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import { useFormik } from 'formik';
import {
  Button,
  chakra,
  Checkbox,
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
import { selectUserToken } from '../user/user.slice';

interface Privilege {
  privilege: string;
  description: string;
}

export const userPrivilegesArray: Privilege[] = [
  {
    privilege: 'View subject requests',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Approve subject requests',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'View datastore connections',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Manage datastore connections',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'View policies',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create policies',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create users',
    description: 'Instructional line about these particular user preferences',
  },
  {
    privilege: 'Create roles',
    description: 'Instructional line about these particular user preferences',
  },
];

const useNewUserForm = () => {
  const token = useSelector(selectUserToken);
  const [isLoading, setIsLoading] = useState(false);
  const formik = useFormik({
    initialValues: {
      username: '',
      name: '',
      password: '',
    },
    onSubmit: async (values) => {
      setIsLoading(true);
      const host =
        process.env.NODE_ENV === 'development'
          ? config.fidesops_host_development
          : config.fidesops_host_production;

      const body = 
        {
          "username": values.username,
          "name": values.name,
          "password": values.password,
        }
      ;

      try {
        const response = await fetch(`${host}/user`, {
          method: 'POST',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'authorization': `Bearer ${token}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });

        const data = await response.json();

        if (data.succeeded.length) {
          console.log("Success")
        }

      } catch (error) {
        console.log("Error")
        return;
      }
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

  return { ...formik, isLoading };
};

const NewUserForm: NextPage = () => {
  const {
    dirty,
    errors,
    handleBlur,
    handleChange,
    handleSubmit,
    isValid,
    isLoading,
    touched,
    values,
  } = useNewUserForm();

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

            <Heading fontSize="xl" colorScheme="primary">
              Preferences
            </Heading>
            <Text>Select privileges to assign to this user</Text>
            <CheckboxGroup colorScheme="secondary">
              <Stack spacing={[1, 5]} direction={'column'}>
                {userPrivilegesArray.map((policy, idx) => (
                  <>
                    <Checkbox value={policy.privilege}>{policy.privilege}</Checkbox>
                    <div>{policy.description}</div>
                  </>
                ))}
              </Stack>
            </CheckboxGroup>
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

export default NewUserForm;
