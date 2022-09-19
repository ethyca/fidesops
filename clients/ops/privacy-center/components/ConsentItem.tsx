import React from "react";
import {
  Flex,
  Box,
  Text,
  Link,
  Radio,
  RadioGroup,
  Stack,
  HStack,
} from "@fidesui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

type ConsentItemProps = {
  fidesDataUseKey: string;
  name: string;
  description: string;
  highlight: boolean;
  url: string;
  defaultValue?: boolean;
};

const ConsentItem: React.FC<ConsentItemProps> = ({
  fidesDataUseKey,
  name,
  description,
  highlight,
  defaultValue,
  url,
}) => {
  const [value, setValue] = React.useState("false");
  const backgroundColor = highlight ? "gray.100" : "";

  return (
    <Flex
      flexDirection="row"
      width="720px"
      backgroundColor={backgroundColor}
      justifyContent="center"
    >
      <Flex mb="24px" mt="24px" mr="35px" ml="35px">
        <Box
          // border="1px solid red"
          // boxSizing="border-box"
          width="100%"
          pr="60px"
        >
          <Text
            fontSize="lg"
            fontWeight="bold"
            lineHeight="7"
            color="gray.600"
            mb="4px"
          >
            {name}
          </Text>
          <Text
            fontSize="sm"
            fontWeight="medium"
            lineHeight="5"
            color="gray.600"
            mb="2px"
          >
            {description}
          </Text>
          <Link href={url} isExternal>
            <HStack>
              <Text
                fontSize="sm"
                fontWeight="medium"
                lineHeight="5"
                color="complimentary.500"
              >
                {" "}
                Find out more about this consent{" "}
              </Text>
              <ExternalLinkIcon mx="2px" color="complimentary.500" />
            </HStack>
          </Link>
        </Box>
        <RadioGroup
          onChange={setValue}
          value={value}
          // display="flex"
          // alignItems="center"
        >
          <Stack direction="row">
            <Radio value="true" colorScheme="whatsapp">
              Yes
            </Radio>
            <Radio value="false" colorScheme="whatsapp">
              No
            </Radio>
          </Stack>
        </RadioGroup>
      </Flex>
    </Flex>
  );
};

export default ConsentItem;
