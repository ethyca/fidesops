import {
  Box,
  Button,
  ButtonGroup,
  Divider,
  Flex,
  Heading,
  HStack,
  Tag,
  Text,
  VStack,
} from "@fidesui/react";
import YamlEditor from "@focus-reactive/react-yaml";
import { ErrorWarningIcon } from "common/Icon";
import React, { useLayoutEffect, useRef, useState } from "react";

type YamlEditorFormProps = {
  data: any;
  isSubmitting: boolean;
  onSubmit: (value: any) => void;
};

const YamlEditorForm: React.FC<YamlEditorFormProps> = ({
  data,
  isSubmitting = false,
  onSubmit,
}) => {
  const actions = useRef();
  const [editData, setEditData] = useState(data);
  const [yamlError, setYamlError] = useState("" as any);

  const handleChange = ({ json }: { json: any }) => {
    setEditData(json);
    setYamlError("");
  };

  const handleCancelClick = () => {
    (actions.current as any).replaceValue({ json: data });
  };

  const handleError = (error: any) => {
    if (typeof error === "object") {
      setYamlError(error);
    }
  };

  const handleSaveClick = () => {
    onSubmit(editData);
  };

  useLayoutEffect(() => {
    setTimeout(() => {
      // Adjust the height of the YAML editor dynamically
      const editor = document.querySelector<HTMLElement>(".cm-editor")!;
      editor.style.height = "calc(100vh - 399px)";
    }, 0);
  }, []);

  return (
    <Flex gap="97px">
      <VStack align="stretch" w="579px">
        <Divider color="gray.100" />
        <YamlEditor
          json={editData}
          onChange={handleChange}
          onError={handleError}
          ref={actions}
        />
        <Divider color="gray.100" />
        <ButtonGroup
          mt="24px !important"
          size="sm"
          spacing="8px"
          variant="outline"
        >
          <Button onClick={handleCancelClick} variant="outline">
            Cancel
          </Button>
          <Button
            bg="primary.800"
            color="white"
            isDisabled={yamlError}
            isLoading={isSubmitting}
            loadingText="Saving Yaml system"
            onClick={handleSaveClick}
            size="sm"
            variant="solid"
            type="submit"
            _active={{ bg: "primary.500" }}
            _hover={{ bg: "primary.400" }}
          >
            Save Yaml system
          </Button>
        </ButtonGroup>
      </VStack>
      {yamlError && (
        <Box w="480px">
          <Divider color="gray.100" />
          <HStack mt="16px">
            <Heading as="h5" color="gray.700" size="xs">
              YAML
            </Heading>
            <Tag colorScheme="red" size="sm" variant="solid">
              Error
            </Tag>
          </HStack>
          <Box
            bg="red.50"
            border="1px solid"
            borderColor="red.300"
            color="red.300"
            mt="16px"
            borderRadius="6px"
          >
            <HStack
              alignItems="flex-start"
              margin={["14px", "17px", "14px", "17px"]}
            >
              <ErrorWarningIcon />
              <Box>
                <Heading
                  as="h5"
                  color="red.500"
                  fontWeight="semibold"
                  size="xs"
                >
                  Error message:
                </Heading>
                <Text color="gray.700" fontSize="sm" fontWeight="400">
                  {yamlError.message}
                </Text>
                <Text color="gray.700" fontSize="sm" fontWeight="400">
                  {yamlError.reason}
                </Text>
                <Text color="gray.700" fontSize="sm" fontWeight="400">
                  Ln <b>{yamlError.mark.line}</b>, Col{" "}
                  <b>{yamlError.mark.column}</b>, Pos{" "}
                  <b>{yamlError.mark.position}</b>
                </Text>
              </Box>
            </HStack>
          </Box>
        </Box>
      )}
    </Flex>
  );
};

export default YamlEditorForm;
