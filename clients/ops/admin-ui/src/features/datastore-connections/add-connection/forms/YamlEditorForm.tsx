import {
  Alert,
  AlertDescription,
  AlertIcon,
  Box,
  Button,
  ButtonGroup,
  Divider,
  Flex,
  Heading,
  HStack,
  SlideFade,
  Tag,
  Text,
  useToast,
  VStack,
} from "@fidesui/react";
import { ErrorWarningIcon } from "common/Icon";
import yaml, { YAMLException } from "js-yaml";
import { narrow } from "narrow-minded";
import dynamic from "next/dynamic";
import React, { useRef, useState } from "react";

const Editor = dynamic(
  // @ts-ignore
  () => import("@monaco-editor/react").then((mod) => mod.default),
  { ssr: false }
);

const isYamlException = (error: unknown): error is YAMLException =>
  narrow({ name: "string" }, error) && error.name === "YAMLException";

export type Values = {
  dataset: string;
};

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
  const monacoRef = useRef(null);
  const toast = useToast();
  const yamlData = yaml.dump(data);
  const [editYamlData, setEditYamlData] = useState(yamlData);
  const [yamlError, setYamlError] = useState(
    undefined as unknown as YAMLException
  );

  const displayError = (content: string | JSX.Element) => {
    toast({
      position: "top",
      render: () => (
        <Alert status="error">
          <AlertIcon />
          <Box>
            <AlertDescription>{content}</AlertDescription>
          </Box>
        </Alert>
      ),
    });
  };

  const validate = (value: string) => {
    yaml.load(value, { json: true });
    setEditYamlData(yaml.dump(value));
    setYamlError(undefined as unknown as YAMLException);
  };

  const handleChange = (value: string | undefined) => {
    try {
      validate(value as string);
    } catch (error) {
      if (isYamlException(error)) {
        setYamlError(error);
      } else {
        displayError("Could not parse the supplied YAML");
      }
    }
  };

  const handleReset = () => {
    (monacoRef.current as any).setValue(yamlData);
    setEditYamlData(yamlData);
    setYamlError(undefined as unknown as YAMLException);
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleMount = (editor: any, _monaco: any) => {
    monacoRef.current = editor;
  };

  const handleSubmit = () => {
    onSubmit(editYamlData);
  };

  return (
    <Flex gap="97px">
      <VStack align="stretch" w="918px">
        <Divider color="gray.100" />
        <Editor
          defaultLanguage="yaml"
          defaultValue={editYamlData}
          height="calc(100vh - 450px)"
          onChange={handleChange}
          onMount={handleMount}
          options={{
            fontFamily: "Menlo",
            fontSize: 13,
            minimap: {
              enabled: true,
            },
          }}
          theme="light"
        />
        <Divider color="gray.100" />
        <ButtonGroup
          mt="24px !important"
          size="sm"
          spacing="8px"
          variant="outline"
        >
          <Button onClick={handleReset} variant="outline">
            Cancel
          </Button>
          <Button
            bg="primary.800"
            color="white"
            isDisabled={!!yamlError}
            isLoading={isSubmitting}
            loadingText="Saving Yaml system"
            onClick={handleSubmit}
            size="sm"
            variant="solid"
            type="submit"
            _active={{ bg: "primary.500" }}
            _disabled={{ opacity: "inherit" }}
            _hover={{ bg: "primary.400" }}
          >
            Save Yaml system
          </Button>
        </ButtonGroup>
      </VStack>
      {yamlError && (
        <SlideFade in>
          <Box w="fit-content">
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
        </SlideFade>
      )}
    </Flex>
  );
};

export default YamlEditorForm;
