import { Box, Divider, Flex, Tag, Text } from "@fidesui/react";
import ClipboardButton from "common/ClipboardButton";
import React from "react";

type EventErrorProps = {
  errorMessage: string;
};

const EventError = ({ errorMessage }: EventErrorProps) => {
  const isError = "sdfsdfsdf";
  return (
    <Box height="100%" id="outer">
      <Flex alignItems="center" paddingBottom="8px">
        <Text
          size="sm"
          color="gray.700"
          fontWeight="medium"
          marginRight="8px"
          lineHeight="20px"
        >
          Status
        </Text>
        <Tag
          size="sm"
          height="20px"
          backgroundColor="red.500"
          color="white"
          marginRight="8px"
        >
          Error
        </Tag>
        <Box padding="0px" marginBottom="3px">
          <ClipboardButton copyText={errorMessage} />
        </Box>
      </Flex>
      <Divider />
      <Box id="errorWrapper" overflow="auto" height="100%">
        {/* <Text>{errorMessage}</Text> */}
        <Text color="gray.800" fontSize="smaller">
          Traceback (most recent call last): File "/usr/local/bin/fidesctl",
          line 33, in module sys.exit(load_entry_point('fidesctl',
          'console_scripts', 'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130
          Traceback (most recent call last): File "/usr/local/bin/fidesctl",
          line 33, in module sys.exit(load_entry_point('fidesctl',
          'console_scripts', 'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130
          Traceback (most recent call last): File "/usr/local/bin/fidesctl",
          line 33, in module sys.exit(load_entry_point('fidesctl',
          'console_scripts', 'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130
          Traceback (most recent call last): File "/usr/local/bin/fidesctl",
          line 33, in module sys.exit(load_entry_point('fidesctl',
          'console_scripts', 'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130, in
          __call__Traceback (most recent call last): File
          "/usr/local/bin/fidesctl", line 33, in module File
          "/usr/local/bin/fidesctl", line 33, in module
          sys.exit(load_entry_point('fidesctl', 'console_scripts',
          'fidesctl')()) File
          "/usr/local/lib/python3.8/site-packages/click/core.py", line 1130
        </Text>
      </Box>
    </Box>
  );
};

export default EventError;
